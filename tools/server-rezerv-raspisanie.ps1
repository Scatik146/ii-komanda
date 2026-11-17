# Сервер команды (Windows): резерв репозиториев по расписанию — каждый день в 03:00 и при входе в Windows.
# Запускает в WSL tools/server-rezerv.sh. Работает, пока пользователь Windows вошёл в систему (сервер не выходит из учётной записи).
# Запуск: PowerShell «от имени администратора», одна строка:
#   irm https://raw.githubusercontent.com/Scatik146/ii-komanda/main/tools/server-rezerv-raspisanie.ps1 | iex

$IMYA = "ii-komanda rezerv"

function Stroka($imya, $znachenie) { "{0,-12} {1}" -f $imya, $znachenie }

function Zadacha-Sozdat {
  $dejstvie = New-ScheduledTaskAction -Execute "wsl.exe" -Argument '-e bash -lc "bash ~/ii-komanda/tools/server-rezerv.sh"'
  $kogda    = @( (New-ScheduledTaskTrigger -Daily -At 3am), (New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME) )
  $nastrojki = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun -ExecutionTimeLimit (New-TimeSpan -Hours 2)
  Register-ScheduledTask -TaskName $IMYA -Action $dejstvie -Trigger $kogda -Settings $nastrojki -User $env:USERNAME -Force | Out-Null
  Stroka "задача" "$IMYA — создана (03:00 и при входе)"
}

function Zadacha-Proverit {          # один запуск сейчас
  Start-ScheduledTask -TaskName $IMYA
  Start-Sleep -Seconds 5
  Stroka "состояние" (Get-ScheduledTask -TaskName $IMYA).State
}

"=== Для Марьям (расписание) ==="
Zadacha-Sozdat
Zadacha-Proverit
"=== конец ==="
