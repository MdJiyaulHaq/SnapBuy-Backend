import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from apps.store.models import Collection, Product


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.post("/store/collections/", {"title": "x"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client):
        api_client.force_authenticate(user={})
        response = api_client.post("/store/collections/", {"title": "x"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_but_data_is_invalid_returns_400(self, api_client):
        api_client.force_authenticate(user=User(is_staff=True))
        response = api_client.post("/store/collections/", {"title": ""})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["title"] is not None

    def test_if_user_is_admin_and_data_is_valid_returns_201(self, api_client):
        api_client.force_authenticate(user=User(is_staff=True))
        response = api_client.post("/store/collections/", {"title": "a"})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0


@pytest.mark.django_db
class TestRetriveCollection:
    def test_if_collection_exits_returns_200(self, api_client):
        collection = baker.make(Collection)
        # Model baker takes care of relationships as well
        baker.make(Product, collection=collection, _quantity=5)
        # this will create one collection with 5 products
        response = api_client.get(f"/store/collections/{collection.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": collection.id,
            "title": collection.title,
            "product_count": 0,
        }
