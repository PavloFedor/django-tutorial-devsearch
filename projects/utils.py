from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProjects(request, projects, resultsCount):
    page = request.GET.get('page')
    paginator = Paginator(projects, resultsCount)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    startIndex = int(page) - 4

    if startIndex < 1:
        startIndex = 1

    endIndex = startIndex + 5

    if (int(page)+1) == endIndex:
        startIndex = startIndex + 1
        endIndex = endIndex + 1

    if endIndex > paginator.num_pages:
        endIndex = paginator.num_pages + 1

    pages_range = range(startIndex, endIndex)

    return pages_range, projects


def searchProjects(request):
    search_query = ""
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    tags = Tag.objects.filter(name__iexact=search_query)

    projects = Project.objects.distinct().order_by('-vote_total', '-vote_ratio', 'created_at').filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )

    return projects, search_query
