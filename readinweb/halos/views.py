#In Halos
from django.shortcuts import render
from readinweb.models import Centrals
from .filters import CentralsFilter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator



def list(req):
    cen_filter = CentralsFilter(req.GET, queryset=Centrals.objects.all().order_by('mem_match_id'))
    cen_filtered = cen_filter.qs
    
    #put each item in the list in a loop
    req.session['results_list'] = list(Centrals.objects.filter(cen_filtered))
    paginator = Paginator(cen_filtered, 50)
    page_num = req.GET.get('page')
    page = paginator.get_page(page_num)
    return render(req, 'list.html', {'page': page})

def index(req):
    return render(req, 'index.html')

def centrals(req):
    index = req.GET.get('index')
    cen_list = request.session['results_list']
    current_cen = cen_list[index - 1]
    #prev_cen = cen_list[index - 2]
    #next_cen = cen_list[index]
    return render(req, 'centrals.html', {'current_cen': current_cen, 'index': index}) 
