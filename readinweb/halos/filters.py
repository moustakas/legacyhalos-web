import django_filters
from readinweb.models import Centrals


class CentralsFilter(django_filters.FilterSet):
    class Meta:
        model = Centrals
        fields = ['objid', 'ctype', 'ra', 'dec', 'mem_match_id', 'z', 'la', 'sdss_objid']
