from django.conf.urls import include, url
from django.urls import path, include
import centrals.views as cen

urlpatterns = [
    url(r'^$', cen.index, name='index'),
]

urlpatterns += [
  #url(r'^photsearch/?$', data.coord_search, name='phot-search'),
  #url(r'^phot_near/?$', data.conesearch_results),
  url(r'^phot_box/?$', cen.boxsearch_results),
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
