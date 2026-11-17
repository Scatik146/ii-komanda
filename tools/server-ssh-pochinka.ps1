# Сервер команды (Windows): замена сломанного OpenSSH-сервера из «компонентов Windows»
# на сборку Microsoft из winget (C:\Program Files\OpenSSH).
# Причина (17.11): sshd.exe из System32 падает с кодом -1073741511 (0xC0000139, не найдена точка входа в DLL).
# Запуск: PowerShell «от имени администратора», одна строка:
#   irm https://raw.githubusercontent.com/Scatik146/ii-komanda/main/tools/server-ssh-pochinka.ps1 | iex

function Stroka($imya, $znachenie) { "{0,-14} {1}" -f $imya, $znachenie }

function Staryj-Ubrat {                # сломанный компонент Windows
  Stop-Service sshd -ErrorAction SilentlyContinue
  $cap = Get-WindowsCapability -Online -Name 'OpenSSH.Server*'
  if ($cap.State -eq 'Installed') { Remove-WindowsCapability -Online -Name $cap.Name | Out-Null }
  Stroka "старый sshd" "убран"
}

function Novyj-Postavit {              # сборка Microsoft через winget
  if (-not (Get-Command winget -ErrorAction SilentlyContinue)) { Write-Host (Stroka "winget" "НЕТ — стоп, вопрос к Марьям"); return $false }
  winget install --id Microsoft.OpenSSH.Preview -e --silent --accept-source-agreements --accept-package-agreements | Out-Null
  $est = Test-Path 'C:\Program Files\OpenSSH\sshd.exe'
  Write-Host (Stroka "новый sshd" $est)
  return $est
}

function Sluzhba-Zapustit {
  Set-Service -Name sshd -StartupType Automatic
  Start-Service sshd
  Stroka "sshd" "$((Get-Service sshd).Status), автозапуск"
}

function Brandmauer {                  # порт 22 для домашней (частной) сети
  if (-not (Get-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -ErrorAction SilentlyContinue)) {
    New-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -DisplayName 'OpenSSH Server (sshd)' -Enabled True `
      -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22 -Profile Private | Out-Null
  }
  Stroka "брандмауэр" "порт 22 открыт (частная сеть)"
}

"=== Для Марьям (SSH) ==="
Staryj-Ubrat
if (Novyj-Postavit) {
  Sluzhba-Zapustit
  Brandmauer
  Stroka "версия" ((& 'C:\Program Files\OpenSSH\sshd.exe' -V) 2>&1 | Select-Object -First 1)
}
"=== конец ==="
