import os
from django import template
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden, QueryDict, StreamingHttpResponse
import os
import astropy.io.fits
import tempfile
from astropy.table import Table
import numpy as np

register = template.Library()

#try another decorator?
@register.simple_tag
def url_replace(req, field, value):
    dict_ = req.GET.copy()
    dict_[field] = value
    return dict_.urlencode()

@register.simple_tag
def url_replace_sort(req, new_sort):
    dict_ = req.GET.copy()
    if 'sort' in dict_ and dict_['sort'] is not "":
        current_sort = dict_['sort']
        if current_sort == new_sort:
            dict_['sort'] = '-' + new_sort
        else:
            dict_['sort'] = new_sort
    else:
        dict_['sort'] = new_sort
    return dict_.urlencode()
    

@register.simple_tag
def url_pull(req):
    dict_ = req.GET.copy()
    search = "Search Criteria:"
    entry = False
    if "mem_match_id__gte" in dict_:
        if dict_["mem_match_id__gte"] == "":
            search += " redMaPPer ID low: 45 |"
        else:
            search += " redMaPPer ID low: " + dict_["mem_match_id__gte"] + " |"
            entry = True
    if "mem_match_id__lte" in dict_:
        if dict_["mem_match_id__lte"] == "":
            search += "redMaPPer ID high: 695620 |"
        else:
            search += " redMaPPer ID high : " + dict_["mem_match_id__lte"] + " |"
            entry = True
    if "ra__gte" in dict_:
        if dict_["ra__gte"] ==  "":
            search += "\n RA low: 0 |"
        else:
            search += "\n RA low: " + dict_["ra__gte"] + " |"
            entry = True
    if "ra__lte" in dict_:
        if dict_["ra__lte"] == "":
            search += " RA high: 360 |"
        else:
            search += " RA high: " + dict_["ra__lte"] + " |"            
            entry = True
    if "dec__gte" in dict_:
        if dict_["dec__gte"] ==  "":
            search += " Dec low: -11 |"
        else:
            search += " Dec low: " + dict_["dec__gte"] + " |"
            entry = True
    if "dec__lte" in dict_:
        if dict_["dec__lte"] == "":
            search += " Dec high: 32 |"
        else:
            search += " Dec high: " + dict_["dec__lte"] + " |"
            entry = True
    if "z__gte" in dict_:
        if dict_["z__gte"] ==  "":
            search += "\n Redshift low: 0 |"
        else:
            search += "\n Redshift low: " + dict_["z__gte"] + " |"
            entry = True
    if "z__lte" in dict_:
        if dict_["z__lte"] == "":
            search += " Redshift high: 32 |"
        else:
            search += " Redshift high: " + dict_["z__lte"] + " |"
            entry = True
    if "la__gte" in dict_:
        if dict_["la__gte"] ==  "":
            search += " Richness low: -11 |"
        else:
            search += " Richness low: " + dict_["dec__gte"] + " |"
            entry = True
    if "la__lte" in dict_:
        if dict_["la__lte"] == "":
            search += " Redshift high: 32 |"
        else:
            search += " Redshift high: " + dict_["la__lte"] + " |"
            entry = True
    if not entry:
        search = "Showing all results"
    else:
        search = search[:-1]
    return search

def create_temp(**kwargs):
    tempdir = os.environ.get('TMPDIR', os.environ.get('TMP','/tmp'))
    f, fn = tempfile.mkstemp(dir=tempdir, **kwargs)
    os.close(f)
    os.unlink(fn)
    return fn

@register.simple_tag
def photo_pull(req, id_num, img_name):
    path = "static/data/" + id_num + "/" + id_num + "-" + img_name 
    return path    

@register.simple_tag
def viewer_link(ra, dec):
    baseurl = 'http://legacysurvey.org/viewer/'
    viewer = '{}?ra={:.6f}&dec={:.6f}&zoom=15&layer=decals-dr5'.format(baseurl, ra, dec)
    return viewer

@register.simple_tag
def skyserver_link(sdss_objid):
        return 'http://skyserver.sdss.org/dr14/en/tools/explore/summary.aspx?id=%d' % sdss_objid

@register.simple_tag
def download(req):
    #cen_list = pickle.loads(req.session['results_list'])
    #for cen in cen_list:
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
    # file was last modified...
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
