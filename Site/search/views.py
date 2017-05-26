from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import SearchForm
from .models import SearchItem
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import Crawler.Crawler.Search.search as Search
import json


# Create your views here.
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['q']
            context = SearchItem.objects.all()
            return render(request, 'search/result.html', {'context': context, 'form': form})
    else:
        form = SearchForm()
    return render(request, 'search/index.html', {'form': form})


def search(request):
    """Handling search request
    """
