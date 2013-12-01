# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import random

class Dataset(models.Model):
    region = models.CharField(max_length=100)
    varname = models.CharField(max_length=100)
    desce = models.TextField()
    descs = models.TextField()
    d1 = models.CharField(max_length=255, blank=True, null=True)
    u1 = models.CharField(max_length=255, blank=True, null=True)
    d2 = models.CharField(max_length=255, blank=True, null=True)
    u2 = models.CharField(max_length=255, blank=True, null=True)
    d3 = models.CharField(max_length=255, blank=True, null=True)
    u3 = models.CharField(max_length=255, blank=True, null=True)
    d4 = models.CharField(max_length=255, blank=True, null=True)
    u4 = models.CharField(max_length=255, blank=True, null=True)
    year = models.IntegerField()
    c1 = models.FloatField(blank=True, null=True, help_text="Avstrija") #old
    c2 = models.FloatField(blank=True, null=True, help_text="Belgija") #old
    c3 = models.FloatField(blank=True, null=True, help_text="Bolgarija") #new
    c4 = models.FloatField(blank=True, null=True, help_text="Ciper") #new
    c5 = models.FloatField(blank=True, null=True, help_text="Češka republika") #new
    c6 = models.FloatField(blank=True, null=True, help_text="Danska") #old
    c7 = models.FloatField(blank=True, null=True, help_text="Estonija") #new
    c8 = models.FloatField(blank=True, null=True, help_text="Finska") #old
    c9 = models.FloatField(blank=True, null=True, help_text="Francija") #old
    c10 = models.FloatField(blank=True, null=True, help_text="Grčija") #old
    c11 = models.FloatField(blank=True, null=True, help_text="Hrvaška") #new
    c12 = models.FloatField(blank=True, null=True, help_text="Irska") #old
    c13 = models.FloatField(blank=True, null=True, help_text="Italija") #old
    c14 = models.FloatField(blank=True, null=True, help_text="Latvija") #new
    c15 = models.FloatField(blank=True, null=True, help_text="Litva") #new
    c16 = models.FloatField(blank=True, null=True, help_text="Luksemburg") #old
    c17 = models.FloatField(blank=True, null=True, help_text="Madžarska") #new
    c18 = models.FloatField(blank=True, null=True, help_text="Malta") #new
    c19 = models.FloatField(blank=True, null=True, help_text="Nemčija") #old
    c20 = models.FloatField(blank=True, null=True, help_text="Nizozemska") #old
    c21 = models.FloatField(blank=True, null=True, help_text="Poljska") #new
    c22 = models.FloatField(blank=True, null=True, help_text="Portugalska") #old
    c23 = models.FloatField(blank=True, null=True, help_text="Romunija") #new
    c24 = models.FloatField(blank=True, null=True, help_text="Slovaška") #new
    c25 = models.FloatField(blank=True, null=True, help_text="Slovenija") #new
    c26 = models.FloatField(blank=True, null=True, help_text="Španija") #old
    c27 = models.FloatField(blank=True, null=True, help_text="Švedska") #old
    c28 = models.FloatField(blank=True, null=True, help_text="Velika Britanija") #old
    sel = models.CharField(max_length=255)

    def get_countries(self):
        data = []
        for i in range(1,29):
            data.append( [self._meta.get_field('c'+str(i)).help_text, getattr(self, 'c'+str(i))] )
        return data

    def __unicode__(self):
        return self.varname
        #return "%s:%s" % (self.varname, self.year)
        
    class Admin:
        search_fields = ['varname']
        list_filter = ['year']
        list_display = ('varname', 'year', 'descs')
        
    def get_selected_countries(self, var2):
        data = []
        countries = sorted(self.sel.split(', ')[0:18], key=int)

        # selected_countries = {}
        # for i in countries:
        #     if not getattr(self, "c"+i) == None:
        #     selected_countries.__setitem__("c"+i, float(str(eval("self.c"+i))))

        for i in countries:
            if not getattr(self, "c"+i) == None:
                data.append( [self._meta.get_field('c'+str(i)).help_text, getattr(self, 'c'+str(i)), getattr(var2, 'c'+str(i)) ] )
        
        return data

    def generate_sample(self):
        seznam = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
        # remove 25 (Slovenia) because we include it everytime
        seznam.remove(25)

        old_member = [1,2,6,8,9,10,12,13,16,19,20,22,26,27,28]
        new_member = [3,4,5,7,11,14,15,17,18,21,23,24]
        picked = [25]

        for i in old_member:
            val = getattr(self, 'c'+str(i))
            if not val or val == 0:
                old_member.remove(i)

        for i in new_member:
            val = getattr(self, 'c'+str(i))
            if not val or val == 0:
                new_member.remove(i)

        for n in range(0,6):
            g = random.choice(old_member)
            old_member.remove(g)
            picked.append(g)
            # print "old:", g

        for n in range(0,3):
            g = random.choice(new_member)
            new_member.remove(g)
            picked.append(g)
            # print "new:", g

        # print "picked #", len(picked)
        s = str(picked).strip('[]')
        self.sel = s
        self.save()        

