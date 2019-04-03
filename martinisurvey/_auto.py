from simobj import SimObj
from simfiles.configs.APOSTLE_SIDM_cosma import __file__ as SFcfg  # EDIT
from simobj.configs.APOSTLE_SIDM_cosma import __file__ as SOcfg  # EDIT

datadir = '/cosma/home/durham/koman/Data/mock_sidm/'  # EDIT


def SOautoload(snap, obj):
    return SimObj(
        snap_id=snap,
        obj_id=obj,
        mask_type='fof',
        mask_args=(obj, ),
        mask_kwargs=dict(),
        configfile=SOcfg,
        simfiles_configfile=SFcfg,
        ncpu=1
    )


def SOautorotate(SO):
    SO.rotate(L_coords=('mHI_g', 'xyz_g', 'vxyz_g'))
