from db import database
from db import database_type as db_type
from os import system
from database_var import database_kasir as db

import cashier_function.daftar_barang as daftar_barang
import cashier_function.kasir as kasir
import cashier_function.pembukuan as pembukuan

def default():
    error_text=None

    while True:
        system("title TerminalKasir ^| Menu Utama")
        system("cls")

        if error_text != None: # Jika error_text tidak sama dengan None (Kosong)
            print("[ERROR] " + error_text + "\n")
            error_text = None

        print("|===========================|")
        print("|       TerminalKasir       |")
        print("|===========================|\n")
        print("1. Daftar Barang")
        print("2. Kasir")
        print("3. Pembukuan")
        print("4. Keluar\n")

        try:
            user_input = int(input("Mohon masukkan angka pada menu yang tertera (1 - 4): "))
            if user_input == 1:
                daftar_barang.init(db)
            elif user_input == 2:
                kasir.init(db)
            elif user_input == 3:
                pembukuan.init(db)
            elif user_input == 4:
                exit(0)
            else: error_text="Input tidak valid. Mohon masukkan angka antara 1 dan 4."
        except ValueError: error_text="Input tidak valid. Mohon masukkan angka antara 1 dan 4."
    
if __name__ == "__main__": # jika dia ngejalanin ini menggunakan "python main.py", bukan nge import. dia bakalan jalan code dibawah
    # load database
    db["daftar_barang"] = database("daftar_barang", False, True)
    db["pembukuan"] = database("pembukuan", False, True)

    # check requirement dari database database tersebut
    if len(list(db["daftar_barang"].info_table().keys())) == 0:
        db["daftar_barang"].create_table("daftar_barang", {
            "nama_barang": db_type.STRING,
            "jumlah_barang": db_type.INT,
            "harga_modal": db_type.INT,
            "harga_jual": db_type.INT,
            "barcode_barang": db_type.STRING
        })

    default()