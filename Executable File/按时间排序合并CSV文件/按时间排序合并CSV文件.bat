@echo off 
color 2f
mode con lines=30 cols=80

set "type=csv" rem 文件类型
set "folder=%~dp0." rem 文件所在目录
set "SubDir=0" rem 是否包含子目录

wmic.exe /? >nul 2>&1 || (echo no wmic, exit& pause&exit/b)

echo ************************** Reorder by time starts! *****************************

if "%~1" neq "" set "folder=%~1"
for %%a in ("%folder%") do set "FileD=%%~da" & set "FileP=%%~pnxa\"

goto skip
rem 先重命名一次，加一段文件名中不会出现的字符串，以防可能的文件名重复问题。
set "ext=%type%" & set "sub="
if "%type%" neq "*" if "%type%" neq "*.*" set "ext=*.%type:,= *.%"
if "%SubDir%" neq "0" set "sub=/s"
for /f "delims=" %%a in ('dir /b %sub% %ext%') do (
    ren "%%~fa" "powerbat@bathome_%%~nxa"
)
:skip

set "part=%FileP:\=\\%"
set "part=%part:[=[[]%"
set "part=%part:_=[_]%"
setlocal enableDelayedExpansion
set "part=!part:%%=[%%]!"
endlocal& set "part=%part%"
if "%type%" neq "*" if "%type%" neq "*.*" (
    set "ext=and (extension='%type:,=' OR extension='%')"
) else set "ext="
if "%SubDir%"=="0" (
    set "Filter=drive='%FileD%' and path='%FileP:\=\\%' %ext%"
) else (
    set "Filter=drive='%FileD%' and path LIKE '%part%%%' %ext%"
)
(set wmic=wmic.exe datafile where "%Filter%" get name^,LastModified)

for /f "tokens=1,3* delims=.+ " %%a in ('%%wmic%%') do (
    set "t=%%a"
    rem 用for过滤掉wmic结果中的不可见字符
    for /f "delims=" %%i in ("%%c") do (
        set "f=%%~fi"
        set "p=%%~dpi"
        set "n=%%~ni"
        set "x=%%~xi"
        setlocal enableDelayedExpansion
        set "t=!t:~,4!-!t:~4,2!-!t:~6,2! !t:~8,2!.!t:~10,2!.!t:~12!"
        if not exist "!p!!t!!x!" (
            ren "!f!" "!t!!x!"
        ) else  if "!t!" neq "!n!" (
            set n=1
            for %%u in ("!p!!t!_*!x!") do set /a n+=1
            ren "!f!" "!t!_!n!!x!"
        )
        endlocal
    )
)
echo ************************ Reorder by time completed! ****************************

python Reference_Combine_CSV.py

pause