import tkinter as tk
from tkinter import ttk

from funkcijas import (
    add_user,
    get_jautajumi,
    get_variants,
    save_atbilde,
    get_valstis,
    get_sezonas,
    get_rezultati,
    rekinat_rezultatu,
    save_rezultats,
    get_tabula,
    get_kategorijas,
    add_valsts,
    add_jautajums,
)

FONS = "#F7F1E5"
KARTE = "#FFFDF7"
MALLA = "#E67EA5"
NAVJOSLA = "#8CC0C4"
ROZE = "#F03D88"
ROZE_TUMSA = "#B63F67"
ROZE_GAISA = "#F091B0"
TEAL = "#24A3A3"
PLUMS = "#691B48"
TAUPE = "#9A8778"
SARKANS = "#A94A4A"
TEKSTS = "#6E5A50"
GIMENE = "Georgia"

lietotaja_id = None

# tkinter deletes images that nothing references, so they are kept here
attelu_saraksts = []

# tables shown as tabs so the teacher can see every table
TABULAS = [
    ("lietotaji", "Lietotāji"),
    ("kategorijas", "Kategorijas"),
    ("jautajumi", "Jautājumi"),
    ("atbilzu_varianti", "Atbilžu varianti"),
    ("atbildes", "Atbildes"),
    ("valstis", "Valstis"),
    ("valstu_kategorijas", "Valstu kategorijas"),
    ("sezonas", "Sezonas"),
    ("valstu_sezonas", "Valstu sezonas"),
    ("rezultati", "Rezultāti"),
]


def rada_attelu(celjs, platums=200):
    # loads an image scaled to platums, or None if the file is missing
    try:
        from PIL import Image, ImageTk  # pip install Pillow
        bilde = Image.open(celjs)
        augstums = int(bilde.height * platums / bilde.width)
        bilde = bilde.resize((platums, augstums))
        attels = ImageTk.PhotoImage(bilde)
    except Exception:
        try:
            attels = tk.PhotoImage(file=celjs)
        except Exception:
            return None

    attelu_saraksts.append(attels)
    return attels


def valsts_attela_nosaukums(valsts_nosaukums):
    # "Itālija" -> "atteli/italija.png"
    mazais = valsts_nosaukums.lower()
    for burts, vienkarsis in {"ā": "a", "č": "c", "ē": "e", "ģ": "g", "ī": "i",
                              "ķ": "k", "ļ": "l", "ņ": "n", "š": "s", "ū": "u",
                              "ž": "z"}.items():
        mazais = mazais.replace(burts, vienkarsis)
    return "atteli/" + mazais + ".png"


def izveidot_pogu(mamma, teksts, komanda):
    poga = tk.Button(
        mamma, text=teksts, command=komanda,
        font=(GIMENE, 11, "bold"), bg=ROZE, fg="#FDFBF4",
        activebackground=ROZE_TUMSA, activeforeground="#FDFBF4",
        relief="flat", borderwidth=0, cursor="hand2", padx=18, pady=5
    )
    poga.bind("<Enter>", lambda e: poga.config(bg=ROZE_TUMSA))
    poga.bind("<Leave>", lambda e: poga.config(bg=ROZE))
    return poga


def izveidot_ritinas(mamma):
    # returns a frame whose content scrolls with the mouse wheel
    canvas = tk.Canvas(mamma, bg=FONS, highlightthickness=0)
    ritina = ttk.Scrollbar(mamma, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=ritina.set)
    ritina.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    saturs = tk.Frame(canvas, bg=FONS)
    saturs.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    window_id = canvas.create_window((0, 0), window=saturs, anchor="nw")

    # keep the inner frame as wide as the canvas, so content (which uses
    # fill="x") stretches across and centered items really sit in the middle
    def pielagot_platumu(event):
        canvas.itemconfig(window_id, width=event.width)
    canvas.bind("<Configure>", pielagot_platumu)

    def ritini(event):
        if event.num == 4 or event.delta > 0:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            canvas.yview_scroll(1, "units")

    def pele_ieksa(event):
        canvas.bind_all("<MouseWheel>", ritini)
        canvas.bind_all("<Button-4>", ritini)
        canvas.bind_all("<Button-5>", ritini)

    def pele_ara(event):
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")

    canvas.bind("<Enter>", pele_ieksa)
    canvas.bind("<Leave>", pele_ara)
    return saturs


