from setuptools import find_packages, setup

setup(
    name='date',
    packages=find_packages(include=['date','date.*']),
    version='0.1.2',
    description='Pipeline que padroniza uma data',
    author='Juliana Nascimento Silva',
    license='Unlicensed'
)