nacin_studija_choices = (
  (0, 'redni'),
  (1, 'izredni'),
  (2, 'stari program'),
)
  
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    vpisna = models.IntegerField()
    #priimek = models.CharField(max_length=100)
    #ime = models.CharField(max_length=100)
    studijsko_leto = models.CharField(max_length=20, blank=True)
    izvajalec = models.CharField(max_length=100, blank=True)
    nacin_studija = models.IntegerField(choices=nacin_studija_choices, null=True, blank=True)
    cikel = models.CharField(max_length=20, blank=True)
    status_studenta = models.CharField(max_length=100, blank=True)
    
    var1 = models.ForeignKey(Dataset, related_name="userprofile_var1")
    var2 = models.ForeignKey(Dataset, related_name="userprofile_var2")
    is_special = models.BooleanField(default=False)

    class Admin:
        search_fields = ['vpisna']

    def __unicode__(self):
        #return str(self.vpisna)
        return "%s: %s %s" % (str(self.vpisna), self.user.first_name, self.user.last_name)

class Country(models.Model):
    number = models.IntegerField()
    names = models.TextField()
    namee = models.TextField()

    def __unicode__(self):
        return self.namee



class Lecture(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.SlugField()
    title = models.CharField(max_length=100)
    professor = models.CharField(max_length=100)
    email = models.EmailField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    active = models.BooleanField()

    class Admin:
        pass

    def __unicode__(self):
        return self.title

class Section(models.Model):
    id = models.AutoField(primary_key=True)
    lecture = models.ForeignKey(Lecture)
    title = models.CharField(max_length=250)
    text = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    active = models.BooleanField()
    
    class Admin:
        pass
      
    def __unicode__(self):
        return str(self.title)

    def get_absolute_url(self):
        return "/%s/%s/" % (self.lecture.url,self.id)

TASK_VISIBLE_CHOICES = (
    (0, 'Visible to everyone'),
    (1, 'Visible just to normal users'),
    (2, 'Visible just to SPSS users')
)
class Task(models.Model):
    id = models.AutoField(primary_key=True)
    #FIXME ime polje
    lecture = models.ForeignKey(Section)
    title = models.CharField(max_length=100)
    text = models.TextField()
    #django ima grozen bug, ki usuje admin, ce je inline vkljucen date - glej ticket #1030
    #pub_date = models.DateTimeField('date published', auto_now_add=True)
    active = models.BooleanField()
    order  = models.IntegerField(blank=True, null=True)
    visible_to = models.IntegerField(choices=TASK_VISIBLE_CHOICES,default=0)
    
    class Admin:
        pass

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/%s/%s/" % (self.lecture.url, self.id)

class Question(models.Model):
    task = models.ForeignKey(Task)
    text = models.CharField(max_length=250)
    validator = models.CharField(max_length=200, blank=True)
    #bug #1030
    #pub_date = models.DateTimeField('date published', auto_now_add=True)
    active = models.BooleanField()
    order  = models.IntegerField(blank=True, null=True)
    visible_to = models.IntegerField(choices=TASK_VISIBLE_CHOICES,default=0)    

    def __unicode__(self):
        return self.text    

class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField('date published', auto_now=True)
    input = models.CharField(max_length=100)
    correct = models.BooleanField()

    def __unicode__(self):
        return self.input
        
    def is_correct(self):
        return self.correct

class ExamLogEntry(models.Model):
    id = models.AutoField(primary_key=True)
    input = models.CharField(max_length=200)
    question = models.ForeignKey(Question, related_name="loggedquestion")
    user = models.ForeignKey(User, related_name="student")
    commited = models.DateTimeField('commited', auto_now_add=True)

    class Admin:
        list_display = ('user', 'question', 'input', 'commited')
        list_filter = ('question', 'user')
        
    def __unicode__(self):
        return "%s: %s" % (self.user, self.input)

class CalculatedAnswer(models.Model):
    var1 = models.ForeignKey(Dataset, related_name='calculated_var1')
    var2 = models.ForeignKey(Dataset, related_name='calculated_var2')
    question = models.ForeignKey(Question, default=0)
    value = models.FloatField()

