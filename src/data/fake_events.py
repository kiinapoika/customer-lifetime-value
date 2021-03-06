from faker import Factory
import datetime
from datetime import datetime
from datetime import timedelta
import json
import random
from random import randint

from CameraProvider import CameraProvider



def fake_event_time(days=0):
    days = randint(0,days)
    ref_datetime = datetime.utcnow()-timedelta(days=days)
    event_time = ref_datetime.isoformat()
    event_time = event_time.split(':')
    event_time[-1] = "%.3f" %(float(event_time[-1]))
    event_time = ':'.join(event_time)+'Z'
    return event_time

def fake_key(n=12):
    faker = Factory.create()
    key = ''.join(faker.uuid4().split('-'))[:n]
    return key

def fake_amount(max_dollars=100.0):
    amount = "%.2f" %(random.uniform(0.1,max_dollars))
    amount = amount +' USD'
    return amount


def fake_customer(verb='NEW',key=fake_key(),days=0):
    event_type = 'CUSTOMER'
    event_verb = verb #'NEW' or 'UPDATE'
    customer = {}
    customer['type'] = event_type
    customer['verb'] = event_verb
    faker = Factory.create()
    customer['last_name'] = faker.last_name()
    customer['adr_state'] = faker.state_abbr()
    customer['adr_city'] = faker.city()
    event_time = fake_event_time(days=days)
    customer['event_time'] = event_time
    customer['key'] = key
    return json.dumps(customer)

def fake_site_vist(customer_key=fake_key(),days=0):
    event_type = 'SITE_VISIT'
    event_verb = 'NEW'
    site_visit = {}
    site_visit['type'] = event_type
    site_visit['verb'] = event_verb
    faker = Factory.create()
    event_time = fake_event_time(days=days)
    site_visit['event_time'] = event_time
    site_visit['key'] = fake_key()
    site_visit['customer_id'] = customer_key
    site_visit['tags'] = {'some key': 'some value'}
    return json.dumps(site_visit)

def fake_image_upload(customer_key=fake_key(),days=0):
    event_type = 'IMAGE'
    event_verb = 'UPLOAD'
    image_upload = {}
    image_upload['type'] = event_type
    image_upload['verb'] = event_verb
    faker = Factory.create()
    faker.add_provider(CameraProvider)
    camera_make,camera_model = faker.camera()
    event_time = fake_event_time(days=days)
    image_upload['event_time'] = event_time
    image_upload['key'] = fake_key()
    image_upload['customer_id'] = customer_key
    image_upload['camera_make'] = camera_make
    image_upload['camera_model'] = camera_model
    return json.dumps(image_upload)

def fake_order(verb='NEW',customer_key=fake_key(),days=0):
    event_type = 'ORDER'
    event_verb = verb #'NEW' or 'UPDATE'
    customer_order = {}
    customer_order['type'] = event_type
    customer_order['verb'] = event_verb
    customer_order['total_amount'] = fake_amount()
    customer_order['key'] = fake_key()
    event_time = fake_event_time(days=days)
    customer_order['event_time'] = event_time
    customer_order['customer_id'] = customer_key
    return json.dumps(customer_order)
