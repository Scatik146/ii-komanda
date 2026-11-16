@echo off
chcp 65001 >nul
rem analiz: кандидаты в словари одной командой — отправить материалы урока, разметить другой моделью, спросить учителя, отправить итог
rem   из папки ii-komanda:  tools\analiz.bat <папка урока>
rem   пример:               tools\analiz.bat ..\teacher-workpad\chernoviki\9-rech
rem   проба на опросе 16.11: tools\analiz.bat forto-prolog\srez-1
rem   разметчик GLM, ответ из чата файлом: tools\analiz.bat <папка урока> --podstavit otvet-glm.md --model glm
rem Запускается дважды. Первый раз кандидатов ещё нет: материалы уходят в GitHub, дальше работает Марьям.
rem Второй раз, когда Марьям положила кандидатов: разметка, очередь вопросов в Блокноте, отправка.
rem Код по-фортовски: слова — метки, над каждой строка «слово: что делает»; ДРАКОН-лист — analiz-list.md
rem Работаем с копии во временной папке: git pull может обновить этот файл, пока он идёт.
if not defined ANALIZ_KOPIYA (
  copy /y "%~f0" "%TEMP%\analiz.bat" >nul
  set "ANALIZ_KOPIYA=%~dp0"
  "%TEMP%\analiz.bat" %*
)
rem Метку снять до setlocal (она не останется в окне cmd), папку tools запомнить в TOOLS.
set "ANALIZ_KOPIYA=" & setlocal & set "TOOLS=%ANALIZ_KOPIYA%"

rem Данные. Папки и файлы; DOP — добавки для analiz.py (--podstavit, --model).
for %%p in ("%TOOLS%..") do set "II=%%~fp"
for %%p in ("%~1") do set "UROK=%%~fp"
for %%p in ("%~1") do set "UROK_IMYA=%%~nxp"
set "KANDIDATY=%UROK%\analiz\kandidaty.md"
set "OCHERED=%UROK%\analiz\ochered-uchitelyu.md"
set "DOP=%2 %3 %4 %5"

call :proverit_vhod "%~1" || goto konec
call :obnovit "%II%" || goto konec
call :sobrat_material || goto konec
call :obnovit "%UROK%" || goto konec
call :otpravit || goto konec
call :est_kandidaty || goto konec
call :razmetit || goto konec
call :sprosit_uchitelya
call :sobrat_itog || goto konec
call :otpravit
:konec
endlocal
exit /b

rem proverit_vhod: папка урока названа и существует
:proverit_vhod
if "%~1"=="" (echo Как запускать: tools\analiz.bat ^<папка урока^>, например: tools\analiz.bat forto-prolog\srez-1& exit /b 1)
if not exist "%UROK%\" (echo Нет папки: %UROK%& exit /b 1)
echo Урок: %UROK%
exit /b 0

rem obnovit: подтянуть свежую версию репозитория; свои незаписанные правки git на время прячет сам
:obnovit
echo Обновляю %~nx1 ...
git -C "%~1" pull --rebase --autostash
if errorlevel 1 (echo Не обновилось: %~1 — напиши Марьям, что сказал git.& exit /b 1)
exit /b 0

rem sobrat_material: новое в папке урока записать в git; чаты уходят в открытый репозиторий — спросить учителя
:sobrat_material
git -C "%UROK%" add -A .
git -C "%UROK%" diff --cached --quiet -- .
if not errorlevel 1 exit /b 0
git -C "%UROK%" status --short .
choice /c YN /m "Эти файлы уйдут в открытый репозиторий. Чаты просмотрены на имена учеников и личное? Y - да, N - нет"
if errorlevel 2 (git -C "%UROK%" reset -q -- . & echo Ничего не отправлено. Просмотри чаты и запусти ещё раз.& exit /b 1)
git -C "%UROK%" commit -q -m "Анализ: материалы урока %UROK_IMYA%" -- .
exit /b 0

rem otpravit: записанное — в GitHub
:otpravit
git -C "%UROK%" push
if errorlevel 1 call :dogon
exit /b

rem dogon: push отклонён — подтянуть чужие коммиты и отправить ещё раз
:dogon
git -C "%UROK%" pull --rebase --autostash
git -C "%UROK%" push
if errorlevel 1 (echo Не отправилось — напиши Марьям, что сказал git.& exit /b 1)
exit /b 0

rem est_kandidaty: кандидаты уже лежат? Нет — первый запуск закончен, дальше работает Марьям
:est_kandidaty
if exist "%KANDIDATY%" exit /b 0
echo.
echo Материалы урока в GitHub. Кандидатов ещё нет: их кладёт Марьям.
echo Напиши ей в чате: «урок готов» и путь к папке урока.
echo Когда она ответит — запусти эту же команду ещё раз.
exit /b 1

rem razmetit: проверка цитат, разметка другой моделью, очередь учителю — команда ii.py analiz
:razmetit
pushd "%II%"
python tools\ii.py analiz "%UROK%" %DOP%
set "KOD=%errorlevel%"
popd
if not "%KOD%"=="0" (echo Разметка остановилась. Напиши Марьям, что сказал скрипт.& exit /b 1)
exit /b 0

rem sprosit_uchitelya: очередь вопросов — в Блокнот; ждать, пока учитель ответит и сохранит
:sprosit_uchitelya
start "" notepad "%OCHERED%"
echo.
echo В Блокноте открыта очередь вопросов. Ответь после слов «ответ:» и сохрани файл.
echo Потом нажми здесь любую клавишу — ответы уйдут в GitHub.
pause >nul
exit /b 0

rem sobrat_itog: разметку и ответы учителя записать в git; нового нет — отправлять нечего
:sobrat_itog
git -C "%UROK%" add -A analiz
git -C "%UROK%" diff --cached --quiet -- analiz
if not errorlevel 1 (echo Нового нет — отправлять нечего.& exit /b 1)
git -C "%UROK%" commit -q -m "Анализ: разметка и ответы учителя, %UROK_IMYA%" -- analiz
exit /b 0
