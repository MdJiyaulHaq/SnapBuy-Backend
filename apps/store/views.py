from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from apps.store.filters import ProductFilter
from apps.store.pagination import ProductPagination
from apps.store.permissions import FullDjangoModelPermission, IsAdminOrReadOnly

from .models import (
    Cart,
    CartItem,
    Collection,
    Customer,
    Order,
    OrderItem,
    Product,
    ProductImage,
    Review,
)
from .serializers import (
    AddCartItemSerializer,
    CartItemSerializer,
    CartSerializer,
    CollectionSerializer,
    CreateOrderSerializer,
    CustomerSerializer,
    OrderItemSerializer,
    OrderSerializer,
    ProductImageSerializer,
    ProductSerializer,
    ReviewSerializer,
    UpdateCartItemSerializer,
    UpdateOrderSerializer,
)


class CartViewSet(
    CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet
):
    lookup_field = "id"
    queryset = Cart.objects.prefetch_related("items__product").all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    lookup_field = "id"
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}

    def get_queryset(self):
        return CartItem.objects.select_related("product").filter(
            cart_id=self.kwargs["cart_pk"]
        )


class ReviewViewSet(ModelViewSet):
    lookup_field = "id"
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_pk = self.kwargs.get("product_pk")
        if product_pk is None:
            return Review.objects.none()
        return Review.objects.filter(product_id=product_pk)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        product_pk = self.kwargs.get("product_pk")
        if product_pk:
            context["product_id"] = product_pk
        return context


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        product_pk = self.kwargs.get("product_pk")
        if product_pk is None:
            return ProductImage.objects.none()
        return ProductImage.objects.filter(product_id=product_pk)

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}


