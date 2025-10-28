from rest_framework import serializers
from store.models import Product,Collection,Review,Cart,CartItem,Customer,Order,OrderItem
from decimal import Decimal
from django.db import transaction

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title','products_count']
    products_count=serializers.IntegerField(read_only=True)    
    # id=serializers.IntegerField()
    # title=serializers.CharField(max_length=255)
  
   

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','unit_price','description','inventory','price_with_tax','collection']
    # id=serializers.IntegerField()
    # title=serializers.CharField(max_length=255)
    # price=serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price')
    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
    # collection=CollectionSerializer() //nested object best way
    # collection=serializers.PrimaryKeyRelatedField( ///primarykey worst way
    #     queryset=Collection.objects.all()
    # )
    #collection=serializers.StringRelatedField() //lest worst


    def calculate_tax(self,product:Product):
        return product.unit_price * Decimal(1.1)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['id','date','name','description']

    def create(self, validated_data):
        product_id=self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)    


class AddCartitemSerializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField()
    class Meta:
        model=CartItem
        fields=['id','product_id','quantity']
    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product found.')
        return value  
    def save(self,**kwargs):
          cart_id=self.context['cart_id']
          product_id=self.validated_data['product_id']
          quantity=self.validated_data['quantity']
          try:
            cart_item= CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            #update
            cart_item.quantity+=quantity
            cart_item.save()
            self.instance=cart_item
         
          except CartItem.DoesNotExist:
              #create
              self.instance=CartItem.objects.create(cart_id=cart_id,**self.validated_data)
            
          return self.instance   

class UpdateCartitemSerializer(serializers.ModelSerializer):
    # product_id=serializers.IntegerField()
    class Meta:
        model=CartItem
        fields=['quantity']
 
    def save(self,**kwargs):
          cart_id=self.context['cart_id']
          item_id=self.context['item_id']
          quantity=self.validated_data['quantity']
          try:
            cart_item= CartItem.objects.get(id=item_id,cart_id=cart_id)
            #update
            cart_item.quantity=quantity
            cart_item.save()
            self.instance=cart_item
         
          except CartItem.DoesNotExist:
              raise serializers.ValidationError('CartItem not found')
              #raise expetion cartItem not found
            #   self.instance=CartItem.objects.create(cart_id=cart_id,**self.validated_data)
            
          return self.instance   
                    
      


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price=serializers.SerializerMethodField(method_name='get_total_price')
    class Meta:
        model=CartItem
        fields = ['id', 'product', 'quantity','total_price']

    def get_total_price(self,cartItem):
        return  (cartItem.quantity * cartItem.product.unit_price)   
      

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

    def get_total_price(self, cart):
        return sum(item.quantity * item.product.unit_price for item in cart.items.all())

    # def calculate_total_price(self,cart:Cart):
    #     total_price=0
    #     for item in list(cart.items):
    #         total_price=total_price + (item.unit_price * item.quantity)
    #     return total_price


        
        
    # items=CartItemSerializer() 
    # items=serializers.StringRelatedField() 
    # items=CartItemSerializer()    

    # def create(self, validated_data):
    #     return Cart.objects.create(**validated_data)    


class CustomerSerializer(serializers.ModelSerializer):
    user_id=serializers.IntegerField(read_only=True)
    class Meta:
        model=Customer
        fields=['id','user_id','phone','birth_date','membership']


class OrderItemSerializer(serializers.ModelSerializer):
    product=ProductSerializer()
    class Meta:
        model=OrderItem
        fields=['id','product','quantity','unit_price']

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True)
    class Meta:
        model=Order
        fields=['id','placed_at','customer','payment_status','items'] 


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['payment_status']



class CreateOrderSerializer(serializers.Serializer):
    def validate_cart_id(self,cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError("Cart does not exists")
        if CartItem.objects.filter(cart_id=cart_id).count()==0:
            raise serializers.ValidationError("No CartItems found.")
        return cart_id
    with transaction.atomic():
        cart_id=serializers.UUIDField()
        def save(self, **kwargs):
            cart_id=self.validated_data['cart_id']
            user_id=self.context['user_id']
            cart=Cart.objects.get(id=self.validated_data['cart_id'])
            # print(cart,user_id)
            (customer,created)=Customer.objects.get_or_create(user_id=user_id)
            order=Order.objects.create(customer=customer)
            cart_items=CartItem.objects.select_related('product').filter(cart_id=cart_id)
            order_items= [OrderItem(
                order=order,
                product=item.product,
                unit_price=item.product.unit_price,
                quantity=item.quantity
            ) for item in cart_items] 

            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk=cart_id).delete()

            return order
                     

 

