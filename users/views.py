from django.shortcuts import render, redirect, reverse
from .models import Profile, Message
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles, paginateProfiles


def loginUser(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request=request, user=user)
                return redirect(request.GET['next'] if 'next' in request.GET else 'profiles')

            else:
                messages.error(
                    request=request,
                    message='Username or password is incorrect'
                )
        except:
            messages.error(
                request=request,
                message='Username does not exists'
            )

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request=request)
    messages.info(
        request=request,
        message='User was logout'
    )
    return redirect('login')


def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request=request, message="User account created!")
            login(request, user=user)
            return redirect('edit-account')
        else:
            messages.error(
                request=request,
                message="An error has occured during registration"
            )

    context = {
        'page': page,
        'form': form
    }
    return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles, search_query = searchProfiles(request=request)
    pages_range, profiles = paginateProfiles(
        request=request,
        profiles=profiles,
        resultsCount=6
    )
    context = {
        "profiles": profiles,
        "search_query": search_query,
        "pages_range": pages_range
    }
    return render(request, 'users/profiles.html', context=context)


def userProfile(request, uuid):
    profile = Profile.objects.get(id=uuid)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description__exact="")
    context = {
        "profile": profile,
        "topSkills": topSkills,
        "otherSkills": otherSkills,
    }
    return render(request, 'users/user-profile.html', context=context)


@login_required(login_url='login')
def userAccount(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        skills = profile.skill_set.all()
        projects = profile.project_set.all()

        context = {
            'profile': profile,
            'skills': skills,
            'projects': projects,
        }
        return render(request, 'users/account.html', context=context)
    except Profile.DoesNotExist:
        logout(request=request)
        messages.error(
            request=request,
            message="Profile for user " + str(user) + " doesn't exists"
        )
        print("Profile for user " + str(user.first_name) + " doesn't exists")

    return redirect('login')


@login_required(login_url='login')
def editAccount(request):
    user = request.user
    try:
        profile = request.user.profile
        form = ProfileForm(instance=profile)

        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()

            return redirect('account')

        context = {
            'form': form
        }
        return render(request, 'users/profile_form.html', context=context)
    except Profile.DoesNotExist:
        logout(request=request)
        messages.error(
            request=request,
            message="Profile for user " + str(user) + " doesn't exists"
        )
        return redirect('login')


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('account')

    return render(request, 'users/skill_form.html', context=context)


@login_required(login_url='login')
def updateSkill(request, uuid):
    profle = request.user.profile
    skill = profle.skill_set.get(id=uuid)

    form = SkillForm(instance=skill)
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('account')

    return render(request, 'users/skill_form.html', context=context)


@login_required(login_url='login')
def deleteSkill(request, uuid):
    profle = request.user.profile
    skill = profle.skill_set.get(id=uuid)
    context = {
        'object': skill
    }

    if request.method == 'POST':
        skill.delete()
        return redirect('account')

    return render(request, 'delete_template.html', context=context)


@login_required(login_url='login')
def inbox(request):
    try:
        profile = request.user.profile
        inboxMessages = profile.messages.all().order_by(
            'is_read',
            '-created_at'
        )
        context = {
            "inboxMessages": inboxMessages,
            "unreadCount": inboxMessages.filter(is_read=False).count()
        }
        return render(request, 'users/inbox.html', context=context)

    except Profile.DoesNotExist:
        logout(request=request)
        return redirect(reverse('login') + "?next=" + request.path)


@login_required(login_url='login')
def inboxMessage(request, id):
    try:
        profile = request.user.profile
        inboxMessage = profile.messages.get(id=id)

        if inboxMessage.is_read == False:
            inboxMessage.is_read = True
            inboxMessage.save()

        context = {
            "inboxMessage": inboxMessage,
        }
        return render(request, 'users/message.html', context=context)

    except Profile.DoesNotExist:
        logout(request=request)
        return redirect(reverse('login') + "?next=" + request.path)


def sendMessage(request, recipientId):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except Profile.DoesNotExist as e:
            profile = None
    else:
        profile = None

    recipient = Profile.objects.get(id=recipientId)

    form = MessageForm(is_authorised_sender=(profile is not None))

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            inboxMessage = form.save(commit=False)
            inboxMessage.recipient = recipient
            if profile:
                inboxMessage.sender = profile
                inboxMessage.name = profile.name
                inboxMessage.email = profile.email
            inboxMessage.save()
            return redirect('user-profile', uuid=recipient.id)

    context = {
        "form": form,
        "recipient": recipient
    }

    return render(request, "users/message_form.html", context=context)
