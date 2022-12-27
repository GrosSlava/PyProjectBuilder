# PyProjectBuilder

It is tool to build your c/c++ project.
It is easier in use than Makefile or CMake.



## Main features

- Not need to write build script
- Use incremental build
- Analyzes files dependencies

## How to use

- First time run ```Install``` script
- Put in the project root directory file 'PyBuildFile.txt'
- Write your build configuration in 'PyBuildFile.txt' (see build config)
- Run python script by ```python3  PPBuilder.py <path to your PyBuildFile.txt>``` if you didn't install tool
- Run tool by ```PPBuild <path to your PyBuildFile.txt>``` if it was installed by using ```Install``` script
- By default (if no path to file) PPBuild searches 'PyBuildFile.txt' in execution directory

## Tool options

```--version```                                         show program's version number and exit \
```-h```, ```--help```                                  show this help message and exit \
```-a TYPE```, ```--Action=TYPE```                      select tool action (Build, Rebuild, Clear) \
```-b TYPE```, ```--BuildType=TYPE```                   type of build (Debug, Shipping) \
```-t ARCH```, ```--TargetArch=ARCH```                  build target architecture (x86, x86_64, arm, arm_64) \
```-s```, ```--SILENT```                                disable compilation logs \
```--NO_MULTIPROCESSING```                              disable parallel compilation



## Build config options

Config options contains flags, arrays and enums.
- Flags will be redefined at each mention. Available values: True, true, TRUE, yes, YES, On, ON, 1, False, false, FALSE, no, NO, No, 0
- Arrays will be extended at each mention. Elements should be separated by ';'.
- Enums should be defined by specific keyword.

```
# It is example config file with all options.

# Relative path to folder for intermediate files.
# By default = Intermediate
IntermediateFolder = Intermediate

# Put all intermediate files in one folder.
# By default = false
FlatIntermediate = false

# Relative path to folder for build files.
# By default = Build
BuildFolder = Build

# Put all build files in one folder.
# By default = false
FlatBuild = false

# Array of relative paths to modules(folders) to build.
# By default =
Modules = Src/Module1;Src/Module2

# Array of relative paths to files/folders to ignore.
# By default =
Ignore =

# Array of relative paths to dirs for includes search.
# By default =
AdditionalIncludeDirs =

# Array of absolute paths to dirs for libraries search.
# By default =
AdditionalLibsDirs =

# Array of absolute paths to libs files or its name to link.
# By default =
Libs = m;c;sfml

# Type of build result.
# Available values = [NoLink, Executable, Dynamic, Static]
# By default = Executable
ResultType = Executable

# Name of building result.
# By default = a
ResultName = MyProgram.out

# Name of the function that will be the entry point (empty means compiler default).
# By default =
EntryPointName =

# Tell compiler convert warnings into errors.
# By default = false
ConvertWarningsToErrors = true

# Tell compiler to show all warnings.
# By default = false
EnableAllWarnings = true

# Console command to execute after build complete.
# By default =
PostBuildAction =
```
