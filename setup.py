from setuptools import setup, find_namespace_packages

setup(
    name='Personalhelper',
    version='0.1.0',
    packages=find_namespace_packages(),
    install_requires=["prettytable"],
    entry_points={"console_scripts": ["personal_helper=personal_helper.personal_helper.personal_helper:main"]}
)
