from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Issue(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    priority = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    class Status(models.IntegerChoices):
        PENDING = 1
        WIP = 2
        WONTFIX = 3
        DONE = 4

    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)


class Tag(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
