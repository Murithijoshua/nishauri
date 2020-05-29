from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, views
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializer import *
from .models import *


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def restricted(request, *args, **kwargs):
    return Response(data="ffff")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        # This data variable will contain refresh and access tokens
        data = super().validate(attrs)
        # You can add more User model's attributes like username,email etc. in the data dictionary like this.
        data['data'] = {'CCCNo': self.user.CCCNo, 'msisdn': self.user.msisdn}
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def depend(request):
    if request.method == 'POST':
        serializer = DependantSerializer(data=request.data)
        # serializer.initial_data.update({"user": request.user.id})
        serializer.user = request.user
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        queryset = Dependants.objects.filter(user=request.user.id)
        serializer = DependantSerializer(queryset, many=True)
        return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.initial_data['password'] != serializer.initial_data['re_password']:
            raise serializers.ValidationError("Passwords don't match")
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({"success": True, "data": {"user": "User Created"}}, status=status.HTTP_201_CREATED)
            else:
                return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    # if request.method == "GET":
    #     queryset = Dependants.objects.filter(user=request.user.id)
    #     serializer = DependantSerializer(queryset, many=True)
    #     return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)



# class UserLogoutAllView(views.APIView):
#     """
#     Use this endpoint to log out all sessions for a given user.
#     """
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         user = request.user
#         user.jwt_secret = uuid.uuid4()
#         user.save()
#         return Response(status=status.HTTP_200_OK)
