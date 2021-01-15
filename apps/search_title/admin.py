from django.contrib import admin
from django.http import HttpResponse

from .models import *


class TitleAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'released', 'genre', 'director', 'writer', 'actors', 'lang', 'poster',
                    'url']
    search_fields = ['name', 'year', 'released', 'genre', 'director', 'writer', 'actors', 'lang', 'poster',
                     'url']


class JobAdmin(admin.ModelAdmin):
    list_display = ['job_name', 'job_id', 'start_time', 'results_output_path', 'sentiments_count', 'job_done']
    search_fields = ['job_name', 'job_id', 'start_time', 'results_output_path', 'sentiments_count', 'job_done']


class ResultAdmin(admin.ModelAdmin):
    list_display = ['job_name', 'positive', 'negative', 'neutral', 'total']
    search_fields = ['job_name', 'positive', 'negative', 'neutral', 'total']


# Register your models here.
admin.site.register(Title, TitleAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Result, ResultAdmin)
