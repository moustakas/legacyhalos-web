from django.shortcuts import render
from legacyhalos_web.models import Centrals
from .filters import CentralsFilter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
import pickle
import tempfile
import os
import astropy.io.fits
from astropy.table import Table

def list(req):
    sort = 'mem_match_id'
    if "sort" in req.GET:
        sort = req.GET.get('sort')
    cen_filter = CentralsFilter(req.GET, queryset=Centrals.objects.all().order_by(sort))
    cen_filtered = cen_filter.qs
    req.session['results_list'] = pickle.dumps(cen_filtered)
    paginator = Paginator(cen_filtered, 50)
    page_num = req.GET.get('page')
    page = paginator.get_page(page_num)
    if req.method== 'POST':
        return download(req)
    return render(req, 'list.html', {'page': page, 'paginator': paginator})

def index(req):
    return render(req, 'index.html')

def centrals(req):
    index = int(req.GET.get('index'))
    cen_list = pickle.loads(req.session['results_list'])
    cen = cen_list[index-1:index][0]
    prev_index = index - 1
    if (prev_index == 0):
        prev_index = len(cen_list)
    next_index = index + 1
    if (next_index > len(cen_list)):
       next_index = 1
    return render(req, 'centrals.html', {'cen_list': cen_list, 'index': index, 'cen': cen, 'next_index': next_index, 'prev_index': prev_index})

def download(req):
    #cen_list = pickle.loads(req.session['results_list'])
    #for cen in cen_list:req.GET.get('
    #    table
    # Create your table of results... probably from a database query.
    # Should probably use astropy.io.fits instead of astrometry.util.fits!
    #data_rows = [{1,2.0, 'x'},
    #             {4,5.0, 'y'},
    #             {5,8.2, 'z'}]
    #table = Table(rows=data_rows, names=('a','b','c'))
    #table.write
    #table = fits_table()
    table = Table([[1, 2], [4, 5], [7, 8]], names=('a', 'b', 'c'))
    #tempfiletable =  tempfile.mkstemp(suffix='.fits')
    #table.write(tempfiletable, format='fits')
    #table.x = np.arange(3)
    f,tmpfn = tempfile.mkstemp(suffix='.fits')
    os.close(f)
    os.unlink(tmpfn)
    # Write the FITS file contents...
    table.write(tmpfn)
    return send_file(tmpfn, 'image/fits', unlink=True, filename='results.fits')


def send_file(fn, content_type, unlink=False, modsince=None, expires=3600,
              filename=None):
    import datetime
    from django.http import HttpResponseNotModified, StreamingHttpResponse
    '''
    modsince: If-Modified-Since header string from the client.
    '''
    st = os.stat(fn)
    f = open(fn, 'rb')
    if unlink:
        os.unlink(fn)
    # file was last modified.
    lastmod = datetime.datetime.fromtimestamp(st.st_mtime)

    if modsince:
        #print('If-modified-since:', modsince #Sat, 22 Nov 2014 01:12:39 GMT)
        ifmod = datetime.datetime.strptime(modsince, '%a, %d %b %Y %H:%M:%S %Z')
        #print('Parsed:', ifmod)
        #print('Last mod:', lastmod)
        dt = (lastmod - ifmod).total_seconds()
        if dt < 1:
            return HttpResponseNotModified()

    res = StreamingHttpResponse(f, content_type=content_type)
    # res['Cache-Control'] = 'public, max-age=31536000'
    res['Content-Length'] = st.st_size
    if filename is not None:
        res['Content-Disposition'] = 'attachment; filename="%s"' % filename
    # expires in an hour?
    now = datetime.datetime.utcnow()
    then = now + datetime.timedelta(0, expires, 0)
    timefmt = '%a, %d %b %Y %H:%M:%S GMT'
    res['Expires'] = then.strftime(timefmt)
    res['Last-Modified'] = lastmod.strftime(timefmt)
    return res
