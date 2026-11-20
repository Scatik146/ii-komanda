# Проверка: «срабатывает» на паре (признак, ответ) = ворота(признак) ∧ возможно(ответ).
# Триты: -1 нет, 0 не знаю, 1 да. И = min (как в книге).
T = (-1, 0, 1)
def vorota(x):   return 1 if x == 1 else -1
def vozmozhno(x): return -1 if x == -1 else 1
def i(a, b):     return min(a, b)

def razresheno(p, o):          # признак не 1 -> ответ только 0
    return p == 1 or o == 0

def zhdem(p, o):               # таблица смыслов: запускается ли правило
    return 1 if p == 1 and o != -1 else -1

oshibki = 0
for p in T:
    for o in T:
        if not razresheno(p, o):
            print(f"({p:2},{o:2}) запрещено")
            continue
        f = i(vorota(p), vozmozhno(o))
        ok = f == zhdem(p, o)
        oshibki += not ok
        print(f"({p:2},{o:2}) формула {f:2}  таблица {zhdem(p, o):2}  {'верно' if ok else 'ОШИБКА'}")
print("всё верно" if oshibki == 0 else f"ошибок: {oshibki}")
