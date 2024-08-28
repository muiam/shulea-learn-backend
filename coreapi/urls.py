from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
     #token
    path('auth/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #register tutor
    path('auth/register/tutor', views.RegisterTutor.as_view(), name='register_tutor'),

    #register learner

    path('auth/register/learner', views.RegisterLearner.as_view(), name='register_learner'),
    
]