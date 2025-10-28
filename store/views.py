from django.shortcuts import render,get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . serializers import ProductSerializer,CollectionSerializer,ReviewSerializer,CartSerializer,CartItemSerializer,AddCartitemSerializer,UpdateCartitemSerializer,CustomerSerializer,OrderSerializer,CreateOrderSerializer,UpdateOrderSerializer
from store.models import Product,Collection,OrderItem,Review,Cart,CartItem,Customer,Order
from django.db.models import Count,F,Sum
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from . filters import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from . pagination import ProductPagination
from . permissions import IsAdminOrReadOnly,FullDjangoModelPermissions,CustomerViewHistoryPermission


class ProductViewSet(ModelViewSet):
     queryset=Product.objects.all()
     serializer_class=ProductSerializer
     filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
     filterset_class=ProductFilter
     search_fields=['title','description']
     ordering_fields=['unit_price','last_update']
     pagination_class=ProductPagination
     permission_classes=[IsAdminOrReadOnly]
     # filterset_fields=['collection_id','unit_price']
     # def get_queryset(self):
     #      queryset=Product.objects.all()
     #      collection_id=self.request.query_params.get('collection_id')
     #      if collection_id is not None:
     #           queryset=queryset.filter(collection_id=collection_id)
     #      return queryset
     def get_serializer_context(self):
          return {'request',self.request}
     def destroy(self, request, *args, **kwargs):
           if OrderItem.objects.filter(pk=kwargs['pk']).count() >0:
                  return Response({
                       "error":"This prodcut cannot be deleted as its asssociiated with another orderitem"
                  },status=status.HTTP_405_METHOD_NOT_ALLOWED)
           return super().destroy(request, *args, **kwargs)
     # def delete(self,request,id):
     #      product=get_object_or_404(Product,pk=id)
     #      if product.orderitem_set.count()>0:
     #              return Response({
     #                   "error":"This prodcut cannot be deleted as its asssociiated with another orderitem"
     #              },status=status.HTTP_405_METHOD_NOT_ALLOWED)
     #      else:
     #              product.delete()
     #              return Response(status=status.HTTP_204_NO_CONTENT)
      
