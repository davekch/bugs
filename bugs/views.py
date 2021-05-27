from django.shortcuts import render, get_object_or_404
from .models import Project, Issue
from .forms import IssueForm, ProjectForm


def projects(request):
    context = {
        "projectform": ProjectForm,
    }
    return render(request, "bugs/projects.html", context=context)


def issues(request, projectname):
    project = get_object_or_404(Project, name=projectname)
    context = {
        "open_issues": project.get_open_issues(),
        "closed_issues": project.get_closed_issues(),
        "open_issue_count": project.get_open_issue_count(),
        "closed_issue_count": project.get_closed_issue_count(),
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
