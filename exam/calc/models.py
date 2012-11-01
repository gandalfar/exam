# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

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
    c11 = models.FloatField(blank=True, null=True, help_text="Irska") #old
    c12 = models.FloatField(blank=True, null=True, help_text="Italija") #old
    c13 = models.FloatField(blank=True, null=True, help_text="Latvija") #new
    c14 = models.FloatField(blank=True, null=True, help_text="Litva") #new
    c15 = models.FloatField(blank=True, null=True, help_text="Luksemburg") #old
    c16 = models.FloatField(blank=True, null=True, help_text="Madžarska") #new
    c17 = models.FloatField(blank=True, null=True, help_text="Malta") #new
    c18 = models.FloatField(blank=True, null=True, help_text="Nemčija") #old
    c19 = models.FloatField(blank=True, null=True, help_text="Nizozemska") #old
    c20 = models.FloatField(blank=True, null=True, help_text="Poljska") #new
    c21 = models.FloatField(blank=True, null=True, help_text="Portugalska") #old
    c22 = models.FloatField(blank=True, null=True, help_text="Romunija") #new
    c23 = models.FloatField(blank=True, null=True, help_text="Slovaška") #new
    c24 = models.FloatField(blank=True, null=True, help_text="Slovenija") #new
    c25 = models.FloatField(blank=True, null=True, help_text="Španija") #old
    c26 = models.FloatField(blank=True, null=True, help_text="Švedska") #old
    c27 = models.FloatField(blank=True, null=True, help_text="Velika Britanija") #old
    sel = models.CharField(max_length=255)

    def __unicode__(self):
        return self.varname
        #return "%s:%s" % (self.varname, self.year)
        
    class Admin:
        search_fields = ['varname']
        list_filter = ['year']
        list_display = ('varname', 'year', 'descs')
        
    def get_selected_countries(self):
      countries = self.sel.split(', ')[0:18]
      
      selected_countries = {}
      for i in countries:
         if getattr(self, "c"+i):
           selected_countries.__setitem__("c"+i, float(str(eval("self.c"+i))))
         
      return selected_countries

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
    studijsko_leto = models.CharField(max_length=20)
    izvajalec = models.CharField(max_length=100)
    nacin_studija = models.IntegerField(choices=nacin_studija_choices)
    cikel = models.CharField(max_length=20)
    status_studenta = models.CharField(max_length=100)
    
    var1 = models.ForeignKey(Dataset, related_name="userprofile_var1")
    var2 = models.ForeignKey(Dataset, related_name="userprofile_var2")

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
