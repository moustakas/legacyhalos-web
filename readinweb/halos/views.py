#In Halos
from django.shortcuts import render
from readinweb.models import Centrals
from .filters import CentralsFilter

def list(req):
    centrals = Centrals.objects.all().order_by('mem_match_id')
    centrals_filter = CentralsFilter(req.GET, queryset=centrals)
    return render(req, 'list.html', {'filter': centrals_filter})

def index(req):
    return render(req, 'index.html')

def boxsearch_results(req, fields_fits_table=False):
    form = SdssPhotRaDecBoxSearchForm(req.GET)
    if not form.is_valid():
        print('Form not valid')
        return HttpResponseRedirect(reverse(coord_search))

    name = form.cleaned_data['name']
    ra = form.cleaned_data['ra']
    declo = form.cleaned_data['dec']

    return _common_search_results(req, form, fields_fits_table=fields_fits_table,
                                  box=(name,ra,dec))

## def coord_search(req):
##     form = None
##     boxform = None

##     if 'coord' in req.GET:
##         form = SdssPhotCoordSearchForm(req.GET)

##         tracking = UserCoordSearch(product=PRODUCT_SDSSPHOT,
##                                    ip=req.META['REMOTE_ADDR'],
##                                    coord_str=form.data.get('coord', None),
##                                    radius_str=form.data.get('radius', None))

##         if form.is_valid():
##             print('Form is valid: data', form.cleaned_data)

##             # Process the data in form.cleaned_data
##             ra,dec = parse_coord(form.cleaned_data['coord'])
##             try:
##                 radius = float(form.cleaned_data['radius'])
##             except:
##                 radius = 0.

##             tracking.ra = ra
##             tracking.dec = dec
##             tracking.radius = radius
##             if dotrack:
##                 tracking.save()

##             datatype = form.cleaned_data['datatype']
##             version = form.cleaned_data['version']
##             password = form.cleaned_data['password']

##             url = 'phot_near/?ra=%g&dec=%g&radius=%g&datatype=%s' % (ra, dec, radius, datatype)
##             if len(version):
##                 url += '&version=%s' % version
##             if len(password):
##                 url += '&password=%s' % password
##             if form.cleaned_data['sdss']:
##                 url += '&sdss'
##             return HttpResponseRedirect(url)

##         # form not valid
##         #print form
        
##         if dotrack:
##             tracking.save()


##     elif 'ralo' in req.GET:
##         boxform = SdssPhotRaDecBoxSearchForm(req.GET)
##         if boxform.is_valid():
##             print('Form is valid: data', boxform.cleaned_data)
##             # Process the data in boxform.cleaned_data
##             ralo = parse_ra(boxform.cleaned_data['ralo'])
##             rahi = parse_ra(boxform.cleaned_data['rahi'])
##             declo = parse_dec(boxform.cleaned_data['declo'])
##             dechi = parse_dec(boxform.cleaned_data['dechi'])
    
##             datatype = boxform.cleaned_data['datatype']
##             version = boxform.cleaned_data['version']
##             password = boxform.cleaned_data['password']
    
##             url = 'phot_box/?ralo=%g&rahi=%g&declo=%g&dechi=%g&datatype=%s' % (ralo, rahi, declo, dechi, datatype)
##             if len(version):
##                 url += '&version=%s' % version
##             if len(password):
##                 url += '&password=%s' % password
##             if boxform.cleaned_data['sdss']:
##                 url += '&sdss'
##             return HttpResponseRedirect(url)

##     if form is None:
##         form = SdssPhotCoordSearchForm()
##         form.initial = dict(coord='200 10', radius=0.1)
##     if boxform is None:
##         boxform = SdssPhotRaDecBoxSearchForm()
##         boxform.initial = dict(ralo=200, rahi=201, declo=10, dechi=11)

##     return render(req, 'sdssphot/coordsearch.html', {
##         #'sdsscollab': 'sdss' in req.GET,
##         'sdsscollab': True,
##         'form': form,
##         'boxform': boxform,
##         'version_choices': version_choices,
##         'datatype_choices': datatype_choices,
##         'url': reverse('phot-search'),
##         'dataurl': settings.SDSSPHOT_DATA_URL,
##     })    
