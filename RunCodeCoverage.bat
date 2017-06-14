@echo off
set workspace=%1%
echo 'Workspace is %1%'
setlocal enabledelayedexpansion
FOR /F "tokens=*" %%G IN ('%1%\ut\tests-service.exe --gtest_list_tests') DO (
echo %%G|find "." > nul
if errorlevel 1 (
set test_case=!test_suite!%%G
echo !test_case!
REM Run Code Coverage Command
OpenCppCoverage --modules tests-service.exe --sources !workspace!\service --excluded_sources !workspace!\service\*.h --export_type=cobertura:!workspace!\codecoverage\!test_case!\cobertura_output.xml -- !workspace!\ut\tests-service.exe --gtest_output="xml:!workspace!\codecoverage\!test_case!\gtest_result.xml" --gtest_filter=!test_case!
) else (
set test_suite=%%G
    echo !test_suite!
)
)