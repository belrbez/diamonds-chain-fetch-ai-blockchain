import setuptools

requirements = ['flask', 'pickle', 'oef', 'fetchai', 'schedule']

setuptools.setup(
    name='Backend',
    packages=setuptools.find_packages(),
    install_requires=requirements)
