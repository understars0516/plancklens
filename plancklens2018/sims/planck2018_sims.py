"""Planck 2018 release simulation libraries.

"""
import healpy as hp
import numpy as np

from plancklens2018 import utils

class smica_dx12:
    """ SMICA 2018 release simulation and data library at NERSC.

    """
    def __init__(self):
        self.cmbs = '/project/projectdirs/cmb/data/planck2018/ffp10/compsep/mc_cmb/dx12_v3_smica_cmb_mc_%05d_005a_2048.fits'
        self.noise = '/project/projectdirs/cmb/data/planck2018/ffp10/compsep/mc_noise/dx12_v3_smica_noise_mc_%05d_005a_2048.fits'
        self.data = '/project/projectdirs/cmb/data/planck2018/pr3/cmbmaps/dx12_v3_smica_cmb_005a_2048.fits'

    def hashdict(self):
        return {'cmbs':self.cmbs, 'noise':self.noise, 'data':self.data}

    def get_sim_tmap(self, idx):
        if idx == -1:
            return self.get_dat_tmap()
        return 1e6 * (hp.read_map(self.cmbs % idx, field=0) + hp.read_map(self.noise % idx, field=0))

    def get_dat_tmap(self):
        return 1e6 * hp.read_map(self.data, field=0)

    def get_sim_pmap(self, idx):
        if idx == -1:
            return self.get_dat_pmap()
        Q = 1e6 * (hp.read_map(self.cmbs % idx, field=1) + hp.read_map(self.noise % idx, field=1))
        U = 1e6 * (hp.read_map(self.cmbs % idx, field=2) + hp.read_map(self.noise % idx, field=2))
        return Q, U

    def get_dat_pmap(self):
        return 1e6 * hp.read_map(self.data, field=1), 1e6 * hp.read_map(self.data, field=2)

class ffp10cmb_widnoise:
    def __init__(self, transf, nlevt, nlevp, pix_libphas, nside=2048):
        """Simulation library with freq-0 FFP10 CMB and ideal, homogeneous noise.

            Args:
                transf: transfer function (beam and pixel window)
                nlevt, nlevp (float): temperature and polarization noise levels in uK-armin.
                pix_libphas: random phases simulation library (see phas.py) of the noise maps.

        """
        assert pix_libphas.shape == (hp.nside2npix(nside),), pix_libphas.shape
        self.nlevt = nlevt
        self.nlevp = nlevp
        self.transf = transf
        self.pix_libphas = pix_libphas
        self.nside = nside

    def hashdict(self):
        return {'transf':utils.clhash(self.transf), 'nlevt':np.float32(self.nlevt), 'nlevp':np.float32(self.nlevp),
                'pix_phas':self.pix_libphas.hashdict()}

    def get_sim_tmap(self, idx):
        T = hp.alm2map(hp.almxfl(cmb_len_ffp10.get_sim_tlm(idx), self.transf), self.nside)
        nlevt_pix = self.nlevt / np.sqrt(hp.nside2pixarea(self.nside, degrees=True)) / 60.
        T += self.pix_libphas.get_sim(idx, idf=0) * nlevt_pix
        return T

    def get_sim_pmap(self, idx):
        elm = hp.almxfl(cmb_len_ffp10.get_sim_elm(idx), self.transf)
        blm = hp.almxfl(cmb_len_ffp10.get_sim_blm(idx), self.transf)
        Q, U = hp.alm2map_spin((elm, blm), self.nside, 2, hp.Alm.getlmax(elm.size))
        del elm, blm
        nlevp_pix = self.nlevp / np.sqrt(hp.nside2pixarea(self.nside, degrees=True)) / 60.
        Q += self.pix_libphas.get_sim(idx, idf=1) * nlevp_pix
        U += self.pix_libphas.get_sim(idx, idf=2) * nlevp_pix
        return Q, U

class cmb_len_ffp10:
    """ FFP10 input sim libraries, lensed alms.

    """
    def __init__(self):
        pass

    def hashdict(self):
        return {'sim_lib': 'ffp10 lensed scalar cmb inputs, freq 0'}

    @staticmethod
    def get_sim_tlm(idx):
        return 1e6 * hp.read_alm('/project/projectdirs/cmb/data/generic/cmb/ffp10/mc/scalar/ffp10_lensed_scl_cmb_000_alm_mc_%04d.fits'%idx, hdu=1)

    @staticmethod
    def get_sim_elm(idx):
        return 1e6 * hp.read_alm('/project/projectdirs/cmb/data/generic/cmb/ffp10/mc/scalar/ffp10_lensed_scl_cmb_000_alm_mc_%04d.fits'%idx, hdu=2)

    @staticmethod
    def get_sim_blm(idx):
        return 1e6 * hp.read_alm('/project/projectdirs/cmb/data/generic/cmb/ffp10/mc/scalar/ffp10_lensed_scl_cmb_000_alm_mc_%04d.fits'%idx, hdu=3)


class cmb_unl_ffp10:
    """ FFP10 input sim libraries, unlensed alms.

    """
    def __init__(self):
        pass

    def hashdict(self):
        return {'sim_lib': 'ffp10 unlensed scalar cmb inputs'}

    @staticmethod
    def get_sim_tlm(idx):
        return 1e6 * hp.read_alm('/project/projectdirs/cmb/data/generic/cmb/ffp10/mc/scalar/ffp10_unlensed_scl_cmb_000_tebplm_mc_%04d.fits'% idx, hdu=1)

    @staticmethod
    def get_sim_elm(idx):
        return 1e6 * hp.read_alm('/project/projectdirs/cmb/data/generic/cmb/ffp10/mc/scalar/ffp10_unlensed_scl_cmb_000_tebplm_mc_%04d.fits'% idx, hdu=2)

    @staticmethod
    def get_sim_blm(idx):
        return 1e6 * hp.read_alm('/project/projectdirs/cmb/data/generic/cmb/ffp10/mc/scalar/ffp10_unlensed_scl_cmb_000_tebplm_mc_%04d.fits'% idx, hdu=3)

    @staticmethod
    def get_sim_plm(idx):
        return hp.read_alm('/project/projectdirs/cmb/data/generic/cmb/ffp10/mc/scalar/ffp10_unlensed_scl_cmb_000_tebplm_mc_%04d.fits'% idx, hdu=4)

