import factory
from factory.django import DjangoModelFactory
from account.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
