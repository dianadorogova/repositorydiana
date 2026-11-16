import sqlite3

database = sqlite3.connect("celojumi.db")
cursor = database.cursor()

# 1. table - lietotaji (users who take the test)
cursor.execute("""CREATE TABLE IF NOT EXISTS lietotaji(
               lietotajs_id INTEGER PRIMARY KEY,
               vards TEXT NOT NULL,
               uzvards TEXT NOT NULL)
""")

# 2. table - kategorijas (beach, city, mountains...)
cursor.execute("""CREATE TABLE IF NOT EXISTS kategorijas(
               kategorija_id INTEGER PRIMARY KEY,
               nosaukums TEXT NOT NULL)
""")

# 3. table - jautajumi
cursor.execute("""CREATE TABLE IF NOT EXISTS jautajumi(
               jautajuma_id INTEGER PRIMARY KEY,
               teksts TEXT NOT NULL)
""")

# 4. table - atbilzu varianti (3 variants per question)
cursor.execute("""CREATE TABLE IF NOT EXISTS atbilzu_varianti(
               variants_id INTEGER PRIMARY KEY,
               jautajuma_id INTEGER NOT NULL,
               teksts TEXT NOT NULL,
               punkti INTEGER NOT NULL,
               kategorija_id INTEGER NOT NULL,

               FOREIGN KEY (jautajuma_id)
                    REFERENCES jautajumi(jautajuma_id),

               FOREIGN KEY (kategorija_id)
                    REFERENCES kategorijas(kategorija_id)
               )
""")

# 5. table - atbildes (what the user answered)
cursor.execute("""CREATE TABLE IF NOT EXISTS atbildes(
               atbilde_id INTEGER PRIMARY KEY,
               lietotajs_id INTEGER NOT NULL,
               jautajuma_id INTEGER NOT NULL,
               variants_id INTEGER NOT NULL,

               FOREIGN KEY (lietotajs_id)
                    REFERENCES lietotaji(lietotajs_id),

               FOREIGN KEY (jautajuma_id)
                    REFERENCES jautajumi(jautajuma_id),

               FOREIGN KEY (variants_id)
                    REFERENCES atbilzu_varianti(variants_id)
               )
""")

# 6. table - valstis
cursor.execute("""CREATE TABLE IF NOT EXISTS valstis(
               valsts_id INTEGER PRIMARY KEY,
               nosaukums TEXT NOT NULL,
               kontinents TEXT NOT NULL,
               apraksts TEXT NOT NULL)
""")

# 7. table - valstu kategorijas (how strong each country is in each category)
cursor.execute("""CREATE TABLE IF NOT EXISTS valstu_kategorijas(
               id INTEGER PRIMARY KEY,
               valsts_id INTEGER NOT NULL,
               kategorija_id INTEGER NOT NULL,
               punkti INTEGER NOT NULL,

               FOREIGN KEY (valsts_id)
                    REFERENCES valstis(valsts_id),

               FOREIGN KEY (kategorija_id)
                    REFERENCES kategorijas(kategorija_id)
               )
""")

# 8. table - sezonas
cursor.execute("""CREATE TABLE IF NOT EXISTS sezonas(
               sezona_id INTEGER PRIMARY KEY,
               nosaukums TEXT NOT NULL)
""")

# 9. table - valstu sezonas (best travel time)
cursor.execute("""CREATE TABLE IF NOT EXISTS valstu_sezonas(
               id INTEGER PRIMARY KEY,
               valsts_id INTEGER NOT NULL,
               sezona_id INTEGER NOT NULL,

               FOREIGN KEY (valsts_id)
                    REFERENCES valstis(valsts_id),

               FOREIGN KEY (sezona_id)
                    REFERENCES sezonas(sezona_id)
               )
""")

# 10. table - rezultati (test results)
cursor.execute("""CREATE TABLE IF NOT EXISTS rezultati(
               rezultats_id INTEGER PRIMARY KEY,
               lietotajs_id INTEGER NOT NULL,
               valsts_id INTEGER NOT NULL,
               punkti INTEGER NOT NULL,
               datums TEXT NOT NULL,

               FOREIGN KEY (lietotajs_id)
                    REFERENCES lietotaji(lietotajs_id),

               FOREIGN KEY (valsts_id)
                    REFERENCES valstis(valsts_id)
               )
""")

# --- starter data ---

cursor.execute("""INSERT OR IGNORE INTO kategorijas (kategorija_id, nosaukums)
    VALUES (1, 'Pludmale')""")
cursor.execute("""INSERT OR IGNORE INTO kategorijas (kategorija_id, nosaukums)
    VALUES (2, 'Pilsēta')""")
