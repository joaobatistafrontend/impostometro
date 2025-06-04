idade = int(input('idade: '))

if idade >= 6 and idade <= 12:
    print(f'gasto diario de internet: 3g')
    print(f'gasto semanal de internet: 15g')
    print(f'gasto mensal de internet: 60g')

elif idade >= 13 and idade <= 17:
    print(f'gasto diario de internet: 4g')
    print(f'gasto semanal de internet: 28g')
    print(f'gasto mensal de internet: 112g')

elif idade >= 18 and idade <= 24:
    print(f'gasto diario de internet: 4g')
    print(f'gasto semanal de internet: 21g')
    print(f'gasto mensal de internet: 100g')

elif idade >= 25 and idade <= 34:
    print(f'gasto diario de internet: 3g')
    print(f'gasto semanal de internet: 21g')
    print(f'gasto mensal de internet: 84g')

elif idade >= 35 and idade <= 49:
    print(f'gasto diario de internet: 3g')
    print(f'gasto semanal de internet: 17g')
    print(f'gasto mensal de internet: 60g')

elif idade >= 50 and idade <= 64:
    print(f'gasto diario de internet: 2g')
    print(f'gasto semanal de internet: 7g')
    print(f'gasto mensal de internet: 28g')

elif idade > 64:
    print(f'gasto diario de internet: 1g')
    print(f'gasto semanal de internet: 7g')
    print(f'gasto mensal de internet: 28g')
