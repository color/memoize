try:
  from setuptools import setup
except:
  from distutils.core import setup


setup(name = "memoize",
      version = "0.2.0",
      description = "A memoize decorator",
      author = "Color Genomics",
      author_email = "dev@getcolor.com",
      url = "https://github.com/ColorGenomics/memoize",
      packages = ["memoize"],
      install_requires=[],
      license = "MIT",
      )
