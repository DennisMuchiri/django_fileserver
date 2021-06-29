from django.contrib import admin

class BaseAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(BaseAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['created_by'].initial = request.user
        return form