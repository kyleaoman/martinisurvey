import astropy.units as U


def target_str(s, o):
    return '-'.join((
        'AP',
        'L'+str(s.res),
        'V'+str(s.vol),
        str(o.fof),
        str(o.sub)
    ))


def targetview_str(s, o, i, az):
    return '_'.join((
        str(s.res),
        '{:02d}'.format(s.vol),
        '{:02d}'.format(o.fof),
        str(o.sub),
        '{:02.0f}'.format(i.to(U.degree).value),
        '{:03.0f}'.format(az.to(U.degree).value)
    ))
