from django.shortcuts import render

from coreapi.models import Post, User
from shulealearn import settings
from . serializers import MyTokenObtainPairSerializer, PostSerializer, RegisterLearnerSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsLearner, IsTutor
from django.core.mail import send_mail , EmailMultiAlternatives
from django.template.loader import render_to_string
from . serializers import RegisterTutorSerializer, RegisterLearnerSerializer, CreateAPostSerializer
from django.utils.html import strip_tags
from rest_framework import status
# Create your views here.


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#register student
class RegisterTutor(APIView):
    def post(self, request, format=None):
        serializer = RegisterTutorSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            try:
                # Set user type to 'Learner'
                serializer.validated_data['type'] = "Tutor"
                user = serializer.save()
                
                # Set the password
                plaintext_password = serializer.validated_data['password']
                user.set_password(plaintext_password)
                user.save()

                # Send email
                html_message = render_to_string('welcome_tutor_email.html', {
                    'user': user.first_name,
                    'email': user.email,
                    'password': plaintext_password
                })
                subject = 'Invitation to Shulea Learn'
                from_email = settings.EMAIL_HOST_USER
                to_email = user.email
                plain_message = strip_tags(html_message)
                email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
                email.attach_alternative(html_message, "text/html")
                email.send()
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                # Handle any exceptions that occur and return an appropriate response
                print(e)
                return Response({'error': 'An error occurred while processing the request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Return validation errors if serializer is not valid
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#register a student   
class RegisterLearner(APIView):
    def post(self, request, format=None):
        serializer = RegisterLearnerSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            try:
                # Set user type to 'Learner'
                serializer.validated_data['type'] = "Learner"
                user = serializer.save()
                
                # Set the password
                plaintext_password = serializer.validated_data['password']
                user.set_password(plaintext_password)
                user.save()

                # Send email
                html_message = render_to_string('welcome_learner_email.html', {
                    'user': user.first_name,
                    'email': user.email,
                    'password': plaintext_password
                })
                subject = 'Invitation to Shulea Learn'
                from_email = settings.EMAIL_HOST_USER
                to_email = user.email
                plain_message = strip_tags(html_message)
                email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
                email.attach_alternative(html_message, "text/html")
                email.send()
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                # Handle any exceptions that occur and return an appropriate response
                print(e)
                return Response({'error': 'An error occurred while processing the request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Return validation errors if serializer is not valid
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    # learner creates a post

class CreateAPost(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLearner]
    serializer_class = CreateAPostSerializer
    def post (self , request , format = None):
        serializer = CreateAPostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = User.objects.get(id = request.user)
            post= serializer.save(owner=user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def get (self , request):
        user = User.objects.get(id = request.user.id)
        all_posts = Post.objects.filter(owner = user)
        serialized_data = PostSerializer(all_posts, many = True)
        return Response(serialized_data.data , status=status.HTTP_200_OK)
    


   

