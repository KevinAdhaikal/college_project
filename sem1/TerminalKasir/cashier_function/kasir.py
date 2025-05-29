from os import system
from db import table_method
from db import database_type
from db import database

import utils
import locale
import main
import sys
import time

list_barang_dibeli = None
total_dibeli = [0, 0]
daftar_barang_table: table_method = None
pembukuan_db: database = None
current_id = 0
footer = None

def init(db):
    global list_barang_dibeli
    global total_dibeli
    global daftar_barang_table
    global footer
    global current_id
    global pembukuan_db

    current_id = 0
    list_barang_dibeli = [["ID", "Nama Barang", "Jumlah Barang", "Harga Barang"]]
    total_dibeli = [0, 0]
    locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8') # berfungsi untuk mengatur currency (mata uang).
    daftar_barang_table = db["daftar_barang"].use_table("daftar_barang")
    pembukuan_db = db["pembukuan"]
    footer = ["", "", "Jumlah Barang: 0", "Harga Barang: Rp0"]

    default()

def default(err_text = None, info_text = None):
    system("title TerminalKasir ^| Kasir")
    global current_id
    global list_barang_dibeli
    global total_dibeli
    global footer

    while True:
        system("cls")
        if err_text != None: # Jika error_text tidak sama dengan None (Kosong)
            print("[ERROR] " + err_text + "\n")
            err_text = None
        if info_text != None: # Jika info_text tidak sama dengan None (Kosong)
            print("[INFO] " + info_text + "\n")
            info_text = None

        print("[INFO] Ketik '?', 'h' atau 'help' untuk mendapatkan command.")
        utils.print_table(list_barang_dibeli, footer_text=footer)
        user_input = input("\n: ").lower()

        if user_input == 'h' or user_input == '?' or user_input == "help":
            print("""\ndelete <ID Barang>: Menghapus spesifikasi barang yang tertera di layar.
find <Nama Barang>: Mencari barang dengan nama, dan menambahkan barang ke layar kasir.
edit <ID Barang> <jumlah barang>: Mengubah spesifikasi jumlah barang yang tertera di layar.
add <ID Barang> <jumlah Barang (Optional)>: Menambahkan barang sesuai ID dari Daftar barang.
exit/quit: Keluar dari kasir dan kembali ke menu utama.
bayar: Bayar dari seluruh yang tertera di layar, dan akan masuk ke pembukuan.
Tidak memasukkan command sama sekali: menambahkan barang ke layar kasir dengan sesuai barcode barang.

Tekan enter untuk kembali ke kasir.""", end="")
            sys.stdin.read(1)
            default()
        elif user_input == "exit" or user_input == "quit":
            global daftar_barang_table
            del(daftar_barang_table)
            daftar_barang_table = None
            main.default()
        elif "edit" in user_input:
            arg_input = user_input[5:].split(" ")

            if len(arg_input) < 1:
                err_text="Command 'edit' harus berisi 2 argumen: <ID Barang> <Jumlah Barang>"
                continue
            try:
                arg_input[0] = int(arg_input[0]) + 1
            except ValueError:
                err_text = "Argumen 'ID Barang' harus berupa angka."
                continue

            try:
                arg_input[1] = int(arg_input[1])
                if arg_input[1] < 1:
                    err_text = "Argumen 'Jumlah Barang' tidak boleh di bawah angka 1."
                    continue
            except ValueError:
                err_text = "Argumen 'Jumlah Barang' tidak boleh kosong dan harus berupa angka."
                continue

            if len(list_barang_dibeli) < arg_input[0]:
                err_text = "ID Barang tidak di temukan di layar"

            select_data = list(daftar_barang_table.select(["nama_barang", "harga_jual"]).values())
            for a in range(len(select_data[0])):
                if select_data[0][a] == list_barang_dibeli[arg_input[0]][1]:
                    list_barang_dibeli[arg_input[0]][2] = str(arg_input[1])
                    list_barang_dibeli[arg_input[0]][3] = locale.currency(select_data[1][a] * arg_input[1], grouping=True)[:-3]
                    break

            # menghitung ulang bagian total_dibeli
            total_dibeli[0] = 0
            total_dibeli[1] = 0
            for a in range(1, len(list_barang_dibeli), 1):
                total_dibeli[0] += int(list_barang_dibeli[a][2])
                total_dibeli[1] += utils.indo_currency_to_int(list_barang_dibeli[a][3])

            footer[2] = "Jumlah Barang: " + str(total_dibeli[0])
            footer[3] = "Harga Barang: " + locale.currency(total_dibeli[1], grouping=True)[:-3]

            continue
        elif "add" in user_input:
            arg_input = user_input[4:].split(" ")

            if len(arg_input) < 0:
                err_text="Command 'add' harus berisi 2 argumen: <ID Barang> <Jumlah (Optional)>"
                continue
            try:
                arg_input[0] = int(arg_input[0])
            except ValueError:
                err_text = "Argumen 'ID Barang' harus berupa angka."
                continue
            try:
                if arg_input[1] is not None:
                    try:
                        arg_input[1] = int(arg_input[1])
                        if arg_input[1] < 1:
                            err_text = "Argumen 'Jumlah Barang' tidak boleh di bawah angka 1."
                            continue
                    except ValueError:
                        err_text = "Argumen 'Jumlah Barang' harus berupa angka."
                        continue
            except:
                arg_input.append(1)

            is_merge = 0
            result = list(daftar_barang_table.select(["nama_barang", "jumlah_barang", "harga_jual", "barcode_barang"]).values())
            if len(result[0]) > arg_input[0]:
                for b in range(1, len(list_barang_dibeli), 1):
                    if list_barang_dibeli[b][1] == result[0][arg_input[0]]:
                        list_barang_dibeli[b][2] = str(int(list_barang_dibeli[b][2]) + (1 if arg_input[1] is not int and arg_input[1] == 0 else arg_input[1]))
                        list_barang_dibeli[b][3] = locale.currency(
                            utils.indo_currency_to_int(
                                list_barang_dibeli[b][3]
                            ) + (result[2][arg_input[0]] if arg_input[1] is not int and arg_input[1] == 0 else (result[2][arg_input[0]] * arg_input[1])), grouping=True
                        )[:-3]
                        is_merge = 1
                        break
                if not is_merge:
                    list_barang_dibeli.append([
                        current_id,
                        result[0][arg_input[0]],
                        1 if arg_input[1] is not int and arg_input[1] == 0 else arg_input[1],
                        locale.currency(result[2][arg_input[0]] if arg_input[1] is not int and arg_input[1] == 0 else (result[2][arg_input[0]] * arg_input[1]),
                        grouping=True)[:-3]]
                    )
                    current_id += 1
                total_dibeli[0] += 1 if arg_input[1] is not int and arg_input[1] == 0 else arg_input[1]
                total_dibeli[1] += result[2][arg_input[0]] if arg_input[1] is not int and arg_input[1] == 0 else (result[2][arg_input[0]] * arg_input[1])

                footer[2] = "Jumlah Barang: " + str(total_dibeli[0])
                footer[3] = "Harga Barang: " + locale.currency(total_dibeli[1], grouping=True)[:-3]
            else:
                err_text="ID Barang tersebut tidak ada. Mohon input ID barang yang benar."
                continue
        elif "find" in user_input:
            user_input = user_input[5:].lower()
            if user_input == "":
                err_text = "Mohon input nama barang."
                continue

            filter_barang = [["ID", "Nama Barang", "Harga Barang", "Barcode Barang"]]
            select_table = list(daftar_barang_table.select(["nama_barang", "harga_jual", "barcode_barang"]).values())

            total_filter = 0
            for a in range(len(select_table[0])):
                if user_input in select_table[0][a].lower():
                    filter_barang.append([total_filter, select_table[0][a], locale.currency(select_table[1][a], grouping=True)[:-3], select_table[2][a]])
                    total_filter += 1

            if total_filter == 0:
                err_text = "Barang bernama '" + user_input + "' tidak di temukan."
                continue
            elif total_filter == 1:
                # check list_barang_beli dulu
                is_merge = 0
                for b in range(1, len(list_barang_dibeli), 1):
                    if list_barang_dibeli[b][1] == filter_barang[1][1]:
                        list_barang_dibeli[b][2] = str(int(list_barang_dibeli[b][2]) + 1)
                        list_barang_dibeli[b][3] = locale.currency(utils.indo_currency_to_int(list_barang_dibeli[b][3]) + utils.indo_currency_to_int(filter_barang[1][2]), grouping=True)[:-3]
                        is_merge = 1
                        break
                
                if not is_merge:
                    list_barang_dibeli.append([current_id, filter_barang[1][1], 1, filter_barang[1][2]])
                    current_id += 1

                total_dibeli[0] += 1
                total_dibeli[1] += utils.indo_currency_to_int(filter_barang[1][2])

                footer[2] = "Jumlah Barang: " + str(total_dibeli[0])
                footer[3] = "Harga Barang: " + locale.currency(total_dibeli[1], grouping=True)[:-3]
                continue
            else:
                while True:
                    system("cls")

                    if err_text != None: # Jika error_text tidak sama dengan None (Kosong)
                        print("[ERROR] " + err_text + "\n")
                        err_text = None

                    print("|===========================|")
                    print("|        Cari Barang        |")
                    print("|===========================|\n")
                    utils.print_table(filter_barang)
                    print("\nTekan CTRL + C untuk kembali ke menu kasir.")
                    try:
                        user_input = int(input("\nMohon masukkan ID Barang yang ingin masuk ke kasir: ")) + 1
                    except ValueError:
                        err_text = "Mohon masukkan ID Barang yang sesuai pada di tampian tersebut."
                        continue
                    except KeyboardInterrupt:
                        info_text = "Operasi Cari Barang dibatalkan."
                        break
                    
                    if user_input < 1:
                        err_text = "Input ID Barang tidak boleh di bawah angka 0."
                        continue
                    if (len(filter_barang) - 1) < user_input:
                        err_text = "ID Barang tidak sesuai. mohon masukkan ID Barang sesuai di layar anda."
                        continue

                    # check list_barang_beli dulu
                    is_merge = 0
                    for b in range(1, len(list_barang_dibeli), 1):
                        if list_barang_dibeli[b][1] == filter_barang[user_input][1]:
                            list_barang_dibeli[b][2] = str(int(list_barang_dibeli[b][2]) + 1)
                            list_barang_dibeli[b][3] = locale.currency(utils.indo_currency_to_int(list_barang_dibeli[b][3]) + utils.indo_currency_to_int(filter_barang[user_input][2]), grouping=True)[:-3]
                            is_merge = 1
                            break

                    if not is_merge:
                        list_barang_dibeli.append([current_id, filter_barang[user_input][1], 1, filter_barang[user_input][2]])
                        current_id += 1

                    total_dibeli[0] += 1
                    total_dibeli[1] += utils.indo_currency_to_int(filter_barang[user_input][2])

                    footer[2] = "Jumlah Barang: " + str(total_dibeli[0])
                    footer[3] = "Harga Barang: " + locale.currency(total_dibeli[1], grouping=True)[:-3]
                    break
        elif "remove" in user_input:
            try:
                user_input = int(user_input[7:]) + 1
            except:
                err_text = "Mohon masukkan ID Barang."
                continue
            if user_input < 1:
                err_text = "Mohon masukkan ID Barang."
                continue

            if len(list_barang_dibeli) <= user_input:
                err_text = "ID Barang tersebut tidak ada."

            total_dibeli[0] -= int(list_barang_dibeli[user_input][2])
            total_dibeli[1] -= utils.indo_currency_to_int(list_barang_dibeli[user_input][3])

            footer[2] = "Jumlah Barang: " + str(total_dibeli[0])
            footer[3] = "Harga Barang: " + locale.currency(total_dibeli[1], grouping=True)[:-3]

            del list_barang_dibeli[user_input]

            current = 0
            for a in list_barang_dibeli[1:]:
                a[0] = current
                current = current + 1
        elif user_input == "bayar":
            if len(list_barang_dibeli) == 1:
                err_text = "Barang masih kosong."
                continue

            keluar_dari_bayar = 0
            while True:
                system("cls")
                if err_text != None: # Jika error_text tidak sama dengan None (Kosong)
                    print("[ERROR] " + err_text + "\n")
                    err_text = None
                utils.print_table(list_barang_dibeli, footer_text=footer)
                input_uang = 0
                try:
                    input_uang = int(input("\nMasukkan nominal uang yang diberikan pelanggan: "))
                except KeyboardInterrupt:
                    keluar_dari_bayar = 1
                    break
                except ValueError:
                    err_text = "Mohon masukkan nominal uang yang benar, nominal uang berupa angka."
                    continue

                if (input_uang - total_dibeli[1]) < 0:
                    err_text = "Uang tidak cukup."
                    continue
                if (input_uang - total_dibeli[1]) == 0:
                    print("Uang Pas!")
                else: print(f"Kembalian: {input_uang - total_dibeli[1]}")

                tanggal_sekarang = time.strftime("%d_%m_%Y", time.localtime())
                waktu_sekarang = time.strftime("%H:%M:%S", time.localtime())

                if not pembukuan_db.info_table().get(tanggal_sekarang):
                    pembukuan_db.create_table(tanggal_sekarang, {
                        "nama_barang": database_type.STRING,
                        "jumlah_barang": database_type.INT,
                        "harga_barang": database_type.INT,
                        "waktu": database_type.STRING
                    })

                table = pembukuan_db.use_table(tanggal_sekarang)
                daftarbarang_nama_barang = list(daftar_barang_table.select(["nama_barang"]).values())
                daftarbarang_jumlah_barang = list(daftar_barang_table.select(["jumlah_barang"]).values())

                for a in range(1, len(list_barang_dibeli), 1):
                    daftar_barang_table.modify(
                        daftarbarang_nama_barang[0].index(list_barang_dibeli[a][1]),
                        ["jumlah_barang"],
                        [daftarbarang_jumlah_barang[0][daftarbarang_nama_barang[0].index(list_barang_dibeli[a][1])] - int(list_barang_dibeli[a][2])]
                    )
                    table.insert([
                        "nama_barang",
                        "jumlah_barang",
                        "harga_barang",
                        "waktu"
                    ], [
                        list_barang_dibeli[a][1],
                        int(list_barang_dibeli[a][2]),
                        utils.indo_currency_to_int(list_barang_dibeli[a][3]),
                        waktu_sekarang
                        ]
                    )
                print("Barang berhasil masuk ke pembukuan!\n\nTekan Enter untuk kembali ke kasir")
                del table # Deinitialize table.
                sys.stdin.read(1)
                break

            if keluar_dari_bayar: continue

            # initialisasi ulang
            list_barang_dibeli = [["ID", "Nama Barang", "Jumlah Barang", "Harga Barang"]]
            total_dibeli = [0, 0]
            footer = ["", "", "Jumlah Barang: 0", "Harga Barang: Rp0"]
            continue
        elif user_input != "": # pencarian barang dengan cara menggunakan barcode barang
            is_found = 0
            is_merge = 0
            result = list(daftar_barang_table.select(["nama_barang", "jumlah_barang", "harga_jual", "barcode_barang"]).values())
            for a in range(len(result[0])):
                if result[3][a] == user_input:
                    
                    # check list_barang_beli dulu
                    for b in range(1, len(list_barang_dibeli), 1):
                        if list_barang_dibeli[b][1] == result[0][a]:
                            list_barang_dibeli[b][2] = str(int(list_barang_dibeli[b][2]) + 1)
                            list_barang_dibeli[b][3] = locale.currency(utils.indo_currency_to_int(list_barang_dibeli[b][3]) + result[2][a], grouping=True)[:-3]
                            is_found = 1
                            is_merge = 1
                            break

                    if not is_merge:
                        list_barang_dibeli.append([current_id, result[0][a], 1, locale.currency(result[2][a], grouping=True)[:-3]])
                        current_id += 1

                    total_dibeli[0] += 1
                    total_dibeli[1] += result[2][a]

                    footer[2] = "Jumlah Barang: " + str(total_dibeli[0])
                    footer[3] = "Harga Barang: " + locale.currency(total_dibeli[1], grouping=True)[:-3]
                    is_found = 1
                    break
            
            if not is_found: default("Kode barcode '" + user_input + "' tidak ditemukan.")
            # mencari barang dengan barcode.

if __name__ == "__main__":
    print("This file should be a module file, not a main one.")