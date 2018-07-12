import django_filters
from readinweb.models import Centrals
#from readinweb.models import FilterFields


class CentralsFilter(django_filters.FilterSet):
    ra = django_filters.NumberFilter()
    ra__gt = django_filters.NumberFilter(name='ra', lookup_expr='gt')
    ra__lt = django_filters.NumberFilter(name='ra', lookup_expr='lt')

    dec = django_filters.NumberFilter()
    dec__gt = django_filters.NumberFilter(name='dec', lookup_expr='gt')
    dec__lt = django_filters.NumberFilter(name='dec', lookup_expr='lt')

    class Meta:
        model = Centrals
        fields = ['objid', 'morphtype', 'ra', 'dec', 'mem_match_id']

## class CentralsFilter(django_filters.FilterSet):
    

##     class Meta:
##         model = FilterFields
##         fields = ['objid', 'ralo', 'rahi', 'declo', 'dechi']
