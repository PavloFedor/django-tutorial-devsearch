from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project, Reviews, Tag


@api_view(['GET'])
def getRotes(requset):
    routes = [
        {'GET': '/api/projects'},
        {'GET': '/api/projects/id'},
        {'POST': '/api/projects/id/vote'},

        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]
    return Response(routes)


@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    return Response(ProjectSerializer(projects, many=True).data)


@api_view(['GET'])
def getProject(request, uuid):
    project = Project.objects.get(id=uuid)
    return Response(ProjectSerializer(project, many=False).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, uuid):
    project = Project.objects.get(id=uuid)
    profile = request.user.profile
    data = request.data

    if project.owner != profile:
        review, created = Reviews.objects.get_or_create(
            owner=profile,
            project=project,
        )
        review.value = data['value']
        review.save()
        project.getVoteCount

        return Response(ProjectSerializer(project, many=False).data)
    else:
        return Response("You could't left review under own project")


@api_view(['DELETE'])
def removeTag(request, uuid):
    tagId = request.data['tag']
    project = Project.objects.get(id=uuid)
    tag = Tag.objects.get(id=tagId)
    project.tags.remove(tag)
    return Response('Tag was deleted')
