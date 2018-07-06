from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden, QueryDict, StreamingHttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django import forms
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import tempfile

#from unwise.common import *
#from unwise.models import *
#from sdssphot.models import *

from astrometry.util.fits import *
from astrometry.util.starutil_numpy import *
from astrometry.libkd.spherematch import *

from legacyhalos_web import settings

#dotrack = True
dotrack = False

def parse_ra(rastr):
    try:
        ra = float(rastr)
    except:
        try:
            ra = hmsstring2ra(rastr)
        except:
            raise ValidationError('Failed to parse RA string: "%s" -- allowed formats are decimal degrees or HH:MM:SS' % rastr)
    return ra
        
def parse_dec(decstr):
    try:
        dec = float(decstr)
    except:
        try:
            dec = dmsstring2dec(decstr)
        except:
            raise ValidationError('Failed to parse Dec string: "%s" -- allowed formats are decimal degrees or +-DD:MM:SS' % decstr)
    return dec

# version_choices = [
#     ('sdss-dr10d', 'SDSS DR10'),
#     ('sdss-dr13',  'SDSS DR13'),
#     ('eboss',      'eBOSS targeting'),
#     #('sequels',    'SEQUELS targeting (requires SDSS password)'),
#     ]
# version_default = 'sdss-dr13'

password_versions = []

#sdssurls = {
#    'sdss-dr10d': 'http://data.sdss3.org/sas/dr10/boss/photoObj/301/',
#    'sdss-dr13' : 'http://data.sdss3.org/sas/ebosswork/eboss/photoObj.v5b/301/',
#    'eboss'     : 'http://data.sdss3.org/sas/ebosswork/eboss/photoObj.v5b/301/',
#    }

# datatype_choices = [
#     ('flat', 'Flat FITS table'),
#     ('wise', 'WISE tiles in range'),
#     ('sdss', 'SDSS fields in range')
#     ]
# datatype_default = 'flat'

#def get_phot_data_url(version, dtype):
#    version = str(version)
#    if version in password_versions:
#        return settings.SDSSPHOT_DATA_URL + '/sdss-collab/' + version + '-' + dtype + '/'
#    return settings.SDSSPHOT_DATA_URL + '/' + version + '-' + dtype + '/'
#
#def get_phot_data_path(version, dtype):
#    version = str(version)
#    if version in password_versions:
#        return os.path.join(settings.SDSSPHOT_DATA_DIR, 'sdss-collab', version + '-' + dtype)
#    return os.path.join(settings.SDSSPHOT_DATA_DIR, version + '-' + dtype)

