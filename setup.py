from setuptools import setup, find_packages


setup(
    name="covid19-estimator-py",
    packages=find_packages(),
    zip_safe=False,
    install_requires=['Flask'],
)
