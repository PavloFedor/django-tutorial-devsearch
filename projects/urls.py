from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name="projects"),
    path('<str:id>/', views.project, name="project"),
    path('create/project/', views.createProject, name="create-project"),
    path(
        'update/project/<str:uuid>/',
        views.updateProject, name="update-project"
    ),
    path(
        'delete/project/<str:uuid>/',
        views.deleteProject, name="delete-project"
    ),
]
