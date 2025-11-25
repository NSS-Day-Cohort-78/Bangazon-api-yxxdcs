from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from bangazonapi.models import Store, Customer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class StoreSerializer(serializers.ModelSerializer):
    """JSON serializer for stores"""

    class Meta:
        model = Store
        fields = ('id', 'name', 'description', 'created_date', 'customer')
        depth = 1

class Stores(ViewSet):
    """Request handlers for Stores"""

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        """GET all stores"""
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """GET single store by id"""
        try:
            store = Store.objects.get(pk=pk)
            serializer = StoreSerializer(store, many=False, context={'request': request})
            return Response(serializer.data)
        except Store.DoesNotExist:
            return Response({'message': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """POST new store"""
        customer = Customer.objects.get(user=request.auth.user)

        if hasattr(customer, 'store'):
            return Response(
                {'message': 'You already have a store'},
                status=status.HTTP_400_BAD_REQUEST
            )

        store = Store()
        store.customer = customer
        store.name = request.data["name"]
        store.description = request.data["description"]
        store.save()

        serializer = StoreSerializer(store, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """PUT update store"""
        try:
            store = Store.objects.get(pk=pk)

            customer = Customer.objects.get(user=request.auth.user)
            if store.customer != customer:
                return Response(
                    {'message': 'You do not own this store'},
                    status=status.HTTP_403_FORBIDDEN
                )

            store.name = request.data["name"]
            store.description = request.data["description"]
            store.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Store.DoesNotExist:
            return Response({'message': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """DELETE a store"""
        try:
            store = Store.objects.get(pk=pk)
            
            # Make sure the user owns this store
            customer = Customer.objects.get(user=request.auth.user)
            if store.customer != customer:
                return Response(
                    {'message': 'You do not own this store'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            store.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
            
        except Store.DoesNotExist:
            return Response({'message': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True)
    def favorite(self, request, pk=None):
        """POST to favorite a store"""
        # To be added later
        return Response({'message': 'Favorite feature not yet implemented'}, status=status.HTTP_501_NOT_IMPLEMENTED)

    @action(methods=['delete'], detail=True)
    def unfavorite(self, request, pk=None):
        """DELETE to unfavorite a store"""
        # To be added later
        return Response({'message': 'Unfavorite feature not yet implemented'}, status=status.HTTP_501_NOT_IMPLEMENTED)
