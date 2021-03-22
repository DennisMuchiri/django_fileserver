from rest_framework import generics, mixins, views
import logging
logger = logging.getLogger(__name__)

class AbstractBaseView(mixins.CreateModelMixin, mixins.UpdateModelMixin):
    
    def perform_create(self, serializer):
        requester_id = self.request.data.get('audit_trail_user', None)
        created_by_val_id = self.request.data.get('created_by', None)

        requester = None
        created_by_val = None


        if requester_id is not None:
            from apps.ke_mixcloud_core.models import get_default_systemuser
            from apps.authentication.models import CustomUser
            requester = CustomUser.objects.get(id=requester_id)

        from django.contrib.auth.models import AnonymousUser
        if requester is None:
            requester = self.request.user
            if requester is None or AnonymousUser:
                from apps.ke_mixcloud_core.models import get_default_systemuser
                from apps.authentication.models import CustomUser
                requester = CustomUser.objects.get(id=get_default_systemuser())

        if created_by_val_id is not None:
            from apps.ke_mixcloud_core.models import get_default_systemuser
            from apps.authentication.models import CustomUser
            created_by_val = CustomUser.objects.get(id=created_by_val_id)

        if created_by_val is None:
            created_by_val = self.request.user
            if created_by_val is None or AnonymousUser:
                from apps.ke_mixcloud_core.models import get_default_systemuser
                from apps.authentication.models import CustomUser
                created_by_val = CustomUser.objects.get(id=get_default_systemuser())

        serializer.save(audit_trail_user=requester, created_by=created_by_val)

    def perform_update(self, serializer):
        requester_id = self.request.data.get('audit_trail_user', None)

        requester = None

        if requester_id is not None:
            from apps.ke_mixcloud_core.models import get_default_systemuser
            from apps.authentication.models import CustomUser
            requester = CustomUser.objects.get(id=requester_id)

        from django.contrib.auth.models import AnonymousUser
        if requester is None:
            requester = self.request.user

            if requester is None or AnonymousUser:
                from apps.ke_mixcloud_core.models import get_default_systemuser
                from apps.authentication.models import CustomUser
                requester = CustomUser.objects.get(id=get_default_systemuser())


        serializer.save(audit_trail_user=requester)