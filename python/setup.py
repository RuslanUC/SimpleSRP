from os.path import join, dirname

from setuptools import setup, find_packages, find_namespace_packages

setup(
    name="simplesrp",
    version="1.0.0b1",

    description='A python implementation of SRP-6a in pure python.',
    long_description='A python implementation of SRP-6a in pure python.',

    author='RuslanUC',

    url='https://github.com/RuslanUC/SimpleSRP',
    repository='https://github.com/RuslanUC/SimpleSRP',
    license="MIT",

    classifiers=[
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Intended Audience :: Developers',
        'Environment :: Console',
    ],
    platforms=['Any'],
    install_requires=[],
    python_requires='>=3.7',

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,
)
