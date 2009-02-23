#!/usr/bin/env python
from distutils.core import setup
import pyppp

setup(
    name='PyPPP',
    version='%s' % pyppp.__version__,
    description='PyPPP is a python implementation of Perfect Paper Passwords a single-use passcode system for multifactor authentification. PyPPP is also bundled with a Django API.',
    author='Kyle Fuller',
    author_email='inbox@kylefuller.co.uk',
    url='http://kylefuller.co.uk/projects/pyppp/',
    download_url='http://media.kylefuller.co.uk/pyppp/pyppp-%s.zip' % lithium.__version__,
    packages=['pyppp', 'pyppp.django'],
    package_data={'pyppp.django': ['templates/pyppp/*.html']},
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Security',
    ]
)