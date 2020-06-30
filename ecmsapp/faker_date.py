import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','first_project.settings')

import django
django.setup()

import random
from .models import Shop_Owner,Customer
from faker import Faker

fakegen = Faker()
topcis =['MarketPlace','Social']

def add_topic():
    t = Topic.objects.get_or_create(top_name=random.choice(topics))[0]
    t.save()
    return t

def populate(N=5):

    for entry in range(N):
        top = add_topic()
        fake_url = fakegen.url()
        fake_name = fakegen.name()
        fake_phone_no = fakegen.phone_number()
        fake_email = fakegen.email()
