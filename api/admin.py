from django.contrib import admin

from .models import DynamicEndpoint, DynamicGraph


def clone_endpoint(modeladmin, request, queryset):
    for obj in queryset:
        obj.id = None
        obj.bridge = None
        obj.save()
clone_endpoint.short_description = "Clone Entry"


class DynamicGraphAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type', 'data', 'description')
    class Media:
        js = ('js/codemirror/codemirror.js',
              'js/codemirror/mode/javascript/javascript.js',
              'js/codemirror/lib/util/formatting.js',
              'js/codemirror_config_graph_data.js')
        css = {
            "all": ("css/admin.css",'css/codemirror/codemirror.css')
        }
    actions = [clone_endpoint]
admin.site.register(DynamicGraph, DynamicGraphAdmin)


class DynamicEndpointAdmin(admin.ModelAdmin):
    list_display = ('id', 'endpoint_url', 'bridge')
    actions = [clone_endpoint]
admin.site.register(DynamicEndpoint, DynamicEndpointAdmin)
