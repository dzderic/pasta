from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from pasta_app.models import Repository
from pasta_app.forms import NewPastaForm

@login_required
def home(request):
    return render(request, 'index.html', {
        'new_pasta_form': NewPastaForm(),
    })

@login_required
def view_pasta(request, owner, slug):
    repo = get_object_or_404(Repository, owner__username=owner, slug=slug)

    return render(request, 'pasta/view.html', {
        'repo': repo,
    })

@login_required
def new_pasta(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('home'))

    repo = NewPastaForm(request.POST).save(commit=False)
    repo.owner = request.user
    repo.save()
    return HttpResponseRedirect(repo.get_absolute_url())