class CollectionViewSet(ModelViewSet):
     queryset=Collection.objects.annotate(products_count=Count('product')).all()
     serializer_class=CollectionSerializer
     permission_classes=[IsAdminOrReadOnly]
     def destroy(self, request, *args, **kwargs):
          if Product.objects.filter(collection__id=kwargs['pk']).count() >0:
               return Response({"error":"Collection cannot be deleted as its related to some product items"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
          return super().destroy(request, *args, **kwargs)
     # def delete(self,request,pk):
     #        collection=get_object_or_404(Collection,pk=pk)
     #        if collection.product_set.count() >0:
     #              return Response({"error":"Collection cannot be deleted as its related to some product items"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
     #        else:
     #           collection.delete()
     #           return Response(status=status.HTTP_204_NO_CONTENT)
      

# class ProdcutList(ListCreateAPIView):
#      queryset=Product.objects.select_related('collection').all()
#      serializer_class=ProductSerializer
#      # def get_queryset(self):
#      #      return Product.objects.select_related('collection').all()
#      # def get_serializer_class(self):
#      #      return ProductSerializer
#      def get_serializer_context(self):
#           return {'request',self.request}
     

     # def get(self,request):
     #    query_set=Product.objects.select_related('collection').all()
     #    serialize=ProductSerializer(query_set,many=True)
     #    return Response(serialize.data)
     # def post(self,request):
     #     serializer=ProductSerializer(data=request.data)
     #     serializer.is_valid(raise_exception=True)
     #     serializer.save()
     #     return Response(serializer.data,status=status.HTTP_201_CREATED)

# class ProdcutList(APIView):
#      def get(self,request):
#         query_set=Product.objects.select_related('collection').all()
#         serialize=ProductSerializer(query_set,many=True)
#         return Response(serialize.data)
#      def post(self,request):
#          serializer=ProductSerializer(data=request.data)
#          serializer.is_valid(raise_exception=True)
#          serializer.save()
#          return Response(serializer.data,status=status.HTTP_201_CREATED)


# Create your views here.
# @api_view(['GET','POST'])
# def product_list(request):
#     if(request.method=='GET'):
#         query_set=Product.objects.select_related('collection').all()
#         serialize=ProductSerializer(query_set,many=True)
#         return Response(serialize.data)
#     elif request.method=='POST':
#          serializer=ProductSerializer(data=request.data)
#          serializer.is_valid(raise_exception=True)
#          serializer.save()
#          return Response(serializer.data,status=status.HTTP_201_CREATED)
        #  if serializer.is_valid():
        #       serializer.validated_data
        #       return Response('ok')
        #  else:
        #       return Response(serializer.errors,status=status)

# class ProdcutDetails(RetrieveUpdateDestroyAPIView):
#      queryset=Product.objects.all()
#      serializer_class=ProductSerializer
#      def delete(self,request,id):
#           product=get_object_or_404(Product,pk=id)
#           if product.orderitem_set.count()>0:
#                   return Response({
#                        "error":"This prodcut cannot be deleted as its asssociiated with another orderitem"
#                   },status=status.HTTP_405_METHOD_NOT_ALLOWED)
#           else:
#                   product.delete()
#                   return Response(status=status.HTTP_204_NO_CONTENT)   
         
# class ProdcutDetails(APIView):
#      def get(self,request,id):
#           product=get_object_or_404(Product,pk=id)
#           serialize=ProductSerializer(product)
#           return Response(serialize.data)
#      def put(self,request,id):
#           product=get_object_or_404(Product,pk=id)
#           serializer=ProductSerializer(product,data=request.data)
#           serializer.is_valid(raise_exception=True)
#           serializer.save()
#           return Response(serializer.data,status=status.HTTP_200_OK)
#      def delete(self,request,id):
#           product=get_object_or_404(Product,pk=id)
#           if product.orderitem_set.count()>0:
#                   return Response({
#                        "error":"This prodcut cannot be deleted as its asssociiated with another orderitem"
#                   },status=status.HTTP_405_METHOD_NOT_ALLOWED)
#           else:
#                   product.delete()
#                   return Response(status=status.HTTP_204_NO_CONTENT)


     


       
        

# @api_view(['GET','PUT','DELETE'])
# def product_details(request,id):
#         product=get_object_or_404(Product,pk=id)
#         if request.method=='GET':
#             serialize=ProductSerializer(product)
#             return Response(serialize.data)
#         elif request.method=='PUT':
#              serializer=ProductSerializer(product,data=request.data)
#              serializer.is_valid(raise_exception=True)
#              serializer.save()
#              return Response(serializer.data,status=status.HTTP_200_OK)
#         elif request.method=='DELETE':
#              if product.orderitem_set.count()>0:
#                   return Response({
#                        "error":"This prodcut cannot be deleted as its asssociiated with another orderitem"
#                   },status=status.HTTP_405_METHOD_NOT_ALLOWED)
#              else:
#                   product.delete()
#                   return Response(status=status.HTTP_204_NO_CONTENT)
             

# class CollectionList(ListCreateAPIView):
#      queryset=Collection.objects.annotate(products_count=Count('product')).all()
#      serializer_class=CollectionSerializer
     
     # if request.method=='GET':
     #      query_set=Collection.objects.annotate(products_count=Count('product')).all()
     #      serializer=CollectionSerializer(query_set,many=True)
     #      return Response(serializer.data,status=status.HTTP_200_OK)
     # elif request.method=='POST':
     #      serializer=CollectionSerializer(data=request.data)
     #      serializer.is_valid(raise_exception=True)
     #      serializer.save()
     #      return Response(serializer.data,status=status.HTTP_201_CREATED)



# @api_view(['GET','POST'])
# def collection_list(request):
#      if request.method=='GET':
#           query_set=Collection.objects.annotate(products_count=Count('product')).all()
#           serializer=CollectionSerializer(query_set,many=True)
#           return Response(serializer.data,status=status.HTTP_200_OK)
#      elif request.method=='POST':
#           serializer=CollectionSerializer(data=request.data)
#           serializer.is_valid(raise_exception=True)
#           serializer.save()
#           return Response(serializer.data,status=status.HTTP_201_CREATED)

# class CollectionDetails(RetrieveUpdateDestroyAPIView):
#       queryset=Collection.objects.annotate(products_count=Count('product')).all()
#       serializer_class=CollectionSerializer
#       def delete(self,request,pk):
#             collection=get_object_or_404(Collection,pk=pk)
#             if collection.product_set.count() >0:
#                   return Response({"error":"Collection cannot be deleted as its related to some product items"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#             else:
#                collection.delete()
#                return Response(status=status.HTTP_204_NO_CONTENT)   
                  
            
                             

# @api_view(['GET',"PUT",'DELETE'])
# def collection_details(request,id):
#      collection=get_object_or_404(Collection,pk=id)
#      if request.method=='GET':
#           serializer=CollectionSerializer(collection)
#           return Response(serializer.data,status=status.HTTP_200_OK)
#      elif request.method=='PUT':
#           serializer=CollectionSerializer(collection,data=request.data)
#           serializer.is_valid(raise_exception=True)
#           serializer.save()
#           return Response(serializer.data,status=status.HTTP_200_OK)
#      elif request.method=='DELETE':
#           collection.delete()
#           return Response(status=status.HTTP_204_NO_CONTENT)             
             
             
class ReviewViewSet(ModelViewSet):
     serializer_class=ReviewSerializer
     def get_queryset(self):
          return Review.objects.filter(product_id=self.kwargs['product_pk'])
     def get_serializer_context(self):
          return {'product_id':self.kwargs['product_pk']}

class CartItemViewSet(ModelViewSet):
     http_method_names=['get','post','patch','delete']
     def get_serializer_class(self):
          if self.request.method =='POST':
               return AddCartitemSerializer 
          elif self.request.method=='PATCH':
               return UpdateCartitemSerializer
          return CartItemSerializer
     def get_queryset(self):
          return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')
     def get_serializer_context(self):
          print("self.kwargs",self.kwargs)
          return {'cart_id':self.kwargs['cart_pk'],'item_id':self.kwargs['cart_pk']}
    




class CartViewSet(CreateModelMixin,RetrieveModelMixin,GenericViewSet,DestroyModelMixin):
     queryset=Cart.objects.prefetch_related('items__product').all()
     serializer_class=CartSerializer

     # def get_object(self,pk):
     #      return Cart.objects.get(id=pk)    

class CustomerViewSet(ModelViewSet):
     queryset=Customer.objects.all()
     serializer_class=CustomerSerializer

     permission_classes=[IsAdminUser]

     @action(detail=True, permission_classes=[CustomerViewHistoryPermission])
     def history(self, request, pk=None):
        return Response('ok')


     @action(detail=False,methods=['GET','PUT'],permission_classes=[IsAuthenticated])
     def me(self,request):
          (customer,created)=Customer.objects.get_or_create(user_id=request.user.id)
          if request.method=='PUT':
               serializer=CustomerSerializer(customer,data=request.data)
               serializer.is_valid(raise_exception=True)
               serializer.save()
               return Response(serializer.data)
          elif request.method=='GET':
               serializer=CustomerSerializer(customer)
               return Response(serializer.data)


class OrdersViewSet(ModelViewSet):
     http_method_names=['get','patch','delete','head','options']
     def get_permissions(self):
          if self.request.method in ['PATCH','DELETE']:
               return [IsAdminUser()]
          return [IsAuthenticated()]
     # queryset=Order.objects.prefetch_related('items').all()

     def create(self, request, *args, **kwargs):
          serializer=CreateOrderSerializer(data=request.data,context={'user_id':request.user.id})
          serializer.is_valid(raise_exception=True)
          order=serializer.save()
          serializer=OrderSerializer(order)
          return Response(serializer.data)

     def get_queryset(self):
          print(self.request.user.is_superuser)
          if self.request.user.is_staff:
               return Order.objects.prefetch_related('items').all()
          else:
               customer=Customer.objects.get(user_id=self.request.user.id)
               return Order.objects.prefetch_related('items').filter(customer_id=customer.id)
     def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method=='PATCH':
             return UpdateOrderSerializer
        return OrderSerializer  # Use OrderSerializer for GET and other methods

     def get_serializer_context(self):
          return {'user_id':self.request.user.id}

   




