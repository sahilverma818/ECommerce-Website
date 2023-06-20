from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .models import Product,Cart
from .serializers import ProductSerializer,UserSerializer,RegisterSerializer
from rest_framework import serializers
from rest_framework import status,generics
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework_simplejwt import views as jwt_views
import json


@csrf_exempt
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def ApiOverview(request):

	api_urls = {
		'all_products': '/all',
		'Search by Product_id': '/all/?product_id=product_id',
		'Search by Product_name': '/all/?product_name=product_name',
		'Add': '/create',
		'Update': '/update/pk',
		'Delete': 'delete/pk/',
	}

	return Response(api_urls)


@api_view(['POST'])
@permission_classes((AllowAny,))
def login_view(request):
    """
    POST API for login
    """
    # data = json.loads(request.data)
    username = request.data.get('username')
    password = request.data.get('password')
    if username is None:
        return JsonResponse({
            "errors": {
                "detail": "Please enter username"
            }
        }, status=400)
    elif password is None:
        return JsonResponse({
            "errors": {
                "detail": "Please enter password"
            }
        }, status=400)

    # authentication user
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return JsonResponse({"success": "User has been logged in"})
    return JsonResponse(
        {"errors": "Invalid credentials"},
        status=400,
    )



#Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer



# @csrf_exempt
@api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def add_product(request):
	
	prod = ProductSerializer(data=request.data)

	# validating for already existing data
	if Product.objects.filter(**request.data).exists():
		""" This data already exixt """
		raise serializers.ValidationError('This data already exists')

	if prod.is_valid():
		prod.save()
		return Response(prod.data)
	else:
		return Response(status=status.HTTP_404_NOT_FOUND)



# @csrf_exempt
@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def view_products(request):
	
	# permission_classes = (IsAuthenticated, )
	# checking for the parameters from the URL
	if request.query_params:
		prods = Product.objects.filter(**request.query_params.dict())
	else:
		prods = Product.objects.all()
		

	# if there is something in items else raise error
	if prods:
	
		serializer = ProductSerializer(prods,many=True)
		return Response(serializer.data)
	else:
		return Response(status=status.HTTP_404_NOT_FOUND)



# @csrf_exempt
@api_view(['PATCH'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def update_products(request, pk):
	prod = Product.objects.get(pk=pk)
	serializer = ProductSerializer(instance=prod, data=request.data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data)
	else:
		return Response(status=status.HTTP_404_NOT_FOUND)

# @csrf_exempt
@api_view(['DELETE'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def delete_products(request, pk):
	# permission_classes = (IsAuthenticated, )
	prod = get_object_or_404(Product, pk=pk)
	prod.delete()
	return Response(status=status.HTTP_202_ACCEPTED)


class CartView(APIView):
	def post(self,request):
	
		prod = ProductSerializer(data=request.data)

		# validating for already existing data
		if Cart.objects.filter(**request.data).exists():
			""" This data already exixt """
			raise serializers.ValidationError('This data already exists')

		if prod.is_valid():
			prod.save()
			return Response(prod.data)
		else:
			return Response(status=status.HTTP_404_NOT_FOUND)