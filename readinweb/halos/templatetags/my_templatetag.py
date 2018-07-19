from django import template

register = template.Library()

@register.simple_tag
def url_replace(req, field, value):
    dict_ = req.GET.copy()
    dict_[field] = value
    return dict_.urlencode()
