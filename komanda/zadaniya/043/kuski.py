# kuski.py - режет diff части 2 на куски «было → стало» (по-фортовски)
import subprocess, re, sys

import os
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
BAZA = "7db768a"
KONEC = "2058881"  # последний коммит с правками (старт a30)
PAPKA = "logika/kniga/chast-2-trit/"

# diff_tekst: diff без контекста
def diff_tekst():
    return subprocess.run(["git", "-C", REPO, "diff", "-U0", BAZA, KONEC, "--", PAPKA],
                          capture_output=True, text=True).stdout

# fajl_novyj: строки файла в HEAD
def fajl_novyj(put):
    t = subprocess.run(["git", "-C", REPO, "show", KONEC + ":" + put], capture_output=True, text=True).stdout
    return t.split("\n")

# zagolovok_nad: ближайший заголовок ### или ## выше строки n
def zagolovok_nad(stroki, n):
    for i in range(min(n, len(stroki)) - 1, -1, -1):
        m = re.match(r"^\*\*Правило \d+\. (.*)\*\*$", stroki[i])
        if m:
            nomer = sum(1 for x in stroki[:i + 1] if x.startswith("**Правило "))
            return f"правило {nomer} - «{m.group(1)}»"
        if re.match(r"^#{2,4} ", stroki[i]):
            return stroki[i].lstrip("# ").strip()
    return "(начало файла)"

# kuski: список (файл, строка, заголовок, было, стало)
def kuski():
    res, put, stroki, tek = [], None, [], None
    for s in diff_tekst().split("\n"):
        if s.startswith("+++ b/"):
            put = s[6:]; stroki = fajl_novyj(put)
        elif s.startswith("@@"):
            n = int(re.search(r"\+(\d+)", s).group(1))
            tek = [put, n, zagolovok_nad(stroki, n), [], []]; res.append(tek)
        elif tek and s.startswith("-") and not s.startswith("---"):
            tek[3].append(s[1:])
        elif tek and s.startswith("+") and not s.startswith("+++"):
            tek[4].append(s[1:])
    return res

if __name__ == "__main__":
    for i, (put, n, z, b, st) in enumerate(kuski(), 1):
        print(f"=== {i} | {put.split('/')[-1]}:{n} | {z}")
        for x in b: print("- " + x)
        for x in st: print("+ " + x)
