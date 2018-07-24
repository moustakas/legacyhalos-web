import django_filters
from legacyhalos_web.models import Centrals

class CentralsFilter(django_filters.FilterSet):
    #ra = django_filters.NumberFilter()
    ra__gt = django_filters.NumberFilter(name='ra', lookup_expr='gt', label='RA low')
    ra__lt = django_filters.NumberFilter(name='ra', lookup_expr='lt', label = 'RA high')

    #dec = django_filters.NumberFilter()
    dec__gt = django_filters.NumberFilter(name='dec', lookup_expr='gt', label='Dec low')
    dec__lt = django_filters.NumberFilter(name='dec', lookup_expr='lt', label='Dec high')



    class Meta:
        model = Centrals
        fields = ['mem_match_id']

        def id(self):
            return self.mem_match_id
