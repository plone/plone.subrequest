from setuptools import find_packages
from setuptools import setup

import os.path


version = "2.0.0"

setup(
    name="plone.subrequest",
    version=version,
    description="Subrequests for Zope2",
    long_description=(
        open("README.rst").read()
        + "\n\n"
        + open(os.path.join("plone", "subrequest", "usage.rst")).read()
        + "\n\n"
        + open("CHANGES.rst").read()
    ),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "Framework :: Zope",
        "Framework :: Zope :: 5",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="plone",
    author="Plone Foundation",
    author_email="plone-developers@lists.sourceforge.net",
    url="https://github.com/plone/plone.subrequest",
    license="GPL version 2",
    packages=find_packages(),
    namespace_packages=["plone"],
    include_package_data=True,
    platforms="Any",
    zip_safe=False,
    install_requires=[
        "setuptools",
        "zope.globalrequest",
    ],
    extras_require={
        "test": [
            "five.localsitemanager",
            "manuel",
            "plone.testing[zope]",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
