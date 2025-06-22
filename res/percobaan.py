from collections import deque
from datetime import datetime, date

# Global variable untuk tanggal sekarang
tanggal_sekarang = date.today()

# Priority queue untuk antrian checkout (belum dipakai)
antrian_checkout = []

# Fungsi untuk mengubah tanggal sekarang
def ubah_tanggal():
    global tanggal_sekarang
    while True:
        tanggal_input = input("Masukkan tanggal sekarang (YYYY-MM-DD): ")
        try:
            tanggal_sekarang = datetime.strptime(tanggal_input, "%Y-%m-%d").date()
            break
        except ValueError:
            print("❌ Format salah! Contoh yang benar: 2025-06-20")

# Struktur data untuk kamar hotel
class Kamar:
    def __init__(self, no_kamar):
        self.no_kamar = no_kamar
        self.tamu = None
        self.tanggal_checkout = None
        self.tanggal_checkin = None

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
def reservasi_kamar():
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
    
    while True:
        check = input("Tanggal checkin (YYYY-MM-DD): ")
        try:
            if check < tanggal_sekarang:
                print("Anda tidak dapat Checkin di masa lalu")
            tanggal_check = datetime.strptime(check, "%Y-%m-%d").date()
            break
        except ValueError:
            print("❌ Format salah! Contoh yang benar: 2025-06-20")

    while True:
        tanggal = input("Tanggal checkout (YYYY-MM-DD): ")
        try:
            tanggal_obj = datetime.strptime(tanggal, "%Y-%m-%d").date()
            break
        except ValueError:
            print("❌ Format salah! Contoh yang benar: 2025-06-20")

    for kamar in lantai.kamar:
        if kamar.tamu is None:
            kamar.tamu = nama
            kamar.tanggal_checkout = tanggal_obj
            lantai.daftar_tamu.appendleft(nama)
            print(f"{nama} berhasil reservasi kamar {kamar.no_kamar} di {lantai.nama} (Rp {lantai.harga:,}, checkout {tanggal})")
            return

    print("Semua kamar penuh di tipe ini.")

# 3. Checkout tamu
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

    print(f"\n--- Daftar Tamu di Lantai {lantai.nama} ---")
    daftar_opsi = []
    for kamar in lantai.kamar:
        if kamar.tamu:
            nama = kamar.tamu
            tgl_checkout = kamar.tanggal_checkout
            if tgl_checkout:
                status = "✅ Boleh checkout" if tanggal_sekarang >= tgl_checkout else "❌ Belum bisa checkout"
            else:
                status = "❓ Belum diatur tanggal checkout-nya"
            print(f"{nama} - Kamar {kamar.no_kamar} - Checkin: {tang} Checkout: {tgl_checkout} --> {status}")
            daftar_opsi.append((nama, kamar, status))

    if not daftar_opsi:
        print("Tidak ada tamu yang sedang menginap di lantai ini.")
        return

    nama_input = input("\nAda yang ingin di-checkout? (Ketik nama atau 'batal'): ").strip()

    if nama_input.lower() == 'batal':
        print("Checkout dibatalkan.")
        return

    for nama, kamar, status in daftar_opsi:
        if nama_input.lower() == nama.lower():
            if status != "✅ Boleh checkout":
                print(f"{nama} belum waktunya checkout")
                return
            kamar.tamu = None
            kamar.tanggal_checkout = None
            if nama in lantai.daftar_tamu:
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
        print(f"Tanggal hari ini : {tanggal_sekarang}")
        
        print("\n1. Tampilkan Kamar")
        print("2. Reservasi Kamar")
        print("3. Checkout")
        print("4. Tampilkan Tamu yang Pernah Menginap")
        print("5. Ubah Tanggal")
        print("6. Keluar")

        pilihan = input("Pilih menu (1-6): ")
        if pilihan == "1":
            tampilkan_kamar()
        elif pilihan == "2":
            reservasi_kamar()
        elif pilihan == "3":
            checkout()
        elif pilihan == "4":
            tampilkan_tamu()
        elif pilihan == "5":
            ubah_tanggal()
        elif pilihan == "6":
            print("Terima kasih telah menggunakan sistem hotel!")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    menu()
