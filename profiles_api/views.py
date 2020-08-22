from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .import serializers
from rest_framework import status
from rest_framework import viewsets
from .import models
from .import permissions 
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
class HelloApiView(APIView):

	serializer_class=serializers.HelloSerializer

	def get(self,request,format=None):
		an_apiview=[
		'uses HTTP methods as function9get,post,put,patch,delete)',
		'It is similar to traditional Django views ',
		'gives you the most control over logic'
		]

		return Response({'message':'hello','an_apiview':an_apiview})

	def post(self,request):
		serializer=serializers.HelloSerializer(data=request.data)
		if serializer.is_valid():
			name=serializer.data.get('name')
			message='Hello {0}'.format(name)
			return Response({'message':message})
		else:
			return Response(serializer.errors,status=status.HTTP_404_BAD_REQUEST)

	def put(self,request,pk=None):
		return Response({'method':'put'})

	def patch(self,request,pk=None):
		return Response({'method':'patch'})

	def delete(self,request,pk=None):
		return Response({'method':'delete'})


class HelloViewSet(viewsets.ViewSet):
	serializer_class=serializers.HelloSerializer
	def list(self,request):
		a_viewset=[
		'uses action(list,create,retrieve,update,partial_update)',
		'automatically maps to urls using Routers'
		]

		return Response({'message':'hello',"a_viewset":a_viewset})

	def create(self,request):
		serializer=serializers.HelloSerializer(data=request.data)
		if serializer.is_valid():
			name=serializer.data.get('name')
			message='Hello{0}'.format(name)
			return Response({'message':message})
		else:
			return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)


	def retrieve(self,request,pk=None):
		return Response({'http_method':'GET'})


	def update(self,request,pk=None):
		return Response({'http_method':'PUT'})

	def partial_update(self,request,pk=None):
		return Response({'http_method':'PATCH'})

	def destroy(self,request,pk=None):
		return Response({'http_method':'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
	serializer_class=serializers.UserProfileSerializer
	queryset=models.UserProfile.objects.all()
	authentication_classes=(TokenAuthentication,)
	permission_class=(permissions.UpdateOwnProfile,)
	filter_backends=(filters.SearchFilter,)
	search_fields=('name','email')


class LoginViewSet(viewsets.ViewSet):
	'''check email and password and return an auth token '''
	serializer_class=AuthTokenSerializer
	def create(self,request):
		'''use the ObtainAuthToken APIView to  validate and create a token '''
		return ObtainAuthToken().post(request)

class UserProfileFeedViewSet(viewsets.ModelViewSet):
	'''Handles creating,reading and updating profile feed items'''
	authentication_classes=(TokenAuthentication,)
	serializer_class=serializers.ProfileFeedItemSerializer
	queryset=models.ProfileFeedItem.objects.all()
	permission_classes=(permissions.PostOwnStatus,IsAuthenticated)
	def perform_create(self,serializer):
		'''sets the user profile to logged in users'''
		serializer.save(user_profile=self.request.user)
