# PyProjectBuilder

It is tool to build your c/c++ project.
It is easier in use than Makefile or CMake.


## Main features
- Not need to write build script
- Use incremental build
- Analyzes files dependencies

## How to use
- Put in the project root directory file 'PyBuildFile.txt'
- Write your build configuration in 'PyBuildFile.txt' (see build config)
- Run python script by ```python3  PPBuilder.py <path to your PyBuildFile.txt>```



## Tool options

```--help```                                            ---List all options \
```--version```                                         ---Print current version \
```--BuildType=[Debug, Shipping]```                     ---Type of build \
```--TargetArch=[x86, x86_64, armm, arm_64]```          ---Build target architecture \
```--BUILD```                                           ---Build project \
```--REBUILD```                                         ---Clear intermediate and build project \
```--CLEAR```                                           ---Clear intermediate files \
```--SILENT```                                          ---Disable compilation logs \
```--NO_MULTIPROCESSING```                              ---Disable parallel compilation

## Build config options

IntermediateFolder = [relative path to intermediate folder (by default 'Intermediate')] \
BuildFolder = [relative path to build folder (by default 'Build')] \
IsLibrary = true (Mark that this project is library, by default false) \
Modules = Source/Module1;Source/Module2 (relative paths to building modules files) \
Modules = Source/Module3 (append array of modules) \
Ignore = Source/Debug.cpp;Source/DebugDir (relative paths to files or folders to ignore) \
AdditionalIncludeDirs = Source/Public (additional relative paths to folders for includes search) \
AdditionalLibsDirs = /media/user/sda/MyLibs (absolute paths to dirs where compiler can search linkig libs) \
Libs = SFML (absolute paths to libs to link or it's name) \
ResultName = MyProgram (name of resulting file, be default 'a') \
EntryPointName = MyFooMain (name of the function that will be the entry point to the program, by default use compiler defaults) \
ConvertWarningsToErrors = false (convert all compilation warnings into errors, by default false)

example file PyBuildFile.txt:

```
ResultName = MyProgram
IntermediateFolder = Intermediate
BuildFolder = Build
IsLibrary = false
Modules = Source/Module1
Modules = Source/Module2
Modules = Source/Module2
AdditionalIncludeDirs = Source/Public;ThirdParty
ConvertWarningsToErrors = true
```
