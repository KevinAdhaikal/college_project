from os import system
from db import table_method

import keyboard # third party (pip install keyboard)
import utils # library gw sendiri
import main # default dari python (sudah di sediakan dari python. bukan third-party)
import locale # default dari python (sudah di sediakan dari python. bukan third-party)

daftar_barang_table: table_method = None

def init(db):
    locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8') # berfungsi untuk mengatur currency (mata uang).
    global daftar_barang_table
    daftar_barang_table = db["daftar_barang"].use_table("daftar_barang")
    default()

def tambah_barang(nama_barang="", jumlah_barang=None, harga_modal=None, harga_jual=None, barcode_barang="", error_text=None):
    system("cls")
    system("title TerminalKasir ^| Tambah Barang")

    if error_text != None: # Jika error_text tidak sama dengan None (Kosong)
        print("[ERROR] " + error_text + "\n")
        error_text = None

    print("|===========================|")
    print("|       Tambah Barang       |")
    print("|===========================|\n")
    print("Tekan CTRL + C untuk kembali ke menu utama.\n")

    try:
        if nama_barang == "":
            while True:
                try:
                    nama_barang = input("Nama Barang: ")
                    if nama_barang == "": tambah_barang(error_text="Input Nama Barang tidak boleh kosong!")
                    else: break
                except KeyboardInterrupt: default(info_text="Operasi Tambah Barang dibatalkan.")
        else: print("Nama Barang: " + nama_barang)

        if jumlah_barang is None:
            while True:
                try:
                    jumlah_barang = int(input("Jumlah Barang: "))
                    if type(jumlah_barang) is int: break
                    else: tambah_barang(nama_barang, error_text="Input Jumlah Barang tidak boleh kosong dan harus berbentuk Angka!")
                except KeyboardInterrupt: default(info_text="Operasi Tambah Barang dibatalkan.")
                except ValueError: tambah_barang(nama_barang, error_text="Input Jumlah Barang tidak boleh kosong dan harus berbentuk Angka!")
        else: print("Jumlah Barang: " + str(jumlah_barang))

        if harga_modal is None:
            while True:
                try:
                    harga_modal = int(input("Harga Modal: "))
                    if type(harga_modal) is int: break
                    else: tambah_barang(nama_barang, jumlah_barang, error_text="Input Harga Modal tidak boleh kosong dan harus berbentuk Angka!")
                except KeyboardInterrupt: default(info_text="Operasi Tambah Barang dibatalkan.")
                except ValueError: tambah_barang(nama_barang, jumlah_barang, error_text="Input Harga Modal tidak boleh kosong dan harus berbentuk Angka!")
        else: print("Harga Modal: " + str(harga_modal))

        if harga_jual is None:
            while True:
                try:
                    harga_jual = int(input("Harga Jual: "))
                    if type(harga_jual) is int: break
                    else: tambah_barang(nama_barang, jumlah_barang, harga_modal, error_text="Input Jumlah Barang tidak boleh kosong dan harus berbentuk Angka!")
                except KeyboardInterrupt: default(info_text="Operasi Tambah Barang dibatalkan.")
                except ValueError: tambah_barang(nama_barang, jumlah_barang, harga_modal, error_text="Input Harga Modal tidak boleh kosong dan harus berbentuk Angka!")
        else: print("Harga Jual: " + str(harga_jual))

        barcode_barang = input("Barcode Barang (Opsional, kosongkan jika tidak ada.): ")

        list_table = list(daftar_barang_table.select(["nama_barang", "barcode_barang"]).values()) # SELECT nama_barang, barcode_barang from daftar_barang

        for a in range(len(list_table[0])):
            if list_table[0][a] == nama_barang: default("Barang bernama '" + nama_barang + "' sudah ada, mohon ubah nama barang dengan yang lain")
            elif list_table[1][a] == barcode_barang: default("Kode Barcode '" + barcode_barang + "' sudah ada, mohon ubah barcode barang dengan yang lain.")

        daftar_barang_table.insert(["nama_barang", "jumlah_barang", "harga_modal", "harga_jual", "barcode_barang"], [nama_barang, jumlah_barang, harga_modal, harga_jual, barcode_barang if barcode_barang != "" or barcode_barang != "" else ""])
        default("Barang bernama '" + nama_barang + "' berhasil di tambahkan ke database!")
    except KeyboardInterrupt: default(info_text="Operasi Tambah Barang dibatalkan.")

