from rest_framework import serializers
from bugs.models import Project, Issue


class ProjectSerializer(serializers.ModelSerializer):
    open_issues = serializers.IntegerField(source="get_open_issue_count", read_only=True)
    url = serializers.URLField(source="get_project_url", read_only=True)

    class Meta:
        model = Project
        fields = ["name", "open_issues", "url"]


class ListIssueSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display", read_only=True)
    url = serializers.URLField(source="get_issue_url")

    class Meta:
        model = Issue
        fields = ["title", "status", "priority", "tags", "url"]
        ordering = ["created_on"]


class IssueSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display")
    url = serializers.URLField(source="get_issue_url", read_only=True)

    class Meta:
        model = Issue
        fields = "__all__"

    def validate_status(self, value):
        if not hasattr(Issue.Status, value.upper()):
            raise serializers.ValidationError(f"{value} is not a valid status")
        return int(getattr(Issue.Status, value.upper()))

    def validate_tags(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("tags must be strings separated by comma")
        return ",".join([t.strip() for t in value.split(",")])

    def create(self, validated_data):
        if "get_status_display" in validated_data:
            validated_data["status"] = validated_data.pop("get_status_display")
        return super(IssueSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if "get_status_display" in validated_data:
            validated_data["status"] = validated_data.pop("get_status_display")
        return super(IssueSerializer, self).update(instance, validated_data)
