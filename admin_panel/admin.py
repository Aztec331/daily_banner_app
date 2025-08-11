from django.contrib import admin
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured

def make_admin_for_model(model):
    field_name = [f.name for f in model._meta.get_fields() if getattr(f, 'concrete', True)]
    list_display = field_name[:6] or ['__str__']

    search_fields = []
    for candidate in ('name', 'title', 'file', 'filename', 'path'):
        if candidate in field_name:
            search_fields.append(candidate)
    
    list_filter = []
    for candidate in field_name:
        try:
            f = model._meta.get_field(candidate)
            if f.get_internal_type() in ('BooleanField', 'NullBooleanField') or getattr(f, 'related_model', None):
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

    return type(f"{model.__name__}Admin", (admin.ModelAdmin,), attrs)

# Set the correct app label
app_label = 'admin_panel'

try:
    app_config = apps.get_app_config(app_label)
except LookupError:
    raise ImproperlyConfigured(f"App '{app_label}' not found. Make sure the app is in INSTALLED_APPS.")

for model in app_config.get_models():
    try:
        admin.site.register(model, make_admin_for_model(model))
    except admin.sites.AlreadyRegistered:
        pass
