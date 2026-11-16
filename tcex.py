"""
Téo CPU Emulator X (TCEX)

usage: python tcex.py

This program show the ROM in real time.
You can configure RAM and Hz frequency to ajust your preferences.
"""

import tkinter as tk
import tkinter.filedialog as fd
import tkinter.ttk as ttk
import cpu
import time
import threading

VERSION = "1.0"

tcpu = cpu.CPU()

rom_title = "No ROM Selected"
rom = []
tcpu.load_rom(rom)

RAM = 16
ram = cpu.RAM(RAM)

tcpu.ram = ram.ram
tcpu.sp = len(tcpu.ram)

HZ = 20

ROM = []
for i in tcpu.rom:
    ROM.append(format(i >> 8, "02X"))
    ROM.append(format(i & 0xFF, "02X"))

root = tk.Tk()
root.title(f"TCEX {VERSION} - {cpu.__CPU} {cpu.__VERSION} ({rom_title})")
root.geometry("900x400")

canvas = tk.Canvas(root)

scrollbar = tk.Scrollbar(
    root,
    orient="vertical",
    command=canvas.yview
)

canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

lignes = 4096 // 16
colonnes = 16

largeur = 40
hauteur = 25

cases = {}
texts = {}

i = 0
for y in range(lignes):
    for x in range(colonnes):
        x1 = x * largeur
        y1 = y * hauteur

        cases[(x, y)] = canvas.create_rectangle(
            x1, y1,
            x1 + largeur, y1 + hauteur,
            outline="black",
            fill="white"
        )

        texts[(x, y)] = canvas.create_text(
            x1+largeur//2, y1+hauteur//2, text=ROM[i], font=("Consolas", 10), fill="black"
        )
        i+=1

canvas.configure(
    scrollregion=(0, 0, colonnes * largeur, lignes * hauteur)
)

def modifycase(i):
    x = (i * 2) % 16
    y = (i * 2) // 16

    canvas.itemconfig(cases[(x, y)], fill="cyan")
    canvas.itemconfig(cases[((x + 1) % 16, y)], fill="cyan")

def modifycase2(i):
    x = (i * 2) % 16
    y = (i * 2) // 16

    canvas.itemconfig(cases[(x, y)], fill="white")
    canvas.itemconfig(cases[((x + 1) % 16, y)], fill="white")

def modifytext(i, t, t2):
    x = (i * 2) % 16
    y = (i * 2) // 16

    canvas.itemconfig(texts[(x, y)], text=t)
    canvas.itemconfig(texts[((x + 1) % 16, y)], text=t2)

info_frame = tk.Frame(root, bg="#222222", width=250)
info_frame.pack(side="right", fill="both")
info_frame.pack_propagate(False)

titre = tk.Label(
    info_frame,
    text=f"{cpu.__CPU} {cpu.__VERSION}",
    font=("Arial", 14, "bold"),
    fg="white",
    bg="#222222"
)
titre.pack(pady=10)

line = ttk.Separator(info_frame, orient="horizontal")
line.pack(fill="x", pady=10)

RegA = tk.Label(
    info_frame,
    text="A : 0",
    font=("Arial", 9, "bold"),
    fg="white",
    bg="#222222"
)
RegA.pack(pady=0)

RegB = tk.Label(
    info_frame,
    text="B : 0",
    font=("Arial", 9, "bold"),
    fg="white",
    bg="#222222"
)
RegB.pack(pady=0)

RegC = tk.Label(
    info_frame,
    text="C : 0",
    font=("Arial", 9, "bold"),
    fg="white",
    bg="#222222"
)
RegC.pack(pady=0)

RegD = tk.Label(
    info_frame,
    text="D : 0",
    font=("Arial", 9, "bold"),
    fg="white",
    bg="#222222"
)
RegD.pack(pady=0)

pc = tk.Label(
    info_frame,
    text="PC : 0",
    font=("Arial", 9, "bold"),
    fg="white",
    bg="#222222"
)
pc.pack(pady=0)

sp = tk.Label(
    info_frame,
    text=f"SP : {hex(tcpu.sp)}",
    font=("Arial", 9, "bold"),
    fg="white",
    bg="#222222"
)
sp.pack(pady=0)

