from django.shortcuts import render, get_object_or_404
from .models import Project, Issue
from .forms import IssueForm


def projects(request):
    return render(request, "bugs/projects.html")


def issues(request, projectname):
    project = get_object_or_404(Project, name=projectname)
    context = {
        "issues": project.get_open_issues(),
        "projectname": projectname,
        "issueform": IssueForm(),
    }
    return render(request, "bugs/projectdetail.html", context=context)


def issue_detail(request, projectname, issueid):
    project = get_object_or_404(Project, name=projectname)
    issue = get_object_or_404(Issue, pk=issueid)
    context = {
        "projectname": projectname,
        "projecturl": project.get_project_url(),
        "title": issue.title,
        "body": issue.body,
        "priority": issue.priority,
        "status": issue.get_status_display(),
        "tags": issue.tags_list(),
        "id": issue.pk,
        "issueform": IssueForm(instance=issue),
    }
    return render(request, "bugs/issuedetail.html", context=context)
