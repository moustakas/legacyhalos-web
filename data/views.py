from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, QueryDict, StreamingHttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django import forms
from django.views.generic import ListView, DetailView

from unwise import settings
from unwise.common import *
from unwise.models import *
from coadd.models import *

from astrometry.util.fits import *
from astrometry.util.starutil_numpy import *

def fulldepth_neo3(req):
    return HttpResponseRedirect('https://faun.rc.fas.harvard.edu/ameisner/unwise/fulldepth_neo3')

def tr_neo2(req):
    return HttpResponseRedirect('https://faun.rc.fas.harvard.edu/ameisner/unwise/tr_neo2')

# When adding a new dataset:
# - add to the list below
# - see unwise/urls.py and add to the URL patterns.
# - weirdly, create a symlink in data/allwise/ pointing to the new directory

coadd_version_choices = [
    ('allwise', 'AllWISE'),
    ('neo1', 'NeoWISE-R 1'),
    ('neo2', 'NeoWISE-R 2'),
    ('neo3', 'NeoWISE-R 3'),
    ]
coadd_version_default = 'neo3'

class CoaddForm(forms.Form):
    version = forms.ChoiceField(required=False, initial=coadd_version_default,
                                choices=coadd_version_choices)

class CoaddCoordSearchForm(CoordSearchForm, CoaddForm):
    pass

class CutoutSearchForm(CoaddForm):
    ra  = forms.FloatField(required=False, validators=[parse_ra])
    dec = forms.FloatField(required=False, validators=[parse_dec])
    size = forms.IntegerField(required=False, initial=100,
                              widget=forms.TextInput(attrs={'size': 6}))
    bands = forms.CharField(required=False, initial='1234',
                            widget=forms.TextInput(attrs={'size': 6}))

    file_img_m    = forms.BooleanField(required=False, initial=True)
    file_invvar_m = forms.BooleanField(required=False, initial=True)
    file_n_m      = forms.BooleanField(required=False, initial=True)
    file_std_m    = forms.BooleanField(required=False, initial=True)

    
class TileList(ListView):
    template_name = 'coadd/tile_list.html'
    paginate_by = 20
    model = Tile

#dotrack = True
dotrack = False

class CoordSearchTileList(TileList):
    def get_queryset(self):
        req = self.request
        form = RaDecSearchForm(req.GET)

        tracking = UserRaDecSearch(product=PRODUCT_COADD,
                                   ip=req.META['REMOTE_ADDR'],
                                   ra_str=form.data.get('ra',''),
                                   dec_str=form.data.get('dec',''),
                                   radius_str=form.data.get('radius',''))

        if not form.is_valid():
            if dotrack:
                tracking.save()
            return []
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

        tracking.ra = ra
        tracking.dec = dec
        tracking.radius = rad
        if dotrack:
            tracking.save()

        tiles = unwise_tiles_near_radec(ra, dec, rad)
        tiles = list(tiles)
        #print 'N tiles:', len(tiles)
        return tiles

    def get_context_data(self, **kwargs):
        context = super(CoordSearchTileList, self).get_context_data(**kwargs)
        req = self.request
        args = req.GET.copy()
        args.pop('page', None)
        pager = context.get('paginator')
        context['total_items'] = pager.count
        context['myurl'] = req.path + '?' + args.urlencode()
        context['ra'] = args.pop('ra', [0])[0]
        context['dec'] = args.pop('dec', [0])[0]
        context['radius'] = args.pop('radius', [0])[0]
        # ??
        context['version'] = args.pop('version', ['1'])[0]
        return context

