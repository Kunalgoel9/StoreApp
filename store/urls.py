from django.urls import path
# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

router=routers.DefaultRouter()

router.register('products',viewset=views.ProductViewSet,basename='products')
router.register('collections',viewset=views.CollectionViewSet)
router.register('carts',viewset=views.CartViewSet,basename='carts')
router.register('customers',viewset=views.CustomerViewSet,basename='customers')
router.register('orders',viewset=views.OrdersViewSet,basename='orders')
products_router=routers.NestedDefaultRouter(router,'products',lookup='product')
products_router.register('reviews',views.ReviewViewSet,basename='products-reviews')

cart_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('items',views.CartItemViewSet,basename='cart-items')



urlpatterns = router.urls + products_router.urls + cart_router.urls
# urlpatterns=[
#     path('products/',views.ProdcutList.as_view()),
#     path('products/<int:pk>',views.ProdcutDetails.as_view()),
#     path('collections/',views.CollectionList.as_view()),
#     path('collections/<int:pk>',views.CollectionDetails.as_view())
# ]