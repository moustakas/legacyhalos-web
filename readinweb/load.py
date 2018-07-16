import os,sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "readinweb.settings")
import django
django.setup()

from readinweb.models import Centrals
import csv
from astropy.table import Table

#if True:
## csv_filepathname="centrals-sample.csv"
## dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
## for row in dataReader:
##     print('Row:', row)
##     centrals=Centrals()
##     centrals.objid=row[0]
##     centrals.morphtype=row[1]
##     centrals.ra = row[2]
##     centrals.dec = row[3]
##     centrals.mem_match_id = row[4]
##     centrals.z = row[5]
##     centrals.la = row[6]
##     centrals.sdss_objid = row[7]
##     centrals.save()

data = Table.read('centrals-sample.fits')
data.rename_column('type', 'morphtype')

for row in data:
    #print('Row:', row)
    centrals=Centrals()
    centrals.objid=row[0]
    centrals.morphtype=row[1]
    centrals.ra = row[2]
    centrals.dec = row[3]
    centrals.mem_match_id_string = '%0*d' % (7, row[4])
    centrals.mem_match_id = row[4]
    centrals.z = "%.3f" % row[5]
    centrals.la = "%.3f" % row[6]
    centrals.sdss_objid = row[7]
    centrals.viewer_link = centrals.viewer_link()
    centrals.skyserver_link = centrals.skyserver_link()
    centrals.save()

## for row in data:
##     centrals = Centrals()
##     for col in data.colnames:
##         col.getattr(centrals, col) = data[row][col]
##     centrals.save()
