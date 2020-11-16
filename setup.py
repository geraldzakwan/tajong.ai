from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    license = f.read()

setup(
    name='hafalin',
    version='0.1.0',
    description='Hafalin API, an API to generate questions given document',
    long_description=readme,
    author='Geraldi Dzakwan; Ari Pratama Zhorifiandi',
    author_email='geraldi.dzakwan@gmail.com; arizho16@gmail.com',
    url='https://github.com/geraldzakwan/tajong.ai',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
