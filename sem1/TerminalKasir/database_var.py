from db import database
from db import database_type as db_type

database_kasir = {
    "daftar_barang": database,
    "pembukuan": database
} # jatuhnya, ini biar tidak keriset
# 2. kita membuat variable ini sebagai global. bener bener global