def list_barang():
    list_table = list(daftar_barang_table.select(["nama_barang", "jumlah_barang", "harga_modal", "harga_jual", "barcode_barang"]).values())
    total_row = len(list_table[0])
    if total_row == 0: default(error_text="Barang belum ada. Mohon tambahkan barang terlebih dahulu.")

    start = 0
    end = 10 if total_row > 10 else total_row
    is_exit = 0

    while True:
        system("cls")
        system("title TerminalKasir ^| List Barang")

        print("|===========================|")
        print("|        List Barang        |")
        print("|===========================|\n")

        print("ESC Untuk Kembali\nkey kanan dan kiri untuk ganti page.\n")
        result = [["ID", "Nama Barang", "Jumlah Barang", "Harga Modal", "Harga Jual", "Barcode Barang"]]
        for a in range(start, end):
            result.append([a, list_table[0][a], list_table[1][a], locale.currency(list_table[2][a], grouping=True)[:-3], locale.currency(list_table[3][a], grouping=True)[:-3], list_table[4][a]])
        utils.print_table(result)
        
        print("\nResult of " + str(start + 1) + " - " + str(end))

        # Keyboard event
        while True:
            key = keyboard.read_event(True)
            if key.event_type == "down":
                if key.name == "esc":
                    is_exit = 1
                    break
                elif key.name == "right":
                    if end < total_row:
                        start = end
                        end = end + 10 if total_row > end + 10 else total_row
                        break
                elif key.name == "left":
                    if start != 0:
                        start -= 10
                        end = start + 10
                        break
                    pass
        
        if is_exit: break
    
    default()

def edit_barang(err_text=None):
    while True:
        system("cls")
        system("title TerminalKasir ^| Edit Barang")
        if err_text is not None:
            print("[ERROR] " + err_text + "\n")
            err_text = None

        print("|===========================|")
        print("|        Edit Barang        |")
        print("|===========================|\n")
        print("Tekan CTRL + C untuk kembali ke menu utama.\n")

        table_list = list(daftar_barang_table.select(["nama_barang", "jumlah_barang", "harga_modal", "harga_jual", "barcode_barang"]).values())
        try:
            barang_id = int(input("Mohon input ID Barang yang ingin di edit: "))
        except KeyboardInterrupt: default(info_text="Operasi Edit Barang dibatalkan.")
        except ValueError: err_text="ID Barang harus berupa angka."

        if len(table_list[0]) > barang_id: # karena ID Barang sesuai dengan loop, jadi kita buat cek id nya ada atau tidak dengan cara cek length.
            while True:
                system("cls")

                if err_text is not None:
                    print("[ERROR] " + err_text + "\n")
                    err_text = None

                print("|===========================|")
                print("|        Edit Barang        |")
                print("|===========================|\n")
                print("Tekan CTRL + C untuk membatal pengeditan.\n")
                print(f"""1. Edit Nama Barang: {table_list[0][barang_id]}
2. Edit Jumlah Barang: {table_list[1][barang_id]}
3. Edit Harga Modal: {table_list[2][barang_id]}
4. Edit Harga Jual: {table_list[3][barang_id]}
5. Edit Barcode Barang: {table_list[4][barang_id]}
6. Simpan dan Kembali ke Menu Daftar Barang
7. Kembali ke Menu Daftar Barang\n""")
                
                try:
                    user_input = int(input("Mohon masukkan angka (1 - 7): "))
                except KeyboardInterrupt: err_text="Input tidak valid. Mohon masukkan angka antara 1 dan 7."
                except ValueError: err_text="Input tidak valid. Mohon masukkan angka antara 1 dan 7."

                if user_input == 1:
                    while True:
                        try:
                            temp = input("Edit Nama Barang: ")
                        except KeyboardInterrupt: pass
                        if temp is None or temp == "": print("[ERROR] Nama Barang tidak boleh kosong.")
                        table_list[0][barang_id] = temp
                        break
                if user_input == 2:
                    while True:
                        try:
                            table_list[1][barang_id] = int(input("Edit Jumlah Barang: "))
                        except KeyboardInterrupt: pass
                        except ValueError: print("[ERROR] Jumlah Barang tidak boleh kosong dan harus berupa angka.")
                        break
                if user_input == 3:
                    while True:
                        try:
                            table_list[2][barang_id] = int(input("Edit Harga Modal: "))
                        except KeyboardInterrupt: pass
                        except ValueError: print("[ERROR] Harga Modal tidak boleh kosong dan harus berupa angka.")
                        break
                if user_input == 4:
                    while True:
                        try:
                            table_list[3][barang_id] = int(input("Edit Harga Jual: "))
                        except KeyboardInterrupt: pass
                        except ValueError: print("[ERROR] Harga Jual tidak boleh kosong dan harus berupa angka.")
                        break
                if user_input == 5:
                    try:
                        table_list[4][barang_id] = input("Edit Barcode Barang: ")
                    except KeyboardInterrupt: pass
                if user_input == 6:
                    daftar_barang_table.modify(
                        barang_id,
                        ["nama_barang", "jumlah_barang", "harga_modal", "harga_jual", "barcode_barang"],
                        [table_list[0][barang_id], table_list[1][barang_id], table_list[2][barang_id], table_list[3][barang_id], table_list[4][barang_id]]
                    )
                    default(info_text="Barang tersebut berhasil di edit.")
                if user_input == 7:
                    default(info_text="Operasi Edit Barang dibatalkan.")
        else: err_text="ID Barang tersebut tidak ada. Mohon input ID barang yang benar."

