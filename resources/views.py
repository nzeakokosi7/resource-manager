import random
import string
import time

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views import View
from rest_framework import viewsets
from datetime import datetime

from . import forms, models, serializers


# Create your views here.
from rest_framework.permissions import IsAuthenticated

@login_required
def upload_success(request):
    link = request.session.get('link')
    key = request.session.get('key')
    return render(request, 'upload_success.html', context={'key': key, 'url': link})


@login_required
def access_granted(request):
    file = request.session.get('file')
    url = request.session.get('url')
    return render(request, 'resource_validation_success.html', context={'file': file, 'url': url})


@login_required
def resource_upload(request):
    form = forms.ResourceUploadForm()
    host = str(request.META['HTTP_HOST'])
    if request.method == 'POST':
        form = forms.ResourceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            # set the uploader to the user before saving the model
            file.uploader = request.user

            time_stamp = current_milli_time()
            key = get_random_password()

            file.time_stamp = time_stamp
            file.key = key
            # now we can save
            file.save()
            link = host + "/resource/retrieve/" + str(time_stamp)
            request.session['key'] = key
            request.session['link'] = link
            return redirect('resource_confirmation')
    return render(request, 'upload.html', context={'form': form})


def update_logs(var):
    today = datetime.today().strftime('%Y-%m-%d')
    if var == "file":
        if models.ResourceLog.objects.filter(datetime=today).exists():
            resource_log = models.ResourceLog.objects.get(datetime=today)
            resource_log_serializer = serializers.ResourceLogSerializer(resource_log,
                                                                        data={"files": resource_log.files + 1},
                                                                        partial=True)
            if resource_log_serializer.is_valid():
                resource_log_serializer.save()
        else:
            models.ResourceLog.objects.create(datetime=today, files=1, links=0)
    else:
        if models.ResourceLog.objects.filter(datetime=today).exists():
            resource_log = models.ResourceLog.objects.get(datetime=today)
            resource_log_serializer = serializers.ResourceLogSerializer(resource_log,
                                                                        data={"links": resource_log.links + 1},
                                                                        partial=True)
            if resource_log_serializer.is_valid():
                resource_log_serializer.save()
        else:
            models.ResourceLog.objects.create(datetime=today, files=0, links=1)


class ResourceFetchView(View):
    verification_template = 'resource_validation.html'
    form_class = forms.ResourceVerificationForm

    def get(self, request, pk):
        form = self.form_class
        if pk:
            try:
                resource = models.Resource.objects.get(time_stamp=pk)
            except models.Resource.DoesNotExist:
                return render(request, self.verification_template, context={'error': 'Invalid Link'})
            if resource.is_expired:
                return render(request, self.verification_template, context={'error': 'Link has expired'})
            return render(request, self.verification_template, context={'form': form})
        return render(request, self.verification_template, context={'error': 'Invalid Link'})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            if models.Resource.objects.filter(time_stamp=pk).exists():
                resource = models.Resource.objects.get(time_stamp=pk)
                print(password)
                print(resource.key)
                if password == resource.key:
                    file = resource.file
                    url = resource.link
                    print(file)
                    if file:
                        request.session['file'] = "true"
                        request.session['url'] = file.url

                        update_logs("file")
                        return redirect('access_granted')
                    update_logs("link")
                    request.session['url'] = url
                    return redirect('access_granted')
                return render(request, self.verification_template,
                              context={'form': form, 'wrong_password': "Wrong password, please try again"})


def current_milli_time():
    return round(time.time() * 1000)


def get_random_password():
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation

    all = lower + upper + symbols + num

    temp = random.sample(all, 8)

    return "".join(temp)


class ResourceLogViewset(viewsets.ModelViewSet):
    queryset = models.ResourceLog.objects.all()
    serializer_class = serializers.ResourceLogSerializer
    permission_classes = [IsAuthenticated, ]
