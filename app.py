import tkinter as tk
from tkinter import ttk

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

# te glabajas lietotaja id pirms testa sakuma
lietotaja_id = None

def saktTestu():
    global lietotaja_id

    vards = name_input.get()
    uzvards = surname_input.get()

    if vards and uzvards:
        lietotaja_id = add_user(vards, uzvards)
        result.config(text="Tagad atbildi uz visiem jautājumiem!", fg="green")
    else:
        result.config(text="Aizpildi abus laukus!", fg="red")


def paraditRezultatus():
    # nodzes veco tekstu rezultatu loga
    for vecais in rezultatu_block.winfo_children():
        vecais.destroy()

    for rezultats in get_rezultati():
        teksts = rezultats[0] + " " + rezultats[1] + " - " + rezultats[2] + " (" + str(rezultats[3]) + " punkti, " + rezultats[4] + ")"
        tk.Label(rezultatu_block, text=teksts).pack(anchor="w")


def paradiRezultatu():
    global lietotaja_id

    if lietotaja_id is None:
        final_result.config(text="Vispirms ievadi vārdu un uzvārdu!", fg="red")
        return

    atbildes_saglabasanai = []

    # parbauda visas ievades un sagatavo atbildes
    for jautajuma_id, ievade in variantu_ievades:
        teksts = ievade.get()

        if not teksts:
            final_result.config(text="Atbildi uz visiem jautājumiem!", fg="red")
            return

        try:
            skaitlis = int(teksts)
        except ValueError:
            final_result.config(text="Atbildē jābūt skaitlim!", fg="red")
            return

        # dabu sī jautājuma variantus un izvēlas pareizo pēc numura
        varianti = get_variants(jautajuma_id)

        if skaitlis < 1 or skaitlis > len(varianti):
            final_result.config(text="Tāda varianta nav! Ievadi 1, 2 vai 3!", fg="red")
            return

        variants_id = varianti[skaitlis - 1][0]
        atbildes_saglabasanai.append((jautajuma_id, variants_id))

    # saglaba visas atbildes datubaze
    for atbilde in atbildes_saglabasanai:
        save_atbilde(lietotaja_id, atbilde[0], atbilde[1])

    # saskaita rezultatu un saglaba to
    valsts_id, valsts_nosaukums, punkti, sezona = rekinat_rezultatu(lietotaja_id)
    save_rezultats(lietotaja_id, valsts_id, punkti)

    final_result.config(
        text="Tev vispiemērotākā valsts ir " + valsts_nosaukums + "! Labākais laiks: " + sezona + " (punkti: " + str(punkti) + ")",
        fg="green"
    )

    # atjauno rezultatu sarakstu
    paraditRezultatus()


window = tk.Tk()

window.title("Ceļojumu tests")
window.geometry("850x700")

tabs = ttk.Notebook(window)
tabs.pack(fill="both", expand=True)

test_tab = ttk.Frame(tabs)
rezultatu_tab = ttk.Frame(tabs)

tabs.add(test_tab, text="Tests")
tabs.add(rezultatu_tab, text="Rezultāti")

# ==========================================
# ritinas izveide, lai var skatit visus jautajumus

# canvas ir vieta uz kuras var likt saturu un ritinat to
canvas = tk.Canvas(test_tab)

# rina kas stāv labaja mala
scrollbar = ttk.Scrollbar(test_tab, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# te bus viss saturs ko var ritinat
scroll_frame = tk.Frame(canvas)

# kad saturs maina izmeru, atjaunojam ritinas apgabalu
scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# ielikam saturu ieksa canvasi
canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

# pele rites ritina uz augsu un leju
def ritinat(event):
    canvas.yview_scroll(-1 * int(event.delta / 120), "units")

canvas.bind_all("<MouseWheel>", ritinat)
# ==========================================

# VISU tagad liekam scroll_frame ieksa, nevis test_tab

header = tk.Label(
    scroll_frame,
    text="Atradi savu ideālo ceļojuma valsti!",
    font=("Arial", 20, "bold")
)
header.pack(pady=20)

# bloks ar lietotaja datiem
user_block = tk.LabelFrame(
    scroll_frame,
    text="Tavi dati",
    padx=10,
    pady=10
)
user_block.pack(fill="x", padx=20, pady=10)

tk.Label(user_block, text="Vārds").pack()

name_input = tk.Entry(user_block, width=40)
name_input.pack(pady=5)

tk.Label(user_block, text="Uzvārds").pack()

surname_input = tk.Entry(user_block, width=40)
surname_input.pack(pady=5)

start_button = tk.Button(user_block, text="Sākt testu", command=saktTestu)
start_button.pack(pady=5)

result = tk.Label(user_block, text="")
result.pack(pady=5)

# bloks ar jautajumiem
questions_block = tk.LabelFrame(
    scroll_frame,
    text="Jautājumi (ievadi varianta numuru)",
    padx=10,
    pady=10
)
questions_block.pack(fill="x", padx=20, pady=10)

jautajumi = get_jautajumi()
variantu_ievades = []

for jautajums in jautajumi:
    tk.Label(
        questions_block,
        text=jautajums[1],
        font=("Arial", 11, "bold")
    ).pack(pady=(8, 2))

    # paradam variantus ar numuriem 1, 2, 3
    varianti = get_variants(jautajums[0])
    numurs = 0

    for variants in varianti:
        numurs = numurs + 1
        tk.Label(questions_block, text=str(numurs) + ". " + variants[1]).pack()

    ievade = tk.Entry(questions_block, width=10)
    ievade.pack(pady=5)

    variantu_ievades.append((jautajums[0], ievade))

# bloks ar rezultata pogu
result_block = tk.LabelFrame(
    scroll_frame,
    text="Rezultāts",
    padx=10,
    pady=10
)
result_block.pack(fill="x", padx=20, pady=10)

finish_button = tk.Button(result_block, text="Iegūt rezultātu", command=paradiRezultatu)
finish_button.pack(pady=5)

final_result = tk.Label(result_block, text="", font=("Arial", 13, "bold"))
final_result.pack(pady=5)

# otra taba - valstis un rezultati
valstu_block = tk.LabelFrame(
    rezultatu_tab,
    text="Valstis datubāzē",
    padx=10,
    pady=10
)
valstu_block.pack(fill="x", padx=20, pady=10)

for valsts in get_valstis():
    tk.Label(valstu_block, text=valsts[1] + " (" + valsts[2] + ") - " + valsts[3]).pack(anchor="w")

rezultatu_block = tk.LabelFrame(
    rezultatu_tab,
    text="Visi rezultāti",
    padx=10,
    pady=10
)
rezultatu_block.pack(fill="x", padx=20, pady=10)

paraditRezultatus()

window.mainloop()