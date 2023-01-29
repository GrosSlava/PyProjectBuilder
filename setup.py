# Copyright (c) 2022 - 2023 GrosSlava. All rights reserved.

from setuptools import setup

from PyProjectBuilder.PyProjectBuildLibrary import PY_PROJECT_BUILD_VERSION





setup(
	name= 'PyProjectBuilder',
	version = PY_PROJECT_BUILD_VERSION,
	packages = ["PyProjectBuilder"],
	entry_points = {
		'console_scripts': [
			"PPBuild = PyProjectBuilder.PPBuilder:Run"
		]
	},
	install_requires = ["CppHeaderParser"]
)