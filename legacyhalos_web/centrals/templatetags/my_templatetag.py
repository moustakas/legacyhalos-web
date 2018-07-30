from django import template

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
