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

    #make a post
    path('post/create', views.CreateAPost.as_view() ),

    #get my posts
    path('posts/my/all', views.CreateAPost.as_view() ),

    #tutor make a bid to a post
    path('bid/<int:post_id>/', views.CreateBid.as_view() ),

    #learner view bids of his or her post
    path('bids/<int:post_id>/', views.QuestionBids.as_view() ),

    #tutor views his or her bids 
    path('bid/my/all/', views.CreateBid.as_view() ),

    #learner accepts a bid
    path('bids/accept/<int:bid_id>/', views.AcceptBid.as_view() ),

    #teacher add a resource
    path('resource/add/<int:post_id>/', views.CreateResource.as_view() ),

    #teacher fetch his own resources
    path('my/resources/', views.CreateResource.as_view() ),

    #learner fetch resources shared
    path('learner/my/resources/<int:post_id>', views.learnerPostResources ),

    #posts feed to tutors
    path('posts/feed/all/', views.PostsFeed.as_view() ),

    #tutor make a class

    path ('new/class/' , views.CreateLearningClass.as_view()),

    #tutor get his class/es

    path ('my/learningclasses/all/' , views.CreateLearningClass.as_view()),






    
]