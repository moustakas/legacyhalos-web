#In Halos
from django.shortcuts import render
from readinweb.models import Centrals
from .filters import CentralsFilter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def list(req):
    cen_filtered = CentralsFilter(req.GET, queryset=Centrals.objects.all().order_by('mem_match_id')).qs
    #cen_filtered.save()
    paginator = Paginator(cen_filtered, 50)
    page_num = req.GET.get('page')
    page = paginator.get_page(page_num)
    return render(req, 'list.html', {'page': page})

def index(req):
    return render(req, 'index.html')

def centrals(req):
    return render(req, 'centrals.html') 
