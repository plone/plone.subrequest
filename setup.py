# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

import os.path


version = '1.8.6'

setup(
    name='plone.subrequest',
    version=version,
    description='Subrequests for Zope2',
    long_description=(
        open("README.rst").read() + "\n\n" +
        open(os.path.join('plone', 'subrequest', 'usage.rst')).read() +
        "\n\n" +
        open("CHANGES.rst").read()),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Framework :: Zope2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
    ],
    keywords='plone',
    author='Plone Foundation',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://pypi.python.org/pypi/plone.subrequest/',
    license='GPL version 2',
    packages=find_packages(),
    namespace_packages=['plone'],
    include_package_data=True,
    platforms='Any',
    zip_safe=False,
    install_requires=[
        # 'Acquisition',
        'five.globalrequest',
        'setuptools',
        'six',
        'zope.globalrequest',
        ],
    extras_require={
        'test': [
            'five.localsitemanager',
            'manuel',
            'plone.testing [z2]',
        ],
        'archetypes': [
            'plone.app.blob',
            # see https://github.com/plone/plone.app.blob/issues/19
            'Products.MimetypesRegistry',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
