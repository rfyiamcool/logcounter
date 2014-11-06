from distutils.core import setup

with open('README.md') as file:
    long_description = file.read()

setup(name='logcounter',
      version='1.0',
      description='no-block count log success and error sum num',
      long_description=long_description,
      author='rfyiamcool',
      author_email='rfyiamcool@163.com',
      url='https://github.com/rfyiamcool',
      scripts=['logcounter'])
