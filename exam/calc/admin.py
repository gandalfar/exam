from django.contrib import admin

from exam.calc.models import Lecture, Task, Section, Question, Answer, ExamLogEntry, Dataset, UserProfile, CalculatedAnswer

class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['vpisna', 'user__first_name', 'user__last_name', 'var1__varname', 'var2__varname']
    raw_id_fields = ['user',]
admin.site.register(UserProfile, UserProfileAdmin)

class ExamLogEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'input', 'commited')
    list_filter = ('question', 'user')
    raw_id_fields = ['user',]
    search_fields = ['user__first_name', 'user__last_name', 'user__userprofile__vpisna']

class DatasetAdmin(admin.ModelAdmin):
    list_display = ('varname', 'year')
    list_filter = ('year',)
    search_fields = ('varname', )

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'order')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('task', 'text', 'active', 'order', 'id', 'visible_to')
    list_filter = ('task','visible_to')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('input', 'question', 'user', 'correct', 'id')
    search_fields = ['user__first_name', 'user__last_name', 'user__userprofile__vpisna']    
    list_filter = ('correct',)

class CalculatedAnswerAdmin(admin.ModelAdmin):
    list_display = ('var1', 'var2', 'question', 'value')
    search_fields = ('var1__varname', 'var2__varname')

admin.site.register(Question, QuestionAdmin)
admin.site.register(ExamLogEntry, ExamLogEntryAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Section)
admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(CalculatedAnswer, CalculatedAnswerAdmin)
