from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .serializers import RegisterSerializer, UserSerializer
from notifications.models import Notification

CustomUser = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowUserView(generics.GenericAPIView):
    """
    View to follow a user.
    POST /api/follow/<user_id>/
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        
        if request.user == user_to_follow:
            return Response(
                {'error': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if user_to_follow in request.user.following.all():
            return Response(
                {'message': f'You are already following {user_to_follow.username}.'},
                status=status.HTTP_200_OK
            )
        
        request.user.following.add(user_to_follow)
        
        # Create notification for the followed user
        Notification.objects.create(
            recipient=user_to_follow,
            actor=request.user,
            verb='started following you',
            target_content_type=ContentType.objects.get_for_model(request.user),
            target_object_id=request.user.id
        )
        
        return Response(
            {'message': f'You are now following {user_to_follow.username}.'},
            status=status.HTTP_201_CREATED
        )


class UnfollowUserView(generics.GenericAPIView):
    """
    View to unfollow a user.
    POST /api/unfollow/<user_id>/
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
        
        if request.user == user_to_unfollow:
            return Response(
                {'error': 'You cannot unfollow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if user_to_unfollow not in request.user.following.all():
            return Response(
                {'message': f'You are not following {user_to_unfollow.username}.'},
                status=status.HTTP_200_OK
            )
        
        request.user.following.remove(user_to_unfollow)
        return Response(
            {'message': f'You have unfollowed {user_to_unfollow.username}.'},
            status=status.HTTP_200_OK
        )


class UserListView(generics.ListAPIView):
    """
    View to list all users.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