def aizpildi_tabulu(tabulas_nosaukums, koks):
    # fills one table tab with everything that is in that table
    kolonnas, rindas = get_tabula(tabulas_nosaukums)

    koks["columns"] = kolonnas
    for kolonna in kolonnas:
        koks.heading(kolonna, text=kolonna)
        koks.column(kolonna, width=130, anchor="w")

    for veca_rinda in koks.get_children():
        koks.delete(veca_rinda)

    for rinda in rindas:
        koks.insert("", "end", values=rinda)


def saktTestu():
    global lietotaja_id

    vards = name_input.get().strip()
    uzvards = surname_input.get().strip()

    if vards and uzvards:
        lietotaja_id = add_user(vards, uzvards)
        result.config(text="Lieliski, " + vards + "! Tagad atbildi uz visiem jautājumiem.", fg=TEAL)
    else:
        result.config(text="Aizpildi abus laukus!", fg=SARKANS)


def paraditRezultatus():
    for vecais in rezultatu_block.winfo_children():
        vecais.destroy()

    for rezultats in get_rezultati():
        teksts = (rezultats[0] + " " + rezultats[1] + " — " + rezultats[2]
                  + "  (" + str(rezultats[3]) + " punkti, " + rezultats[4] + ")")
        tk.Label(rezultatu_block, text=teksts, font=(GIMENE, 10),
                 bg=KARTE, fg=TEKSTS, anchor="w").pack(fill="x", pady=1)


def paradiRezultatu():
    global lietotaja_id

    if lietotaja_id is None:
        final_result.config(text="Vispirms ievadi vārdu un uzvārdu!", fg=SARKANS)
        return

    atbildes_saglabasanai = []

    for jautajuma_id, ievade in variantu_ievades:
        teksts = ievade.get().strip()

        if not teksts:
            final_result.config(text="Atbildi uz visiem jautājumiem!", fg=SARKANS)
            return

        try:
            skaitlis = int(teksts)
        except ValueError:
            final_result.config(text="Atbildē jābūt skaitlim!", fg=SARKANS)
            return

        varianti = get_variants(jautajuma_id)

        if skaitlis < 1 or skaitlis > len(varianti):
            final_result.config(text="Tāda varianta nav! Ievadi 1, 2 vai 3!", fg=SARKANS)
            return

        variants_id = varianti[skaitlis - 1][0]
        atbildes_saglabasanai.append((jautajuma_id, variants_id))

    for atbilde in atbildes_saglabasanai:
        save_atbilde(lietotaja_id, atbilde[0], atbilde[1])

    valsts_id, valsts_nosaukums, punkti, sezona = rekinat_rezultatu(lietotaja_id)

    if valsts_nosaukums is None:
        final_result.config(text="Ups! Rezultātu neizdevās izrēķināt!", fg=SARKANS)
        return

    save_rezultats(lietotaja_id, valsts_id, punkti)

    final_result.config(
        text=("Tev vispiemērotākā valsts ir " + valsts_nosaukums + "!\n"
              "Labākais laiks ceļot: " + sezona + "   •   Punkti: " + str(punkti)),
        fg=TEAL
    )

    for vecais in rezultata_attela_vieta.winfo_children():
        vecais.destroy()
    rezultata_attels = rada_attelu(valsts_attela_nosaukums(valsts_nosaukums), 230)
    if rezultata_attels:
        tk.Label(rezultata_attela_vieta, image=rezultata_attels, bg=KARTE).pack(pady=4)

    for jautajuma_id, ievade in variantu_ievades:
        ievade.delete(0, "end")

    paraditRezultatus()


window = tk.Tk()
window.title("Ceļojumu tests")
window.minsize(760, 560)
window.configure(bg=FONS)

# center the window on the screen
PLATUMS = 1020
AUGSTUMS = 700
x = (window.winfo_screenwidth() - PLATUMS) // 2
y = (window.winfo_screenheight() - AUGSTUMS) // 2
window.geometry(str(PLATUMS) + "x" + str(AUGSTUMS) + "+" + str(x) + "+" + str(y))

stils = ttk.Style(window)
try:
    stils.theme_use("clam")
except Exception:
    pass
