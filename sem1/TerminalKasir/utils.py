# utils.py = berisi function kebutuhan kita. seperti print_table()

import os

# Fungsi untuk memecah teks panjang
def wrap_text(text, width):
    return [text[i:i+width] for i in range(0, len(text), width)]

def print_table(data: list[list[str]], max_width = os.get_terminal_size().columns, footer_text: list[str]=None):
    """
    Akan mengeprint menjadi membentuk sebuah tabel.

    result = [
        ["Judul 1", "Judul 2"],
        ["Isi 1", "Isi 2"],
        ["Isi 3", "Isi 4"]
        dan seterusnya...
    ]

    utils.print_table(result)
    """
    # Tentukan lebar kolom (dibatasi oleh max_width)

    if footer_text is not None:
        col_width = []
        for i in range(len(data[0])):  # Loop melalui setiap kolom
            if footer_text[i] != "": max_length_in_column = len(footer_text[i])  # Cari panjang maksimum di kolom ini
            else: max_length_in_column = max(len(str(row[i])) for row in data)  # Cari panjang maksimum di kolom ini
            adjusted_width = min(max_length_in_column, max_width)  # Batasi lebar maksimum sesuai max_width
            col_width.append(adjusted_width)
    else: col_width = [
        min(max(len(str(row[i])) for row in data), max_width) for i in range(len(data[0]))
    ]
        
    separator = "-+-".join("-" * width for width in col_width)

    # Cetak Header
    print(separator)
    print(" | ".join(f"{str(data[0][i]):<{col_width[i]}}" for i in range(len(data[0]))))
    print(separator)

    # Cetak isi tabel
    for row in data[1:]:
        # Wrap teks panjang di setiap kolom
        wrapped_columns = [wrap_text(str(row[i]), col_width[i]) for i in range(len(row))]
        
        # Hitung jumlah baris maksimum dalam satu baris data
        max_lines = max(len(col) for col in wrapped_columns)
        
        # Cetak baris data dengan wrap text
        for line in range(max_lines):
            print(" | ".join(
                f"{wrapped_columns[i][line] if line < len(wrapped_columns[i]) else '':<{col_width[i]}}"
                for i in range(len(row))
            ))
        print(separator)

    if footer_text is not None:
        # Wrap teks panjang di setiap kolom
        wrapped_columns = [wrap_text(str(footer_text[i]), col_width[i]) for i in range(len(footer_text))]

        # Hitung jumlah baris maksimum dalam satu baris data
        max_lines = max(len(col) for col in wrapped_columns)
        
        # Cetak baris data dengan wrap text
        for line in range(max_lines):
            print(" | ".join(
                f"{wrapped_columns[i][line] if line < len(wrapped_columns[i]) else '':<{col_width[i]}}"
                for i in range(len(footer_text))
            ))
        print(separator)

def indo_currency_to_int(val: str):
    return int(val[2:].replace(".", ""))