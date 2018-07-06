from django.db.models import Model, IntegerField, CharField, FloatField, IPAddressField, DateTimeField, ManyToManyField, TextField, BooleanField

class UserDownload(Model):
    ip = IPAddressField()
    time = DateTimeField(auto_now=True)
    tiles = TextField(blank=True)
    products = TextField(blank=True)
    w1 = BooleanField(default=False)
    w2 = BooleanField(default=False)
    w3 = BooleanField(default=False)
    w4 = BooleanField(default=False)