cursor.execute("""INSERT OR IGNORE INTO kategorijas (kategorija_id, nosaukums)
    VALUES (3, 'Kalni')""")
cursor.execute("""INSERT OR IGNORE INTO kategorijas (kategorija_id, nosaukums)
    VALUES (4, 'Vēsture')""")
cursor.execute("""INSERT OR IGNORE INTO kategorijas (kategorija_id, nosaukums)
    VALUES (5, 'Piedzīvojumi')""")

cursor.execute("""INSERT OR IGNORE INTO jautajumi (jautajuma_id, teksts)
    VALUES (1, 'Kā tu vēlētos pavadīt dienu ceļojumā?')""")
cursor.execute("""INSERT OR IGNORE INTO jautajumi (jautajuma_id, teksts)
    VALUES (2, 'Kāds ir tavs iecienītākais ēdiens?')""")
cursor.execute("""INSERT OR IGNORE INTO jautajumi (jautajuma_id, teksts)
    VALUES (3, 'Kā tev patīk atpūsties vakaros?')""")
cursor.execute("""INSERT OR IGNORE INTO jautajumi (jautajuma_id, teksts)
    VALUES (4, 'Kas tev vairāk patīk?')""")
cursor.execute("""INSERT OR IGNORE INTO jautajumi (jautajuma_id, teksts)
    VALUES (5, 'Kādu laiku tu izvēlētos ceļojumam?')""")
cursor.execute("""INSERT OR IGNORE INTO jautajumi (jautajuma_id, teksts)
    VALUES (6, 'Kāda ainava tev liek pasmaidīt?')""")
cursor.execute("""INSERT OR IGNORE INTO jautajumi (jautajuma_id, teksts)
    VALUES (7, 'Ko tu darītu brīvā dienā ceļojumā?')""")

cursor.execute("""INSERT OR IGNORE INTO atbilzu_varianti (variants_id, jautajuma_id, teksts, punkti, kategorija_id)
    VALUES (1, 1, 'Gulēšana pludmalē zem saules', 2, 1)""")
cursor.execute("""INSERT OR IGNORE INTO atbilzu_varianti (variants_id, jautajuma_id, teksts, punkti, kategorija_id)
    VALUES (2, 1, 'Pastaiga pa pilsētu un muzejiem', 2, 2)""")
cursor.execute("""INSERT OR IGNORE INTO atbilzu_varianti (variants_id, jautajuma_id, teksts, punkti, kategorija_id)
    VALUES (3, 1, 'Kāpšana kalnos', 2, 3)""")
cursor.execute("""INSERT OR IGNORE INTO atbilzu_varianti (variants_id, jautajuma_id, teksts, punkti, kategorija_id)
    VALUES (4, 2, 'Jūras veltes', 1, 1)""")
cursor.execute("""INSERT OR IGNORE INTO atbilzu_varianti (variants_id, jautajuma_id, teksts, punkti, kategorija_id)
    VALUES (5, 2, 'Makaroni un pica', 1, 2)""")
cursor.execute("""INSERT OR IGNORE INTO atbilzu_varianti (variants_id, jautajuma_id, teksts, punkti, kategorija_id)
    VALUES (6, 2, 'Grilēta gaļa pie ugunskura', 1, 5)""")
cursor.execute("""INSERT OR IGNORE INTO atbilzu_varianti (variants_id, jautajuma_id, teksts, punkti, kategorija_id)
    VALUES (7, 3, 'Klusums un dabas skaņas', 1, 3)""")
cursor.execute("""INSERT OR IGNORE INTO atbilzu_varianti (variants_id, jautajuma_id, teksts, punkti, kategorija_id)
    VALUES (8, 3, 'Trokšņotas pilsētas ielas', 1, 2)""")
cursor.execute("""INSERT OR IGNORE INTO atbilzu_varianti (variants_id, jautajuma_id, teksts, punkti, kategorija_id)
    VALUES (9, 3, 'Ugunskurs pie jūras', 1, 1)""")
cursor.execute("""INSERT OR IGNORE INTO atbilzu_varianti (variants_id, jautajuma_id, teksts, punkti, kategorija_id)
    VALUES (10, 4, 'Sena vēsture un celtnes', 2, 4)""")
cursor.execute("""INSERT OR IGNORE INTO atbilzu_varianti (variants_id, jautajuma_id, teksts, punkti, kategorija_id)
    VALUES (11, 4, 'Ekstrēmi sporta veidi', 2, 5)""")