## mix-in
#class SdssPhotForm(forms.Form):
#    sdss = forms.BooleanField(required=False, initial=False)
#
#    #version = forms.ChoiceField(required=False, initial=version_default,
#    #                            choices=version_choices,)
#    #datatype = forms.ChoiceField(required=True, initial=datatype_default,
#    #                             choices=datatype_choices)
#    #password = forms.CharField(widget=forms.PasswordInput(),#render_value=True),
#    #                           required=False)
#
#    def clean(self):
#        if self.cleaned_data['datatype'] == 'flat':
#            if self.cleaned_data.get('radius',0) > 1.:
#                raise ValidationError('For flat FITS tables, the maximum search radius is 1 degree')
#        if self.cleaned_data['datatype'] == 'sdss':
#            if self.cleaned_data.get('radius',0) > 10.:
#                raise ValidationError('For SDSS fields, the maximum search radius is 10 degrees')
#
#        if 'ralo' in self.cleaned_data:
#            if not 'rahi' in self.cleaned_data:
#                raise ValidationError('If RA low is given, RA high must be given too')
#            if not float(self.cleaned_data['ralo']) < float(self.cleaned_data['rahi']):
#                raise ValidationError('RA low must be less than RA high')
#
#            dra = self.cleaned_data.get('rahi') - self.cleaned_data.get('ralo')
#            if self.cleaned_data['datatype'] == 'flat':
#                if dra > 1.:
#                    raise ValidationError('For flat FITS tables, the maximum RAhi - RAlo is 1 degree')
#            if self.cleaned_data['datatype'] == 'sdss':
#                if dra > 10.:
#                    raise ValidationError('For SDSS fields, the maximum RAhi - RAlo is 1 degree')
#
#        if 'declo' in self.cleaned_data:
#            if not 'dechi' in self.cleaned_data:
#                raise ValidationError('If Dec low is given, Dec high must be given too')
#            if not float(self.cleaned_data['declo']) < float(self.cleaned_data['dechi']):
#                raise ValidationError('Dec low must be less than Dec high')
#
#            ddec = self.cleaned_data.get('dechi') - self.cleaned_data.get('declo')
#            if self.cleaned_data['datatype'] == 'flat':
#                if ddec > 1.:
#                    raise ValidationError('For flat FITS tables, the maximum DEChi - DEClo is 1 degree')
#            if self.cleaned_data['datatype'] == 'sdss':
#                if ddec > 10.:
#                    raise ValidationError('For SDSS fields, the maximum DEChi - DEClo is 1 degree')
#
#
#        version = str(self.cleaned_data['version'])
#        print 'Version', version
#        if version is None or len(version) == 0:
#            version = version_default
#        print 'Version', version
#        if not version in [k for k,v in version_choices]:
#            raise ValidationError('Unknown version')
#        print 'known version'
#        if version in password_versions:
#            password = self.cleaned_data['password']
#            if not password in settings.SDSS_PASSWORDS:
#                raise ValidationError('Incorrect password.  Contact dstndstn@gmail.com for help.')
#            print 'password okay'
#        else:
#            print 'public version'
#        self.cleaned_data['version'] = version
#        return self.cleaned_data


class CentralsRaDecBoxSearchForm(forms.Form):

    ralo  = forms.FloatField(required=False, validators=[parse_ra])
    rahi  = forms.FloatField(required=False, validators=[parse_ra])
    declo = forms.FloatField(required=False, validators=[parse_dec])
    dechi = forms.FloatField(required=False, validators=[parse_dec])

    cen = forms.BooleanField(required=False, initial=False)

    
tempdir = os.environ.get('TMPDIR', os.environ.get('TMP', '/tmp'))
def create_temp(**kwargs):
    f,fn = tempfile.mkstemp(dir=tempdir, **kwargs)
    os.close(f)
    os.unlink(fn)
    return fn

    
class mytabledata(tabledata):
    def __getitem__(self, I):
        if isinstance(I, basestring):
            raise TypeError('Cannot index using string')
        return super(mytabledata, self).__getitem__(I)

def boxsearch_results(req, fields_fits_table=False):
    form = CentralsRaDecBoxSearchForm(req.GET)
    if not form.is_valid():
        print 'Form not valid'
        return HttpResponseRedirect(reverse(coord_search))

    ralo = form.cleaned_data['ralo']
    rahi = form.cleaned_data['rahi']
    declo = form.cleaned_data['declo']
    dechi = form.cleaned_data['dechi']

    return _common_search_results(req, form, fields_fits_table=fields_fits_table,
                                  box=(ralo,rahi,declo,dechi))

def conesearch_results(req, fields_fits_table=False):
    #
    form = SdssPhotRaDecSearchForm(req.GET)
    if not form.is_valid():
        print 'Form not valid'
        return HttpResponseRedirect(reverse(coord_search))

    ra  = form.cleaned_data['ra']
    if ra is None:
        ra = 0.
    dec = form.cleaned_data['dec']
    if dec is None:
        dec = 0
    rad = form.cleaned_data['radius']
    if rad is None:
        rad = 0.
    rad = max(0., rad)

    return _common_search_results(req, form, fields_fits_table=fields_fits_table,
                                  cone=(ra,dec,rad))


