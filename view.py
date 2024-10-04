from tkinter import *
from tkinter import ttk

root = Tk()
root.title("My App")

root.geometry("400x200")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

cpf = StringVar()
cpf_entry = ttk.Entry(mainframe, width=7, textvariable=cpf)
cpf_entry.grid(column=2, row=1, sticky=(W, E))


meters = StringVar()
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))

ttk.Button(mainframe, text="Buscar").grid(column=3, row=3, sticky=W)
ttk.Label(mainframe, text="Insira os dados de cpf").grid(column=2, row=3, sticky=W)
ttk.Label(mainframe, text="CPF:").grid(column=1, row=1, sticky=E)
ttk.Label(mainframe, text="Meters:").grid(column=1, row=2, sticky=E)


root.mainloop()