stils.configure("TFrame", background=FONS)
stils.configure("TNotebook", background=FONS, borderwidth=0)
stils.configure("TNotebook.Tab", background=MALLA, foreground=PLUMS,
                padding=(14, 7), font=(GIMENE, 10, "bold"))
stils.map("TNotebook.Tab",
          background=[("selected", TEAL)],
          foreground=[("selected", "#FDFBF4")])

tabs = ttk.Notebook(window)

test_tab = ttk.Frame(tabs)
rezultatu_tab = ttk.Frame(tabs)
tabs.add(test_tab, text="Tests")
tabs.add(rezultatu_tab, text="Rezultāti")

# one tab for every table in the database
koki = {}
for tabulas_nosaukums, virsraksts in TABULAS:
    tab = ttk.Frame(tabs)
    tabs.add(tab, text=virsraksts)

    koks = ttk.Treeview(tab, show="headings")
    ritina = ttk.Scrollbar(tab, orient="vertical", command=koks.yview)
    koks.configure(yscrollcommand=ritina.set)
    ritina.pack(side="right", fill="y")
    koks.pack(side="left", fill="both", expand=True)

    koki[tabulas_nosaukums] = koks
    aizpildi_tabulu(tabulas_nosaukums, koks)

# -------------------------------------------------
# Admin tab - data typed here goes straight into the database

admin_tab = ttk.Frame(tabs)
tabs.add(admin_tab, text="Admin")

kategorijas = get_kategorijas()
kategoriju_nosaukumi = [kategorija[1] for kategorija in kategorijas]

statuss = tk.Label(admin_tab, text="", font=(GIMENE, 10), bg=FONS)
statuss.pack(side="bottom", pady=8)

tk.Label(admin_tab, text="Šeit ievadītie dati uzreiz tiek saglabāti datubāzē (pārbaudi citās tabās)",
         font=(GIMENE, 10, "italic"), bg=FONS, fg=TAUPE).pack(anchor="w", padx=15, pady=(10, 4))

valsts_bloks = tk.LabelFrame(admin_tab, text=" Pievienot valsti ", font=(GIMENE, 11, "bold"),
                             bg=FONS, fg=PLUMS, padx=12, pady=10,
                             highlightthickness=1, highlightbackground=MALLA, highlightcolor=MALLA)
valsts_bloks.pack(fill="x", padx=15, pady=8)

tk.Label(valsts_bloks, text="Nosaukums:", bg=FONS, fg=TEKSTS, font=(GIMENE, 10)).grid(row=0, column=0, sticky="w", pady=3)
valsts_nosaukums_ievade = tk.Entry(valsts_bloks, width=45, font=(GIMENE, 10))
valsts_nosaukums_ievade.grid(row=0, column=1, pady=3)

tk.Label(valsts_bloks, text="Kontinents:", bg=FONS, fg=TEKSTS, font=(GIMENE, 10)).grid(row=1, column=0, sticky="w", pady=3)
valsts_kontinents_ievade = tk.Entry(valsts_bloks, width=45, font=(GIMENE, 10))
valsts_kontinents_ievade.grid(row=1, column=1, pady=3)

tk.Label(valsts_bloks, text="Apraksts:", bg=FONS, fg=TEKSTS, font=(GIMENE, 10)).grid(row=2, column=0, sticky="w", pady=3)
valsts_apraksts_ievade = tk.Entry(valsts_bloks, width=45, font=(GIMENE, 10))
valsts_apraksts_ievade.grid(row=2, column=1, pady=3)


def saglabat_valsti():
    nosaukums = valsts_nosaukums_ievade.get().strip()
    kontinents = valsts_kontinents_ievade.get().strip()
    apraksts = valsts_apraksts_ievade.get().strip()

    if not nosaukums or not kontinents or not apraksts:
        statuss.config(text="Aizpildi visus valsts laukus!", fg=SARKANS)
        return

    add_valsts(nosaukums, kontinents, apraksts)
    aizpildi_tabulu("valstis", koki["valstis"])

    # the navbar country list updates without restarting
    nav_valstis.config(text="Iespējamie rezultāti:  " + "  •  ".join([v[1] for v in get_valstis()]))

    valsts_nosaukums_ievade.delete(0, "end")
    valsts_kontinents_ievade.delete(0, "end")
    valsts_apraksts_ievade.delete(0, "end")

    statuss.config(text="Valsts \"" + nosaukums + "\" pievienota datubāzei!", fg=TEAL)


