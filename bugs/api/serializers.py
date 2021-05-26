from rest_framework import serializers
from bugs.models import Project, Issue


class ProjectSerializer(serializers.ModelSerializer):
    open_issues = serializers.IntegerField(source="get_open_issue_count")

    class Meta:
        model = Project
        fields = ["name", "open_issues"]


class IssueSerializer(serializers.ModelSerializer):
    project = serializers.CharField(source="project.name", read_only=True)
    status = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Issue
        fields = "__all__"


class CreateIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"
