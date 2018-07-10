from django.db.models import Model, IntegerField, CharField, FloatField, IPAddressField, DateTimeField, ManyToManyField, TextField, BooleanField

class Halos(Model):
    name = FloatField(null=True)
    ra = FloatField(null=True)
    dec = FloatField(null=True)

    def __str__(self):
        return ('user Halo Search(%s, %s,%s)' % (self.name, self.ra, self.dec))
