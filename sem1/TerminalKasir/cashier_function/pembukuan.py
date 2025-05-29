from os import system
from db import database

import locale
import main
import time
import utils
import sys

pembukuan_db: database = None

def init(db):
    global pembukuan_db
    pembukuan_db = db["pembukuan"]
    locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8') # berfungsi untuk mengatur currency (mata uang).

    default()

def print_pembukuan(tanggal):
    if pembukuan_db.info_table().get(tanggal) is None: return -1

    table = pembukuan_db.use_table(tanggal)
    isi_table = list(table.select("*").values())

    result_table = [["Nomor", "Nama Barang", "Jumlah Barang", "Harga Barang", "Waktu"]]
    total_hasil = [0, 0]

    for a in range(len(isi_table[0])):
        result_table.append([
            str(a + 1), # Nomor
            isi_table[0][a],
            isi_table[1][a],
            locale.currency(isi_table[2][a], grouping=True)[:-3],
            isi_table[3][a],
        ])

        total_hasil[0] += isi_table[1][a]
        total_hasil[1] += isi_table[2][a]

    utils.print_table(result_table, footer_text=["", "", "Jumlah Barang: " + str(total_hasil[0]), "Jumlah Uang: " + locale.currency(total_hasil[1], grouping=True)[:-3], ""])
    print("\nTekan Enter untuk kembali ke Menu Pembukuan.", end="")
    sys.stdin.read(1)
    return 0

def default():
    error_text = None
    system("title TerminalKasir ^| Pembukuan")

    while True:
        system("cls")

        if error_text != None: # Jika error_text tidak sama dengan None (Kosong)
            print("[ERROR] " + error_text + "\n")
            error_text = None

        print("|===========================|")
        print("|         Pembukuan         |")
        print("|===========================|\n")
        print("1. Pembukuan Hari ini")
        print("2. Pembukuan Sesuai Tanggal")
        print("3. List Tanggal Pembukuan")
        print("4. Kembai ke Menu Utama\n")

        try:
            user_input = int(input("Mohon masukkan angka pada menu yang tertera (1 - 4): "))
            if user_input == 1:
                system("cls")
                print("|===========================|")
                print("|         Pembukuan         |")
                print("|===========================|\n")
                if print_pembukuan(time.strftime("%d_%m_%Y", time.localtime())) == -1:
                    error_text = "Hari ini belum ada catatan pembukuan sama sekali."
                    continue
            elif user_input == 2:
                system("cls")
                print("|===========================|")
                print("|         Pembukuan         |")
                print("|===========================|\n")

                result_table = [["Tanggal"]]
                for list_tanggal in list(pembukuan_db.info_table().keys()): result_table.append([list_tanggal])

                utils.print_table(result_table)
                print("\nTekan Enter untuk kembali ke Menu Pembukuan.", end="")
                sys.stdin.read(1)

            elif user_input == 3:
                while True: # 
                    system("cls")
                    print("|===========================|")
                    print("|         Pembukuan         |")
                    print("|===========================|\n")
                    print("Tekan CTRL + C Untuk kembali ke menu pembukuan.\n")
                    if error_text != None: # Jika error_text tidak sama dengan None (Kosong)
                        print("[ERROR] " + error_text + "\n")
                        error_text = None

                    try:
                        user_input = input("Mohon masukkan tanggal (Contoh: atau DD_MM_YYYY): ")
                    except KeyboardInterrupt: break
                    print("\n")
                    if print_pembukuan(user_input) == -1:
                        error_text = "Pembukuan pada tanggal " + user_input + " tidak ada."
                    else: break
            elif user_input == 4:
                main.default()
            else: error_text="Input tidak valid. Mohon masukkan angka antara 1 dan 4."
        except ValueError: error_text="Input tidak valid. Mohon masukkan angka antara 1 dan 4."

if __name__ == "__main__":
    print("This file should be a module file, not a main one.")