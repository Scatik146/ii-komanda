@echo off
chcp 65001 >nul
rem test-zapusk: тест навыка одной командой — обновить репозитории, запустить задание, отправить итог
rem   из папки ii-komanda:  tools\test-zapusk.bat <задание> <модель>
rem   задание — номер или имя файла без .md: 011 или 011-blok6-prostoe
rem   модель — alisa, deepseek или glm; для glm ответ GLM лежит в ii-komanda\otvet-glm.md
rem   ручные вопросы скрипта test_koda.py задаёт сам — отвечать по ходу
rem Код по-фортовски: слова — метки, над каждой строка «слово: что делает»; ДРАКОН-лист — test-zapusk-list.md
setlocal

rem Данные. Папки и файлы (teacher-workpad — рядом с ii-komanda).
for %%p in ("%~dp0..") do set "II=%%~fp"
for %%p in ("%~dp0..\..\teacher-workpad") do set "TW=%%~fp"
set "ZADANIYA=%TW%\docs\komanda\zadaniya"
set "OTVET_GLM=%II%\otvet-glm.md"
set "MODEL=%~2"

call :najti_zadanie "%~1" || goto konec
call :proverit_otvet || goto konec
call :obnovit "%II%" || goto konec
call :obnovit "%TW%" || goto konec
call :zapustit || goto konec
call :otpravit
:konec
endlocal
exit /b

rem najti_zadanie: по номеру или имени задания найти файл; IMYA — имя файла без .md
:najti_zadanie
set "IMYA="
if not "%~1"=="" if not "%MODEL%"=="" for %%f in ("%ZADANIYA%\%~1*.md") do set "IMYA=%%~nf"
if not defined IMYA (echo Как запускать: tools\test-zapusk.bat ^<задание^> ^<модель^>, например: tools\test-zapusk.bat 011 alisa& exit /b 1)
echo Задание: %IMYA%, модель: %MODEL%
exit /b 0

rem proverit_otvet: для glm — файл ответа есть и без следов копирования
:proverit_otvet
if /i not "%MODEL%"=="glm" exit /b 0
if not exist "%OTVET_GLM%" (echo Нет файла otvet-glm.md в папке ii-komanda — сохрани туда ответ GLM.& exit /b 1)
python "%II%\tools\chistyj_otvet.py" "%OTVET_GLM%"
if errorlevel 1 (echo Скопируй ответ GLM заново и сохрани в otvet-glm.md, потом запусти ещё раз.& exit /b 1)
exit /b 0

rem obnovit: подтянуть свежую версию репозитория
:obnovit
echo Обновляю %~nx1 ...
git -C "%~1" pull --rebase
if errorlevel 1 (echo Не обновилось: %~1 — напиши Марьям, что сказал git.& exit /b 1)
exit /b 0

rem zapustit: прогнать задание через test_koda.py; для glm — с подставленным ответом; остановка — ничего не отправлять
:zapustit
set "PODSTAVIT="
if /i "%MODEL%"=="glm" set "PODSTAVIT=--podstavit "%OTVET_GLM%""
pushd "%II%"
python tools\test_koda.py "%ZADANIYA%\%IMYA%.md" --model %MODEL% %PODSTAVIT%
set "KOD=%errorlevel%"
popd
if not "%KOD%"=="0" (echo Тест остановился — итог не отправляю. Запусти эту же команду ещё раз.& exit /b 1)
exit /b 0

rem otpravit: итог теста — в GitHub; новых итогов нет — ничего не отправлять
:otpravit
git -C "%II%" add testy
git -C "%II%" diff --cached --quiet
if not errorlevel 1 (echo Новых итогов нет — отправлять нечего.& exit /b 0)
git -C "%II%" commit -q -m "Тест навыка: %IMYA% · %MODEL%"
git -C "%II%" push
if errorlevel 1 call :dogon
exit /b 0

rem dogon: push отклонён — подтянуть чужие коммиты и отправить ещё раз
:dogon
git -C "%II%" pull --rebase
git -C "%II%" push
if errorlevel 1 (echo Не отправилось — напиши Марьям, что сказал git.& exit /b 1)
exit /b 0