def tileset_tgz(req):
    tilenames = []
    for key,val in req.POST.items():
        if not key.startswith('tile'):
            continue
        tilenames.append(val)
    tiles = Tile.objects.filter(coadd__in=tilenames)
    maxtiles = 50
    if tiles.count() > maxtiles:
        return HttpResponse('Too many tiles requested; max %i' % maxtiles,
                            status=413)
    
    pats = []
    prods = []
    for key,pat in [('frames',  'frames.fits'),
                    ('masks',   'mask.tgz'),
                    ('imgu',    'img-u.fits'),
                    ('stdu',    'std-u.fits.gz'),
                    ('invvaru', 'invvar-u.fits.gz'),
                    ('nu',      'n-u.fits.gz'),
                    ('imgm',    'img-m.fits'),
                    ('stdm',    'std-m.fits.gz'),
                    ('invvarm', 'invvar-m.fits.gz'),
                    ('nm',      'n-m.fits.gz'),]:
        if key in req.POST:
           pats.append(pat)
           prods.append(key)

    bands = []
    for band in [1,2,3,4]:
        if 'w%i' % band in req.POST:
            bands.append(band)

    version = req.POST['version']
            
    tracking = UserDownload(ip=req.META['REMOTE_ADDR'],
                            products=' '.join(prods),
                            tiles=' '.join([t.coadd for t in tiles]),
                            w1=(1 in bands),
                            w2=(2 in bands),
                            w3=(3 in bands),
                            w4=(4 in bands))
    if dotrack:
        tracking.save()
    
    # print 'Tiles:', tiles
    # print 'Bands:', bands
    # print 'Pats:', pats
    # print 'Prods:', prods
    files = []
    for tile in tiles:
        coadd = tile.coadd
        dirnm = str(os.path.join(version, 'unwise-coadds', 'fulldepth', coadd[:3], coadd))
        for band in bands:
            for pat in pats:
                files.append(str(os.path.join(dirnm, 'unwise-%s-w%i-%s' % (coadd, band, pat))))
    # print 'Files:', files
    return tar_files(req, files, 'unwise.tgz')

def tile_tgz(req, coadd=None, bands=None, version=None):
    tile = get_object_or_404(Tile, coadd=coadd)
    if bands is None:
        bands = [1,2,3,4]
        fn = '%s.tgz' % tile.coadd
    else:
        bands = [int(c,10) for c in bands]
        fn = '%s-w%s.tgz' % (tile.coadd, ''.join(['%i'%b for b in bands]))

    if version is None:
        version = coadd_version_default
        
    tracking = UserDownload(ip=req.META['REMOTE_ADDR'],
                            products='all',
                            tiles=tile.coadd,
                            w1=(1 in bands),
                            w2=(2 in bands),
                            w3=(3 in bands),
                            w4=(4 in bands))
    if dotrack:
        tracking.save()

    files = []
    coadd = tile.coadd
    dirnm = os.path.join(version, 'unwise-coadds', 'fulldepth',
                         coadd[:3], coadd)
    base = os.path.join(dirnm, 'unwise-%s' % coadd)
    for band in bands:
        files.append(str(base + '-w%i-*' % (band)))
    return tar_files(req, files, fn)

def coord_search(req):
    if 'coord' in req.GET:
        form = CoaddCoordSearchForm(req.GET)

        tracking = UserCoordSearch(product=PRODUCT_COADD,
                                   ip=req.META['REMOTE_ADDR'],
                                   coord_str=form.data.get('coord', ''),
                                   radius_str=form.data.get('radius', ''))

        if form.is_valid():
            # Process the data in form.cleaned_data
            ra,dec = parse_coord(form.cleaned_data['coord'])
            try:
                radius = float(form.cleaned_data['radius'])
            except:
                radius = 0.
            version = form.cleaned_data['version']
                
            tracking.ra = ra
            tracking.dec = dec
            tracking.radius = radius
            print 'ra,dec,radius', ra,dec,radius
            
            if dotrack:
                tracking.save()

            return HttpResponseRedirect('tiles_near/?version=%s&ra=%g&dec=%g&radius=%g' % (version, ra, dec, radius))

        if dotrack:
            tracking.save()

    else:
        form = CoaddCoordSearchForm()

    cutoutform = CutoutSearchForm()

    return render(req, 'coordsearch.html', {
        'form': form,
        'cutoutform': cutoutform,
        'url': reverse('search'),
    })    

def index(req):
    return render(req, 'index.html')
   
