from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from pasta_app.models import Repository

@login_required
def home(request):
    return render(request, 'index.html')

@login_required
def edit_pasta(request):
    return render(request, 'index.html')

@login_required
def new_pasta(request):
    if 'new-pasta-name' not in request.POST:
        return HttpResponseRedirect(reverse('home'))

    repo = Repository(owner=request.user, name=request.POST['new-pasta-name'])
    repo.save()
    return HttpResponseRedirect(repo.get_edit_url())
