from django.contrib import admin
from django_cron.admin import CronJobAdmin
from django import forms
# The line `from django_cron.admin import CronJobAdmin` is importing the `CronJobAdmin` class from the
# `django_cron.admin` module. This class is used to customize the admin interface for managing cron
# jobs in Django.
from django_cron.admin import CronJobAdmin
from django_cron.models import CronJobLog
from .models import Property, ScrapingLog, CronJobStatus, CronJobSchedule
from .cron import ScrapePropertiesJob

class CronJobScheduleForm(forms.ModelForm):
    class Meta:
        model = CronJobSchedule
        fields = '__all__'

class CronJobScheduleAdmin(admin.ModelAdmin):
    form = CronJobScheduleForm

class CronJobStatusAdmin(admin.ModelAdmin):
    list_display = ('job_name', 'is_enabled')
    list_filter = ('is_enabled',)
    actions = ['enable_jobs', 'disable_jobs']

    def enable_jobs(self, request, queryset):
        queryset.update(is_enabled=True)
    enable_jobs.short_description = "Enable selected jobs"

    def disable_jobs(self, request, queryset):
        queryset.update(is_enabled=False)
    disable_jobs.short_description = "Disable selected jobs"

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('property_name', 'property_cost', 'property_type', 'property_area', 'property_locality', 'property_city', 'property_link')
    search_fields = ('property_name', 'property_locality', 'property_city')
    list_filter = ('property_city', 'property_locality')

class ScrapingLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'city', 'locality', 'records_scrapped_count')
    list_filter = ('city', 'locality')
    search_fields = ('city', 'locality')

# Register models and admin classes
admin.site.register(Property, PropertyAdmin)
admin.site.register(ScrapingLog, ScrapingLogAdmin)
admin.site.register(CronJobStatus, CronJobStatusAdmin)
admin.site.register(CronJobSchedule, CronJobScheduleAdmin)
admin.site.unregister(CronJobLog)
admin.site.register(ScrapePropertiesJob, CronJobAdmin)