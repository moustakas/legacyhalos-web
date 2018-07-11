import os,sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "readinweb.settings")
import django
django.setup()

from readinweb.models import *
import csv


#T = fits_table('central.csv')
#T.delete_column('row')
#print (len(T), 'rows')
#T.cut(np.argsort(T.coadd_id))

csv_filepathname="centrals-sample.csv"
dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')

for row in dataReader:
    print('Row:', row)
    centrals=Centrals()
    centrals.objid=row[0]
    centrals.ctype=row[1]
    centrals.ra = row[2]
    centrals.dec = row[3]
    centrals.mem_match_id = row[4]
    centrals.z = row[5]
    centrals.lambda_chisq = row[6]
    centrals.sdss_objid = row[7]
    centrals.save()