def cutout_fits(req):
    import tempfile
    import fitsio
    from astrometry.util.util import Tan

    form = CutoutSearchForm(req.GET)
    if not form.is_valid():
        return HttpResponse('failed to parse request')
    ra = form.cleaned_data['ra']
    dec = form.cleaned_data['dec']
    if ra is None or dec is None:
        return HttpResponse('RA and Dec arguments are required')
    size = form.cleaned_data['size']
    if size is None:
        size = 100
    else:
        size = min(256, size)
    bandstr = form.cleaned_data['bands']
    bands = [int(c) for c in bandstr]
    bands = [b for b in bands if b in [1,2,3,4]]

    version = form.cleaned_data['version']

    if version in ['neo1', 'neo2', 'neo3']:
        bands = [b for b in bands if b in [1,2]]

    radius = size/2. * 2.75/3600.
    tiles = unwise_tiles_near_radec(ra, dec, radius)
    tiles = list(tiles)

    # Create a temp dir in which to place cutouts
    tempdir = tempfile.mkdtemp()
    fns = []

    filetypes = []
    types = ['img_m', 'invvar_m', 'n_m', 'std_m']
    for t in types:
        if form.cleaned_data['file_' + t]:
            filetypes.append(t)
    # If none specified, include all filetypes.
    if len(filetypes) == 0:
        filetypes = types
    
    for tile in tiles:
        coadd = tile.coadd
        dirnm = os.path.join(settings.DATA_DIR, version, 'unwise-coadds', 'fulldepth', coadd[:3], coadd)
        base = os.path.join(dirnm, 'unwise-%s' % coadd)
        w1fn = str(base + '-w1-img-m.fits')
        wcs = Tan(w1fn, 0)
        ok,x,y = wcs.radec2pixelxy(ra, dec)
        x = int(round(x-1.))
        y = int(round(y-1.))
        x0 = x - size/2
        x1 = x0 + size
        y0 = y - size/2
        y1 = y0 + size
        if x1 <= 0 or y1 <= 0:
            continue
        if x0 >= wcs.get_width() or y0 >= wcs.get_height():
            continue
        x0 = max(x0, 0)
        y0 = max(y0, 0)
        x1 = min(x1, wcs.get_width())
        y1 = min(y1, wcs.get_height())

        hdr = fitsio.FITSHDR()
        subwcs = wcs.get_subimage(x0, y0, x1-x0, y1-y0)
        subwcs.add_to_header(hdr)

        for band in bands:
            for ft in filetypes:
                pat = { 'img_m':    '-w%i-img-m.fits',
                        'invvar_m': '-w%i-invvar-m.fits.gz',
                        'n_m':      '-w%i-n-m.fits.gz',
                        'std_m':    '-w%i-std-m.fits.gz' }[ft]
                fn = str(base + pat % band)
                img = fitsio.FITS(fn)[0][y0:y1, x0:x1]
                basefn = os.path.basename(fn)
                outfn = os.path.join(tempdir, basefn)
                fitsio.write(outfn, img, header=hdr)
                fns.append(basefn)

    fns.extend([';', 'rm', '-R', tempdir])

    return tar_files(req, fns, 'cutouts-fits_%.4f_%.4f.tar.gz' % (ra, dec),
                     basedir=tempdir)


