# Есть ли цифра в пароле
parol = input()
naydeno = False
for simvol in parol:
    if simvol.isdigit():
        naydeno = True
    else:
        pass
print(naydeno)
