import django_filters
from legacyhalos_web.models import Centrals

class CentralsFilter(django_filters.FilterSet):
    #name is the Centrals object variable
    #lookup_expr is used to get ranges (currently using greater/less than or equal to  
    ra__gte = django_filters.NumberFilter(field_name='ra', lookup_expr='gte')
    ra__lte = django_filters.NumberFilter(field_name='ra', lookup_expr='lte')

    dec__gte = django_filters.NumberFilter(field_name='dec', lookup_expr='gte')
    dec__lte = django_filters.NumberFilter(field_name='dec', lookup_expr='lte')

    z__gte = django_filters.NumberFilter(field_name='z', lookup_expr='gte')
    z__lte = django_filters.NumberFilter(field_name='z', lookup_expr='lte')

    la__gte = django_filters.NumberFilter(field_name='la', lookup_expr='gte')
    la__lte = django_filters.NumberFilter(field_name='la', lookup_expr='lte')

    mem_match_id__gte = django_filters.NumberFilter(field_name='mem_match_id', lookup_expr='gte')
    mem_match_id__lte = django_filters.NumberFilter(field_name='mem_match_id', lookup_expr='lte')

    class Meta:
        model = Centrals
        #add variable to the field if looking for exact match
        fields = []

        def id(self):
            return self.mem_match_id
