import os,sys
os.environ.setdefault("DJANGO_SETTINGS_MODULS", "unwise.settings")

from readinweb.models import *
import csv
import fitsio

#T = fits_table('central.csv')
#T.delete_column('row')
#print (len(T), 'rows')
#T.cut(np.argsort(T.coadd_id))

csv_filepathname="centrals.csv"
dataReader = csv.reader(open(csv_filepathname), delimeter=',', quotechar='"')

for row in dataReader:
    halos=Halos()
    halos.name=row[0]
    halos.ra = row[1]
    halos.dec = row[2]
    halos.save()
