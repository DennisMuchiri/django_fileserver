from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext as _


def log_addition(object):
    """
    Log that an object has been successfully added.
    The default implementation creates an admin LogEntry object.
    """
    from django.contrib.admin.models import LogEntry, ADDITION
    LogEntry.objects.log_action(
        user_id=object.audit_trail_user.id,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=str(object),
        action_flag=ADDITION,
        change_message=_('Added' )
    )


def log_change(object):
    """
    Log that an object has been successfully changed.
    The default implementation creates an admin LogEntry object.
    """
    from django.contrib.admin.models import LogEntry, CHANGE
    LogEntry.objects.log_action(
        user_id=object.audit_trail_user.id,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=str(object),
        action_flag=CHANGE,
        change_message=_('Editted' )
    )


def log_deletion(object):
    """
    Log that an object will be deleted. Note that this method is called
    before the deletion.
    The default implementation creates an admin LogEntry object.
    """
    from django.contrib.admin.models import LogEntry, DELETION
    LogEntry.objects.log_action(
        user_id=object.audit_trail_user.id,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=str(object),
        action_flag=DELETION,
        change_message=_('Deleted' )
    )

def log_permanent_deletion(object):
    """
    Log that an object will be deleted. Note that this method is called
    before the deletion.
    The default implementation creates an admin LogEntry object.
    """
    from django.contrib.admin.models import LogEntry, DELETION
    LogEntry.objects.log_action(
        user_id=object.audit_trail_user.id,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=str(object),
        action_flag=DELETION,
        change_message=_('Deleted Permanently' )
    )