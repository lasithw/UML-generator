from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('firstpage/', views.firstpage, name='firstpage'),
    path('getrequirement/', views.get_requirement, name='get_requirement'),
    path('classpage/', views.get_classpage, name='get_classpage'),
    path('activitypage/', views.get_activitypage, name='get_activitypage'),
    path('sequencepage/', views.get_sequencepage, name='get_sequencepage'),
    path('userinput/', views.class_user_input, name='get_userinput'),
    path('home/firstpage/', views.firstpage, name='firstpage'),
    path('home/getrequirement/', views.get_requirement, name='get_requirement'),
    path('home/classpage/', views.get_classpage, name='get_classpage'),
    path('home/activitypage/', views.get_activitypage, name='get_activitypage'),
    path('home/sequencepage/', views.get_sequencepage, name='get_sequencepage'),
    path('home/userinput/', views.class_user_input, name='get_userinput'),
    path('seq_input/', views.get_seq_input, name='seq_input'),

    # path('getrequirement/drawDiagram/', views.drawDiagram, name='drawDiagram'),
    # path('getrequirement/antsModel/', views.antsModel, name='antsModel'),
]


