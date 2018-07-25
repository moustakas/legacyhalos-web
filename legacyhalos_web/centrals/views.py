#In Halos
from django.shortcuts import render
from legacyhalos_web.models import Centrals
from .filters import CentralsFilter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
#from django.core.serializers.json import DjangoJSONEncoder
#from django.core.serializers import serialize
#import json
from django.http import HttpResponse
import pickle 


def list(req):
    cen_filter = CentralsFilter(req.GET, queryset=Centrals.objects.all().order_by('mem_match_id'))
    cen_filtered = cen_filter.qs
    req.session['results_list'] = pickle.dumps(cen_filtered)
    #req.session['results_list'] = serialize('json', cen_filtered, cls=LazyEncoder)
    paginator = Paginator(cen_filtered, 50)
    page_num = req.GET.get('page')
    page = paginator.get_page(page_num)
    return render(req, 'list.html', {'page': page, 'paginator': paginator})

def index(req):
    return render(req, 'index.html')

def centrals(req):
    index = int(req.GET.get('index'))
    #cen_list = json.loads(req.session['results_list'])
    cen_list = pickle.loads(req.session['results_list'])
    cen = cen_list[index:index+1][0]
    #cen = cen_list[index - 1]['field']
    prev_index = index - 1
    if (prev_index < 0):
        prev_index = len(cen_list)-1
    next_index = index + 1
    if (next_index == len(cen_list)):
       next_index = 0
    return render(req, 'centrals.html', {'cen_list': cen_list, 'index': index, 'cen': cen, 'next_index': next_index, 'prev_index': prev_index}) 

#class LazyEncoder(DjangoJSONEncoder):
#    def default(self, obj):
#        if instance(obj, Centrals):
#            return str(obj)
#        return super().default(obj)
        
