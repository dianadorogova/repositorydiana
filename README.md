Projekts ir ceļojumu ieteikšanas sistēma
Tas palīdz lietotājam atrast piemērotāko ceļojuma valsti, balstoties uz viņa interesēm un vēlmēm.
Lietotājs aizpilda testu ar pieciem jautājumiem, un programma, aprēķinot iegūtos punktus, iesaka piemērotāko valsti un labāko ceļošanas sezonu.
_______________________________________________________________
Izmantoju: Python, SQLite, SQL, Tkinter
_______________________________________________________________
Projekta faili
main.py – izveido datubāzi, tabulas un ievieto sākotnējos datus.
app.py – nodrošina grafisko lietotāja saskarni.
funkcijas.py – satur funkcijas darbam ar datubāzi un rezultātu aprēķināšanu.
terminal.py – nodrošina programmas izmantošanu terminālī.
celojumi.db – datubāzes fails.
_______________________________________________________________
Datubāzē ir 10 tabulas:
lietotaji
kategorijas
jautajumi
atbilzu_varianti
atbildes
valstis
valstu_kategorijas
sezonas
valstu_sezonas
rezultati
_______________________________________________________________
Programmas darbība:
Lietotājs ievada vārdu un uzvārdu.
Atbild uz pieciem jautājumiem.
Programma aprēķina punktus katrā kategorijā.
Tiek noteikta piemērotākā valsts.
Lietotājs saņem ieteikumu un labāko ceļošanas sezonu.
Rezultāts tiek saglabāts datubāzē.
_______________________________________________________________
izlabot: pievienot funkciju "pievienot jaunu valsti"
pievienot attelu ikonas vietas
