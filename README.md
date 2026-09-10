# commit-brick-breaker

<p align="center">
  <img src="game.gif" alt="commit-brick-breaker" />
</p>

## Panduan Instalasi & Penggunaan

### 1. Pasang di Profil GitHub (Otomatis)
Untuk menjalankan generator otomatis di profil GitHub tanpa instalasi lokal:

1. Di repo profil GitHub Anda (`username/username`), buat file `.github/workflows/brick-breaker.yml`:
```yaml
name: Generate Brick Breaker

on:
  schedule:
    - cron: "0 0 * * *"
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4

      - uses: MakdumIbrohim/commit-brick-breaker@main
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          github_user: ${{ github.repository_owner }}
          output_path: game.gif
          ball_skin: classic # Opsi: classic | fire | ice | lightning | poison
          theme: dark # Opsi: dark | light

      - name: Commit and Push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add game.gif
          git diff --staged --quiet || git commit -m "chore: update brick breaker game"
          git pull --rebase --autostash origin main || true
          git push
```

#### Pilihan & Preview Skin (`ball_skin`)
Ubah nilai parameter `ball_skin` pada workflow di atas sesuai skin yang diinginkan:

| Parameter `ball_skin` | Preview Animasi |
| :---: | :---: |
| `classic` (default) | <img src="assets/preview/sample_classic.gif" width="340" alt="classic" /> |
| `fire` | <img src="assets/preview/sample_fire.gif" width="340" alt="fire" /> |
| `ice` | <img src="assets/preview/sample_ice.gif" width="340" alt="ice" /> |
| `lightning` | <img src="assets/preview/sample_lightning.gif" width="340" alt="lightning" /> |
| `poison` | <img src="assets/preview/sample_poison.gif" width="340" alt="poison" /> |

#### Opsi Tema Board (`theme`)
Ubah nilai parameter `theme` pada workflow:

| Parameter `theme` | Preview |
| :---: | :---: |
| `dark` (default) | <img src="assets/preview/sample_classic.gif" width="340" alt="dark theme" /> |
| `light` | <img src="assets/preview/sample_light.gif" width="340" alt="light theme" /> |

2. Beri izin write: buka repo **Settings** > **Actions** > **General** > **Workflow permissions** > pilih **Read and write permissions** > **Save**.

3. Tampilkan di `README.md` profil Anda:
```markdown
<p align="center">
  <img src="game.gif" alt="Brick Breaker Game" />
</p>
```

---

### 2. Penggunaan di Lokal
Untuk menjalankan dan men-generate GIF secara manual di komputer Anda:

1. Clone repositori & install dependensi:
```bash
git clone https://github.com/MakdumIbrohim/commit-brick-breaker.git
cd commit-brick-breaker
pip install pillow
```

2. Jalankan perintah generator:
```bash
python generate.py <username_github> [output_file.gif] [skin] [theme]
```

Contoh pemakaian:
```bash
# Default (classic skin, dark theme)
python generate.py MakdumIbrohim game.gif

# Tema terang (light theme)
python generate.py MakdumIbrohim game.gif classic light

# Skin api dengan tema terang
python generate.py MakdumIbrohim game.gif fire light

# Menggunakan token jika ingin mengambil data privat atau menghindari rate-limit
GITHUB_TOKEN="ghp_xxx" python generate.py MakdumIbrohim game.gif ice dark
```
