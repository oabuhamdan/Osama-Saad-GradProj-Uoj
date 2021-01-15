from .models import *
from django.forms import ModelForm


class TitleForm(ModelForm):
    model = Title
    fields = '__all__'


class JobForm(ModelForm):
    model = Job
    fields = '__all__'


class ResultForm(ModelForm):
    model = Result
    fields = '__all__'
