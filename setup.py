
from setuptools import setup, find_packages

setup(name='Shorty',
    version='0.1',
    description='Simple URL shortener WSGI app with Beaker cache backend',
    author='Aleksandar Radulovic',
    author_email='alex@a13x.net',
    url='hub.com/a13x/various.py/blob/master/shorty.py',
    py_modules=['shorty'],
    packages=find_packages(exclude=['ez_setup']),
    #packages=['bobo', 'Beaker'],
    include_package_data=True,
    zip_safe=False,
    )
