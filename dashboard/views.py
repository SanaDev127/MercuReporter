from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
from django.http import HttpResponse


@login_required
def owner_dashboard(request):
    user = request.user # get the user, get their data, return it to the template
    return render(request,
                  'dashboards/owner_dashboard.html',
                  {'section': 'dashboards'})  # Data required to render dashboard


@login_required
def supervisor_dashboard(request):
    user = request.user # get the user, get their data, return it to the template
    return render(request,
                  'dashboards/supervisor_dashboard.html',
                  {'section': 'dashboards'})  # Data required to render dashboard


@login_required
def driver_dashboard(request):
    user = request.user # get the user, get their data, return it to the template
    return render(request,
                  'dashboards/driver_dashboard.html',
                  {'section': 'dashboards'})  # Data required to render dashboard


def upload_transaction_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['file']
        return HttpResponse(f'The name of the file is {file}')
    else:
        form = UploadFileForm()
    return render(request, 'admin/file_upload.html', {'form': form})


class HomePageView(TemplateView):
    template_name = "home.html"

