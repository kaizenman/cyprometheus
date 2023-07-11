from skbuild import setup
from setuptools import find_packages
from setuptools import Extension
import os

setup_requires = [
    "setuptools>=18.0",
    "setuptools_scm",
]

install_requires = [
    "flask",
    "prometheus-client",
    "requests",
]

extras_require = {
    "dev": [
   ],
}

extensions = [
    Extension(
        name="cyprometheus.foo.foo_init",
        sources=["cyprometheus/foo/foo_init.pyx"],
    )
]

setup(
    name="cyprometheus",
    description="Prototype",
    keywords="prototype",
    packages=find_packages(),
    platforms=["linux", "darwin"],
    classifiers=[
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    data_files=[
    ],
    setup_requires=setup_requires,
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={
    },
    cmake_install_dir="cyprometheus/cpp",
    cmake_args=[
    ]
)