izveidot_pogu(valsts_bloks, "Saglabāt valsti", saglabat_valsti).grid(row=3, column=1, sticky="e", pady=8)

jautajuma_bloks = tk.LabelFrame(admin_tab, text=" Pievienot jautājumu (3 varianti) ", font=(GIMENE, 11, "bold"),
                                bg=FONS, fg=PLUMS, padx=12, pady=10,
                                highlightthickness=1, highlightbackground=MALLA, highlightcolor=MALLA)
jautajuma_bloks.pack(fill="x", padx=15, pady=8)

tk.Label(jautajuma_bloks, text="Jautājums:", bg=FONS, fg=TEKSTS, font=(GIMENE, 10)).grid(row=0, column=0, sticky="w", pady=3)
jautajuma_teksts_ievade = tk.Entry(jautajuma_bloks, width=60, font=(GIMENE, 10))
jautajuma_teksts_ievade.grid(row=0, column=1, columnspan=3, pady=3, sticky="w")

tk.Label(jautajuma_bloks, text="Varianti:", bg=FONS, fg=TEKSTS, font=(GIMENE, 10)).grid(row=1, column=0, sticky="nw", pady=3)
tk.Label(jautajuma_bloks, text="Teksts", bg=FONS, fg=TAUPE, font=(GIMENE, 9, "bold")).grid(row=1, column=1, sticky="w")
tk.Label(jautajuma_bloks, text="Kategorija", bg=FONS, fg=TAUPE, font=(GIMENE, 9, "bold")).grid(row=1, column=2, sticky="w")
tk.Label(jautajuma_bloks, text="Punkti", bg=FONS, fg=TAUPE, font=(GIMENE, 9, "bold")).grid(row=1, column=3, sticky="w")

variantu_lauki = []

for i in range(3):
    rinda = i + 2

    tk.Label(jautajuma_bloks, text=str(i + 1) + ":", bg=FONS, fg=TEKSTS, font=(GIMENE, 10)).grid(row=rinda, column=0, sticky="w", pady=3)

    teksts_ievade = tk.Entry(jautajuma_bloks, width=35, font=(GIMENE, 10))
    teksts_ievade.grid(row=rinda, column=1, pady=3, padx=(0, 10), sticky="w")

    kategorija_izvele = ttk.Combobox(jautajuma_bloks, values=kategoriju_nosaukumi, width=16, state="readonly")
    kategorija_izvele.current(0)
    kategorija_izvele.grid(row=rinda, column=2, pady=3, padx=(0, 10))

    punkti_ievade = tk.Entry(jautajuma_bloks, width=5, font=(GIMENE, 10))
    punkti_ievade.insert(0, "1")
    punkti_ievade.grid(row=rinda, column=3)

    variantu_lauki.append((teksts_ievade, kategorija_izvele, punkti_ievade))


def saglabat_jautajumu():
    jautajuma_teksts = jautajuma_teksts_ievade.get().strip()

    if not jautajuma_teksts:
        statuss.config(text="Ievadi jautājuma tekstu!", fg=SARKANS)
        return

    jaunie_varianti = []

    for teksts_ievade, kategorija_izvele, punkti_ievade in variantu_lauki:
        teksts = teksts_ievade.get().strip()

        if not teksts:
            statuss.config(text="Aizpildi visus 3 variantus!", fg=SARKANS)
            return

        try:
            punkti = int(punkti_ievade.get())
        except ValueError:
            statuss.config(text="Punktiem jābūt skaitlim!", fg=SARKANS)
            return

        kategorija_id = kategorijas[kategoriju_nosaukumi.index(kategorija_izvele.get())][0]
        jaunie_varianti.append((teksts, kategorija_id, punkti))

    add_jautajums(jautajuma_teksts, jaunie_varianti)
    aizpildi_tabulu("jautajumi", koki["jautajumi"])
    aizpildi_tabulu("atbilzu_varianti", koki["atbilzu_varianti"])

    jautajuma_teksts_ievade.delete(0, "end")
    for teksts_ievade, kategorija_izvele, punkti_ievade in variantu_lauki:
        teksts_ievade.delete(0, "end")
        punkti_ievade.delete(0, "end")
        punkti_ievade.insert(0, "1")

    statuss.config(text="Jautājums pievienots datubāzei!", fg=TEAL)


