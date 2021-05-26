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
    status = serializers.CharField(source="get_status_display")

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
        return [t.strip() for t in value.split(",")]

    def update(self, instance, validated_data):
        if "get_status_display" in validated_data:
            validated_data["status"] = validated_data.pop("get_status_display")
        if "tags" in validated_data:
            tags = validated_data.pop("tags")
            instance.set_tags(tags)
        return super(CreateIssueSerializer, self).update(instance, validated_data)
