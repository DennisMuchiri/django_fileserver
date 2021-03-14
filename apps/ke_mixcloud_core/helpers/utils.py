import string
import datetime
from django.conf import settings
import random
import json
import requests
import math
from django.core.validators import RegexValidator
from rest_framework import exceptions



PHONE_REGEX = RegexValidator(
    regex=r'^(?:254)?(7(?:(?:[0-9][0-9]))[0-9]{6})$', message='Phone number must be of the format 254718999999. Upto 12 digits allowed.')

def generate_code():
    """Generate OTP by taking random choices from
        ascii_letters and digits
        Args:
                        None
        Returns:
                        generate_pass (str) generated OTP
    """
    val = math.floor(10000 + random.random()*90000)
    return val

def get_week(date):
    return date.isocalendar()[1]


def get_year(date):
    return date.isocalendar()[0]

def send_sms(data):
    url = settings.SMS_GATEWAY_URL
    data['SenderId'] = settings.SMS_SENDER_ID
    data['ApiKey'] = settings.SMS_API_KEY
    data['ClientId'] = settings.SMS_CLIENT_ID
    headers = {'content-type': 'application/json'}
    result = requests.post(url, data=json.dumps(data), headers=headers)
    return result


def customPermissionSwitchCase(perm, obj):
    switcher = {
        'View': obj.filter(view=True).exists(),
        'Edit': obj.filter(edit=True).exists(),
        'Create': obj.filter(create=True).exists(),
        'Delete': obj.filter(delete=True).exists(),
        'Approver': obj.filter(approver=True).exists()
    }
    return switcher.get(perm, None)


def customPermissionSwitchCaseList(perm, obj):
    switcher = {
        'View': obj.filter(view=True).exists(),
        'Edit': obj.filter(edit=True).exists(),
        'Create': obj.filter(create=True).exists(),
        'Delete': obj.filter(delete=True).exists(),
        'Approver': obj.filter(approver=True).exists()
    }
    return switcher.get(perm, None)

def get_obj_or_none(klass, *args, **kwargs):
    """
    This method will be used to check if object exists.
    If the it exists it returns the object else it returns None.
    query_p: The parameter to be used e.g id or username
    model: The model to query against eg User or Team
    param: The value of parameter
    """
    try:
        res = klass.objects.get(*args, **kwargs)
    except:
        res = None
    return res

def filter_obj_or_none(klass, *args, **kwargs):
    """
    This method will be used to check if object exists.
    If the it exists it returns the object else it returns None.
    query_p: The parameter to be used e.g id or username
    model: The model to query against eg User or Team
    param: The value of parameter
    """
    try:
        res = klass.objects.filter(*args, **kwargs)
    except:
        res = None
    return res

def latest_obj_or_none(klass, *args, **kwargs):
    """
    This method will be used to check if object exists.
    If the it exists it returns the object else it returns None.
    query_p: The parameter to be used e.g id or username
    model: The model to query against eg User or Team
    param: The value of parameter
    """
    try:
        res = klass.objects.filter(*args, **kwargs).latest('created_at')
    except:
        res = None
    return res
