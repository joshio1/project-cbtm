rm -R %WORKSPACE%\codecoverage -f
cd %WORKSPACE%\build\beta-x64\
@echo off
setlocal enabledelayedexpansion
REM To allow variables to be expanded as the program runs. Otherwise, module etc. is expanded at the start itself.
FOR /F "tokens=1,2* delims=," %%G IN ('python C:\project-cbtm\cbtm\testcases_generator.py %WORKSPACE% %GIT_COMMIT% %GIT_PREVIOUS_COMMIT%') DO (
REM delims=, means every line is split using comma as separator. 1,2 means that only 1st and second tokens are picked up. %%G is the first token and %%H is the second
if %%H==service (
REM Run Code Coverage Command
set module=service
) else (
set module=worker
)
OpenCppCoverage --modules tests-!module!.exe --sources %WORKSPACE%\!module! --excluded_sources %WORKSPACE%\!module!\*.h --export_type=cobertura:%WORKSPACE%\codecoverage\!module!\%%G\coberturaCoverage.xml -- .\ut\tests-!module!.exe --gtest_output="xml:%WORKSPACE%\codecoverage\!module!\%%G\test.xml" --gtest_filter=%%G
)