import setuptools

requirements = ['flask', 'pickle', 'oef', 'schedule']

setuptools.setup(
    name='Backend',
    version='0.0.1',
    packages=setuptools.find_packages(),
    install_requires=requirements)
