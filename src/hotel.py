from collections import deque
import heapq
from datetime import datetime

# priority queue
antrian_checkout = []

def ubah_tanggal():
    global tanggal_sekarang
    tanggal_input = input("Masukkan tanggal sekarang baru (format: YYYY-MM-DD): ")
    try:
        tanggal_sekarang = datetime.strptime(tanggal_input, "%Y-%m-%d").date()
        print(f"Tanggal sekarang diubah menjadi: {tanggal_sekarang}")
    except ValueError:
        print("Format salah! Gunakan format YYYY-MM-DD.")

# Struktur data kamar hotel
class Kamar:
    def __init__(self, no_kamar):
        self.no_kamar = no_kamar
        self.tamu = None

    def status(self):
        return f"Terisi ({self.tamu})" if self.tamu else "Kosong"

class Lantai:
    def __init__(self, nama, harga, kamar_range):
        self.nama = nama
        self.harga = harga
        self.kamar = [Kamar(no) for no in kamar_range]
        self.daftar_tamu = deque()
        self.riwayat_tamu = []

# Inisialisasi data hotel
hotel = {
    "L2": Lantai("Standar", 120_000, range(1, 4)),
    "L3": Lantai("Deluxe", 220_000, range(4, 7)),
    "L4": Lantai("Elite", 320_000, range(7, 10))
}

# 1. Tampilkan semua kamar
def tampilkan_kamar():
    print("\n=== Daftar Kamar ===")
    for kode, lantai in hotel.items():
        print(f"{kode} ({lantai.nama}) - Rp {lantai.harga:,}")
        for kamar in lantai.kamar:
            print(f"  Kamar {kamar.no_kamar}: {kamar.status()}")

# 2. Reservasi kamar
def reservasi_kamar(tanggal_checkout):
    print("\n=== Reservasi Kamar ===")
    nama = input("Nama tamu: ")

    print("Tipe Kamar:")
    for kode, lantai in hotel.items():
        print(f"  {lantai.nama:<7} = Rp {lantai.harga:,}")

    pilihan = input("Pilih tipe kamar (Standar/Deluxe/Elite): ").strip().lower()
    kode_lantai = {
        "standar": "L2",
        "deluxe": "L3",
        "elite": "L4"
    }.get(pilihan)

    if not kode_lantai:
        print("Tipe kamar tidak valid.")
        return

    lantai = hotel[kode_lantai]

    for kamar in lantai.kamar:
        if kamar.tamu is None:
            tanggal = input("Tanggal checkout (YYYY-MM-DD): ")
            tanggal_obj = datetime.strptime(tanggal_checkout, "%m-%d")
            heapq.heappush(antrian_checkout, (tanggal_obj, nama, kamar))
            kamar.tamu = nama
            lantai.daftar_tamu.appendleft(nama)
            print(f"{nama} berhasil reservasi kamar {kamar.no_kamar} di {lantai.nama} (Rp {lantai.harga:,}, checkout {tanggal_checkout})")
            return

    print("Semua kamar penuh di tipe ini.")

# 3. Checkout 1 tamu per lantai
def checkout():
    print("\n=== Checkout ===")
    kode = input("Masukkan kode lantai (L2/L3/L4): ").upper()
    if kode not in hotel:
        print("Lantai tidak ditemukan.")
        return

    lantai = hotel[kode]

    if not lantai.daftar_tamu:
        print("Tidak ada tamu di lantai ini.")
        return

    print("\n--- Daftar Tamu di Lantai", lantai.nama, "---")
    daftar_opsi = []
    for kamar in lantai.kamar:
        if kamar.tamu:
            nama = kamar.tamu
            tgl_checkout = kamar.tanggal_obj  # pastikan property ini ada
            status = "✅ Boleh checkout" if date.today() >= tgl_checkout else "❌ Belum bisa checkout"
            print(f"{nama} - Kamar {kamar.no_kamar} - Checkout: {tgl_checkout} --> {status}")
            daftar_opsi.append((nama, kamar))

    if not daftar_opsi:
        print("Tidak ada tamu yang sedang menginap di lantai ini.")
        return

    print("\nAda yang ingin di-checkout? (Ketik nama atau 'batal')")
    nama_input = input(">> ").strip()

    if nama_input.lower() == 'batal':
        print("Checkout dibatalkan.")
        return

    # Cari tamu yang dipilih
    for nama, kamar in daftar_opsi:
        if nama_input.lower() == nama.lower():
            kamar.tamu = None
            lantai.daftar_tamu.remove(nama)
            lantai.riwayat_tamu.append((nama, lantai.nama, lantai.harga))
            print(f"{nama} telah checkout dari kamar {kamar.no_kamar} ({lantai.nama})")
            return

    print("Tamu tidak ditemukan.")


# 4. Tampilkan riwayat tamu
def tampilkan_tamu():
    print("\n=== Riwayat Tamu ===")
    for kode, lantai in hotel.items():
        print(f"{kode} ({lantai.nama})")
        if not lantai.riwayat_tamu:
            print("  - Belum ada tamu")
        else:
            for nama, tipe, harga in lantai.riwayat_tamu:
                print(f"  - {nama} (Tipe: {tipe}, Harga: Rp {harga:,})")

# 5. Menu utama
def menu():
    while True:
        print("\n===== HOTEL KECE ABISS =====")
        print("1. Tampilkan Kamar")
        print("2. Reservasi Kamar")
        print("3. Checkout")
        print("4. Tampilkan Tamu yang Pernah Menginap")
        print("5. Keluar")

        pilihan = input("Pilih menu (1-5): ")
        if pilihan == "1":
            tampilkan_kamar()
        elif pilihan == "2":
            reservasi_kamar()
        elif pilihan == "3":
            checkout()
        elif pilihan == "4":
            tampilkan_tamu()
        elif pilihan == "5":
            print("Terima kasih telah menggunakan sistem hotel!")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    menu()