from django.db.models import Model, IntegerField, CharField, FloatField, IPAddressField, DateTimeField, ManyToManyField, TextField, BooleanField

class Centrals(Model):
    objid = IntegerField(null=True)
    morphtype = CharField(max_length=64, null=True)
    ra = FloatField(null=True)
    dec = FloatField(null=True)
    mem_match_id = IntegerField(null=True)
    z = FloatField(null=True)
    la = FloatField(null=True)
    sdss_objid = FloatField(null=True)

    def __str__(self):
        return ('user Central Search(%s,%s,%s,%s,%s,%s,%s,%s)' % (self.objid, self.morphtype, self.ra, self.dec, self.mem_match_id, self.z, self.la, self.sdss_objid))

## class FilterFields(Model):
##     objid = IntegerField(null=True)
##     ralo = FloatField(null=True)
##     rahi = FloatField(null=True)
##     declo = FloatField(null=True)
##     dechi = FloatField(null=True)

##     def __str__(self):
##         return('Filter entry(%s,%s,%s,%s,%s)' % (self.objid, self.ralo, self.rahi, self.declo, self.dechi))
