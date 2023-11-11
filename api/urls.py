from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('users/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),

    path('', view=views.getRotes),
    path('projects/', view=views.getProjects),
    path('projects/<str:uuid>', view=views.getProject),
    path('projects/<str:uuid>/vote/', view=views.projectVote),
    path('projects/<str:uuid>/remove/tag/', view=views.removeTag)
]
