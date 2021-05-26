from django.db import models
from django.urls import reverse


class Project(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def get_open_issue_count(self):
        return len(self.get_open_issues())

    def get_open_issues(self):
        return self.issue_set.filter(
            status__in=[Issue.Status.PENDING, Issue.Status.WIP, Issue.Status.WONTFIX]
        )

    def get_issues_by_tags(self, tags):
        """returns all issues that have one or more of the given tags"""
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]
        return [issue for issue in self.issue_set.all() if any(tag in issue.tags_list() for tag in tags)]

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

    def get_issue_url(self):
        return reverse("issuedetails", args=[self.project.name, self.pk])

    def set_tags(self, tags):
        self.tags = ",".join(tags)

    def tags_list(self):
        if self.tags:
            return self.tags.split(",")
        return []
