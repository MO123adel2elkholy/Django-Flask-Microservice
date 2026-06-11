from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, User
from .serializers import ProductSerializer
import random
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .producer import publish

class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            products = Product.objects.all()
            publish({"id":4})
            serializer = ProductSerializer(products, many=True)
            return Response({'success': True, 'data': serializer.data})
        except Exception as e:
            return Response({'success': False, 'message': 'Failed to retrieve products', 'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        try:
            serializer = ProductSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'success': False, 'message': 'Validation error', 'errors': serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({'success': False, 'message': 'Database integrity error', 'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'message': 'Failed to create product', 'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(id=pk)
            serializer = ProductSerializer(product)
            return Response({'success': True, 'data': serializer.data})
        except Product.DoesNotExist:
            return Response({'success': False, 'message': f'Product with id {pk} not found'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'message': 'Failed to retrieve product', 'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({'success': False, 'message': f'Product with id {pk} not found'},
                            status=status.HTTP_404_NOT_FOUND)
        try:
            serializer = ProductSerializer(instance=product, data=request.data)
            if not serializer.is_valid():
                return Response({'success': False, 'message': 'Validation error', 'errors': serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({'success': False, 'message': 'Failed to update product', 'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            product = Product.objects.get(id=pk)
            product.delete()
            return Response({'success': True, 'message': f'Product with id {pk} deleted'},
                            status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({'success': False, 'message': f'Product with id {pk} not found'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'message': 'Failed to delete product', 'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserAPIView(APIView):
    def get(self, _):
        try:
            users = User.objects.all()
            if not users.exists():
                return Response({'success': False, 'message': 'No users available'}, status=status.HTTP_404_NOT_FOUND)
            user = random.choice(list(users))
            return Response({'success': True, 'id': user.id})
        except Exception as e:
            return Response({'success': False, 'message': 'Failed to fetch a user', 'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
