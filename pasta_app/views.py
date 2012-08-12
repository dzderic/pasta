from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from guardian.decorators import permission_required_or_403

from pasta_app.models import Repository
from pasta_app.forms import NewPastaForm

@login_required
def home(request):
    return render(request, 'index.html', {
        'new_pasta_form': NewPastaForm(),
        'pastas': Repository.objects.filter(owner=request.user).order_by('-created'),
    })

@login_required
@permission_required_or_403('read', (Repository, 'owner__username', 'owner', 'slug', 'slug'))
def do_commit(request, owner, slug):
    pasta = get_object_or_404(Repository, owner__username=owner, slug=slug)

    # TODO
    to_commit = simplejson.loads(request.raw_post_data)
    pasta.commit(request.user, to_commit['message'], to_commit['files'])
    return HttpResponse('{}', mimetype='application/json')

@login_required
@permission_required_or_403('read', (Repository, 'owner__username', 'owner', 'slug', 'slug'))
def view_pasta(request, owner, slug, ref):
    pasta = get_object_or_404(Repository, owner__username=owner, slug=slug)
    if not ref:
        return HttpResponseRedirect(reverse('view-pasta',
                                    kwargs={'owner': owner, 'slug': slug, 'ref': 'master'}))

    return render(request, 'pasta/view.html', {
        'pasta': pasta,
        'ref': ref,
        'files': list(pasta.get_files(ref)),
    })

@login_required
def new_pasta(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('home'))

    repo = NewPastaForm(request.POST).save(commit=False)
    repo.owner = request.user
    repo.save()
    return HttpResponseRedirect(repo.get_absolute_url())
