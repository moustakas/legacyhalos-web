#In Halos
from django.shortcuts import render
from readinweb.models import Centrals
from .filters import CentralsFilter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def list(req):
    centrals_filter = CentralsFilter(req.GET, queryset=Centrals.objects.all().order_by('mem_match_id')).qs
    paginator = Paginator(centrals_filter, 50)
    page = req.GET.get('page')
    result = paginator.get_page(page)
    return render(req, 'list.html', {'result': result})

def index(req):
    return render(req, 'index.html')


