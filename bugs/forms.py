from django import forms
from .models import Issue, Project


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ["title", "body", "priority", "tags"]


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name"]
