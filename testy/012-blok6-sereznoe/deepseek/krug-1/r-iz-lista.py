# Число R по числу N
# Ввод
n = int(input())
# Шестнадцатеричная запись
m = n
h = ''
while m > 0:
    h = '0123456789ABCDEF'[m % 16] + h
    m = m // 16
# Подсчёт цифр B
k = 0
for c in h:
    if c == 'B':
        k = k + 1
    else:
        k = k
# Дописать единицу
if k % 2 == 0:
    h = '1' + h
elif k % 2 == 1:
    h = h + '1'
print(int(h, 16))
