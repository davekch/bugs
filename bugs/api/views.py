from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bugs.models import Project, Issue, Tag
from functools import wraps
from .serializers import ProjectSerializer


class ProjectListApiView(APIView):

    def get(self, request, *args, **kwargs):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, context={"request": request}, many=True)
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
