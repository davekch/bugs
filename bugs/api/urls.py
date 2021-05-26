from django.conf.urls import url
from django.urls import path, include
from .views import (
    ProjectListApiView,
    ProjectDetailApiView,
    IssueListApiView,
    IssueDetailApiView,
)

urlpatterns = [
    path('', ProjectListApiView.as_view()),
    path('<str:name>/', ProjectDetailApiView.as_view()),
    path('<str:projectname>/issues/', IssueListApiView.as_view()),
    path('<str:projectname>/issues/<int:issueid>/', IssueDetailApiView.as_view()),
]
