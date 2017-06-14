REM Running all the test-cases one by one, generating code coverage data per test-case
rm -R %WORKSPACE%\codecoverage -f
cd %WORKSPACE%\build\beta-x64


@echo off
setlocal enabledelayedexpansion

FOR /F "tokens=*" %%G IN ('ut\tests-service.exe --gtest_list_tests') DO (
echo %%G|find "." > nul
if errorlevel 1 (
set test_case=!test_suite!%%G
echo !test_case!
REM Run Code Coverage Command
OpenCppCoverage --modules tests-service.exe --sources %WORKSPACE%\service --excluded_sources %WORKSPACE%\service\*.h --export_type=cobertura:%WORKSPACE%\codecoverage\service\!test_case!\cobertura_output.xml -- ut\tests-service.exe --gtest_output="xml:%WORKSPACE%\codecoverage\service\!test_case!\gtest_result.xml" --gtest_filter=!test_case!
) else (
set test_suite=%%G
    echo !test_suite!
)
)

FOR /F "tokens=*" %%G IN ('ut\tests-worker.exe --gtest_list_tests') DO (
echo %%G|find "." > nul
if errorlevel 1 (
set test_case=!test_suite!%%G
echo !test_case!
REM Run Code Coverage Command
OpenCppCoverage --modules tests-worker.exe --sources %WORKSPACE%\worker --excluded_sources %WORKSPACE%\worker\*.h --export_type=cobertura:%WORKSPACE%\codecoverage\worker\!test_case!\cobertura_output.xml -- ut\tests-worker.exe --gtest_output="xml:%WORKSPACE%\codecoverage\worker\!test_case!\gtest_result.xml" --gtest_filter=!test_case!
) else (
set test_suite=%%G
    echo !test_suite!
)
)