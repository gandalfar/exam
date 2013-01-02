from django.conf.urls import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),
     (r'^admin/', include(admin.site.urls)),
     (r'^media/(.*)$','django.views.static.serve', { 'document_root': settings.MEDIA_ROOT } ),

     (r'^accounts/login/$', 'django.contrib.auth.views.login'),
     (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
     
     (r'^answer/remove/(?P<aid>[-\w]+)/$', 'exam.calc.views.remove_answer'),
     
     (r'^summary/$', 'exam.calc.views.summary'),
     # url(r'^import_data/$', 'exam.calc.views.import_data', name="import_data"),
     
     (r'^review/cikel/(?P<cikel>[-\w\s]+)/$', 'exam.calc.views.review'),
     (r'^review/student/(?P<username>[-\w]+)/$', 'exam.calc.views.review_student'),
     (r'^review/$', 'exam.calc.views.review_index'),
     (r'^$', 'exam.calc.views.index'),
    
     # most greedy comes last
     # (r'^(?P<lecture>[a-z][a-z0-9_]*)/$', 'exam.calc.views.lecture'),
     (r'^(?P<lecture>[a-z][a-z0-9_]*)/(?P<section>[a-z0-9_]+)/$', 'exam.calc.views.task'),
     
     
)