cursor.execute("""INSERT OR IGNORE INTO atbilzu_varianti (variants_id, jautajuma_id, teksts, punkti, kategorija_id)
    VALUES (12, 4, 'Peldēšanās un saule', 2, 1)""")
cursor.execute("""INSERT OR IGNORE INTO atbilzu_varianti (variants_id, jautajuma_id, teksts, punkti, kategorija_id)
    VALUES (13, 5, 'Silts vasaras laiks', 1, 1)""")
cursor.execute("""INSERT OR IGNORE INTO atbilzu_varianti (variants_id, jautajuma_id, teksts, punkti, kategorija_id)
    VALUES (14, 5, 'Ziema un sniegs', 1, 3)""")
cursor.execute("""INSERT OR IGNORE INTO atbilzu_varianti (variants_id, jautajuma_id, teksts, punkti, kategorija_id)
    VALUES (15, 5, 'Pavasaris pilsētā', 1, 2)""")
cursor.execute("""INSERT OR IGNORE INTO atbilzu_varianti (variants_id, jautajuma_id, teksts, punkti, kategorija_id)
    VALUES (16, 6, 'Tirkīzzila jūra un baltas smiltis', 2, 1)""")
cursor.execute("""INSERT OR IGNORE INTO atbilzu_varianti (variants_id, jautajuma_id, teksts, punkti, kategorija_id)
    VALUES (17, 6, 'Mirdzošas pilsētas gaismas', 2, 2)""")
cursor.execute("""INSERT OR IGNORE INTO atbilzu_varianti (variants_id, jautajuma_id, teksts, punkti, kategorija_id)
    VALUES (18, 6, 'Sniegotas kalnu virsotnes', 2, 3)""")
cursor.execute("""INSERT OR IGNORE INTO atbilzu_varianti (variants_id, jautajuma_id, teksts, punkti, kategorija_id)
    VALUES (19, 7, 'Izpētītu senas celtnes un muzejus', 1, 4)""")
cursor.execute("""INSERT OR IGNORE INTO atbilzu_varianti (variants_id, jautajuma_id, teksts, punkti, kategorija_id)
    VALUES (20, 7, 'Pamēģinātu kaut ko drosmīgu un jaunu', 1, 5)""")
cursor.execute("""INSERT OR IGNORE INTO atbilzu_varianti (variants_id, jautajuma_id, teksts, punkti, kategorija_id)
    VALUES (21, 7, 'Atpūstos klusi pie jūras', 1, 1)""")

cursor.execute("""INSERT OR IGNORE INTO valstis (valsts_id, nosaukums, kontinents, apraksts)
    VALUES (1, 'Itālija', 'Eiropa', 'Sena vēsture, garšīgs ēdiens un skaistas pludmales')""")
cursor.execute("""INSERT OR IGNORE INTO valstis (valsts_id, nosaukums, kontinents, apraksts)
    VALUES (2, 'Japāna', 'Āzija', 'Mūsdienīgas pilsētas, senas tradīcijas un kalni')""")
cursor.execute("""INSERT OR IGNORE INTO valstis (valsts_id, nosaukums, kontinents, apraksts)
    VALUES (3, 'Nepāla', 'Āzija', 'Augstākie kalni pasaulē un piedzīvojumi')""")
cursor.execute("""INSERT OR IGNORE INTO valstis (valsts_id, nosaukums, kontinents, apraksts)
    VALUES (4, 'Ēģipte', 'Āfrika', 'Karstas pludmales, jūra un piramīdas')""")
cursor.execute("""INSERT OR IGNORE INTO valstis (valsts_id, nosaukums, kontinents, apraksts)
    VALUES (5, 'Brazīlija', 'Dienvidamerika', 'Skaistas pludmales, dejas un džungļi')""")
cursor.execute("""INSERT OR IGNORE INTO valstis (valsts_id, nosaukums, kontinents, apraksts)
    VALUES (6, 'Šveice', 'Eiropa', 'Kalni, ezeri un tīrs gaiss')""")
cursor.execute("""INSERT OR IGNORE INTO valstis (valsts_id, nosaukums, kontinents, apraksts)
    VALUES (7, 'Griekija', 'Eiropa', 'Saulainas salas, tirkīzzila jūra un antīkā vēsture')""")

cursor.execute("""INSERT OR IGNORE INTO valstu_kategorijas (id, valsts_id, kategorija_id, punkti)
    VALUES (1, 1, 1, 1)""")
cursor.execute("""INSERT OR IGNORE INTO valstu_kategorijas (id, valsts_id, kategorija_id, punkti)
    VALUES (2, 1, 2, 2)""")
