REM Test the code!
cd %WORKSPACE%\build\beta-x64

REM Run worker tests with OpenCppCoverage
rm %WORKSPACE%\workerCoverage.xml -f
OpenCppCoverage --modules tests-worker.exe --sources %WORKSPACE%\worker --excluded_sources %WORKSPACE%\worker\*.h --export_type=cobertura:%WORKSPACE%\workerCoverage.xml -- ut\tests-worker.exe --gtest_output="xml:%WORKSPACE%\workertests.xml" --gtest_filter=-KeyboardTest.KbdLocaleTest

REM Run service tests with OpenCppCoverage
rm %WORKSPACE%\serviceCoverage.xml -f
OpenCppCoverage --modules tests-service.exe --sources %WORKSPACE%\service --excluded_sources %WORKSPACE%\service\*.h --export_type=cobertura:%WORKSPACE%\serviceCoverage.xml -- ut\tests-service.exe --gtest_output="xml:%WORKSPACE%\servicetests.xml"

REM Run abctrl tests (requires psexec for pipe privilege issues) 
%TCROOT%\win32\PsTools-2.44-1\PsExec -accepteula -s -w %WORKSPACE%\build\beta-x64 %WORKSPACE%\build\beta-x64\ut\tests-abctrl.exe --gtest_output="xml:%WORKSPACE%\abctrltests.xml"