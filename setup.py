from setuptools import setup, find_packages

version = '1.1'

setup(
    name = 'plone.subrequest',
    version = version,
    description = 'Subrequests for Zope2',
    long_description=open("README.txt").read() + "\n\n" + open("CHANGES.txt").read(),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Zope2",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        ],
    keywords='plone',
    author='Plone Foundation',
    author_email='plone-developers@lists.sourceforge.net',
    url='http://pypi.python.org/pypi/plone.subrequest/',
    license='GPL version 2',
    packages = find_packages(),
    namespace_packages = ['plone'],
    include_package_data = True,
    platforms = 'Any',
    zip_safe = False,
    install_requires=[
        # 'Acquisition',
        'five.globalrequest',
        'setuptools',
        'zope.globalrequest',
        ],
    extras_require = {
        'test': [
            'plone.testing [z2]',
            'manuel',
            ],
        },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
    )
