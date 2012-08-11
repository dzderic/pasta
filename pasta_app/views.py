from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from guardian.decorators import permission_required_or_403

from pasta_app.models import Repository
from pasta_app.forms import NewPastaForm

@login_required
def home(request):
    return render(request, 'index.html', {
        'new_pasta_form': NewPastaForm(),
        'pastas': Repository.objects.filter(owner=request.user),
    })

@login_required
@permission_required_or_403('read', (Repository, 'owner__username', 'owner', 'slug', 'slug'))
def view_pasta(request, owner, slug, ref):
    pasta = get_object_or_404(Repository, owner__username=owner, slug=slug)
    ref = ref or 'master'

    return render(request, 'pasta/view.html', {
        'pasta': pasta,
        'ref': ref,
        'files': pasta.get_files(ref),
    })

@login_required
def new_pasta(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('home'))

    repo = NewPastaForm(request.POST).save(commit=False)
    repo.owner = request.user
    repo.save()
    return HttpResponseRedirect(repo.get_absolute_url())
