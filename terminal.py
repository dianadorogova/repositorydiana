from funkcijas import (
    add_user,
    get_jautajumi,
    get_variants,
    save_atbilde,
    get_valstis,
    get_rezultati,
    rekinat_rezultatu,
    save_rezultats,
)

while True:
    print("\nCELOJUMU TESTS")
    print("1 - Sak testu")
    print("2 - Paradit visas valstis")
    print("3 - Paradit rezultatus")
    print("0 - Izeja")

    choise = input("Izvele:")

    if choise == "1":
        name = input("Tavs vards:")
        surname = input("Tavs uzvards:")
        lietotaja_id = add_user(name, surname)
        print("Lietotajs izveidots. ID:", lietotaja_id)

        print("\nAtbildi ar varianta numuru (1-3)!")

        for jautajums in get_jautajumi():
            print("\n" + jautajums[1])

            # paradam variantus ar numuriem 1, 2, 3
            varianti = get_variants(jautajums[0])
            numurs = 0

            for variants in varianti:
                numurs = numurs + 1
                print(str(numurs) + ". " + variants[1])

            skaitlis = int(input("Tava atbilde:"))
            variants_id = varianti[skaitlis - 1][0]

            save_atbilde(lietotaja_id, jautajums[0], variants_id)
1
        # saskaita un saglaba rezultatu
        valsts_id, valsts_nosaukums, punkti, sezona = rekinat_rezultatu(lietotaja_id)
        save_rezultats(lietotaja_id, valsts_id, punkti)

        print("\nTev vispiemerotaka valsts ir:", valsts_nosaukums)
        print("Labakais laiks celet:", sezona)
        print("Punkti:", punkti)

    elif choise == "2":
        print("\nValstu saraksts:")
        for valsts in get_valstis():
            print(valsts)

    elif choise == "3":
        print("\nRezultatu saraksts:")
        for rezultats in get_rezultati():
            print(rezultats)

    if choise == "0":
        break