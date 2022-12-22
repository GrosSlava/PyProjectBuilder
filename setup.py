# Copyright (c) 2022 GrosSlava

from setuptools import setup

from PyProjectBuilder.PyProjectBuildLibrary import PY_PROJECT_BUILD_VERSION





setup(
    name= 'PPBuild',
    version = PY_PROJECT_BUILD_VERSION,
    packages = ["PyProjectBuilder"],
    entry_points = {
        'console_scripts': [
            "PPBuild = PyProjectBuilder.PPBuilder:Run"
        ]
    },
    install_requires = ["CppHeaderParser"]
)