izveidot_pogu(jautajuma_bloks, "Saglabāt jautājumu", saglabat_jautajumu).grid(row=5, column=1, sticky="w", pady=8)

# packed before the notebook, so the navbar stays at the top of the window
navbar = tk.Frame(window, bg=NAVJOSLA)
navbar.pack(fill="x")

nav_augsa = tk.Frame(navbar, bg=NAVJOSLA)
nav_augsa.pack(fill="x", padx=16, pady=(8, 0))

tk.Label(nav_augsa, text="CEĻOJUMU TESTS", font=(GIMENE, 14, "bold"),
         bg=NAVJOSLA, fg=PLUMS).pack(side="left")

tk.Label(nav_augsa, text="atbildi uz jautājumiem un uzzini savu valsti",
         font=(GIMENE, 10, "italic"), bg=NAVJOSLA, fg=TAUPE).pack(side="right")

# countries come straight from the database, so new ones show up here automatically
valstu_nosaukumi = [valsts[1] for valsts in get_valstis()]

nav_apaksa = tk.Frame(navbar, bg=NAVJOSLA)
nav_apaksa.pack(fill="x", padx=16, pady=(2, 8))

nav_valstis = tk.Label(nav_apaksa,
                       text="Iespējamie rezultāti:  " + "  •  ".join(valstu_nosaukumi),
                       font=(GIMENE, 10, "bold"), bg=NAVJOSLA, fg=ROZE_TUMSA)
nav_valstis.pack(side="left")

tabs.pack(fill="both", expand=True, padx=10, pady=(8, 10))

scroll_frame = izveidot_ritinas(test_tab)

header = tk.Label(
    scroll_frame,
    text="Atradi savu ideālo ceļojuma valsti!",
    font=(GIMENE, 20, "bold"),
    bg=FONS, fg=PLUMS
)
header.pack(pady=(18, 2))

tk.Label(
    scroll_frame,
    text="Atbildi uz jautājumiem un uzzini, kura valsts tev ir piemērotākā.",
    font=(GIMENE, 11),
    bg=FONS, fg=TAUPE
).pack(pady=(0, 8))

baneris = rada_attelu("atteli/baneris.png", 540)
if baneris:
    tk.Label(scroll_frame, image=baneris, bg=FONS).pack(pady=(0, 10))

user_block = tk.LabelFrame(
    scroll_frame, text=" Tavi dati ", font=(GIMENE, 11, "bold"),
    bg=KARTE, fg=PLUMS, padx=12, pady=10,
    highlightthickness=1, highlightbackground=MALLA, highlightcolor=MALLA
)
user_block.pack(fill="x", padx=20, pady=10)

tk.Label(user_block, text="Vārds", font=(GIMENE, 10), bg=KARTE, fg=TEKSTS).pack()

name_input = tk.Entry(user_block, width=32, font=(GIMENE, 11), bg=FONS,
                      fg=TEKSTS, relief="flat", highlightthickness=1,
                      highlightbackground=ROZE_GAISA, highlightcolor=ROZE)
name_input.pack(pady=5, ipady=3)

tk.Label(user_block, text="Uzvārds", font=(GIMENE, 10), bg=KARTE, fg=TEKSTS).pack()

surname_input = tk.Entry(user_block, width=32, font=(GIMENE, 11), bg=FONS,
                         fg=TEKSTS, relief="flat", highlightthickness=1,
                         highlightbackground=ROZE_GAISA, highlightcolor=ROZE)
surname_input.pack(pady=5, ipady=3)

start_button = izveidot_pogu(user_block, "Sākt testu", saktTestu)
start_button.pack(pady=6)

result = tk.Label(user_block, text="", font=(GIMENE, 10), bg=KARTE, fg=TEAL)
result.pack(pady=2)

questions_block = tk.LabelFrame(
    scroll_frame, text=" Jautājumi (ievadi varianta numuru) ",
    font=(GIMENE, 11, "bold"), bg=KARTE, fg=PLUMS, padx=12, pady=10,
    highlightthickness=1, highlightbackground=MALLA, highlightcolor=MALLA
)
questions_block.pack(fill="x", padx=20, pady=10)

