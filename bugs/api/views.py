from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bugs.models import Project, Issue
from functools import wraps
from .serializers import (
    ProjectSerializer,
    ListIssueSerializer,
    IssueSerializer,
)


class ProjectListApiView(APIView):

    def get(self, request, *args, **kwargs):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """create a new project"""
        data = {
            "name": request.data.get("name")
        }
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailApiView(APIView):

    def get(self, request, name, *args, **kwargs):
        try:
            project = Project.objects.get(name=name)
        except Project.DoesNotExist:
            return Response(
                {"res": "Object does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, name, *args, **kwargs):
        """delete given project"""
        try:
            project = Project.objects.get(name=name)
        except Project.DoesNotExist:
            return Response(
                {"res": "Object does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        project.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


class IssueListApiView(APIView):

    def get(self, request, projectname, *args, **kwargs):
        try:
            project = Project.objects.get(name=projectname)
        except Project.DoesNotExist:
            return Response(
                {"res": "Project does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if "tags" in request.GET:
            issues = project.get_issues_by_tags(request.GET["tags"], ("closed" in request.GET))
        else:
            if "closed" in request.GET:
                issues = project.get_closed_issues()
            else:
                issues = project.get_open_issues()
        serializer = ListIssueSerializer(issues, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, projectname, *args, **kwargs):
        try:
            project = Project.objects.get(name=projectname)
        except Project.DoesNotExist:
            return Response(
                {"res": "Project does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            "project": project.pk,
            "title": request.data.get("title"),
            "body": request.data.get("body"),
            "priority": request.data.get("priority") or Issue.priority.field.default,
            "tags": request.data.get("tags"),
            "status": Issue.status.field.default.name,
        }
        data = {k: v for k,v in data.items() if v}
        serializer = IssueSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueDetailApiView(APIView):

    def get(self, request, projectname, issueid, *args, **kwargs):
        try:
            issue = Issue.objects.get(pk=issueid)
        except Issue.DoesNotExist:
            return Response(
                {"res": "Object does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = IssueSerializer(issue)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, projectname, issueid, *args, **kwargs):
        try:
            issue = Issue.objects.get(pk=issueid)
        except Issue.DoesNotExist:
            return Response(
                {"res": "Object does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            "title": request.data.get("title"),
            "body": request.data.get("body"),
            "priority": request.data.get("priority"),
            "status": request.data.get("status"),
            "tags": request.data.get("tags"),
        }
        data = {k: v for k,v in data.items() if v}
        serializer = IssueSerializer(issue, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, projectname, issueid, *args, **kwargs):
        try:
            issue = Issue.objects.get(pk=issueid)
        except Issue.DoesNotExist:
            return Response(
                {"res": "Object does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        issue.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
