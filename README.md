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
```--BUILD```                                           ---Build project \
```--REBUILD```                                         ---Clear intermediate and build project \
```--CLEAR```                                           ---Clear intermediate files \
```--SILENT```                                          ---Disable compilation logs

## Build config options

IntermediateFolder = [relative path to intermediate folder (by default 'Intermediate')] \
BuildFolder = [relative path to build folder (by default 'Build')] \
IsLibrary = true (Mark that this project is library, by default false) \
Modules = Source/Module1;Source/Module2 (relative paths to building modules files) \
Modules = Source/Module3 (append array of modules) \
Ignore = Source/Debug.cpp;Source/DebugDir (relative paths to files or folders to ignore) \
AdditionalInclude = Source/Public (additional relative paths to folders for includes search) \
ResultName = MyProgram (name of resulting file, be default 'a')

example file PyBuildFile.txt:

```
ResultName = MyProgram
IntermediateFolder = Intermediate
BuildFolder = Build
IsLibrary = false
Modules = Source/Module1
Modules = Source/Module2
Modules = Source/Module2
AdditionalInclude = Source/Public;ThirdParty
```
