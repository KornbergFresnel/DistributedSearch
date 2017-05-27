from django.shortcuts import render, redirect
from .forms import SearchForm
from .models import SearchItem
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import Crawler.Crawler.Search.search as Search
import datetime


# Create your views here.
def index(request):
    # if this is a POST request we need to process the form data
    now = datetime.datetime.now()
    return render(request, 'search/index.html', {'current_time': now})


def search(request):
    """Handling search request
    """
    if 'q' in request.GET:
        q = request.GET['q']
        # results = SearchItem.objects.all()
        results = Search.search_request(q)
        return render(request, 'search/result.html', {'results': results, 'query': q})
