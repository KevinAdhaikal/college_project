from os import system
from public_var import antrian
from rs_controller import controller
import display_antrian as display
import threading

def main():
    threading.Thread(target=display.init, daemon=True).start()
    antrian["display_ready"].wait_signal()

    notify_type = None
    notify_text = None
    canvas = antrian["display_canvas"]

    while 1:
        system("clear")
        threading.Thread(target=display.thread_time, daemon=True).start()
        
        if notify_type != None: # Jika error_text tidak sama dengan None (Kosong)
            print(f"[{notify_type}] {notify_text}\n")
            notify_type = None
            notify_text = None

        print("===================================")
        print("|       Antrian rumah sakit       |")
        print("===================================")
        print("""
1. Tambah antrian
2. Daftar antrian
3. Kontrol antrian
4. Exit
""")
        
        try:
            user_input = int(input("Mohon masukkan angka pada menu yang tertera (1 - 4): "))
            if user_input == 1:
                system("clear")
                print("Informasi Jenis Antrian\n- o: Obat\n- p: Pembayaran\n")

                try:
                    nama_pasien = input("Nama pasien: ")
                    jenis_antrian = input("Jenis Antrian: ")
                except KeyboardInterrupt:
                    print("interrupt!")

                if jenis_antrian == 'o':
                    antrian["current_antrian_obat"] += 1
                    antrian["antrian_obat"].enqueue({
                        "nama_pasien": nama_pasien,
                        "nomor_antrian": f'O{antrian["current_antrian_obat"]}'
                    })

                    notify_type = "INFO"
                    notify_text = f"Berhasil memasukkan ke antrian obat\nNama pasien: {nama_pasien}\nNomor antrian: {antrian["current_antrian_obat"]}"

                    if antrian["antrian_obat"].size == 1:
                        # Ini langsung taruh ke label current
                        canvas.after(0, lambda: canvas.itemconfig(antrian["cao_label"], text=f'O{antrian["current_antrian_obat"]}'))
                    elif antrian["antrian_obat"].size == 2:
                        # ini langsung taruh ke label next
                        canvas.after(0, lambda: canvas.itemconfig(antrian["nao_label"], text=f'O{antrian["current_antrian_obat"]}'))

                elif jenis_antrian == 'p':
                    antrian["current_antrian_pembayaran"] += 1
                    antrian["antrian_pembayaran"].enqueue({
                        "nama_pasien": nama_pasien,
                        "nomor_antrian": f'P{antrian["current_antrian_pembayaran"]}'
                    })

                    if antrian["antrian_pembayaran"].size == 1:
                        # Ini langsung taruh ke current
                        canvas.after(0, lambda: canvas.itemconfig(antrian["cap_label"], text=f'P{antrian["current_antrian_pembayaran"]}'))
                    elif antrian["antrian_pembayaran"].size == 2:
                        # ini langsung taruh ke next
                        canvas.after(0, lambda: canvas.itemconfig(antrian["nap_label"], text=f'P{antrian["current_antrian_pembayaran"]}'))
                    notify_type = "INFO"
                    notify_text = f"Berhasil memasukkan ke antrian pembayaran\nNama pasien: {nama_pasien}\nNomor antrian: {antrian["current_antrian_pembayaran"]}"
                else:
                    notify_type = "ERROR"
                    notify_text = "Jenis antrian tidak valid. mohon masukkan jenis antrian sesuai dengan kode nya."
                    pass
            elif user_input == 2:
                print(f"Antrian obat\n{antrian["antrian_obat"]}\n\nAntrian pembayaran\n{antrian["antrian_pembayaran"]}\n")
                input("Tekan enter untuk kembali ke menu utama...")
            elif user_input == 3:
                controller()
            elif user_input == 4: exit(0)
            else:
                notify_type = "ERROR"
                notify_text ="Input tidak valid. Mohon masukkan angka antara 1 dan 4."
        except ValueError:
            notify_type = "ERROR"
            notify_text ="Input tidak valid. Mohon masukkan angka antara 1 dan 4."

if __name__ != "__main__":
    print("This isnt a module file! please run it by typing `python main.py`")
    pass
else:
    main()