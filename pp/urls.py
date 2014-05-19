from django.conf.urls import patterns, include, url
from main import views

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'main.views.index', name='index'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^adminUsers/', views.adminUsers, name='adminUsers'),
                       url(r'^adminCategories/', views.adminCategories, name='adminCategories'),
                       url(r'^moderator/', views.moderator, name='moderator'),
                       url(r'^categories/', views.categories, name='categories'),
                       url(r'^(?P<cat_id>\d+)/projects/', views.projects, name='projects'),
                       url(r'^projects/', views.projects, name='projects'),
                       url(r'^observed/', views.observed, name='observed'),
                       url(r'^addobserved/(?P<proid>\d+)/', views.addobserved, name='addobserved'),
                       url(r'^project/(?P<pro_id>\d+)/', views.project, name='project'),
                       url(r'^rejestracja/$', views.UserRegister, name='register'),
                       url(r'^newproject/$', views.AddNewProject, name='newproject'),
                       url(r'^editproject/(?P<project_id>\d+)/$', views.EditProject, name='editproject'),
                       url(r'^addcoment/(?P<pro_id>\d+)/', views.addcoment, name='addcoment'),
                       url(r'^logowanie/$', views.Signin, name='signin'),
                       url(r'^wspieranie/(?P<pro_id>\d+)/', views.Support, name='support'),
                       url(r'^newMessage/(?P<user_id>\d+)/', views.newMessage, name='newMessage'),
                       url(r'^newMessage/', views.newMessage, name='newMessage'),
                       url(r'^messages/', views.messages, name='messages'),
                       url(r'^notices/', views.notices, name='notices'),
                       url(r'^logout/', views.logout, name='logout'),
                       url(r'^message/(?P<mes_id>\d+)/', views.message, name='message'),
                       url(r'^updateusr/(?P<uid>\d+)/', views.UserUpdate, name='updateusr'),
                       url(r'^updatecat/(?P<uid>\d+)/', views.CatUpdate, name='updatecat'),
                       url(r'^updatecat/', views.CatUpdate, name='addcat'),
                       url(r'^updatecom/(?P<uid>\d+)/', views.CommentUpdate, name='updatecom'),
                       url(r'^delusr/(?P<uid>\d+)/', views.delUser, name='delusr'),
                       url(r'^delcom/(?P<uid>\d+)/', views.delCom, name='delcom'),
                       url(r'^delcat/(?P<uid>\d+)/', views.delCat, name='delcat'),
                       url(r'^delpro/(?P<uid>\d+)/', views.delPro, name='delpro'),
                       url(r'^delobserved/(?P<id>\d+)/', views.delobserved, name='delobserved'),
                       url(r'^delobservedp/(?P<proid>\d+)/', views.delobservedp, name='delobservedp'),
                       url(r'^adminusr/', views.adminUsers, name='adminUsers'),
                       url(r'^admincat/', views.adminCategories, name='adminCategories'),
                       url(r'^adminpro/', views.adminProjects, name='adminProjects'),
                       url(r'^admincom/', views.adminComments, name='adminComments'),
                       url(r'^saveeditedproject/(?P<project_id>\d+)/', views.saveeditedproject, name='saveeditedproject')
)