class ProductViewSet(ModelViewSet):
    # throttle_scope = "products"
    lookup_field = "id"
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = ProductPagination
    queryset = Product.objects.order_by("-last_update").prefetch_related("images").all()
    serializer_class = ProductSerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]
    filterset_class = ProductFilter
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update", "title"]

    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(pk=kwargs["pk"]).count() > 0:
            return Response(
                {"error": "Item cannot be deleted."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


# class ProductList(ListCreateAPIView):
#     # using advanced concepts like Mixins

#     def get_queryset(self):
#         return Product.objects.select_related("collection").all()

#     def get_serializer_class(self):
#         return ProductSerializer

#     def get_serializer_context(self):
#         return super().get_serializer_context()

#     # it can be shortened even more because we are not using any special logic

#     queryset = Product.objects.select_related("collection").all()
#     serializer_class = ProductSerializer

#     def get_serializer_context(self):
#         return super().get_serializer_context()


# class ProductList(APIView):
#     def get(self, request):
#         queryset = Product.objects.select_related("collection").all()
#         serializer = ProductSerializer(
#             queryset, many=True, context={"request": request}
#         )
#         serializer.data
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.validated_data
#         serializer.save
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(["GET", "POST"])
# def product_list(request):
#     if request.method == "GET":
#         queryset = Product.objects.select_related("collection").all()
#         serializer = ProductSerializer(queryset, many=True)
#         serializer.data
#         return Response(serializer.data)

#     elif request.method == "POST":
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.validated_data
#         serializer.save
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     # override the delete method for extra
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, id=pk)
#         if product.orderitem_set.count() > 0:
#             return Response(
#                 {"error": "Item cannot be deleted."},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED,
#             )
#         product.delete
#         return Response({"error": "Item Deleted"}, status=status.HTTP_204_NO_CONTENT)


# class ProductDetail(APIView):

#     def get(self, request, pk):
#         product = get_object_or_404(Product, id=pk)
#         serializer = ProductSerializer(product)
#         serializer.data
#         return Response(serializer.data)

#     def put(self, request, pk):
#         product = get_object_or_404(Product, id=pk)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.validated_data
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def delete(self, request, pk):
#         product = get_object_or_404(Product, id=pk)
#         if product.orderitem_set.count() > 0:
#             return Response(
#                 {"error": "Item cannot be deleted."},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED,
#             )
#         product.delete
#         return Response({"error": "Item Deleted"}, status=status.HTTP_204_NO_CONTENT)


# @api_view(["GET", "PUT", "DELETE"])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, id=pk)
#     if request.method == "GET":
#         serializer = ProductSerializer(product)
#         serializer.data
#         return Response(serializer.data)

#     elif request.method == "PUT":
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.validated_data
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     elif request.method == "DELETE":
#         if product.orderitem_set.count() > 0:
#             return Response(
#                 {"error": "Item cannot be deleted."},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED,
#             )
#         product.delete
#         return Response({"error": "Item Deleted"}, status=status.HTTP_204_NO_CONTENT)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count("product"))
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        collection = (
            Collection.objects.filter(pk=kwargs["pk"])
            .annotate(product_count=Count("product"))
            .first()
        )
        if collection and collection.product_count > 0:
            return Response(
                {"error": "collection cannot be deleted"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"error": "Collection Deleted"}, status=status.HTTP_204_NO_CONTENT
        )


# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(product_count=Count("product")).all()
#     serializer_class = CollectionSerializer

#     def get_serializer_context(self):
#         return {"request": self.request}


# class CollectionList(APIView):
#     def get(self, request):
#         queryset = Collection.objects.annotate(product_count=Count("product")).all()
#         serializer = CollectionSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(["GET", "POST"])
# def collection_list(request):
#     if request.method == "GET":
#         queryset = Collection.objects.annotate(product_count=Count("product")).all()
#         serializer = CollectionSerializer(queryset, many=True)
#         return Response(serializer.data)

#     elif request.method == "POST":
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(product_count=Count("product"))
#     serializer_class = CollectionSerializer

#     def get_serializer_context(self):
#         return {"request": self.request}

#     def delete(self, delete, pk):
#         collection = get_object_or_404(
#             Collection.objects.annotate(product_count=Count("product")), id=pk
#         )
#         if collection.product_set.count() > 0:
#             return Response(
#                 {"error": "collection cannot be deleted"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         collection.delete()
#         return Response(
#             {"error": "Collection Deleted"}, status=status.HTTP_204_NO_CONTENT
#         )


# class CollectionDetail(APIView):
#     def get(self, request, pk):
#         collection = get_object_or_404(
#             Collection.objects.annotate(product_count=Count("product")), id=pk
#         )
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         collection = get_object_or_404(
#             Collection.objects.annotate(product_count=Count("product")), id=pk
#         )
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def delete(self, delete, pk):
#         collection = get_object_or_404(
#             Collection.objects.annotate(product_count=Count("product")), id=pk
#         )
#         if collection.product_set.count() > 0:
#             return Response(
#                 {"error": "collection cannot be deleted"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         collection.delete()
#         return Response(
#             {"error": "Collection Deleted"}, status=status.HTTP_204_NO_CONTENT
#         )


# @api_view(["GET", "PUT", "DELETE"])
# def collection_detail(request, pk):
#     collection = get_object_or_404(
#         Collection.objects.annotate(product_count=Count("product")), id=pk
#     )
#     if request.method == "GET":
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)

#     elif request.method == "PUT":
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     elif request.method == "DELETE":
#         if collection.product_set.count() > 0:
#             return Response(
#                 {"error": "collection cannot be deleted"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         collection.delete()
#         return Response(
#             {"error": "Collection Deleted"}, status=status.HTTP_204_NO_CONTENT
#         )


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(
        detail=False,
        methods=["GET", "PUT", "PATCH"],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == "GET":
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == "PATCH":
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    http_methods_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data, context={"user_id": self.request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        # order is retured from custom save method in CreateOrderSerializer
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        elif self.request.method == "PATCH":
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()

        customer = Customer.objects.only("id").filter(user_id=user.id).first()
        if not customer:
            return Order.objects.none()
        return Order.objects.filter(customer_id=customer.id)
