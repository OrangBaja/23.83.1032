import requests
import json

API_BASE_URL = "http://127.0.0.1:8000"

def print_response(response):
    """Print response data in a formatted way."""
    if response.status_code in [200, 201]:
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Error {response.status_code}: {response.text}")

def create_film():
    """Send POST request to create a new film."""
    print("\nMasukkan detail film (ketik '0' untuk keluar):")
    judul_film = input("Judul Film: ").strip()
    if judul_film == "0":
        print("Operasi dibatalkan.")
        return
    if not judul_film:
        print("Judul Film tidak boleh kosong!")
        return

    deskripsi = input("Deskripsi: ").strip()
    if deskripsi == "0":
        print("Operasi dibatalkan.")
        return
    if not deskripsi:
        print("Deskripsi tidak boleh kosong!")
        return

    try:
        rating_input = input("Rating (0-10): ").strip()
        if rating_input == "0":
            print("Operasi dibatalkan.")
            return
        rating = float(rating_input)
        if not (0 <= rating <= 10):
            print("Error: Rating harus berupa angka antara 0 dan 10!")
            return
    except ValueError:
        print("Error: Rating harus berupa angka desimal atau bulat!")
        return

    sutradara = input("Sutradara: ").strip()
    if sutradara == "0":
        print("Operasi dibatalkan.")
        return
    if not sutradara:
        print("Sutradara tidak boleh kosong!")
        return

    try:
        tahun_rilis_input = input("Tahun Rilis: ").strip()
        if tahun_rilis_input == "0":
            print("Operasi dibatalkan.")
            return
        tahun_rilis = int(tahun_rilis_input)
        if tahun_rilis < 1800 or tahun_rilis > 2100:
            print("Error: Tahun Rilis harus berupa angka antara 1800 dan 2100!")
            return
    except ValueError:
        print("Error: Tahun Rilis harus berupa angka!")
        return

    payload = {
        "judul_film": judul_film,
        "deskripsi": deskripsi,
        "rating": rating,
        "sutradara": sutradara,
        "tahun_rilis": tahun_rilis
    }
    response = requests.post(f"{API_BASE_URL}/film", json=payload)
    print_response(response)

def read_all_films():
    """Send GET request to fetch all films."""
    confirm = input("Tekan ENTER untuk melanjutkan atau ketik '0' untuk keluar: ").strip()
    if confirm == "0":
        print("Operasi dibatalkan.")
        return
    response = requests.get(f"{API_BASE_URL}/film", headers={"Cache-Control": "no-cache"})
    print_response(response)

def read_film_by_id():
    """Send GET request to fetch a film by ID."""
    film_id = input("Masukkan ID film (atau ketik '0' untuk keluar): ").strip()
    if film_id == "0":
        print("Operasi dibatalkan.")
        return
    if not film_id.isdigit():
        print("Error: ID film harus berupa angka!")
        return
    response = requests.get(f"{API_BASE_URL}/film/{film_id}")
    if response.status_code == 404:
        print(f"Error: Film dengan ID {film_id} tidak ditemukan.")
    else:
        print_response(response)

def update_film():
    """Send PUT request to update a film."""
    film_id = input("Masukkan ID film untuk diperbarui (atau ketik '0' untuk keluar): ").strip()
    if film_id == "0":
        print("Operasi dibatalkan.")
        return
    if not film_id.isdigit():
        print("Error: ID film harus berupa angka!")
        return

    # Validasi keberadaan film sebelum memperbarui
    response = requests.get(f"{API_BASE_URL}/film/{film_id}")
    if response.status_code == 404:
        print(f"Error: Film dengan ID {film_id} tidak ditemukan. Tidak dapat diperbarui.")
        return

    print("\nMasukkan detail yang diperbarui (ketik '0' untuk keluar):")
    judul_film = input("Judul Film: ").strip()
    if judul_film == "0":
        print("Operasi dibatalkan.")
        return
    if not judul_film:
        print("Judul Film tidak boleh kosong!")
        return

    deskripsi = input("Deskripsi: ").strip()
    if deskripsi == "0":
        print("Operasi dibatalkan.")
        return
    if not deskripsi:
        print("Deskripsi tidak boleh kosong!")
        return

    try:
        rating_input = input("Rating (0-10): ").strip()
        if rating_input == "0":
            print("Operasi dibatalkan.")
            return
        rating = float(rating_input)
        if not (0 <= rating <= 10):
            print("Error: Rating harus berupa angka antara 0 dan 10!")
            return
    except ValueError:
        print("Error: Rating harus berupa angka desimal atau bulat!")
        return

    sutradara = input("Sutradara: ").strip()
    if sutradara == "0":
        print("Operasi dibatalkan.")
        return
    if not sutradara:
        print("Sutradara tidak boleh kosong!")
        return

    try:
        tahun_rilis_input = input("Tahun Rilis: ").strip()
        if tahun_rilis_input == "0":
            print("Operasi dibatalkan.")
            return
        tahun_rilis = int(tahun_rilis_input)
        if tahun_rilis < 1800 or tahun_rilis > 2100:
            print("Error: Tahun Rilis harus berupa angka antara 1800 dan 2100!")
            return
    except ValueError:
        print("Error: Tahun Rilis harus berupa angka!")
        return

    payload = {
        "judul_film": judul_film,
        "deskripsi": deskripsi,
        "rating": rating,
        "sutradara": sutradara,
        "tahun_rilis": tahun_rilis
    }
    response = requests.put(f"{API_BASE_URL}/film/{film_id}", json=payload)
    print_response(response)

def delete_film():
    """Send DELETE request to delete a film."""
    film_id = input("Masukkan ID film untuk dihapus (atau ketik '0' untuk keluar): ").strip()
    if film_id == "0":
        print("Operasi dibatalkan.")
        return
    if not film_id.isdigit():
        print("Error: ID film harus berupa angka!")
        return
    response = requests.delete(f"{API_BASE_URL}/film/{film_id}")
    if response.status_code == 404:
        print(f"Error: Film dengan ID {film_id} tidak ditemukan. Tidak dapat dihapus.")
    else:
        print_response(response)

def main():
    """Main menu for CRUD operations."""
    while True:
        print("\nMenu:")
        print("1. Tambah Film")
        print("2. Tampilkan Semua Film")
        print("3. Cari Film berdasarkan ID")
        print("4. Perbarui Film")
        print("5. Hapus Film")
        print("6. Keluar")
        choice = input("Masukkan pilihan Anda: ").strip()

        if choice == "1":
            create_film()
        elif choice == "2":
            read_all_films()
        elif choice == "3":
            read_film_by_id()
        elif choice == "4":
            update_film()
        elif choice == "5":
            delete_film()
        elif choice == "6":
            print("Keluar...")
            break
        else:
            print("Pilihan tidak valid. Silakan masukkan angka 1-6.")

if __name__ == "__main__":
    main()
