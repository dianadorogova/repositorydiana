import sqlite3
import datetime


def connect():
    database = sqlite3.connect("celojumi.db")
    database.execute("PRAGMA foreign_keys = ON")
    return database


def add_user(vards, uzvards):
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT INTO lietotaji (vards, uzvards) VALUES (?,?)", (vards, uzvards))
    database.commit()
    lietotaja_id = cursor.lastrowid
    database.close()
    return lietotaja_id


def get_jautajumi():
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT jautajuma_id, teksts FROM jautajumi ORDER BY jautajuma_id")
    jautajumi = cursor.fetchall()
    database.close()
    return jautajumi


def get_variants(jautajuma_id):
    database = connect()
    cursor = database.cursor()
    cursor.execute("""SELECT variants_id, teksts FROM atbilzu_varianti
                      WHERE jautajuma_id = ? ORDER BY variants_id""", (jautajuma_id,))
    varianti = cursor.fetchall()
    database.close()
    return varianti


def save_atbilde(lietotaja_id, jautajuma_id, variants_id):
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT INTO atbildes (lietotajs_id, jautajuma_id, variants_id) VALUES (?,?,?)",
                   (lietotaja_id, jautajuma_id, variants_id))
    database.commit()
    database.close()


def get_valstis():
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT valsts_id, nosaukums, kontinents, apraksts FROM valstis")
    valstis = cursor.fetchall()
    database.close()
    return valstis


# used by the Admin tab to fill the category dropdown
def get_kategorijas():
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT kategorija_id, nosaukums FROM kategorijas ORDER BY kategorija_id")
    kategorijas = cursor.fetchall()
    database.close()
    return kategorijas


def add_valsts(nosaukums, kontinents, apraksts):
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT INTO valstis (nosaukums, kontinents, apraksts) VALUES (?,?,?)",
                   (nosaukums, kontinents, apraksts))
    database.commit()
    valsts_id = cursor.lastrowid
    database.close()
    return valsts_id


# varianti = list of (teksts, kategorija_id, punkti)
def add_jautajums(teksts, varianti):
    database = connect()
    cursor = database.cursor()

    cursor.execute("INSERT INTO jautajumi (teksts) VALUES (?)", (teksts,))
    jautajuma_id = cursor.lastrowid

    for variants_teksts, kategorija_id, punkti in varianti:
        cursor.execute("""INSERT INTO atbilzu_varianti (jautajuma_id, teksts, punkti, kategorija_id)
                          VALUES (?,?,?,?)""",
                       (jautajuma_id, variants_teksts, punkti, kategorija_id))

    database.commit()
    database.close()
    return jautajuma_id


# reads one whole table; the name comes from the fixed list in main.py, not from user input
def get_tabula(tabulas_nosaukums):
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT * FROM " + tabulas_nosaukums)
    kolonnas = [d[0] for d in cursor.description]
    rindas = cursor.fetchall()
    database.close()
    return kolonnas, rindas


# returns {valsts_id: sezonas nosaukums}
def get_sezonas():
    database = connect()
    cursor = database.cursor()
    cursor.execute("""
        SELECT valstu_sezonas.valsts_id, sezonas.nosaukums
        FROM valstu_sezonas

        JOIN sezonas
            ON valstu_sezonas.sezona_id = sezonas.sezona_id
    """)
    sezonas = {}
    for rinda in cursor.fetchall():
        sezonas[rinda[0]] = rinda[1]
    database.close()
    return sezonas


def rekinat_rezultatu(lietotaja_id):
    database = connect()
    cursor = database.cursor()

    # the user's points in each category
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

    cursor.execute("SELECT valsts_id FROM valstis")
    valstis = cursor.fetchall()

    if not valstis:
        database.close()
        return None, None, 0, None

    # total score for every country
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

            if kategorija_id in lietotaja_punkti:
                kopejie_punkti = kopejie_punkti + valsts_punkti * lietotaja_punkti[kategorija_id]

        if kopejie_punkti > labakie_punkti:
            labakie_punkti = kopejie_punkti
            labaka_valsts_id = valsts_id

    # name and best season of the winning country
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

    if rinda is None:
        return None, None, 0, None

    return rinda[0], rinda[1], labakie_punkti, rinda[2]


def save_rezultats(lietotaja_id, valsts_id, punkti):
    datums = str(datetime.date.today())

    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT INTO rezultati (lietotajs_id, valsts_id, punkti, datums) VALUES (?,?,?,?)",
                   (lietotaja_id, valsts_id, punkti, datums))
    database.commit()
    database.close()


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