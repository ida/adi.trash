from setuptools import setup, find_packages
import os

version = '0.5'

setup(name='adi.trash',
      version=version,
      description="Plone addon, changing deletion-behaviour: " + 
                  "Moves items into a trash-folder, instead of deleting them.",
      long_description=open("README.rst").read() + '\n' + 
                       open('docs/CHANGES.rst').read(),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Ida Ebkes',
      author_email='contact@ida-ebkes.eu',
      url='https://github.com/ida/adi.trash',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['adi'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'plone.api',
          'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