def _common_search_results(req, form, fields_fits_table=False,
                           box=None, cone=None):

    assert((box is not None) or (cone is not None))

    version = form.cleaned_data['version']
    dtype = form.cleaned_data['datatype']
    if dtype is None or dtype == '':
        dtype = datatype_default

    if version in password_versions:
        # if the form validated, the password matched.
        req.session['authenticated']  = True
        req.session['version'] = version

    if cone is not None:
        ra,dec,rad = cone
    else:
        ralo,rahi,declo,dechi = box
        ra  = (ralo  + rahi ) / 2.
        dec = (declo + dechi) / 2.
        rad = degrees_between(ralo, declo, rahi, dechi) / 2.

    if dtype in ['flat', 'sdss'] or fields_fits_table:
        # FIXME -- this is resolve-specific, ie version-specific.
        kdfn = settings.WINDOW_FLIST_KD
        # Find SDSS fields in range.
        kd = tree_open(kdfn)

        # enlarge search radius by SDSS field size
        srad = rad + np.hypot(14.,10.)/60./2.
        #print 'Search radius:', srad, 'deg'
        I,nil = tree_search_radec(kd, ra, dec, srad,
                                  sortdists=True)
        tree_close(kd)
        #print 'Search result:', len(I), 'fields'
        if len(I):
            T = fits_table(kdfn, hdu=6, rows=I, tabledata_class=mytabledata)
        else:
            T = tabledata()

        if box is not None:
            # Cut cone to box...
            T.cut((T.dec - srad <= dechi) * (T.dec + srad >= declo))
            dra = srad / np.cos(np.deg2rad(dec))
            if ralo - dra < 0 or rahi + dra > 360:
                # wrap-around...
                if ralo < dra:
                    # close to 0
                    I = np.logical_or(T.ra < rahi + dra, T.ra > ralo + 360. - dra)
                else:
                    # close to 360
                    I = np.logical_or(T.ra > ralo - dra, T.ra < rahi + dra - 360.)
            else:
                # plain old
                I = (T.ra > ralo - dra) * (T.ra < rahi + dra)
            T.cut(I)

    if fields_fits_table:
        T.wiseurl = np.array([req.build_absolute_uri(
            '%s%s/%s/photoWiseForced-%06i-%i-%04i.fits' %
            (get_phot_data_url(version, 'pobj'), t.run, t.camcol, t.run, t.camcol, t.field))
                              for t in T])
        T.sdssurl = np.array([sdssurls[version] +
                              '%s/%s/photoObj-%06i-%i-%04i.fits' %
                              (t.run, t.camcol, t.run, t.camcol, t.field)
                              for t in T])
        
        tempfn = create_temp()
        T.writeto(tempfn)
        res = StreamingHttpResponse(open(tempfn))
        os.unlink(tempfn)
        res['Content-type'] = 'application/fits'
        res['Content-Disposition'] = 'attachment; filename="sdss-fields.fits"'
        return res

    if dtype == 'flat':
        TT = []
        #print len(T), 'SDSS fields'
        if len(T) == 0:
            return HttpResponseBadRequest('No objects match your query (probably outside SDSS footprint).')
        for run,camcol,field in zip(T.run, T.camcol, T.field):
            fn = os.path.join(get_phot_data_path(version, 'pobj'),
                              '%i'%run, '%i'%camcol,
                              'photoWiseForced-%06i-%i-%04i.fits' %
                              (run, camcol, field))
            if not os.path.exists(fn):
                #print 'Does not exist:', fn
                continue
            tt = fits_table(fn)
            if tt is None:
                continue
            #print len(tt), 'from', fn
            tt.cut(tt.objid != '                   ')
            #print len(tt), 'with objids'
            if len(tt) == 0:
                continue
            #
            if cone is not None:
                dists = degrees_between(ra, dec, tt.ra, tt.dec)
                I = np.atleast_1d(dists <= rad)
            else:
                I = ((tt.ra  >= ralo ) * (tt.ra  <= rahi) *
                     (tt.dec >= declo) * (tt.dec <= dechi))

            tt.cut(I)
            if len(tt) == 0:
                continue
            if cone is not None:
                tt.match_dist = dists[I]
            n = len(tt)
            tt.run = np.empty(n, np.int16)
            tt.run[:] = run
            tt.camcol = np.empty(n, np.uint8)
            tt.camcol[:] = camcol
            tt.field = np.empty(n, np.int16)
            tt.field[:] = field
            TT.append(tt)
        if len(TT) == 0:
            return HttpResponseBadRequest('No objects match your query.')
        T = merge_tables(TT)
        if cone is not None:
            T.cut(np.argsort(T.match_dist))
        del TT
        #print 'Total of', len(T), 'sources'
        #print 'has_wise_phot:', np.unique(T.has_wise_phot)
        tempfn = create_temp()
        ### HACK!!
        T.has_wise_phot = np.ones(len(T), bool)
        T.writeto(tempfn)
        del T
        res = StreamingHttpResponse(open(tempfn))
        os.unlink(tempfn)
        res['Content-type'] = 'application/fits'
        res['Content-Disposition'] = 'attachment; filename="sdsswise.fits"'
        return res

    if dtype == 'sdss':
        args = req.GET.copy()
        args.pop('page', None)
        T.path = np.array(['%s/%s/photoWiseForced-%06i-%i-%04i.fits' %
                           (t.run, t.camcol, t.run, t.camcol, t.field)
                           for t in T])
        keep = []
        base = get_phot_data_path(version, 'pobj')
        for i,p in enumerate(T.path):
            if os.path.exists(os.path.join(base, p)):
                keep.append(i)
        if len(keep) == 0:
            return HttpResponseBadRequest('No objects match your query. (%i listed)' % len(T))
        T.cut(np.array(keep))

        T.filename = np.array(['photoWiseForced-%06i-%i-%04i.fits' %
                           (t.run, t.camcol, t.field) for t in T])
        T.sdssurl = np.array([sdssurls[version] +
                              '%s/%s/photoObj-%06i-%i-%04i.fits' %
                              (t.run, t.camcol, t.run, t.camcol, t.field)
                              for t in T])
        T.sdssfile = np.array(['photoObj-%06i-%i-%04i.fits' %
                              (t.run, t.camcol, t.field) for t in T])

        ctxt = {
            'total_items': len(T),
            'object_list': T,
            'version': version,
            'dtype': dtype,
            'dataurl': get_phot_data_url(version, 'pobj'),
            'myurl': req.path + '?' + args.urlencode()
            }
        if cone is not None:
            ctxt.update(ra=ra, dec=dec, radius=rad, cone=True)
        else:
            ctxt.update(ralo=ralo, rahi=rahi, declo=declo, dechi=dechi,
                        cone=False)

        pagination = 20
        if len(T) > pagination*1.5:
            paginator = Paginator(T, pagination)
            page = req.GET.get('page')
            try:
                page = paginator.page(page)
            except PageNotAnInteger:
                page = paginator.page(1)
            except EmptyPage:
                # 9999 -> last page
                page = paginator.page(paginator.num_pages)
            # print 'Page:', page
            # print 'has_next', page.has_next()
            ctxt.update(
                paginator = paginator,
                is_paginated = True,
                page_obj = page,
                object_list = page,
                )
        
        return render(req, 'sdssphot/field_list.html', ctxt)

    if dtype == 'wise':
        tiles = unwise_tiles_near_radec(
            ra, dec, rad,
            tablename='sdssphot_phottile',
            extra_where="and version='%s'" % version,
            tileclass=PhotTile)
        tiles = list(tiles)
        print 'N tiles:', len(tiles)

        if box is not None:
            # Cut cone to box...
            ddec = 2048 * 2.75 / 3600. * 1.01 / 2.
            tiles = [t for t in tiles if (t.dec - ddec <= dechi) and (t.dec + ddec >= declo)]
            dra = ddec / np.cos(np.deg2rad(dec))
            if ralo - dra < 0 or rahi + dra > 360:
                # wrap-around...
                if ralo < dra:
                    # close to 0
                    tiles = [t for t in tiles if
                             (t.ra < rahi + dra) or (t.ra > ralo + 360. - dra)]
                else:
                    # close to 360
                    tiles = [t for t in tiles if
                             (t.ra > ralo - dra) or (t.ra < rahi + dra - 360.)]
            else:
                # plain old
                tiles = [t for t in tiles if
                         (t.ra > ralo - dra) and (t.ra < rahi + dra)]

        args = req.GET.copy()
        args.pop('page', None)

        ctxt = {
            'total_items': len(tiles),
            'object_list': tiles,
            'version': version,
            'dataurl': get_phot_data_url(version, 'phot'),
            'myurl': req.path + '?' + args.urlencode()
            }

        if cone is not None:
            ctxt.update(ra=ra, dec=dec, radius=rad, cone=True)
        else:
            ctxt.update(ralo=ralo, rahi=rahi, declo=declo, dechi=dechi,
                        cone=False)

        pagination = 20
        if len(tiles) > pagination*1.5:
            paginator = Paginator(tiles, pagination)
            pagenum = req.GET.get('page')
            try:
                page = paginator.page(pagenum)
            except PageNotAnInteger:
                page = paginator.page(1)
            except EmptyPage:
                # 9999 -> last page
                page = paginator.page(paginator.num_pages)
            ctxt.update(
                paginator = paginator,
                is_paginated = True,
                page_obj = page,
                object_list = page,
                )
        return render(req, 'sdssphot/tile_list.html', ctxt)
    
