# Сервер команды (Windows): проверка шагов 1–4, вход по SSH (шаг 12), адрес (шаг 13).
# Запуск: Пуск → PowerShell → правой кнопкой «Запуск от имени администратора», одна строка:
#   irm https://raw.githubusercontent.com/Scatik146/ii-komanda/main/tools/server-windows.ps1 | iex
# Настройки сети и сна скрипт НЕ меняет — только показывает. Меняет одно: ставит и запускает OpenSSH-сервер.

function Stroka($imya, $znachenie) { "{0,-16} {1}" -f $imya, $znachenie }

function Windows-Versiya {             # шаг 1: нужна сборка 19041+
  $v = Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion'
  Stroka "Windows" "$($v.DisplayVersion) сборка $($v.CurrentBuild)"
}

function Virtualizaciya {              # шаг 2: при работающем WSL2 бывает «False» — это нормально
  $cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
  Stroka "Виртуализация" $cpu.VirtualizationFirmwareEnabled
}

function Set-Profil {                  # шаг 3: должно быть Private
  Get-NetConnectionProfile | ForEach-Object { Stroka "Сеть" "$($_.Name): $($_.NetworkCategory)" }
}

function Son {                         # шаг 4: должно быть 0 (никогда)
  $s = powercfg /query SCHEME_CURRENT SUB_SLEEP STANDBYIDLE | Select-String 'переменного тока|AC Power'
  Stroka "Сон (от сети)" "$($s -replace '.*:\s*','') (0x00000000 = никогда)"
}

function Ssh-Postavit {                # шаг 12
  $cap = Get-WindowsCapability -Online -Name 'OpenSSH.Server*'
  if ($cap.State -ne 'Installed') { Add-WindowsCapability -Online -Name $cap.Name | Out-Null }
  Set-Service -Name sshd -StartupType Automatic
  Start-Service sshd
  Stroka "sshd" "$((Get-Service sshd).Status), автозапуск"
}

function Adres {                       # шаг 13: адрес — только в чат Марьям, не в репозиторий
  Get-NetIPAddress -AddressFamily IPv4 -PrefixOrigin Dhcp,Manual -ErrorAction SilentlyContinue |
    Where-Object { $_.IPAddress -notlike '169.*' -and $_.IPAddress -ne '127.0.0.1' } |
    ForEach-Object { Stroka "IPv4" "$($_.IPAddress) ($($_.InterfaceAlias))" }
  Stroka "Пользователь" $env:USERNAME
}

"=== Для Марьям (Windows) ==="
Windows-Versiya
Virtualizaciya
Set-Profil
Son
Ssh-Postavit
Adres
"=== конец: скопируйте всё между строками === в чат Марьям ==="
