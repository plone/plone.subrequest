from pathlib import Path
from setuptools import find_packages
from setuptools import setup


version = "2.0.5"

long_description = f"""
{Path("README.rst").read_text()}
\n\n
{(Path("plone") / "subrequest" / "usage.rst").read_text()}
\n\n
{Path("CHANGES.rst").read_text()}
"""

setup(
    name="plone.subrequest",
    version=version,
    description="Subrequests for Zope2",
    long_description=long_description,
    long_description_content_type="text/x-rst",
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
    python_requires=">=3.8",
    install_requires=[
        "AccessControl",
        "Acquisition",
        "plone.protect",
        "setuptools",
        "zope.component",
        "zope.globalrequest",
        "zope.interface",
        "zope.publisher",
    ],
    extras_require={
        "test": [
            "five.localsitemanager",
            "manuel",
            "plone.testing[zope]",
            "zope.configuration",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