cursor.execute("""INSERT OR IGNORE INTO valstu_kategorijas (id, valsts_id, kategorija_id, punkti)
    VALUES (3, 1, 4, 2)""")
cursor.execute("""INSERT OR IGNORE INTO valstu_kategorijas (id, valsts_id, kategorija_id, punkti)
    VALUES (4, 2, 2, 2)""")
cursor.execute("""INSERT OR IGNORE INTO valstu_kategorijas (id, valsts_id, kategorija_id, punkti)
    VALUES (5, 2, 4, 1)""")
cursor.execute("""INSERT OR IGNORE INTO valstu_kategorijas (id, valsts_id, kategorija_id, punkti)
    VALUES (6, 2, 3, 1)""")
cursor.execute("""INSERT OR IGNORE INTO valstu_kategorijas (id, valsts_id, kategorija_id, punkti)
    VALUES (7, 3, 3, 3)""")
cursor.execute("""INSERT OR IGNORE INTO valstu_kategorijas (id, valsts_id, kategorija_id, punkti)
    VALUES (8, 3, 5, 3)""")
cursor.execute("""INSERT OR IGNORE INTO valstu_kategorijas (id, valsts_id, kategorija_id, punkti)
    VALUES (9, 4, 1, 3)""")
cursor.execute("""INSERT OR IGNORE INTO valstu_kategorijas (id, valsts_id, kategorija_id, punkti)
    VALUES (10, 4, 4, 1)""")
cursor.execute("""INSERT OR IGNORE INTO valstu_kategorijas (id, valsts_id, kategorija_id, punkti)
    VALUES (11, 5, 1, 2)""")
cursor.execute("""INSERT OR IGNORE INTO valstu_kategorijas (id, valsts_id, kategorija_id, punkti)
    VALUES (12, 5, 5, 2)""")
cursor.execute("""INSERT OR IGNORE INTO valstu_kategorijas (id, valsts_id, kategorija_id, punkti)
    VALUES (13, 6, 3, 2)""")
cursor.execute("""INSERT OR IGNORE INTO valstu_kategorijas (id, valsts_id, kategorija_id, punkti)
    VALUES (14, 6, 5, 1)""")
cursor.execute("""INSERT OR IGNORE INTO valstu_kategorijas (id, valsts_id, kategorija_id, punkti)
    VALUES (15, 7, 1, 3)""")
cursor.execute("""INSERT OR IGNORE INTO valstu_kategorijas (id, valsts_id, kategorija_id, punkti)
    VALUES (16, 7, 4, 2)""")

cursor.execute("""INSERT OR IGNORE INTO sezonas (sezona_id, nosaukums)
    VALUES (1, 'Vasara')""")
cursor.execute("""INSERT OR IGNORE INTO sezonas (sezona_id, nosaukums)
    VALUES (2, 'Ziema')""")
cursor.execute("""INSERT OR IGNORE INTO sezonas (sezona_id, nosaukums)
    VALUES (3, 'Pavasaris')""")
cursor.execute("""INSERT OR IGNORE INTO sezonas (sezona_id, nosaukums)
    VALUES (4, 'Rudens')""")

cursor.execute("""INSERT OR IGNORE INTO valstu_sezonas (id, valsts_id, sezona_id)
    VALUES (1, 1, 1)""")
cursor.execute("""INSERT OR IGNORE INTO valstu_sezonas (id, valsts_id, sezona_id)
    VALUES (2, 2, 3)""")
cursor.execute("""INSERT OR IGNORE INTO valstu_sezonas (id, valsts_id, sezona_id)
    VALUES (3, 3, 4)""")
cursor.execute("""INSERT OR IGNORE INTO valstu_sezonas (id, valsts_id, sezona_id)
    VALUES (4, 4, 2)""")
cursor.execute("""INSERT OR IGNORE INTO valstu_sezonas (id, valsts_id, sezona_id)
    VALUES (5, 5, 1)""")
cursor.execute("""INSERT OR IGNORE INTO valstu_sezonas (id, valsts_id, sezona_id)
    VALUES (6, 6, 2)""")
cursor.execute("""INSERT OR IGNORE INTO valstu_sezonas (id, valsts_id, sezona_id)
    VALUES (7, 7, 1)""")

# show what is in the database
cursor.execute("SELECT * FROM valstis")
valstis = cursor.fetchall()

print("\nVALSTIS")
for valsts in valstis:
    print(valsts)

cursor.execute("SELECT * FROM jautajumi")
jautajumi = cursor.fetchall()

print("\nJAUTAJUMI")
for jautajums in jautajumi:
    print(jautajums)

database.commit()
database.close()