import os

from setuptools import (
    setup,
    find_packages,
    )

try:
    README = open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               'README.rst')).read()
except IOError:
    README = ''

setup(name='linode',
      version='0.2',
      packages=find_packages(),
      description=('Provides dynamic, always up to date, Python bindings '
                   'for the Linode API'),
      long_description=README,
      install_requires=['requests'],
      author='Kane Mathers',
      author_email='kane@kanemathers.name',
      url='https://github.com/kanemathers/linode'
)
