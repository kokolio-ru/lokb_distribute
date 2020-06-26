from django import forms
from . import models


class PatientForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=False)
    diagnosis = forms.CharField(max_length=100, required=False)
    status = forms.ModelChoiceField(queryset=models.Status.objects.all())
    comment = forms.Textarea()
    important = forms.BooleanField(required=False)

    class Meta:
        model = models.Patient
        fields = ('name', 'diagnosis', 'status', 'comment', 'important')
