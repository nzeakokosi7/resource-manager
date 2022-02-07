import requests
from django import forms
from django.forms import RadioSelect

from . import models


class ResourceUploadForm(forms.ModelForm):
    class Meta:
        model = models.Resource
        fields = ['file', 'link']

    # this function will be used for the validation
    def clean(self):

        # data from the form is fetched using super function
        super(ResourceUploadForm, self).clean()

        # extract the username and text field from the data
        file = self.cleaned_data.get('file')
        link = self.cleaned_data.get('link')

        if not link and not file:
            self._errors['file'] = self.error_class([
                "Both inputs can't be blank"])
        if link:
            try:
                response = requests.get(link)
                print("URL is valid and exists on the internet")
            except requests.ConnectionError as exception:
                print("URL does not exist on Internet")
                self._errors['link'] = self.error_class([
                    'URL does not exist on Internet'])

        # return any errors if found
        return self.cleaned_data


class ResourceVerificationForm(forms.Form):
    password = forms.CharField(label="Passkey", max_length=8)
