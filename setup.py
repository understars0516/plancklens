import setuptools
from numpy.distutils.core import setup
from numpy.distutils.misc_util import Configuration

with open("README.md", "r") as fh:
    long_description = fh.read()


def configuration(parent_package='', top_path=''):
    config = Configuration('', parent_package, top_path)
    config.add_extension('plancklens.wigners.wigners', ['plancklens/wigners/wigners.f90'])
    config.add_extension('plancklens.n1.n1f', ['plancklens/n1/n1f.f90'],
                         libraries=['gomp'],  extra_compile_args=['-Xpreprocessor', '-fopenmp', '-w'])
    return config

setup(
    name='plancklens',
    version='0.0.1',
    packages=['plancklens', 'plancklens.n1', 'plancklens.filt', 'plancklens.sims', 'plancklens.helpers',
              'plancklens.qcinv', 'plancklens.wigners', 'plancklens.wigners'],
    data_files=[('plancklens/data/cls', ['plancklens/data/cls/FFP10_wdipole_lensedCls.dat',
                                'plancklens/data/cls/FFP10_wdipole_lenspotentialCls.dat',
                                'plancklens/data/cls/FFP10_wdipole_params.ini'])],
    url='https://github.com/carronj/plancklens',
    author='Julien Carron',
    author_email='to.jcarron@gmail.com',
    description='Planck lensing python pipeline',
    install_requires=['numpy', 'healpy', 'six', 'mpi4py'],
    requires=['numpy', 'healpy', 'six', 'mpi4py', 'scipy'],
    long_description=long_description,
    configuration=configuration)

