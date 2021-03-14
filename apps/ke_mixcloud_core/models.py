from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .helpers.audit_actions import log_addition, log_change, log_deletion, log_permanent_deletion


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_at', '-updated_at')


class CustomManager(models.Manager):

    def get_queryset(self):
        return super(CustomManager, self).get_queryset().filter(deleted=False)


class DeletedManager(models.Manager):
    def get_queryset(self):
        return super(DeletedManager, self).get_queryset().filter(deleted=True)


class PermanentDeletedManager(models.Manager):
    def get_queryset(self):
        return super(PermanentDeletedManager, self).get_queryset().filter(permanent_delete=True)


class AbstractBase(TimestampedModel):
    deleted = models.BooleanField(
        default=False,
        help_text="This is to make sure deletes are not actual deletes")
    permanent_delete = models.BooleanField(default=False,
                                           help_text="This false deletes items from recycle bin")
    audit_trail_user = models.ForeignKey('authentication.CustomUser', on_delete=models.DO_NOTHING, blank=True,
                                         null=True, editable=False)
    createdby = models.ForeignKey('authentication.CustomUser', related_name="%(app_label)s_%(class)s_related",
                                   on_delete=models.DO_NOTHING, blank=True, null=True)
    # everything will be used to query deleted objects e.g Model.everything.all()
    everything = models.Manager()
    objects = CustomManager()
    trash = DeletedManager()
    permanentrash = PermanentDeletedManager()

    def delete(self, *args, **kwargs):

        if self.deleted:
            self.permanent_delete = True
        else:
            self.deleted = True
        self.save()

    class Meta:
        abstract = True
        ordering = ('-created_at', '-updated_at')


@receiver(post_save)
def audit_trail_handler(sender, instance, created, using, **kwargs):
    if isinstance(instance, AbstractBase):
        if not instance.audit_trail_user:
            pass
        elif created:
            log_addition(instance)
        elif not created and instance.permanent_delete == True:
            log_permanent_deletion(instance)
        elif not created and instance.deleted == True:
            log_deletion(instance)
        else:
            log_change(instance)


class UpperCaseField(models.CharField):

    def __init__(self, *args, **kwargs):
        super(UpperCaseField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if value:
            value = value.upper()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(UpperCaseField, self).pre_save(model_instance, add)


class CapitalizeField(models.CharField):

    def __init__(self, *args, **kwargs):
        super(CapitalizeField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if value:
            value = value.capitalize()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(CapitalizeField, self).pre_save(model_instance, add)
