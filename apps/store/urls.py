from django.urls import include, path
from rest_framework_nested import routers

from apps.store import views

app_name = "store"

router = routers.DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("collections", views.CollectionViewSet)
router.register("carts", views.CartViewSet)
router.register("customers", views.CustomerViewSet)
router.register("orders", views.OrderViewSet, basename="orders")

product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", views.ReviewViewSet, basename="product-reviews")
product_router.register("images", views.ProductImageViewSet, basename="product-images")

cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("items", views.CartItemViewSet, basename="cart-items")

urlpatterns = [
    path("store/", include(router.urls)),
    path("store/", include(product_router.urls)),
    path("store/", include(cart_router.urls)),
]
