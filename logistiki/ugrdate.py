

def date2gr(adate):
    return f'{adate.day}/{adate.month}/{adate.year}'


def date_gr2iso(greek_date):
    """Μετατρέπει μια Ελληνική ημερομηνία σε iso"""
    dd, mm, yyyy = greek_date.split('/')
    return '%s-%s-%s' % (yyyy, mm, dd)


def date_iso2gr(isodate):
    """Μετατρέπει μια iso ημερομηνία σε Ελληνική"""
    try:
        yyyy, mm, dd = isodate.split('-')
        return f'{dd}/{mm}/{yyyy}'
    except AttributeError:
        return ''