flag = tk.Label(
    info_frame,
    text=f"FLAG : {tcpu.flag}",
    font=("Arial", 9, "bold"),
    fg="white",
    bg="#222222"
)
flag.pack(pady=0)

line = ttk.Separator(info_frame, orient="horizontal")
line.pack(fill="x", pady=10)

hzlabel = tk.Label(
    info_frame,
    text=f"Hz frequency : {HZ}",
    font=("Arial", 9, "bold"),
    fg="white",
    bg="#222222"
)
hzlabel.pack(pady=0)

ramstock = tk.Label(
    info_frame,
    text=f"Ram installed : {RAM}kb",
    font=("Arial", 9, "bold"),
    fg="white",
    bg="#222222"
)
ramstock.pack(pady=0)

line = ttk.Separator(info_frame, orient="horizontal")
line.pack(fill="x", pady=10)

def loadROM():
    global rom, rom_title, ROM
    file = fd.askopenfilename(title="Load a ROM File", filetypes=[("ROM File", "*.bin")])
    rom_title = file
    root.title(f"TCEX {VERSION} - {cpu.__CPU} {cpu.__VERSION} ({rom_title})")
    with open(file, "rb") as f:
        while instruction := f.read(2):
            rom.append(int.from_bytes(instruction, byteorder="big"))
    tcpu.load_rom(rom)
    for i in range(len(tcpu.rom)-1):
        #ROM.append(format(i >> 8, "02X"))
        #ROM.append(format(i & 0xFF, "02X"))
        modifytext(i, format(tcpu.rom[i] >> 8, "02X"), format(tcpu.rom[i] & 0xFF, "02X"))

loadRomButton = tk.Button(
    info_frame,
    text="Load ROM (.bin)",
    height=1,
    command=loadROM
)

loadRomButton.pack(pady=0)

def openconf():
    fenetre = tk.Toplevel(root)
    fenetre.title("Configure CPU")
    fenetre.geometry("300x160")
    fenetre.resizable(False, False)

    tk.Label(fenetre, text="Hz Frequency :").pack()
    input1 = tk.Entry(fenetre)
    input1.pack()

    tk.Label(fenetre, text="RAM (in kb) :").pack()
    input2 = tk.Entry(fenetre)
    input2.pack()

    def valider():
        global HZ, RAM
        valeur1 = input1.get()
        valeur2 = input2.get()
        HZ = int(valeur1)
        clock.set_hertz(HZ)
        RAM = int(valeur2)
        ram = cpu.RAM(RAM)
        tcpu.ram = ram.ram
        tcpu.sp = len(tcpu.ram)

        ramstock.config(text=f"Ram installed : {RAM}kb")
        hzlabel.config(text=f"Hz frequency : {HZ}")
        fenetre.destroy()

    tk.Button(fenetre, text="OK", command=valider).pack(pady=10)

setHZram = tk.Button(
    info_frame,
    text="Configure CPU",
    command=openconf
)

setHZram.pack(pady=5)

Launch = tk.Button(
    info_frame,
    text="Run",
    command=lambda: thread.start()
)

Launch.pack(pady=5)

clock = cpu.Clock()
clock.set_hertz(HZ)

prochain = time.perf_counter()
oldi = 0

def update():
    global prochain
    global oldi
    while cpu.state and not event.is_set():
        modifycase2(oldi)
        tcpu.execute()
        
        RegA.config(text=f"A : {tcpu.reg[0]}")
        RegB.config(text=f"B : {tcpu.reg[1]}")
        RegC.config(text=f"C : {tcpu.reg[2]}")
        RegD.config(text=f"D : {tcpu.reg[3]}")
        pc.config(text=f"PC : {tcpu.pc}")
        sp.config(text=f"SP : {hex(tcpu.sp)}")
        flag.config(text=f"FLAG : {tcpu.flag}")
        modifycase(tcpu.pc)
        oldi = tcpu.pc
        
        prochain += clock.time
        pause = prochain - time.perf_counter()
        if pause > 0:
            time.sleep(pause)
        else:
            prochain = time.perf_counter()

event = threading.Event()

def fermer():
    global event
    if thread.is_alive():
        event.set()       # Demande au thread de s'arrêter
        thread.join()     # Attend qu'il soit terminé
    root.destroy()    # Ferme Tkinter


root.protocol("WM_DELETE_WINDOW", fermer)

thread = threading.Thread(target=update)

root.mainloop()
