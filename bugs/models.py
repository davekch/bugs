from django.db import models
from django.urls import reverse


class Project(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def get_open_issue_count(self):
        return len(self.get_open_issues())

    def get_open_issues(self):
        return self.issue_set.filter(
            status__in=[Issue.Status.PENDING, Issue.Status.WIP]
        )

    def get_closed_issue_count(self):
        return len(self.get_closed_issues())

    def get_closed_issues(self):
        return self.issue_set.filter(
            status__in=[Issue.Status.DONE, Issue.Status.WONTFIX]
        ).order_by("-created_on")

    def get_issues_by_tags(self, tags, closed=False):
        """returns all issues that have one or more of the given tags"""
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]
        if closed:
            return [issue for issue in self.get_closed_issues() if any(tag in issue.tags_list() for tag in tags)]
        else:
            return [issue for issue in self.get_open_issues() if any(tag in issue.tags_list() for tag in tags)]

    def get_project_url(self):
        return reverse("projectdetails", args=[self.name])


class Issue(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField(null=True)
    priority = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=200, null=True)

    class Status(models.IntegerChoices):
        PENDING = 1
        WIP = 2
        WONTFIX = 3
        DONE = 4

    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)

    class Meta:
        ordering = ["-priority", "-created_on"]

    def get_issue_url(self):
        return reverse("issuedetails", args=[self.project.name, self.pk])

    def tags_list(self):
        if self.tags:
            return self.tags.split(",")
        return []
