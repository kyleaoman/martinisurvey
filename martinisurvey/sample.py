import astropy.units as U
from target import Target
from _id_defs import snap_id, obj_id

incls = (60. * U.deg, )
azs = (0. * U.deg, )

# EDIT
sample = \
    [
        (
            snap_id(res=1, phys='hydro', vol=1, snap=127),
            [
                obj_id(fof=1, sub=0),
            ]
        ),
    ]

targets = [Target(s[0], o, incls, azs) for s in sample for o in s[1]]


def selected(s, o, sample):
    for snap, objs in sample:
        if s == snap:
            for obj in objs:
                if o == obj:
                    return True
    return False
