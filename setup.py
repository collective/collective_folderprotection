from setuptools import setup, find_packages
import os

version = '2.0.1'

long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='collective_folderprotection',
      version=version,
      description="",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Enfold Systems, Inc.',
      author_email='info@enfoldsystems.com',
      url='https://github.com/collective/collective_folderprotection',
      license='gpl',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'six',
          'plone.app.contenttypes',
      ],
      extras_require={
          'test': [
              'cssselect',
              'lxml',
              'mock',
              'plone.api >=1.8.5',
              'plone.app.robotframework',
              'plone.app.testing [robot]',
              'plone.browserlayer',
              'plone.cachepurging',
              'plone.testing',
              'robotsuite',
              'testfixtures',
              'transaction',
              'tzlocal',
          ],
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
