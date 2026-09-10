# gh-brick-breaker

Animasi retro game penghancur balok (Brick Breaker / Arkanoid) yang dibuat otomatis dari grafik kontribusi GitHub.

![Pratinjau Permainan](game.gif)

## Fitur Utama

- **Data Real-time**: Mengambil riwayat kontribusi commit menggunakan GitHub GraphQL API.
- **Simulasi Otomatis (AI Paddle)**: Dayung bergerak otomatis melacak bola dan menghancurkan balok kontribusi.
- **Siap Jadi GitHub Action**: Terintegrasi langsung ke profil GitHub untuk pembaruan harian via GitHub Actions.
- **Ringan & Tanpa Dependensi Berat**: Hanya memerlukan Python dan pustaka Pillow untuk pembuatan animasi GIF.

## Struktur Modul

- `src/config.py`: Konstanta konfigurasi canvas, warna, dan fisika game.
- `src/fetcher.py`: Mengambil data kontribusi pengguna dari GitHub GraphQL API (1 Januari sampai sekarang).
- `src/engine.py`: Logika fisika bola, dayung kontrol AI, deteksi tabrakan dinding, dan kalkulasi balok hancur.
- `src/renderer.py`: Render grafis frame per frame dan ekspor hasil akhir ke format animasi GIF.
- `generate.py`: Entrypoint utama CLI untuk eksekusi proses pembuatan animasi.

---

## Panduan Penggunaan Lokal

### 1. Prasyarat
- Python 3.9 atau lebih baru.
- Pustaka Pillow:
  ```bash
  pip install pillow
  ```

### 2. Jalankan Generator
Jalankan skrip dengan menyertakan username GitHub target dan skin bola (opsional):
```bash
python generate.py <username_github> [nama_output.gif] [skin]
```

Pilihan skin berelemen:
- `fire`: Bola api oranye-kemerahan dengan partikel percikan api (*sparks*) dan bara (*embers*) yang melayang ke atas.
- `ice`: Bola es biru muda dengan partikel kepingan salju (*snowflakes*) dan kristal es (*frost crystals*) yang melayang turun.
- `lightning`: Bola petir kuning-ungu dengan partikel cabang kilat dan percikan listrik tajam (*zaps*).
- `poison`: Bola asam hijau toksik dengan partikel gelembung (*bubbles*) beracun.
- `classic`: Bola hijau polos (`#39D353`) bersih tanpa efek partikel atau jejak trail.

### Galeri Preview Skin

| Skin | Preview Animasi |
| :---: | :---: |
| **Fire** | <img src="assets/preview/sample_fire.gif" width="340" alt="Skin Fire" /> |
| **Ice** | <img src="assets/preview/sample_ice.gif" width="340" alt="Skin Ice" /> |
| **Lightning** | <img src="assets/preview/sample_lightning.gif" width="340" alt="Skin Lightning" /> |
| **Poison** | <img src="assets/preview/sample_poison.gif" width="340" alt="Skin Poison" /> |
| **Classic** | <img src="assets/preview/sample_classic.gif" width="340" alt="Skin Classic" /> |

Contoh:
```bash
python generate.py MakdumIbrohim game.gif ice
```

Jika ingin menggunakan data commit riil dari akun privat atau menghindari batasan rate-limit publik:
```bash
GITHUB_TOKEN="ghp_token_anda" python generate.py MakdumIbrohim game.gif
```

---

## Panduan Pemasangan di Profil GitHub

Otomatiskan pembuatan game animasi di profil GitHub Anda menggunakan GitHub Actions.

### Cara Mengganti Skin Bola (Untuk Pengguna Action)

Cukup ubah parameter **`ball_skin`** di file workflow Anda (`.github/workflows/brick-breaker.yml`):

| Parameter | Tipe | Default | Nilai yang Tersedia | Keterangan |
|---|---|---|---|---|
| `ball_skin` | string | `classic` | `classic`, `fire`, `ice`, `lightning`, `poison` | Menentukan efek animasi, warna bola, trail, dan partikel |

Contoh pemakaian:
```yaml
- uses: MakdumIbrohim/gh-brick-breaker@main
  with:
    ball_skin: ice # Ganti ke: fire, ice, lightning, poison, atau classic
```

---

### Langkah 1: Buat File Workflow
Pada repositori profil Anda (biasanya bernama sama dengan username Anda, contoh `username/username`), buat file baru di `.github/workflows/brick-breaker.yml`:

```yaml
name: Perbarui Brick Breaker

on:
  schedule:
    # Berjalan otomatis setiap hari pada jam 00:00 UTC
    - cron: "0 0 * * *"
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout Repositori
        uses: actions/checkout@v4

      - name: Buat Animasi Game
        uses: MakdumIbrohim/gh-brick-breaker@main
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          github_user: ${{ github.repository_owner }}
          output_path: game.gif
          ball_skin: fire # <-- GANTI DI SINI: fire | ice | lightning | poison | classic

      - name: Commit dan Simpan Hasil
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add game.gif
          git diff --staged --quiet || git commit -m "chore: perbarui animasi game brick breaker"
          git pull --rebase --autostash origin main || true
          git push
```

### Langkah 2: Tampilkan di `README.md`
Tambahkan tag gambar berikut di lokasi yang diinginkan pada `README.md` profil Anda:

```markdown
<p align="center">
  <img src="game.gif" alt="Game Brick Breaker Kontribusi GitHub" />
</p>
```

### Langkah 3: Beri Izin Workflow (Read & Write)
1. Buka repo profil di browser -> Tab **Settings**.
2. Pilih menu samping **Actions** -> **General**.
3. Gulir ke bawah ke bagian **Workflow permissions**, pilih opsi **Read and write permissions**.
4. Klik **Save**.
