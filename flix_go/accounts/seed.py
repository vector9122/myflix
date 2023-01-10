from .models import MyAccountManager
from faker import Faker
def seed_db(n):
    for i in range(0,n):
        MyAccountManager.objects.create