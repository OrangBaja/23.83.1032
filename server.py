from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import os
import mysql.connector

# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="API Bioskop",
    description="API untuk mengelola data film di bioskop, termasuk CRUD film.",
    version="1.0.0",
    contact={
        "name": "Developer Anda",
        "email": "developer@example.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Konfigurasi template
templates = Jinja2Templates(directory=os.path.join(os.getcwd(), "templates"))

@app.get("/", response_class=FileResponse)
def read_root():
    # Tentukan path file index.html
    file_path = os.path.join(os.getcwd(), "templates", "index.html")
    return FileResponse(file_path)

# Konfigurasi Database
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "bioskop_db"
}

# Model Pydantic
class Film(BaseModel):
    id: int
    judul_film: str
    deskripsi: str
    rating: float
    sutradara: str
    tahun_rilis: int

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "judul_film": "Film Contoh",
                "deskripsi": "Ini adalah deskripsi film contoh.",
                "rating": 8.5,
                "sutradara": "John Doe",
                "tahun_rilis": 2023
            }
        }


class FilmCreate(BaseModel):
    judul_film: str
    deskripsi: str
    rating: float
    sutradara: str
    tahun_rilis: int

    class Config:
        schema_extra = {
            "example": {
                "judul_film": "Film Baru",
                "deskripsi": "Ini adalah deskripsi film baru.",
                "rating": 7.8,
                "sutradara": "Jane Doe",
                "tahun_rilis": 2024
            }
        }


# Koneksi Database
def get_db_connection():
    return mysql.connector.connect(**db_config)


# CRUD Endpoints
@app.post("/film", response_model=Film, summary="Tambah Film", description="Endpoint ini digunakan untuk menambahkan data film baru.")
def create_film(film: FilmCreate):
    if not (0 <= film.rating <= 10):
        raise HTTPException(status_code=400, detail="Rating harus berada di antara 0 dan 10.")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """INSERT INTO film (judul_film, deskripsi, rating, sutradara, tahun_rilis) VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(query, (film.judul_film, film.deskripsi, film.rating, film.sutradara, film.tahun_rilis))
    connection.commit()
    film_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return {**film.dict(), "id": film_id}


@app.get("/film", response_model=List[Film], summary="Tampilkan Semua Film", description="Endpoint ini digunakan untuk menampilkan semua data film.")
def read_all_films():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM film"
    cursor.execute(query)
    films = cursor.fetchall()
    cursor.close()
    connection.close()
    return films


@app.get("/film/{film_id}", response_model=Film, summary="Tampilkan Film berdasarkan ID", description="Endpoint ini digunakan untuk menampilkan detail film berdasarkan ID.")
def read_film(film_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM film WHERE id = %s"
    cursor.execute(query, (film_id,))
    film = cursor.fetchone()
    cursor.close()
    connection.close()
    if not film:
        raise HTTPException(status_code=404, detail="Film tidak ditemukan")
    return film


@app.put("/film/{film_id}", response_model=Film, summary="Perbarui Film", description="Endpoint ini digunakan untuk memperbarui data film berdasarkan ID.")
def update_film(film_id: int, film: FilmCreate):
    if not (0 <= film.rating <= 10):
        raise HTTPException(status_code=400, detail="Rating harus berada di antara 0 dan 10.")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """UPDATE film SET judul_film = %s, deskripsi = %s, rating = %s, sutradara = %s, tahun_rilis = %s WHERE id = %s"""
    cursor.execute(query, (film.judul_film, film.deskripsi, film.rating, film.sutradara, film.tahun_rilis, film_id))
    connection.commit()
    cursor.close()
    connection.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Film tidak ditemukan")
    return {**film.dict(), "id": film_id}


@app.delete("/film/{film_id}", summary="Hapus Film", description="Endpoint ini digunakan untuk menghapus data film berdasarkan ID.")
def delete_film(film_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM film WHERE id = %s"
    cursor.execute(query, (film_id,))
    connection.commit()
    cursor.close()
    connection.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Film tidak ditemukan")
    return {"message": "Film berhasil dihapus"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
