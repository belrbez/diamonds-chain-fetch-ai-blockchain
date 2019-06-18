import setuptools

requirements = ['flask', 'oef', 'schedule']

setuptools.setup(
    name='Backend',
    version='0.0.1',
    packages=setuptools.find_packages(),
    install_requires=requirements)
