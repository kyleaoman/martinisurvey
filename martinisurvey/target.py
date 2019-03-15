from martini import Martini, DataCube
from martini.beams import GaussianBeam
from martini.spectral_models import GaussianSpectrum
from martini.sph_kernels import WendlandC2Kernel, GaussianKernel
from martini.sources import SOSource
import astropy.units as U
from itertools import product
from _str import target_str, targetview_str
from _auto import SOautoload, datadir
from os import path


class TargetView(object):

    def __init__(self, snap_id, obj_id, incl, az):
        self.snap_id = snap_id
        self.obj_id = obj_id
        self.incl = incl
        self.az = az

        self.SO = SOautoload(self.snap_id, self.obj_id)

    def __repr__(self):
        return targetview_str(self.snap_id, self.obj_id, self.incl, self.az)

    def generate_datacube(self):
        if path.exists(path.join(datadir, self.__repr__() + '.fits')):
            print('Already completed.')
            return
        print(self, 'Launching MARTINI.')

        # EDIT - MARTINI configuration
        source = SOSource(
            distance=3.657 * U.Mpc,
            rotation={'L_coords': (self.incl, self.az)},
            ra=0. * U.deg,
            dec=0. * U.deg,
            SO_instance=self.SO
        )
        # can rotate on the sky with:
        # source.rotate(axis_angle=('x', PA * U.deg))
        
        datacube = DataCube(
            n_px_x=1024,
            n_px_y=1024,
            n_channels=100,
            px_size=3. * U.arcsec,
            channel_width=4. * U.km * U.s ** -1,
            velocity_centre=source.vsys
        )
        
        beam = GaussianBeam(
            bmaj=6. * U.arcsec,
            bmin=6. * U.arcsec,
            bpa=0. * U.deg,
            truncate=4.
        )
        
        noise = None
        
        spectral_model = GaussianSpectrum(
            sigma='thermal'
        )
        
        sph_kernel = GaussianKernel.mimic(WendlandC2Kernel)
        
        M = Martini(
            source=source,
            datacube=datacube,
            beam=beam,
            noise=noise,
            spectral_model=spectral_model,
            sph_kernel=sph_kernel
        )
        
        M.insert_source_in_cube()
        M.add_noise()
        M.convolve_beam()
        M.write_beam_fits(
            path.join(datadir, self.__repr__() + '.beam.fits'),
            channels='velocity'
        )
        M.write_fits(
            path.join(datadir, self.__repr__() + '.fits'),
            channels='velocity'
        )


class Target(object):

    def __init__(self, snap_id, obj_id, incls, azs):
        self.snap_id = snap_id
        self.obj_id = obj_id
        self.views = [TargetView(snap_id, obj_id, incl, az)
                      for incl, az in product(incls, azs)]

    def __repr__(self):
        return target_str(self.snap_id, self.obj_id)
        