def cutout_jpg(req):
    import tempfile
    import fitsio
    from astrometry.util.util import Tan
    from astrometry.util.resample import resample_with_wcs

    form = CutoutSearchForm(req.GET)
    if not form.is_valid():
        return HttpResponse('failed to parse request')
    ra = form.cleaned_data['ra']
    dec = form.cleaned_data['dec']
    if ra is None or dec is None:
        return HttpResponse('RA and Dec arguments are required')
    size = form.cleaned_data['size']
    if size is None:
        size = 100
    else:
        size = min(256, size)
    # Ignoring this for now...
    # bandstr = form.cleaned_data['bands']
    # bands = [int(c) for c in bandstr]
    # bands = [b for b in bands if b in [1,2,3,4]]
    version = form.cleaned_data['version']
    
    radius = size/2. * 2.75/3600.
    tiles = unwise_tiles_near_radec(ra, dec, radius)
    tiles = list(tiles)

    pixscale = 2.75 / 3600.
    cowcs = Tan(*[float(x) for x in
                  [ra, dec, 0.5 + size/2., 0.5 + size/2.,
                   -pixscale, 0., 0., pixscale,
                   size, size]])
    bands = [1,2]
    coims = [np.zeros((size,size), np.float32) for b in bands]
    con = np.zeros((size,size), int)
    
    for tile in tiles:
        coadd = tile.coadd
        dirnm = os.path.join(settings.DATA_DIR, version, 'unwise-coadds', 'fulldepth', coadd[:3], coadd)
        base = os.path.join(dirnm, 'unwise-%s' % coadd)

        subwcs = None
        ims = []
        for band in bands:
            fn = str(base + '-w%i-img-m.fits' % band)
            if subwcs is None:
                wcs = Tan(fn)
                ok,x,y = wcs.radec2pixelxy(ra, dec)
                x = int(round(x-1.))
                y = int(round(y-1.))
                x0 = x - size/2
                x1 = x0 + size
                y0 = y - size/2
                y1 = y0 + size
                if x1 <= 0 or y1 <= 0:
                    break
                if x0 >= wcs.get_width() or y0 >= wcs.get_height():
                    break
                x0 = max(x0, 0)
                y0 = max(y0, 0)
                x1 = min(x1, wcs.get_width())
                y1 = min(y1, wcs.get_height())
                subwcs = wcs.get_subimage(x0, y0, x1-x0, y1-y0)

            if subwcs is None:
                break
            img = fitsio.FITS(fn)[0][y0:y1, x0:x1]
            ims.append(img)

        if subwcs is None:
            continue

        try:
            Yo,Xo,Yi,Xi,rims = resample_with_wcs(cowcs, subwcs, ims, 3)
        except:
            continue
        for rim,co in zip(rims, coims):
            co[Yo,Xo] += rim
        con[Yo,Xo] += 1

    for co in coims:
        co /= np.maximum(con, 1)

    rgb = np.zeros((size,size,3), np.uint8)
    lo,hi = -3,10
    scale = 10.
    rgb[:,:,2] = np.clip(255. * ((coims[1] / scale) - lo) / (hi-lo), 0, 255)
    rgb[:,:,1] = np.clip(255. * (((coims[0]+coims[1])/2. / scale) - lo) / (hi-lo), 0, 255)
    rgb[:,:,0] = np.clip(255. * ((coims[0] / scale) - lo) / (hi-lo), 0, 255)

    f,tempfn = tempfile.mkstemp(suffix='.jpg')
    os.close(f)

    # import matplotlib
    # matplotlib.use('Agg')
    # import pylab as plt
    # plt.imsave(tempfn, rgb, interpolation='nearest', origin='lower')

    from PIL import Image
    pic = Image.fromarray(rgb)
    pic.save(tempfn)
    
    return send_file(tempfn, 'image/jpeg', unlink=True)


def usage(req):
    import traceback
    fn = settings.DATABASES['usage']['NAME']
    ss = []
    ss.append('DB: %s, exists? %s' % (fn, os.path.exists(fn)))
    try:
        uu = UserCoordSearch.objects.all()
        uu = uu.filter(product=PRODUCT_COADD)
        ss.append('%i UserCoordSearch objects' % uu.count())
        ss.extend([str(u) for u in uu])
    except:
        ss.append('Failed to get UserCoordSearch objects')
        ss.append(traceback.format_exc())

    for cmd in [['file', fn],
                ['file', '-L', fn],
                ['sqlite3', fn, '.tables'],
                ]:
        try:
            import subprocess
            #rtn = subprocess.check_output(cmd)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            rtn = p.communicate()[0]

            ss.extend([' '.join(cmd), rtn])
        except:
            ss.append('failed to run %s' % cmd)
            ss.append(traceback.format_exc())

    try:
        uu = UserRaDecSearch.objects.all()
        uu = uu.filter(product=PRODUCT_COADD)
        ss.append('%i UserRaDecSearch objects' % uu.count())
        ss.extend([str(u) for u in uu])
    except:
        ss.append('Failed to get UserRaDecSearch objects')
        ss.append(traceback.format_exc())

    # try:
    #     uu = UserRaDecSearch(ip=req.META['REMOTE_ADDR'],
    #                          ra_str="42", dec_str="27", radius_str="1.2")
    #     uu.ra = 42.
    #     uu.dec = 27.
    #     uu.radius = 1.2
    # 
    #     ss.append('Saving: %s' % str(uu))
    #     uu.save()
    # 
    # except:
    #     ss.append('Failed to save UserRaDecSearch object')
    #     ss.append('<pre>' + traceback.format_exc() + '</pre>')


    return HttpResponse('<br/>'.join(ss))
