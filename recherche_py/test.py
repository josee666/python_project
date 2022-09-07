


chif =[1,2,3,4,5]

lettre = ['a', 'b', 'c']

for i in chif:
    print(i)

    try:
        for y in lettre:
            print(y)
            if y == 'b':
                raise Exception
    except:
        continue
