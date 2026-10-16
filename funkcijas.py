import sqlite3
import datetime

def connect():
    database = sqlite3.connect("celojumi.db")
    database.execute("PRAGMA foreign_keys = ON")
    return database

# pievieno lietotaju un atgriez vinja id
def add_user(vards, uzvards):
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT INTO lietotaji (vards, uzvards) VALUES (?,?)", (vards, uzvards))
    database.commit()
    lietotaja_id = cursor.lastrowid
    database.close()
    return lietotaja_id

# dabu visus jautajumus
def get_jautajumi():
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT jautajuma_id, teksts FROM jautajumi")
    jautajumi = cursor.fetchall()
    database.close()
    return jautajumi

# dabu visus variantus vienam jautajumam
def get_variants(jautajuma_id):
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT variants_id, teksts FROM atbilzu_varianti WHERE jautajuma_id = ?", (jautajuma_id,))
    varianti = cursor.fetchall()
    database.close()
    return varianti

# saglaba vienu atbildi
def save_atbilde(lietotaja_id, jautajuma_id, variants_id):
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT INTO atbildes (lietotajs_id, jautajuma_id, variants_id) VALUES (?,?,?)", (lietotaja_id, jautajuma_id, variants_id))
    database.commit()
    database.close()

# dabu visas valstis
def get_valstis():
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT valsts_id, nosaukums, kontinents, apraksts FROM valstis")
    valstis = cursor.fetchall()
    database.close()
    return valstis

# saskaita punktus un atrod vispiemerotako valsti
def rekinat_rezultatu(lietotaja_id):
    database = connect()
    cursor = database.cursor()

    # 1. saskaita cik punktu lietotajs dabuja katra kategorija
    cursor.execute("""
        SELECT
            atbilzu_varianti.kategorija_id,
            SUM(atbilzu_varianti.punkti)
        FROM atbildes

        JOIN atbilzu_varianti
            ON atbildes.variants_id = atbilzu_varianti.variants_id

        WHERE atbildes.lietotajs_id = ?

        GROUP BY atbilzu_varianti.kategorija_id
    """, (lietotaja_id,))

    lietotaja_punkti = {}
    for rinda in cursor.fetchall():
        lietotaja_punkti[rinda[0]] = rinda[1]

    # 2. dabu visas valstis
    cursor.execute("SELECT valsts_id FROM valstis")
    valstis = cursor.fetchall()

    # 3. katrai valstij saskaita kopejos punktus
    labaka_valsts_id = None
    labakie_punkti = -1

    for valsts in valstis:
        valsts_id = valsts[0]

        cursor.execute("""
            SELECT kategorija_id, punkti
            FROM valstu_kategorijas
            WHERE valsts_id = ?
        """, (valsts_id,))

        kopejie_punkti = 0

        for rinda in cursor.fetchall():
            kategorija_id = rinda[0]
            valsts_punkti = rinda[1]

            # ja lietotajam ir punkti saja kategorija
            if kategorija_id in lietotaja_punkti:
                kopejie_punkti = kopejie_punkti + valsts_punkti * lietotaja_punkti[kategorija_id]

        if kopejie_punkti > labakie_punkti:
            labakie_punkti = kopejie_punkti
            labaka_valsts_id = valsts_id

    # 4. dabu labakas valsts nosaukumu un labako sezonu
    cursor.execute("""
        SELECT
            valstis.valsts_id,
            valstis.nosaukums,
            sezonas.nosaukums
        FROM valstis

        LEFT JOIN valstu_sezonas
            ON valstis.valsts_id = valstu_sezonas.valsts_id

        LEFT JOIN sezonas
            ON valstu_sezonas.sezona_id = sezonas.sezona_id

        WHERE valstis.valsts_id = ?
    """, (labaka_valsts_id,))

    rinda = cursor.fetchone()
    database.close()

    return rinda[0], rinda[1], labakie_punkti, rinda[2]

# saglaba rezultatu
def save_rezultats(lietotaja_id, valsts_id, punkti):
    datums = str(datetime.date.today())

    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT INTO rezultati (lietotajs_id, valsts_id, punkti, datums) VALUES (?,?,?,?)", (lietotaja_id, valsts_id, punkti, datums))
    database.commit()
    database.close()

# dabu visus rezultatus ar vardi un valstim
def get_rezultati():
    database = connect()
    cursor = database.cursor()
    cursor.execute("""
    SELECT
        lietotaji.vards,
        lietotaji.uzvards,
        valstis.nosaukums,
        rezultati.punkti,
        rezultati.datums
    FROM rezultati

    JOIN lietotaji
        ON rezultati.lietotajs_id = lietotaji.lietotajs_id

    JOIN valstis
        ON rezultati.valsts_id = valstis.valsts_id
    ORDER BY rezultati.rezultats_id
""")
    rezultati = cursor.fetchall()
    database.close()
    return rezultati