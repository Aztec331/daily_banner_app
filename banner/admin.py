from django.contrib import admin
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured

# Register your models here.
def make_admin_for_model(model):
    field_names = [f.name for f in model._meta.get_fields() if getattr(f, 'concrete', True)]
    list_display = field_names[:6] or ['__str__']

    search_fields = []
    for candidate in ('name', 'title', 'file', 'filename', 'path'):
        if candidate in field_names:
            search_fields.append(candidate)

    list_filter = []
    for candidate in field_names:
        try:
            f = model._meta.get_field(candidate)
            if f.get_internal_type() in ('BooleanField','NullBooleanField') or getattr(f,'related_model',None):
                list_filter.append(candidate)
        except Exception:
            continue
    attrs = {}
    if list_display:
        attrs['list_display'] = list_display
    if search_fields:
        attrs['search_fields'] = search_fields
    if list_filter:
        attrs['list_filter'] = list_filter

    return type(f"{model.__name__}Admin", (admin.ModelAdmin,),attrs)

app_label = 'banner'
try:
    app_config = apps.get_app_config(app_label)
except LookupError:
    raise ImproperlyConfigured(f"App '{app_label}' not found. Make sure the app is in INSTALLED_APPS.")

for model in app_config.get_models():
    try:
        admin.site.register(model, make_admin_for_model(model))
    except admin.sites.AlreadyRegistered:
        pass