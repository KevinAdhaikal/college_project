from os import system
from public_var import antrian
import display_antrian as display

def controller():
    notify_type = None
    notify_text = None
    is_changed = False

    canvas = antrian["display_canvas"]

    while 1:
        obat_peek = {"nama_pasien": None, "nomor_antrian": None} if antrian["antrian_obat"].peek() is None else antrian["antrian_obat"].peek()
        obat_next_peek = {"nama_pasien": None, "nomor_antrian": None} if antrian["antrian_obat"].peek_next() is None else antrian["antrian_obat"].peek_next()
        pembayaran_peek = {"nama_pasien": None, "nomor_antrian": None} if antrian["antrian_pembayaran"].peek() is None else antrian["antrian_pembayaran"].peek()
        pembayaran_next_peek = {"nama_pasien": None, "nomor_antrian": None} if antrian["antrian_pembayaran"].peek_next() is None else antrian["antrian_pembayaran"].peek_next()

        system("clear")

        if notify_type != None: # Jika error_text tidak sama dengan None (Kosong)
            print(f"[{notify_type}] {notify_text}\n")
            notify_type = None
            notify_text = None

        if is_changed is True:
            is_changed = False

            canvas.after(0, lambda: canvas.itemconfig(antrian["cao_label"], text=obat_peek["nomor_antrian"] if obat_peek["nomor_antrian"] is not None else "Kosong"))
            canvas.after(0, lambda: canvas.itemconfig(antrian["cap_label"], text=pembayaran_peek["nomor_antrian"] if pembayaran_peek["nomor_antrian"] is not None else "Kosong"))
            canvas.after(0, lambda: canvas.itemconfig(antrian["nao_label"], text=obat_next_peek["nomor_antrian"] if obat_next_peek["nomor_antrian"] is not None else "Kosong"))
            canvas.after(0, lambda: canvas.itemconfig(antrian["nap_label"], text=pembayaran_next_peek["nomor_antrian"] if pembayaran_next_peek["nomor_antrian"] is not None else "Kosong"))
        
        print("==================================")
        print("|     Controller Rumah Sakit     |")
        print("==================================")
        print(f"""
- Antrian Obat
Antrian Sekarang: {"Kosong" if obat_peek["nomor_antrian"] is None else obat_peek["nomor_antrian"]}
Nama Pasien Sekarang: {"Kosong" if obat_peek["nama_pasien"] is None else obat_peek["nama_pasien"]}
Antrian Selanjutnya: {"Kosong" if obat_next_peek["nomor_antrian"] is None else obat_next_peek["nomor_antrian"]}
Nama Pasien Selanjutnya: {"Kosong" if obat_next_peek["nama_pasien"] is None else obat_next_peek["nama_pasien"]}

- Antrian Pembayaran
Antrian Sekarang: {"Kosong" if pembayaran_peek["nomor_antrian"] is None else pembayaran_peek["nomor_antrian"]}
Nama Pasien Sekarang: {"Kosong" if pembayaran_peek["nama_pasien"] is None else pembayaran_peek["nama_pasien"]}
Antrian Selanjutnya: {"Kosong" if pembayaran_next_peek["nomor_antrian"] is None else pembayaran_next_peek["nomor_antrian"]}
Nama Pasien Selanjutnya: {"Kosong" if pembayaran_next_peek["nama_pasien"] is None else pembayaran_next_peek["nama_pasien"]}

1. Next Antrian Obat
2. Next Antrian Pembayaran
3. Kembali ke menu utama
""")
        
        try:
            user_input = int(input("Mohon masukkan angka pada menu yang tertera (1 - 3): "))

            if user_input == 1:
                if obat_next_peek["nomor_antrian"] is None:
                    notify_type = "ERROR"
                    notify_text ="Gagal mengganti antrian obat dikarenakan antrian selanjutnya masih kosong."
                else:
                    antrian["antrian_obat"].dequeue()

                    is_changed = True
                    notify_type = "INFO"
                    notify_text ="Berhasil mengganti antrian obat ke selanjutnya."
            elif user_input == 2:
                if pembayaran_next_peek["nomor_antrian"] is None:
                    notify_type = "ERROR"
                    notify_text ="Gagal mengganti antrian pembayaran dikarenakan antrian selanjutnya masih kosong."
                else:
                    antrian["antrian_pembayaran"].dequeue()

                    is_changed = True
                    notify_type = "INFO"
                    notify_text ="Berhasil mengganti antrian pembayaran ke selanjutnya."
            elif user_input == 3:
                break
            else:
                notify_type = "ERROR"
                notify_text ="Input tidak valid. Mohon masukkan angka antara 1 dan 3."
        except ValueError:
            notify_type = "ERROR"
            notify_text ="Input tidak valid. Mohon masukkan angka antara 1 dan 3."

if __name__ == "__main__":
    print("This file is a module, not a main.")