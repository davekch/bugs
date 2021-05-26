from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('api/', include('bugs.api.urls')),
    path('projects/', views.projects, name='projects'),
    path('projects/<str:projectname>/', views.issues, name='projectdetails'),
    path('projects/<str:projectname>/issues/<int:issueid>/', views.issue_detail, name="issuedetails"),
]
