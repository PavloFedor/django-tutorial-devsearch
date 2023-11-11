from django.shortcuts import render, redirect

from django.http import HttpResponse
from .models import Project, Tag
from .utils import searchProjects, paginateProjects
from .forms import ProjectForm, ReviewForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.models import Profile


def projects(request):
    projects, search_query = searchProjects(request=request)
    pages_range, projects = paginateProjects(
        request=request,
        projects=projects,
        resultsCount=6
    )

    context = {
        'projects': projects,
        'search_query': search_query,
        'pages_range': pages_range
    }

    return render(request, 'projects/projects.html', context)


def project(request, id):
    projectObj = Project.objects.get(id=id)
    tags = projectObj.tags.all()
    profile = None

    try:
        if request.user.is_authenticated:
            profile = request.user.profile
    except Profile.DoesNotExist as e:
        print(str(e))

    reviews = projectObj.reviews_set.filter(body__isnull=False)

    alreadyLeftReview = any(
        review.owner == profile for review in reviews
    )
    isProjectOwner = profile == projectObj.owner

    form = None
    cantReviewMessage = None

    if isProjectOwner:
        cantReviewMessage = {
            "message": "You couldn't lefe review for own projects"
        }
    elif alreadyLeftReview:
        cantReviewMessage = {
            "message": "You have already left review for this project"
        }
    elif profile is None:
        cantReviewMessage = {
            "message": "Please login to left a review",
            "action": "login"
        }

    else:
        form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.owner = profile
            review.project = projectObj
            review.save()

            messages.success(
                request=request,
                message='Yor review was successfully submitted'
            )
            return redirect('project', id=projectObj.id)

    context = {
        "project": projectObj,
        "tags": tags,
        "form": form,
        "cantReviewMessage": cantReviewMessage,
        "reviews": reviews,
    }
    return render(request, 'projects/single-project.html', context=context)


@login_required(login_url="login")
def createProject(request):
    form = ProjectForm()
    profile = request.user.profile
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        newtags = request.POST.get('newtags').replace(',', " ").split()
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(
                    defaults={'name': tag},
                    name__iexact=tag
                )
                project.tags.add(tag)
            return redirect('account')

    context = {
        'form': form
    }
    return render(request, "projects/project_form.html", context=context)


@login_required(login_url="login")
def updateProject(request, uuid):
    profile = request.user.profile
    project = profile.project_set.get(id=uuid)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()

        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(
                    defaults={'name': tag},
                    name__iexact=tag
                )
                project.tags.add(tag)

            return redirect('account')

    context = {
        'form': form,
        'project': project,
    }
    return render(request, "projects/project_form.html", context=context)


@login_required(login_url="login")
def deleteProject(request, uuid):
    profile = request.user.profile
    project = profile.project_set.get(id=uuid)

    if request.method == 'POST':
        project.delete()
        return redirect('account')

    context = {
        'object': project
    }
    return render(request, 'delete_template.html', context=context)
