import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


def pytest_configure(config):
    import drfpytest.checks

    drfpytest.checks.nomigrations = config.option.nomigrations


@pytest.fixture()
def api_client(db: None) -> APIClient:
    return APIClient()


@pytest.fixture()
def user(db: None) -> User:
    return User.objects.create(username='test')
