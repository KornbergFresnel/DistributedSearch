from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import SearchForm
from .models import SearchItem
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import json


# Create your views here.
def index(request):
    # if this is a POST request we need to process the form data
    form = SearchForm(request.GET)
    if form.is_valid():
        q = form.cleaned_data['requery_text']
        return redirect(reverse('search.views.ResultView', kwargs={'requery_text': q}))
    else:
        form = SearchForm()
        return render(request, 'search/index.html', {'form': form})


class ResultView(ListView):
    """This view function operate the display of searching results
    """
    template_name = 'search/result.html'
    pk_url_kwarg = 'requery_text'

    def get_queryset(self):
        search_result = SearchItem.objects.all()
        return search_result

    def get_context_data(self, **kwargs):
        """POST method
        """
        context = super(ResultView, self).get_context_data(**kwargs)
        return context


def result(request, requery_text):
    return render(request, 'search/result.html')
