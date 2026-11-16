# Ceļojumu tests

Šis ir ceļojumu ieteikšanas projekts. Programma palīdz lietotājam atrast piemērotāko ceļojuma valsti atkarībā no viņa interesēm. Lietotājs aizpilda testu ar jautājumiem, programma aprēķina punktus un iesaka valsti, kā arī labāko ceļošanas sezonu.

## Izmantotās tehnoloģijas

- Python 3
- SQLite (datubāze)
- SQL
- Tkinter (grafiskā saskarne)
- Pillow (attēliem, neobligāti)

## Projekta faili

```
celojumu-tests/
├── main.py          # izveido datubāzi, tabulas un sākotnējos datus
├── app.py           # grafiskā lietotāja saskarne
├── funkcijas.py     # funkcijas darbam ar datubāzi
├── terminal.py      # programmas izmantošana terminālī
├── celojumi.db      # datubāzes fails
└── atteli/          # mape ar valstu attēliem
    ├── baneris.png
    ├── italija.png
    └── ...
```

- **main.py** — izveido datubāzi celojumi.db, 10 tabulas un ievieto sākotnējos datus
- **app.py** — Tkinter grafiskā saskarne ar cilnēm: Tests, Rezultāti, tabulu skati un Admin
- **funkcijas.py** — funkcijas datubāzes darbam un rezultātu aprēķināšanai (add_user, save_atbilde, rekinat_rezultatu, add_valsts, add_jautajums u.c.)
- **terminal.py** — vienkāršota versija terminālim ar izvēlni (1 — sākt testu, 2 — valstis, 3 — rezultāti, 0 — izeja)
- **celojumi.db** — SQLite datubāzes fails, ko izveido main.py

## Datubāzes struktūra

Datubāzē ir 10 tabulas:

1. **lietotaji** — lietotāji, kas veic testu (vārds, uzvārds)
2. **kategorijas** — intereses kategorijas (Pludmale, Pilsēta, Kalni, Vēsture, Piedzīvojumi)
3. **jautajumi** — testa jautājumi
4. **atbilzu_varianti** — 3 atbilžu varianti katram jautājumam (teksts, punkti, kategorija)
5. **atbildes** — lietotāja atbildes
6. **valstis** — valstis (nosaukums, kontinents, apraksts)
7. **valstu_kategorijas** — cik stipra katra valsts ir katrā kategorijā
8. **sezonas** — gadalaiki (Vasara, Ziema, Pavasaris, Rudens)
9. **valstu_sezonas** — labākais ceļošanas laiks katrai valstij
10. **rezultati** — testu rezultāti (lietotājs, valsts, punkti, datums)

Tabulas ir savienotas ar FOREIGN KEY:

- atbildes → lietotaji, jautajumi, atbilzu_varianti
- atbilzu_varianti → jautajumi, kategorijas
- valstu_kategorijas → valstis, kategorijas
- valstu_sezonas → valstis, sezonas
- rezultati → lietotaji, valstis

## Kā palaist

Vispirms vajag Python 3. Pēc tam terminālī:

1. (Neobligāti) Instalē Pillow, ja grib attēlus:

   ```
   pip install pillow
   ```

   Bez Pillow programma darbosies, tikai attēli neparādīsies.

2. Izveido datubāzi (palaiž vienreiz):

   ```
   python main.py
   ```

3. Palaid programmu:

   ```
   python app.py
   ```

   vai termināla versiju:

   ```
   python terminal.py
   ```

## Programmas darbība

1. Lietotājs ievada vārdu un uzvārdu (saglabājas tabulā lietotaji).
2. Atbild uz 7 jautājumiem, izvēlas varianta numuru (1, 2 vai 3).
3. Programma saskaita punktus katrā no 5 kategorijām.
4. Tiek aprēķināts kopskaitlis katrai valstij:

   ```
   valsts_punkti = SUM(valsts_kategorijas_punkti * lietotaja_kategorijas_punkti)
   ```

   Valsts ar augstāko kopskaitli tiek izvēlēta.
5. Lietotājs redz ieteikumu — valsti un labāko sezonu.
6. Rezultāts saglabājas tabulā rezultati ar datumu.

## Admin funkcijas

Admin cilnē var tieši pievienot jaunus datus datubāzei. Tie uzreiz parādās arī citās cilnēs.

**Pievienot jaunu valsti:**

- Ievada nosaukumu (piem., "Spānija")
- Ievada kontinentu (piem., "Eiropa")
- Ievada aprakstu
- Poga "Saglabāt valsti" ievieto valsti tabulā valstis

Ja grib, lai jaunajai valstij rādās attēls, jāpievieno PNG fails atteli/ mapē ar nosaukumu mazajiem burtiem bez diakritiskajām zīmēm (piem., "Spānija" → atteli/spanija.png).

**Pievienot jaunu jautājumu:**

- Ievada jautājuma tekstu
- Ievada 3 variantus (katram tekstu, kategoriju un punktus)
- Poga "Saglabāt jautājumu" ievieto jautājumu un visus variantus datubāzē


## Sākotnējie dati

Pēc main.py palaišanas datubāzē ir:

- 5 kategorijas: Pludmale, Pilsēta, Kalni, Vēsture, Piedzīvojumi
- 7 jautājumi ar 21 atbilžu variantiem
- 7 valstis: Itālija, Japāna, Nepāla, Ēģipte, Brazīlija, Šveice, Grieķija
- 4 sezonas: Vasara, Ziema, Pavasaris, Rudens

## Iespējamie uzlabojumi

- Pievienot attēlus visām valstīm
- Atļaut vairākas sezonas vienai valstij
- Pievienot iespēju dzēst vai rediģēt datus
