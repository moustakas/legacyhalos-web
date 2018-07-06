# Miscellaneous tools

from astrometry.util.starutil_numpy import hmsstring2ra, dmsstring2dec

def parse_ra(rastr):
    try:
        ra = float(rastr)
    except:
        try:
            ra = hmsstring2ra(rastr)
        except:
            raise ValidationError('Failed to parse RA string: "%s" -- allowed formats are decimal degrees or HH:MM:SS' % rastr)
    return ra
        
def parse_dec(decstr):
    try:
        dec = float(decstr)
    except:
        try:
            dec = dmsstring2dec(decstr)
        except:
            raise ValidationError('Failed to parse Dec string: "%s" -- allowed formats are decimal degrees or +-DD:MM:SS' % decstr)
    return dec
