@echo off
chcp 65001 > nul

<nul set /p="Создание билда для Konva: "
cd /d "%~dp0"
cd konva
call npm run build >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка!
    pause
    exit /b %errorlevel%
)
echo Ок


<nul set /p="Создание билда для guntt: "
cd ..
set "source=.\konva\dist"
set "destination=.\guntt\src\components\Konva"
xcopy "%source%" "%destination%" /E /Y /I /Q >nul
cd guntt
call npm run build >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка!
    pause
    exit /b %errorlevel%
)
echo Ок

<nul set /p="Обновление public директории: "
cd ..
set "source=.\guntt\build"
set "destination=.\public"
xcopy "%source%" "%destination%" /E /Y /I /Q >nul
echo Ок

timeout /t 3 /nobreak
