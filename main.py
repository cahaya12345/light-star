
import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

FILE_NAME = "data.csv"


if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Tanggal", "Keterangan", "Tipe", "Jumlah"])

# Fungsi load data
def load_data():
    with open(FILE_NAME, newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)

# Fungsi simpan data
def save_data(data):
    with open(FILE_NAME, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Tanggal", "Keterangan", "Tipe", "Jumlah"])
        for row in data:
            writer.writerow([row["Tanggal"], row["Keterangan"], row["Tipe"], row["Jumlah"]])

# Fungsi hitung saldo akhir
def get_saldo(data):
    saldo = 0
    for row in data:
        if row["Tipe"] == "Pemasukan":
            saldo += int(row["Jumlah"])
        elif row["Tipe"] == "Pengeluaran":
            saldo -= int(row["Jumlah"])
    return saldo

# GUI
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Manajemen Keuangan Pribadi")

        self.data = load_data()
        self.selected_index = None

        # Form input
        self.label_ket = tk.Label(root, text="Keterangan:")
        self.entry_ket = tk.Entry(root)
        self.label_jumlah = tk.Label(root, text="Jumlah:")
        self.entry_jumlah = tk.Entry(root)
        self.label_tipe = tk.Label(root, text="Tipe:")
        self.combo_tipe = ttk.Combobox(root, values=["Pemasukan", "Pengeluaran"])
        self.combo_tipe.current(0)

        self.btn_tambah = tk.Button(root, text="Tambah", command=self.tambah_data)
        self.btn_update = tk.Button(root, text="Ubah", command=self.ubah_data)
        self.btn_hapus = tk.Button(root, text="Hapus", command=self.hapus_data)

        self.label_saldo = tk.Label(root, text="Saldo: Rp 0", font=("Arial", 12, "bold"))

        # Tabel riwayat
        self.tree = ttk.Treeview(root, columns=("Tanggal", "Keterangan", "Tipe", "Jumlah"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.bind("<<TreeviewSelect>>", self.select_item)

        # Layout
        self.label_ket.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_ket.grid(row=0, column=1, padx=5, pady=5)
        self.label_jumlah.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_jumlah.grid(row=1, column=1, padx=5, pady=5)
        self.label_tipe.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.combo_tipe.grid(row=2, column=1, padx=5, pady=5)

        self.btn_tambah.grid(row=0, column=2, padx=5, pady=5)
        self.btn_update.grid(row=1, column=2, padx=5, pady=5)
        self.btn_hapus.grid(row=2, column=2, padx=5, pady=5)

        self.label_saldo.grid(row=3, column=0, columnspan=3, pady=10)
        self.tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for idx, row in enumerate(self.data):
            self.tree.insert("", "end", iid=idx, values=(row["Tanggal"], row["Keterangan"], row["Tipe"], row["Jumlah"]))
        self.label_saldo.config(text=f"Saldo: Rp {get_saldo(self.data):,}".replace(",", "."))

    def tambah_data(self):
        ket = self.entry_ket.get()
        jumlah = self.entry_jumlah.get()
        tipe = self.combo_tipe.get()
        if not ket or not jumlah.isdigit():
            messagebox.showwarning("Input salah", "Isi keterangan dan jumlah dengan benar.")
            return
        tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data.append({"Tanggal": tanggal, "Keterangan": ket, "Tipe": tipe, "Jumlah": jumlah})
        save_data(self.data)
        self.refresh()
        self.clear_input()

    def select_item(self, event):
        selected = self.tree.selection()
        if selected:
            self.selected_index = int(selected[0])
            row = self.data[self.selected_index]
            self.entry_ket.delete(0, tk.END)
            self.entry_ket.insert(0, row["Keterangan"])
            self.entry_jumlah.delete(0, tk.END)
            self.entry_jumlah.insert(0, row["Jumlah"])
            self.combo_tipe.set(row["Tipe"])

    def ubah_data(self):
        if self.selected_index is None:
            messagebox.showwarning("Pilih Data", "Pilih data yang akan diubah.")
            return
        ket = self.entry_ket.get()
        jumlah = self.entry_jumlah.get()
        tipe = self.combo_tipe.get()
        if not ket or not jumlah.isdigit():
            messagebox.showwarning("Input salah", "Isi keterangan dan jumlah dengan benar.")
            return
        self.data[self.selected_index]["Keterangan"] = ket
        self.data[self.selected_index]["Jumlah"] = jumlah
        self.data[self.selected_index]["Tipe"] = tipe
        save_data(self.data)
        self.refresh()
        self.clear_input()
        self.selected_index = None

    def hapus_data(self):
        if self.selected_index is None:
            messagebox.showwarning("Pilih Data", "Pilih data yang akan dihapus.")
            return
        del self.data[self.selected_index]
        save_data(self.data)
        self.refresh()
        self.clear_input()
        self.selected_index = None

    def clear_input(self):
        self.entry_ket.delete(0, tk.END)
        self.entry_jumlah.delete(0, tk.END)
        self.combo_tipe.current(0)

# Jalankan aplikasi
root = tk.Tk()
app = App(root)
root.mainloop()
