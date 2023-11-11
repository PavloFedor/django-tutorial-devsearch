from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProfiles(request, profiles, resultsCount):
    page = request.GET.get('page')
    paginator = Paginator(profiles, resultsCount)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

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

    return pages_range, profiles


def searchProfiles(request):
    search_query = ""
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    skills = Skill.objects.filter(name__iexact=search_query)

    profiles = Profile.objects.distinct().order_by("user__date_joined").filter(
        Q(name__icontains=search_query)
        | Q(short_intro__icontains=search_query)
        | Q(skill__in=skills)
    )

    return profiles, search_query
