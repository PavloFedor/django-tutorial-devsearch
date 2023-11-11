from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('account/', views.userAccount, name="account"),
    path('account/edit', views.editAccount, name='edit-account'),
    path('register/', views.registerUser, name="register"),
    path('', views.profiles, name="profiles"),
    path('profile/<str:uuid>/', views.userProfile, name="user-profile"),
    path('profile/skill/create', views.createSkill, name="user-skill-create"),
    path(
        'profile/skill/update/<str:uuid>',
        views.updateSkill,
        name="user-skill-update"
    ),
    path(
        'profile/skill/delete/<str:uuid>',
        views.deleteSkill,
        name="user-skill-delete"
    ),
    path(
        'indbox/',
        views.inbox,
        name='inbox'
    ),
    path(
        'indbox/<str:id>/',
        views.inboxMessage,
        name='inbox-message'
    ),
    path(
        'profile/message/<str:recipientId>',
        views.sendMessage,
        name='profile-message'
    )
]
