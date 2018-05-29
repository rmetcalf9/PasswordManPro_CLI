from setuptools import setup
import versioneer

#Dependancy lists maintained here and in tox.ini
sp_install_requires = [
#  'pytz==2018.4',
#  'flask==0.12.2',
#  'flask_restplus==0.10.1',
#  'python-dateutil==2.7.2',
#  'sortedcontainers==1.5.9'
]
sp_tests_require = [
  'nose==1.3.7'
]

all_require = sp_install_requires + sp_tests_require

setup(name='passwordmanpro_cli',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='Python based command line interface for Password Manager Pro',
      url='https://github.com/rmetcalf9/passwordmanpro_cli',
      author='Robert Metcalf',
      author_email='rmetcalf9@googlemail.com',
      license='MIT',
      packages=['passwordmanpro_cli'],
      zip_safe=False,
      install_requires=sp_install_requires,
      tests_require=sp_tests_require,
      include_package_data=True)