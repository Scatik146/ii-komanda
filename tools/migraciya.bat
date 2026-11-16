@echo off
chcp 65001 >nul
rem migraciya: перенос папки команды в ii-komanda одной командой — обновить, проба, сверка, перенос, проверка, отправка
rem   из папки ii-komanda:  tools\migraciya.bat
rem   рядом в одной папке (Documents) — ii-komanda, drakon-graf, teacher-workpad, memory_maryam_ai
rem   любой шаг упал — дальше не идёт; уже сделанные коммиты остаются на ноутбуке (push — только в конце)
rem Код по-фортовски: слова — метки, над каждой строка «слово: что делает»; ДРАКОН-лист — migraciya-list.md
rem Работаем с копии во временной папке: git pull может обновить этот файл, пока он идёт.
if not defined MIGRACIYA_KOPIYA (
  copy /y "%~f0" "%TEMP%\migraciya.bat" >nul
  set "MIGRACIYA_KOPIYA=%~dp0"
  "%TEMP%\migraciya.bat" %*
)
rem Метку снять до setlocal (она не останется в окне cmd), папку tools запомнить в TOOLS.
set "MIGRACIYA_KOPIYA=" & setlocal & set "TOOLS=%MIGRACIYA_KOPIYA%"

rem Данные. Корень — папка, где лежат все четыре репозитория.
for %%p in ("%TOOLS%..\..") do set "KOREN=%%~fp"
set "II=%KOREN%\ii-komanda"
set "PROBA=%II%\komanda\migraciya\proba.md"
set "REPOZITORII=ii-komanda drakon-graf teacher-workpad memory_maryam_ai"

call :proverit_papki || goto konec
for %%r in (%REPOZITORII%) do call :obnovit "%%r" || goto konec
call :shag "Проба" || goto konec
call :sverit || goto konec
call :shag "Перенос" --sdelat || goto konec
call :shag "Проверка" --proverit || goto konec
for %%r in (%REPOZITORII%) do call :otpravit "%%r" || goto konec
echo.
echo Миграция сделана и отправлена во все четыре репозитория.
:konec
endlocal
pause
exit /b

rem proverit_papki: все четыре репозитория рядом; нет memory_maryam_ai — подсказать, как склонировать
:proverit_papki
set "NET="
for %%r in (%REPOZITORII%) do if not exist "%KOREN%\%%r\.git" set "NET=%%r"
if not defined NET exit /b 0
echo Нет папки %KOREN%\%NET% (или это не репозиторий git).
if "%NET%"=="memory_maryam_ai" echo Склонируй: cd /d "%KOREN%" ^&^& git clone https://github.com/Scatik146/memory_maryam_ai
exit /b 1

rem obnovit: подтянуть свежую версию репозитория (проба должна видеть всё, что уже в GitHub)
:obnovit
echo Обновляю %~1 ...
git -C "%KOREN%\%~1" pull --rebase
if errorlevel 1 (echo Не обновилось: %~1 — напиши Марьям, что сказал git.& exit /b 1)
exit /b 0

rem shag: один запуск migraciya.py с ключом; упал — стоп
:shag
echo.
echo === %~1 ===
pushd "%II%"
python tools\migraciya.py %2
set "KOD=%errorlevel%"
popd
if not "%KOD%"=="0" (echo %~1 остановился — дальше не иду. Перешли Марьям то, что выше.& exit /b 1)
exit /b 0

rem sverit: открыть proba.md и ждать решения учителя: 1 — переносить, 2 — стоп
:sverit
start "" notepad "%PROBA%"
echo.
echo Сверь proba.md (открыт в Блокноте): битых 0, руками 0, числа как в последней записке Марьям.
choice /c 12 /n /m "1 — переносить, 2 — стоп: "
if errorlevel 2 (echo Стоп. Ничего не перенесено.& exit /b 1)
exit /b 0

rem otpravit: push одного репозитория; отклонён — догнать и отправить ещё раз
:otpravit
echo Отправляю %~1 ...
git -C "%KOREN%\%~1" push
if not errorlevel 1 exit /b 0
git -C "%KOREN%\%~1" pull --rebase
git -C "%KOREN%\%~1" push
if errorlevel 1 (echo Не отправилось: %~1 — напиши Марьям, что сказал git.& exit /b 1)
exit /b 0
