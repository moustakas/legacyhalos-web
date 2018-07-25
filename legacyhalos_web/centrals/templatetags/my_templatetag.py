from django import template

register = template.Library()

#try another decorator?
@register.simple_tag
def url_replace(req, field, value):
    dict_ = req.GET.copy()
    dict_[field] = value
    return dict_.urlencode()

#@register.simple_tag
#def get_central(req, index, cen_list):
    

@register.simple_tag
def url_pull(req):
    dict_ = req.GET.copy()
    search = "Search Criteria:"
    entry = False
    if "mem_match_id" in dict_ and dict_["mem_match_id"] is not "":
        search += " redMaPPer ID: " + dict_["mem_match_id"] + " |"
        entry = True
    if "ra__gt" in dict_:
        if dict_["ra__gt"] ==  "":
            search += " RA low: 0 |"
        else:
            search += " RA low: " + dict_["ra__gt"] + " |"
            entry = True
    if "ra__lt" in dict_:
        if dict_["ra__lt"] == "":
            search += " RA high: 360 |"
        else:
            search += " RA high: " + dict_["ra__lt"] + " |"            
            entry = True
    #if "ra__lt" in dict_ and dict_["ra__lt"] is not "":
    #    search += " RA high: " + dict_["ra__lt"] + " |"
    #    entry = True
    if "dec__gt" in dict_:
        if dict_["dec__gt"] ==  "":
            search += " Dec low: -11 |"
        else:
            search += " Dec low: " + dict_["dec__gt"] + " |"
            entry = True
    if "dec__lt" in dict_:
        if dict_["dec__lt"] == "":
            search += " Dec high: 32 |"
        else:
            search += " Dec high: " + dict_["dec__lt"] + " |"
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
