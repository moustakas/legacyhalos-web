from django.conf.urls import include, url

import data.views as co

tilepattern = r'[0-9]{4}[pm][0-9]{3}'

urlpatterns = [
    url(r'^fulldepth_neo3/?$', co.fulldepth_neo3),
    url(r'^tr_neo2/?$', co.tr_neo2),
    url(r'^tiles/$', co.TileList.as_view()),
    url(r'^tiles_near/$', co.CoordSearchTileList.as_view()),
    url(r'^tiledata/(?P<version>(neo3|neo2|neo1|allwise))/(?P<coadd>' + tilepattern +
        ')-w(?P<bands>1?2?3?4?).tgz/?$',
        co.tile_tgz, name='tile-tgz'),
    url(r'^tiledata/(?P<version>(neo3|neo2|neo1|allwise))/(?P<coadd>' + tilepattern + ').tgz/?$',
        co.tile_tgz, name='tile-tgz'),
    url(r'^tilesetdata/?$', co.tileset_tgz, name='tileset-tgz'),
    url(r'^imgsearch/?$', co.coord_search, name='search'),
    url(r'^search/?$', co.coord_search, name='search'),
    url(r'^cutout_fits/?$', co.cutout_fits, name='cutout_fits'),
    url(r'^cutout_jpg/?$', co.cutout_jpg, name='cutout_jpg'),
    # url(r'^usage/?$', usage),
    url(r'^$', co.index, name='index'),
]

#urlpatterns += patterns('animate',
#  url(r'^gif/?$', 'animate'))

### DEBUG
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# urlpatterns += staticfiles_urlpatterns()
# 
# from django.conf import settings
# urlpatterns += [
#     '',
#     #url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
#     #    {'document_root': settings.MEDIA_ROOT}),
#     url(r'^data/(?P<path>.*)$', django.views.static.serve,
#         {'document_root': settings.DATA_DIR, 'show_indexes': True}),
#     url(r'^data-sdssphot/(?P<path>.*)$', django.views.static.serve,
#         {'document_root': settings.SDSSPHOT_DATA_DIR, 'show_indexes': True}),
# ]
