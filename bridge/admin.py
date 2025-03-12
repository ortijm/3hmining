from django.contrib import admin
from django import forms
from .models import BridgeTask, Minera, TypeBridgeTask, BridgeResponse, BridgeConnectionLog
from django.forms import ValidationError
#from prettyjson import PrettyJSONWidget
#from django.utils.translation import ugettext_lazy as _

class BridgeTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'enabled','desc', 'init','ping', 'bridge')
    list_filter = ['bridge','typeTask']
    class Media:
        js = ('js/codemirror/codemirror.js',
              'js/codemirror/mode/sql/sql.js',
              'js/codemirror_bridge_task.js')
        css = {
            "all": ("css/admin.css",'css/codemirror/codemirror.css')
        }
    def clean(self):
        # Validation goes here :)
        raise ValidationError("TEST EXCEPTION!")


admin.site.register(BridgeTask, BridgeTaskAdmin)


class MineraAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'enabled')


admin.site.register(Minera, MineraAdmin)


class TypeBridgeTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'function')


admin.site.register(TypeBridgeTask, TypeBridgeTaskAdmin)


class BridgeResponseForm(forms.ModelForm):
    class Meta:
        model = BridgeResponse
        fields = '__all__'
        #widgets = {
        #  'response': PrettyJSONWidget(),
        #}
    class Media:
        js = ('js/codemirror/codemirror.js',
              'js/codemirror/mode/javascript/javascript.js',
              'js/codemirror/lib/util/formatting.js',
              'js/codemirror_config_bridge_response.js')
        css = {
            "all": ("css/admin.css",'css/codemirror/codemirror.css')
        }



class BridgeResponseAdmin(admin.ModelAdmin):
    list_display = ('bridge', 'name', 'status', 'dateResponse')
    form = BridgeResponseForm
    list_filter = ['bridge', 'status', 'typeTask']

admin.site.register(BridgeResponse, BridgeResponseAdmin)

class BridgeConnectionLogForm(forms.ModelForm):
    class Meta:
        model = BridgeConnectionLog
        fields = '__all__'
        #widgets = {
        #  'response': PrettyJSONWidget(),
        #}
    class Media:
        js = ('js/codemirror/codemirror.js',
              'js/codemirror/mode/javascript/javascript.js',
              'js/codemirror/lib/util/formatting.js',
              'js/codemirror_config_bridge_access.js')
        css = {
            "all": ("css/admin.css",'css/codemirror/codemirror.css')
        }


class BridgeConnectionLogAdmin(admin.ModelAdmin):
    list_display = ('remoteId', 'bridgeName','accessTime')
    list_filter = ['remoteId', 'bridgeName']
    form = BridgeConnectionLogForm

admin.site.register(BridgeConnectionLog, BridgeConnectionLogAdmin)