def hapus_barang(err_text = None):
    system("title TerminalKasir ^| Hapus Barang")
    table_list = list(daftar_barang_table.select(["nama_barang"]).values())

    while True:
        system("cls")

        if err_text is not None:
            print("[ERROR] " + err_text + "\n")
            err_text = None

        print("|===========================|")
        print("|       Hapus Barang        |")
        print("|===========================|\n")
        print("Tekan CTRL + C untuk kembali ke menu utama.\n")

        try:
            barang_id = int(input("Mohon input ID Barang yang ingin di edit: "))

            if len(table_list[0]) > barang_id:
                try:
                    y_or_n = input("Anda yakin ingin menghapus barang bernama '" + table_list[0][barang_id] + "'? (Y/N): ").lower()
                    if y_or_n == 'y':
                        daftar_barang_table.delete(barang_id)
                        default("Barang bernama '" + table_list[0][barang_id] + "' berhasil di hapus.")
                    else:
                        default("Barang bernama '" + table_list[0][barang_id] + "' tidak jadi di hapus.")
                except KeyboardInterrupt: default(info_text="Operasi Hapus Barang dibatalkan.")
            else: err_text="ID Barang tersebut tidak ada. Mohon input ID barang yang benar."
        except KeyboardInterrupt: default(info_text="Operasi Hapus Barang dibatalkan.")
        except ValueError: err_text="ID Barang harus berupa angka."

def default(info_text=None, error_text=None):
    while True:
        system("title TerminalKasir ^| Daftar Barang")
        system("cls")

        if info_text is not None:
            print("[INFO] " + info_text + "\n")
            info_text = None
        elif error_text is not None:
            print("[ERROR] " + error_text + "\n")
            error_text = None

        print("|===========================|")
        print("|       Daftar Barang       |")
        print("|===========================|\n")
        print("1. Tambah Barang")
        print("2. List Barang")
        print("3. Edit Barang")
        print("4. Hapus Barang")
        print("5. Kembali ke Menu Utama\n")
        try:
            user_input = int(input("Mohon masukkan angka pada menu yang tertera (1 - 5): "))
            if user_input == 1: tambah_barang()
            elif user_input == 2: list_barang()
            elif user_input == 3: edit_barang()
            elif user_input == 4: hapus_barang()
            elif user_input == 5:
                global daftar_barang_table
                del(daftar_barang_table) # ini buat nge deinitialize class table.
                main.default() # kembali ke menu utama
            else: error_text="Input tidak valid. Mohon masukkan angka antara 1 dan 5."
        except ValueError: error_text="Input tidak valid. Mohon masukkan angka antara 1 dan 5."

if __name__ == "__main__":
    print("This file should be a module file, not a main file.")