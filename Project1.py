import json
import customtkinter as ctk
import sys
import os
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")



root = ctk.CTk()
root.title("Inventory Manager")
root.geometry("800x800")
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

root.iconbitmap(resource_path("stock-rotation.ico"))
root.after(200, lambda: root.iconbitmap(resource_path("stock-rotation.ico")))
ctk.CTkLabel(root, text="Inventory Manager", font=("Arial", 20, "bold")).pack(pady=10)
output = ctk.CTkTextbox(root, height=200, width=600,font= ("Arial",14))
output.pack()
ctk.CTkLabel(root, text="Item Name").pack()
entry_good = ctk.CTkEntry(root,width = 300)
entry_good.pack()
ctk.CTkLabel(root,text = "Quantity/Price").pack()
entry_qty = ctk.CTkEntry(root,width = 300)
entry_qty.pack()
ctk.CTkLabel(root, text="Search").pack()
entry_search = ctk.CTkEntry(root, width=300)
entry_search.pack()

default_inventory = {
    "apple" : {"qty": 0, "price": 10},
    "bread" : {"qty": 0, "price": 5},
    "chips" : {"qty": 0, "price": 10},
    "milk" : {"qty": 0, "price": 15},
    "orange": {"qty": 0, "price": 7},
    "yarn" : {"qty": 0, "price": 6}
}

def search(event=None):
    query = entry_search.get().lower().strip()
    output.delete("1.0", ctk.END)  # clear output first
    if not query:
        return
    results = [g for g in inventory if query in g]
    if results:
        for g in results:
            output.insert(ctk.END, f"{g} — Qty: {inventory[g]['qty']}, Price: {inventory[g]['price']}\n")
    else:
        output.insert(ctk.END, "No results found.\n")

def make_button(text, command, fg_color, hover_color):
    ctk.CTkButton(
        root,
        text=text,
        command=command,
        width=200,
        height=40,
        corner_radius=10,
        fg_color=fg_color,
        hover_color=hover_color,
        font=("Arial", 14, "bold")
    ).pack(pady=5)

try:
    with open("inv.json", "r") as inv:
        inventory = json.load(inv)
except FileNotFoundError:
    inventory = default_inventory
    with open("inv.json", "w") as inv:
        json.dump(default_inventory, inv)
except json.JSONDecodeError:
    inventory = default_inventory
    with open("inv.json", "w") as inv:
        json.dump(default_inventory, inv)
def add_good():
    good = entry_good.get().lower().rstrip()
    if not entry_good.get().strip():
        output.insert(ctk.END, "Please enter an item name.\n")
        return
    if not entry_qty.get().strip():
        output.insert(ctk.END, "Please enter a quantity.\n")
        return
    try:
        price = int(entry_qty.get())
        if price <= 0:
            output.insert(ctk.END,"Please enter a reasonable price.\n")
        else:
            inventory[good] = {"qty": 0, "price": price}
            output.insert(ctk.END,f"Added {good} for price {price}\n")
    except ValueError:
        output.insert(ctk.END,"Please enter a number.\n")
def restock():
    rstck_good = entry_good.get().lower().strip()
    if not entry_good.get().strip():
        output.insert(ctk.END, "Please enter an item name.\n")
        return
    if not entry_qty.get().strip():
        output.insert(ctk.END, "Please enter a quantity.\n")
        return
    try:
        new_qty = int(entry_qty.get())
    except ValueError:
        output.insert(ctk.END, "Please enter a valid number for quantity.\n")
        return
    
    if new_qty < 0:
        output.insert(ctk.END, "Enter a positive value.\n")
        return
    
    if rstck_good in inventory:
        inventory[rstck_good]["qty"] += new_qty
        output.insert(ctk.END, f"Restocked {rstck_good} by {new_qty}.\n")
    else:
        output.insert(ctk.END, f"{rstck_good} is not a valid item.\n")

def sell():
    sell_good = entry_good.get().lower().rstrip()
    if not entry_good.get().strip():
        output.insert(ctk.END, "Please enter an item name.\n")
        return
    if not entry_qty.get().strip():
        output.insert(ctk.END, "Please enter a quantity.\n")
        return
    try:
        sell_qty = int(entry_qty.get())
    except ValueError:
        output.insert(ctk.END,"Enter a number.\n")
        return
    if sell_good in inventory:
        if sell_qty <= inventory[sell_good]["qty"]:
            inventory[sell_good]["qty"] -= sell_qty
            output.insert(ctk.END, f"Sold {sell_good} by {sell_qty}\n")
        else:
            output.insert(ctk.END,"Not enough quantity.\n")
    else:
        output.insert(ctk.END,"Not a valid good\n")

def view():
    for goods in inventory:
        output.insert(ctk.END,f"Good: {goods}, Quantity: {inventory[goods]['qty']}, Price: {inventory[goods]['price']}\n")

def value():
    value_goods = 0
    for goods in inventory:
        value_goods += inventory[goods]['qty'] * inventory[goods]['price']
    output.insert(ctk.END,f"The value of all goods in your inventory is {value_goods}\n")

def savenquit():
    with open("inv.json", "w") as inv:
        json.dump(inventory, inv)
    quit()
entry_search.bind("<KeyRelease>", search)
make_button("Add Item",       add_good,  "#2ecc71", "#27ae60")
make_button("Restock",        restock,   "#3498db", "#2980b9")
make_button("Sell",           sell,      "#e74c3c", "#c0392b")
make_button("View Inventory", view,      "#9b59b6", "#8e44ad")
make_button("Total Value",    value,     "#f39c12", "#d68910")
make_button("Quit",           savenquit, "#7f8c8d" , "#616a6b")

root.mainloop()


        
        