def coord_search(req):
    form = None
    boxform = None

    if 'coord' in req.GET:
        form = SdssPhotCoordSearchForm(req.GET)

        tracking = UserCoordSearch(product=PRODUCT_SDSSPHOT,
                                   ip=req.META['REMOTE_ADDR'],
                                   coord_str=form.data.get('coord', None),
                                   radius_str=form.data.get('radius', None))

        if form.is_valid():
            print 'Form is valid: data', form.cleaned_data

            # Process the data in form.cleaned_data
            ra,dec = parse_coord(form.cleaned_data['coord'])
            try:
                radius = float(form.cleaned_data['radius'])
            except:
                radius = 0.

            tracking.ra = ra
            tracking.dec = dec
            tracking.radius = radius
            if dotrack:
                tracking.save()

            datatype = form.cleaned_data['datatype']
            version = form.cleaned_data['version']
            password = form.cleaned_data['password']

            url = 'phot_near/?ra=%g&dec=%g&radius=%g&datatype=%s' % (ra, dec, radius, datatype)
            if len(version):
                url += '&version=%s' % version
            if len(password):
                url += '&password=%s' % password
            if form.cleaned_data['sdss']:
                url += '&sdss'
            return HttpResponseRedirect(url)

        # form not valid
        #print form
        
        if dotrack:
            tracking.save()

    elif 'ralo' in req.GET:
        boxform = CentralsRaDecBoxSearchForm(req.GET)
        if boxform.is_valid():
            print 'Form is valid: data', boxform.cleaned_data
            # Process the data in boxform.cleaned_data
            ralo = parse_ra(boxform.cleaned_data['ralo'])
            rahi = parse_ra(boxform.cleaned_data['rahi'])
            declo = parse_dec(boxform.cleaned_data['declo'])
            dechi = parse_dec(boxform.cleaned_data['dechi'])
    
            datatype = boxform.cleaned_data['datatype']
            version = boxform.cleaned_data['version']
            password = boxform.cleaned_data['password']
    
            url = 'phot_box/?ralo=%g&rahi=%g&declo=%g&dechi=%g&datatype=%s' % (ralo, rahi, declo, dechi, datatype)
            if len(version):
                url += '&version=%s' % version
            if len(password):
                url += '&password=%s' % password
            if boxform.cleaned_data['sdss']:
                url += '&sdss'
            return HttpResponseRedirect(url)

    if form is None:
        form = SdssPhotCoordSearchForm()
        form.initial = dict(coord='200 10', radius=0.1)
    if boxform is None:
        boxform = CentralsRaDecBoxSearchForm()
        boxform.initial = dict(ralo=200, rahi=201, declo=10, dechi=11)

    return render(req, 'sdssphot/coordsearch.html', {
        #'sdsscollab': 'sdss' in req.GET,
        'sdsscollab': True,
        'form': form,
        'boxform': boxform,
        'version_choices': version_choices,
        'datatype_choices': datatype_choices,
        'url': reverse('phot-search'),
        'dataurl': settings.SDSSPHOT_DATA_URL,
    })    

