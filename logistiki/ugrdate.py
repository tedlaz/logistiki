

def date2gr(adate):
    return f'{adate.day}/{adate.month}/{adate.year}'


def date_gr2iso(greek_date):
    """Μετατρέπει μια iso Ημερομηνία σε Ελληνική"""
    dd, mm, yyyy = greek_date.split('/')
    return '%s-%s-%s' % (yyyy, mm, dd)
