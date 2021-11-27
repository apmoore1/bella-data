from setuptools import find_packages
from setuptools import setup

setup(name='bella_data',
      version='0.0.1',
      description='Bella-Data',
      long_description='',
      long_description_content_type="text/markdown",
      url='https://github.com/apmoore1/bella-data',
      author='Andrew Moore',
      author_email='andrew.p.moore94@gmail.com',
      license='Apache License 2.0',
      install_requires=[
          "dataclasses;python_version<'3.7'"
      ],
      python_requires='>=3.6.1',
      packages=find_packages(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3.6'
      ])