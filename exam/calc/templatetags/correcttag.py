from django.template import Library
from django import template

from exam.calc.validators import validator_core
from django.contrib.auth.models import User
from exam.calc.models import Lecture, Task, Section, Question, Answer, ExamLogEntry, Dataset

from exam.calc.validators.statistika import check_student_section, calc_show_correct, calc_show_const

register = Library()

class CheckAllClass(template.Node):
    def __init__(self, section_id, student_id):
        self.section_id = section_id
        self.student_id = student_id
                
    def render(self, context):
        section_id = template.resolve_variable(self.section_id, context)
        student_id = template.resolve_variable(self.student_id, context)
        
        c, a = check_student_section(student_id, section_id)
        
        context['correct_count'] = c
        context['answer_count'] = a
        return ''
        
def check_all(parser, token):
    """ {% check_all section.id student.id %} """
    tag_name, section_id, student_id = token.split_contents()
    return CheckAllClass(section_id, student_id)
register.tag('check_all', check_all)

class ShowCorrectClass(template.Node):
    def __init__(self, question_id, student_id):
        self.question_id = question_id
        self.student_id  = student_id
    
    def render(self, context):
        question_id = template.resolve_variable(self.question_id, context)
        student_id = template.resolve_variable(self.student_id, context)
        
        student_ans, calc_ans  = calc_show_correct(question_id, student_id)
        
        context['student_ans'] = student_ans
        context['calc_ans'] = calc_ans
        
        return ''

def show_correct(parser, token):
    """ {% show_correct question.id student.id %}"""
    tag_name, question_id, student_id = token.split_contents()
    return ShowCorrectClass(question_id, student_id)
register.tag('show_correct', show_correct)

class ShowPrecisionClass(template.Node):
  def __init__(self, question_id, student_id):
    self.question_id = question_id
    self.student_id  = student_id
    
  def render(self, context):
    question_id = template.resolve_variable(self.question_id, context)
    student_id = template.resolve_variable(self.student_id, context)
  
    precision  = calc_show_const(question_id, student_id)
    
    return str(precision)

def show_precision(parser, token):
    """ {% show_precision question.id student.id %}"""
    tag_name, question_id, student_id = token.split_contents()
    return ShowPrecisionClass(question_id, student_id)
register.tag('show_precision', show_precision)

@register.filter_function
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)
