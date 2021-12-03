from django.contrib import admin
from django import forms
from .models import HelpMessage


class HelpMessageAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(HelpMessageAdminForm, self).__init__(*args, **kwargs)
        # user = kwargs['instance'].customer.user
        # self['first_name'].initial = user.first_name
        # self['last_name'].initial = user.last_name
        # self['email'].initial = user.email

    class Meta:
        model = HelpMessage
        fields = '__all__'


class HelpMessageAdmin(admin.ModelAdmin):
    model = HelpMessage
    form = HelpMessageAdminForm
    list_display = ('get_email', 'get_first_name', 'get_last_name', 'message')
    list_filter = ('firstname',)

    def get_first_name(self, obj):
        return obj.firstname if len(obj.firstname) > 1 else 'Not provided'
    get_first_name.short_description = 'Имя'

    def get_last_name(self, obj):
        return obj.surname if len(obj.surname) > 1 else 'Not provided'
    get_last_name.short_description = 'Фамилия'

    def get_email(self, obj):
        return obj.email if len(obj.email) > 1 else 'Not provided'
    get_email.short_description = 'Электронная почта'


admin.site.register(HelpMessage, HelpMessageAdmin)
