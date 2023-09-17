from django.db import models
from crontab import CronTab

class Property(models.Model):
    property_name = models.CharField(max_length=255)
    property_cost = models.CharField(max_length=100)
    property_type = models.CharField(max_length=255)
    property_area = models.CharField(max_length=100)
    property_locality = models.CharField(max_length=255)
    property_city = models.CharField(max_length=255)
    property_link = models.URLField()

class ScrapingLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    records_scrapped_count = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.timestamp} - {self.city}, {self.locality}'

class CronJobStatus(models.Model):
    job_name = models.CharField(max_length=100, unique=True)
    is_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.job_name

class CronJobSchedule(models.Model):
    job_name = models.CharField(max_length=100, unique=True)
    cron_schedule = models.CharField(max_length=50)

    def __str__(self):
        return self.job_name
