from django.db.models import Model, IntegerField, CharField, FloatField, IPAddressField, DateTimeField, ManyToManyField, TextField, BooleanField

class Centrals(Model):
    objid = IntegerField(null=True)
    morphtype = CharField(max_length=6, null=True)
    ra = FloatField(null=True)
    dec = FloatField(null=True)
    mem_match_id = FloatField(null=True)
    mem_match_id_string = CharField(max_length=7, null=False, primary_key = True)
    z = FloatField(null=True)
    la = FloatField(null=True)
    sdss_objid = FloatField(null=True)
    viewer_link = CharField(null=True)
    skyserver_link = CharField(null = True)

    def __str__(self):
        return ('user Central Search(%s,%s,%s,%s,%s,%s,%s,%s)' % (self.objid, self.morphtype, self.ra, self.dec, self.mem_match_id, self.z, self.la, self.sdss_objid))

    def viewer_link(self):
        baseurl = 'http://legacysurvey.org/viewer/'
        viewer = '{}?ra={:.6f}&dec={:.6f}&zoom=15&layer=decals-dr5'.format(
            baseurl, self.ra, self.dec)
        return viewer

    def skyserver_link(self):
        return 'http://skyserver.sdss.org/dr14/en/tools/explore/summary.aspx?id=%d' % self.sdss_objid