jautajumi = get_jautajumi()
variantu_ievades = []

for jautajuma_numurs, jautajums in enumerate(jautajumi, start=1):
    tk.Label(
        questions_block,
        text=str(jautajuma_numurs) + ". " + jautajums[1],
        font=(GIMENE, 11, "bold"), bg=KARTE, fg=TEKSTS, anchor="w"
    ).pack(fill="x", pady=(10, 2))

    varianti = get_variants(jautajums[0])
    numurs = 0

    for variants in varianti:
        numurs = numurs + 1
        tk.Label(
            questions_block,
            text="      " + str(numurs) + ".  " + variants[1],
            font=(GIMENE, 10), bg=KARTE, fg=TEKSTS, anchor="w"
        ).pack(fill="x")

    ievade = tk.Entry(questions_block, width=8, font=(GIMENE, 11), justify="center",
                      bg=FONS, fg=TEKSTS, relief="flat", highlightthickness=1,
                      highlightbackground=ROZE_GAISA, highlightcolor=ROZE)
    ievade.pack(pady=6)

    variantu_ievades.append((jautajums[0], ievade))

result_block = tk.LabelFrame(
    scroll_frame, text=" Rezultāts ", font=(GIMENE, 11, "bold"),
    bg=KARTE, fg=PLUMS, padx=12, pady=10,
    highlightthickness=1, highlightbackground=MALLA, highlightcolor=MALLA
)
result_block.pack(fill="x", padx=20, pady=10)

finish_button = izveidot_pogu(result_block, "Iegūt rezultātu", paradiRezultatu)
finish_button.pack(pady=6)

final_result = tk.Label(result_block, text="", font=(GIMENE, 13, "bold"),
                        bg=KARTE, fg=TEAL, justify="center")
final_result.pack(pady=5)

rezultata_attela_vieta = tk.Frame(result_block, bg=KARTE)
rezultata_attela_vieta.pack()

rez_scroll_frame = izveidot_ritinas(rezultatu_tab)

valstu_block = tk.LabelFrame(
    rez_scroll_frame, text=" Valstis datubāzē ", font=(GIMENE, 11, "bold"),
    bg=KARTE, fg=PLUMS, padx=12, pady=10,
    highlightthickness=1, highlightbackground=MALLA, highlightcolor=MALLA
)
valstu_block.pack(fill="x", padx=20, pady=10)

valstu_block.columnconfigure(0, weight=1)
valstu_block.columnconfigure(1, weight=1)

sezonas = get_sezonas()

for indekss, valsts in enumerate(get_valstis()):
    karte_rinda = indekss // 2
    kolonna = indekss % 2

    karte = tk.Frame(valstu_block, bg=KARTE, padx=10, pady=8,
                     highlightthickness=1, highlightbackground=MALLA)
    karte.grid(row=karte_rinda, column=kolonna, padx=8, pady=8, sticky="new")

    kartes_attels = rada_attelu(valsts_attela_nosaukums(valsts[1]), 190)
    if kartes_attels:
        tk.Label(karte, image=kartes_attels, bg=KARTE).pack()

    tk.Label(karte, text=valsts[1], font=(GIMENE, 13, "bold"),
             bg=KARTE, fg=PLUMS).pack()

    tk.Label(karte, text=valsts[2], font=(GIMENE, 9, "italic"),
             bg=KARTE, fg=TAUPE).pack()

    tk.Label(karte, text=valsts[3], font=(GIMENE, 10), bg=KARTE, fg=TEKSTS,
             wraplength=200, justify="center").pack(pady=2)

    if valsts[0] in sezonas:
        tk.Label(karte, text="Labākais laiks: " + sezonas[valsts[0]],
                 font=(GIMENE, 9, "bold"), bg=KARTE, fg=TEAL).pack()

rezultatu_block = tk.LabelFrame(
    rez_scroll_frame, text=" Visi rezultāti ", font=(GIMENE, 11, "bold"),
    bg=KARTE, fg=PLUMS, padx=12, pady=10,
    highlightthickness=1, highlightbackground=MALLA, highlightcolor=MALLA
)
rezultatu_block.pack(fill="x", padx=20, pady=10)

paraditRezultatus()

window.mainloop()