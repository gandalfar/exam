# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import RequestContext
from exam.calc.models import Lecture, Task, Section, Question, Answer, ExamLogEntry, Dataset
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist

from exam.calc.validators import validator_core
from django.contrib.auth.models import User
from pprint import pprint
from django import forms

@login_required
def index(request):
    var1 = request.user.get_profile().var1
    var2 = request.user.get_profile().var2
    
    section_list = Section.objects.filter(active__exact=True)
    
    context = {
      'var1': var1,
      'var2': var2,
      'd': var1.get_selected_countries(),
      'section_list': section_list,
    }
    return render_to_response('exam/index.html', context, context_instance=RequestContext(request))

@login_required
def lecture(request, lecture):
    lect = get_object_or_404(Lecture, url=lecture)
    tasks = Section.objects.filter(lecture__id__exact=lect.id)
    context = { 
        'lecture' : lect,
        'task_list' : tasks,
        }
    return render_to_response('exam/lecture.html', context, context_instance=RequestContext(request))

@login_required
def task(request, lecture, section):
  
    this_section = Section.objects.get(pk=section)
    #FIXME- lecture mora biti section
    task_list = Task.objects.filter(lecture__exact=this_section.id, active__exact=True).order_by('order');
  
    #questions = list(Question.objects.filter(task__lecture__url__exact=lecture, task=this_task.id))
    #questions = task_list[0].question_set.all()
    questions = Question.objects.filter(task__lecture__exact=this_section.id, active__exact=True).order_by('order', 'id')
    
    answers = Answer.objects.filter(question__task__lecture=this_section.id, 
                                    user=request.user)
    #answers = questions[0].answer_set.all()
    #print dir(questions)

    if request.POST:
        qnum = request.POST.get('qnum',0)
        student_input = request.POST.get('input',None)
        try:
            q = Question.objects.get(pk=int(qnum))
        except Question.DoesNotExist:
            pass # fails silently on wrong POST
        else:
          
            if Answer.objects.filter(question=q, user=request.user).count():
                a = Answer.objects.filter(question=q, user=request.user).latest('id')
            else:
                a = Answer(question=q, user=request.user)
            
            a.input = student_input
            log = ExamLogEntry(user=request.user, question=q, input=student_input)
            log.save()

            try:
                if '://' in q.validator:
                    i = q.validator.split("://")
                    a.correct = validator_core.validate[i[0]](request.user, q, student_input, i[1])
                else:
                    a.correct = validator_core.validate[q.validator](request.user, q, student_input)
            except KeyError:
                # send a mail to admin notifying him of an invalid question
                from django.core.mail import mail_managers
                subject = "Invalid question"
                message = "Question with id %d has invalid validator:\n%s" % (q.id, q.validator)
                mail_managers(subject, message, fail_silently=True)

            a.save()
        return HttpResponseRedirect(request.path)
    
    for q in questions:
        for a in answers:
            if q.id == a.question.id:
                q.a = a
                
    section_list = Section.objects.filter(active__exact=True)
    context = {
        #'this_task' : this_task,
        'task_list' : task_list,
        'question_list' : questions,
        'sid': str(this_section.id),
        'section_list': section_list,
        }
    
    return render_to_response('exam/task.html', context, context_instance=RequestContext(request))

#decorator to limit certain pages to staff only
staff_required = user_passes_test(lambda u: u.is_staff)

@staff_required
def review(request, cikel):
    # if cikel == "Stari":
    #   cikel = "Stari program"
    
    exclude = {}
    lookup = {}
    q_lookup = None
    if cikel == 'R1Z':
        lookup = {'userprofile__studijsko_leto__exact': '2010/11',
                  'userprofile__izvajalec__contains': 'Z'
                 }
    elif cikel == 'R1P':
        lookup = {'userprofile__studijsko_leto__exact': '2010/11',
                  'userprofile__izvajalec__contains': 'P'
                 }
    elif cikel == 'IZ':
        lookup = {'userprofile__izvajalec__startswith': 'I',
                 }
    elif cikel == 'ST':
        q_lookup = User.objects.exclude(userprofile__studijsko_leto__contains='2010/11').exclude(userprofile__cikel='Ostalo')
    elif cikel == 'OS':
        lookup = {'userprofile__cikel__exact': 'Ostalo',
                 }
    
    section_list = Section.objects.filter(active__exact=True)
    
    if q_lookup:
        user_list = q_lookup.select_related()
    else:
        user_list = User.objects.filter(**lookup).exclude(**exclude).select_related()
    
    return render_to_response('exam/review_detail.html', 
                              {'user_list': user_list,
                              'section_list': section_list,},
                              context_instance=RequestContext(request))
                 
@staff_required
def review_student(request, username):
    user = get_object_or_404(User, username=username)
    
    section_list = Section.objects.filter(active__exact=True)
    
    return render_to_response('exam/review_student.html',
                              {'student': user,
                               'section_list': section_list,},                              
                              context_instance=RequestContext(request))

def remove_answer(request, aid):
    #ExamLogEntry(user=request.user, question=q, input=student_input)
    try:
        answer = Answer.objects.get(id=aid)
    except ObjectDoesNotExist:
        #oh well, we tried
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', "/"))
        
    if answer.user == request.user:
      answer.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', "/"))

@staff_required
def import_data(request, ftype='vars'):
    class DeleteVariablesForm(forms.Form):
        del_vars = forms.CharField(widget=forms.CheckboxInput(), label="Izbriši spremenljivke", required=True)

    var_form = DeleteVariablesForm()
    if ftype == 'vars':
        if request.POST:
            var_form = DeleteVariablesForm(request.POST)
            if var_form.is_valid():
                if var_form.cleaned_data.get('del_vars') == 'on':
                    Dataset.objects.all().exclude(varname='PS25.2001').exclude(varname='GEB1.2001').delete()



    ctx = {
        'num_users': User.objects.filter(is_staff=False).count(),
        'num_admin': User.objects.filter(is_staff=True).count(),
        'num_vars': Dataset.objects.all().count(),
        'var_form': var_form
    }
    return render(request, 'exam/import_data.html', ctx)


@login_required
def summary(request):
    user = request.user
    var1 = request.user.get_profile().var1
    var2 = request.user.get_profile().var2
    
    section_list = Section.objects.filter(active__exact=True)
    
    return render_to_response('exam/summary.html',
                              {'student': user,
                               'section_list': section_list,
                               'var1': var1,
                               'var2': var2},
                              context_instance=RequestContext(request))
