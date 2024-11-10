from django.shortcuts import render

from coreapi.models import Bid, Credit, Escrow, LearningClass, Post, Resource, User
from shulealearn import settings
from . serializers import BidSerializer, ClassSerializer, MyTokenObtainPairSerializer, PostSerializer, RegisterLearnerSerializer, ResourceSerializer
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

#register tutor
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
        user = User.objects.get(id = request.user)
        serializer = CreateAPostSerializer(data=request.data, context={'request': request})
        #check whether the learner has atleast 2500 credits before allowing a post
        
        credit = Credit.objects.get(owner =  user)
        if credit.available_balance > 2500:
            if serializer.is_valid():
                post= serializer.save(owner=user)
                return Response(status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)

    def get (self , request):
        user = User.objects.get(id = request.user.id)
        all_posts = Post.objects.filter(owner = user)
        serialized_data = PostSerializer(all_posts, many = True)
        return Response(serialized_data.data , status=status.HTTP_200_OK)


#show tutor the post
class PostsFeed (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsTutor]
    def get (self , request):
        all_posts = Post.objects.filter(answered = False)
        for post in all_posts:
            bids_count = Bid.objects.filter(post=post).count()
            if bids_count >= 3:
                return Response(status=status.HTTP_404_NOT_FOUND)
        serialized_data = PostSerializer(all_posts, many = True)
        return Response(serialized_data.data , status=status.HTTP_200_OK)



#create a bid
class CreateBid (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsTutor]
    serializer_class = BidSerializer
    def post(self, request, post_id, format=None):
        tutor = request.user  # Directly use the user from the request
        try:
            post = Post.objects.get(id=post_id, answered=False)  # Use get to retrieve a single post
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Count existing bids for the post
        bids_count = Bid.objects.filter(post=post).count()
        if bids_count >= 3:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Serialize and save the new bid
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(tutor=tutor, post=post)
            # save the bid
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get (self , request):
        user = User.objects.get(id = request.user.id)
        all_bids = Bid.objects.filter(tutor = user)
        if all_bids:
            serialized_data = BidSerializer(all_bids, many = True)
            return Response(serialized_data.data , status=status.HTTP_200_OK)
        return Response(serialized_data.data , status=status.HTTP_404_NOT_FOUND)
    

class QuestionBids(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLearner]
    def get (self , request, post_id):
        user = User.objects.get(id = request.user.id)
        try:
            post_id = Post.objects.get(id = post_id , owner = user)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            all_bids = Bid.objects.filter(tutor = user, post = post_id)
            serialized_data = BidSerializer(all_bids, many = True)
            return Response(serialized_data.data , status=status.HTTP_200_OK)
        except Bid.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class AcceptBid (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLearner]
    def post (self , request, bid_id):
        user = User.objects.get(id = request.user.id)
        bid = Bid.objects.get(id = bid_id)
        tutor = User.objects.get(id = bid.tutor.id)
        #deduct the learner the bid amount
        amount_deductible = bid.credits
        credit = Credit.objects.get(owner =  user)
        if credit.available_balance >= bid.credits:
            new_credit_balance = credit.available_balance - amount_deductible
            credit.available_balance = new_credit_balance
            credit.save()
            #release money to an escrow
            Escrow.objects.create(
                origin = user,
                destination = tutor,
                amount = amount_deductible
            )

            bid.accepted = True
            bid.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    

class CreateResource (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsTutor]
    serializer_class = ResourceSerializer
    def post(self, request, post_id, format=None):
        tutor = request.user  # Directly use the user from the request
        try:
            post = Post.objects.get(id=post_id, answered=False)  # Use get to retrieve a single post
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # check for existing bid for the post which is for the tutor and has been accepted
        try:
            Bid.objects.filter(post=post, accepted = True, tutor = tutor)
        except Bid.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Serialize and save the new resource
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(tutor=tutor, post=post)
            # save the resource
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get (self , request):
        user = User.objects.get(id = request.user.id)
        all_resources = Resource.objects.filter(tutor = user)
        if all_resources:
            serialized_data = ResourceSerializer(all_resources, many = True)
            return Response(serialized_data.data , status=status.HTTP_200_OK)
        return Response(serialized_data.data , status=status.HTTP_404_NOT_FOUND)
    

def learnerPostResources(request,post_id):
    user = User.objects.get(id = request.user.id)
    all_resources = Resource.objects.filter(tutor = user, post = post_id , post__owner= request.user.id)
    if all_resources:
        serialized_data = ResourceSerializer(all_resources, many = True)
        return Response(serialized_data.data , status=status.HTTP_200_OK)
    return Response(serialized_data.data , status=status.HTTP_404_NOT_FOUND)


class CreateLearningClass(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsTutor]
    serializer_class = ClassSerializer
    def post (self,request):
        owner = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(owner = owner)
            return Response(status= status.HTTP_201_CREATED)
        else:
            return Response (serializer.errors)
        
    def get (self, request):
        tutor = request.user
        try:
            my_classes = LearningClass.objects.filter (owner = tutor)
            serialized_data = ClassSerializer(my_classes , many=True)
            return Response (serialized_data.data,status = status.HTTP_200_OK)
        except  LearningClass.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)











   

