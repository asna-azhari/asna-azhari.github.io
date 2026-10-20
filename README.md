# Portofolio Asna Azhari

Situs statis. Tidak butuh PHP, Node.js, basis data, atau proses build.

**Tayang di:** https://asna-azhari.github.io

---

## Untuk yang memasang di server

Unggah **seluruh isi folder ini apa adanya** ke document root. Selesai.

```
about.html           halaman tentang
index.html           halaman depan
projects.html        katalog proyek
skills.html          keahlian
Asset/               render 3D board (PNG tembus pandang)
boards/              3D viewer  →  index.html + models/*.glb + latar/
img/                 foto, favicon, gambar pratinjau tautan
```

Berkas yang dibuka pengunjung: **`index.html`**.

### ⚠ Satu hal yang wajib diperhatikan

**3D viewer mengambil model lewat `fetch`, jadi harus disajikan lewat HTTP.**
Membuka berkasnya langsung dari disk (`file://`) membuat halaman tetap tampil, tetapi
viewer-nya gagal memuat model. Server apa pun sudah cukup — Apache, nginx, GitHub Pages,
Netlify, semuanya jalan tanpa penyetelan khusus.

### Jenis MIME

Pastikan `.glb` disajikan sebagai `model/gltf-binary` atau `application/octet-stream`.
Kebanyakan server sudah benar. Kalau viewer-nya kosong padahal berkasnya ada, ini yang
pertama dicek. Untuk Apache:

```apache
AddType model/gltf-binary .glb
```

### Kalau dipasang di subfolder

Misalnya `domain.com/portofolio/`. Seluruh tautan antar halaman sudah relatif, jadi
**tidak perlu diubah**. Yang perlu disesuaikan hanya alamat lengkap di bagian `<head>`
tiap halaman — baris `og:url`, `og:image`, dan `canonical` — supaya pratinjau tautan
di WhatsApp dan LinkedIn menunjuk ke alamat yang benar.

### Huruf

Halaman memuat **Archivo** dari Google Fonts. Kalau server tidak boleh memanggil ke luar,
hapus tiga baris `<link>` ke `fonts.googleapis.com` dan `fonts.gstatic.com` di `<head>`.
Tampilannya tetap jalan memakai huruf bawaan sistem.

---

## Ukuran

| Bagian | Ukuran |
|---|---|
| Seluruh situs | ~30 MB |
| `boards/models/` | 17 MB, **diambil hanya saat board itu dipilih** |
| `Asset/` | 11 MB render |
| Halaman terberat | `projects.html`, ~12 MB gambar |

3D viewer sendiri **22 KB**. Model tidak ditanam di dalamnya; pengunjung hanya mengunduh
board yang benar-benar dia buka, antara 0,4 dan 4,3 MB.

---

## Membangun ulang 3D viewer

`boards/index.html` bukan berkas yang disunting tangan — dia dibangkitkan:

```
python -I tools/build_viewer_split.py
```

Dijalankan dari akar repo. Sumbernya `boards.json` dan `tools/build_viewer_split.py`,
keduanya ada di repo ini, jadi **repo ini bisa membangun ulang dirinya sendiri.**

**Menambah board:** salin `.glb` ke `boards/models/`, tambah satu entri di `boards.json`
berisi `key`, `project`, `label`, dan `glb`, lalu jalankan skripnya. Daftar di panel kiri
viewer mengelompokkan sendiri menurut `project`.

Skrip lain di `tools/` (`obj2glb.mjs`, `build_all.py`, `build_viewer.py`) mengolah ekspor
OBJ dari EasyEDA menjadi GLB. **Itu butuh bahan sumber 111 MB yang sengaja tidak ikut repo**,
dan hanya dipakai saat ada board baru.

---

## Menjalankan di komputer sendiri

```
python -m http.server 8000
```

lalu buka `http://localhost:8000/`. Di Windows ada `jalankan lokal.bat` yang melakukan
keduanya sekaligus.

---

## Isi

Lima produk, empat belas board, ditambah empat board alat kerja. Delapan di antaranya
punya model 3D yang bisa diputar. Skematik, Gerber, dan BOM tidak diterbitkan, sebab
bahan itu milik perusahaan tempat board-nya dirancang.

Kontak: [asnaazhari12@gmail.com](mailto:asnaazhari12@gmail.com) ·
[WhatsApp](https://wa.me/6285701496855) ·
[LinkedIn](https://linkedin.com/in/asna-azhari)
