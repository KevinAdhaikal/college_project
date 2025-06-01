from typing import TypedDict
from utils.rs_queue import queue
from tkinter import Tk, Canvas
from utils.wasig import wasig

class AntrianDict(TypedDict):
    antrian_obat: queue
    antrian_pembayaran: queue
    current_antrian_obat: int
    current_antrian_pembayaran: int
    cao_label: int
    cap_label: int
    nao_label: int
    nap_label: int
    display_window: Tk
    display_canvas: Canvas
    display_ready: wasig

antrian: AntrianDict = {
    "antrian_obat": queue(), # untuk antrian nomor obat
    "antrian_pembayaran": queue(), # untuk antrian nomor pembayaran
    "current_antrian_obat": 0, # angka antrian obat sekarang
    "current_antrian_pembayaran": 0, # angka antrian pembayaran sekarang
    "cao_label": None, # Current antrian obat label
    "cap_label": None, # Current antrian pembayaran label
    "nao_label": None, # Next antrian obat label
    "nap_label": None, # Next antrian pembayaran label
    "display_window": None, # Tk Window
    "display_canvas": None, # Display Canvas
    "display_ready": wasig()
}