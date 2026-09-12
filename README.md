# Generate Brick Breaker

<p align="center">
  <a href="https://github.com/marketplace/actions/generate-brick-breaker">
    <img src="https://img.shields.io/badge/Marketplace-v1.3.1-blue.svg?logo=github&style=flat-square" alt="Marketplace" />
  </a>
  <a href="https://github.com/MakdumIbrohim/generate-brick-breaker/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/MakdumIbrohim/generate-brick-breaker/generate.yml?branch=main&style=flat-square&label=build" alt="Build Status" />
  </a>
  <a href="https://github.com/MakdumIbrohim/generate-brick-breaker/stargazers">
    <img src="https://img.shields.io/github/stars/MakdumIbrohim/generate-brick-breaker?style=flat-square&logo=github" alt="Stars" />
  </a>
  <a href="https://github.com/MakdumIbrohim/generate-brick-breaker/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/MakdumIbrohim/generate-brick-breaker?style=flat-square" alt="License" />
  </a>
</p>

<p align="center">
  <img src="game.svg" alt="generate-brick-breaker" />
</p>

Turn your GitHub contribution graph into an automated retro Brick Breaker game animation (SVG or GIF) for your profile README.

[English](#english) • [Bahasa Indonesia](#bahasa-indonesia)

---

## English

### 1. GitHub Profile Integration (Automated)

1. In your GitHub profile repository (`username/username`), create `.github/workflows/brick-breaker.yml`:

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

      - uses: MakdumIbrohim/generate-brick-breaker@main
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          github_user: ${{ github.repository_owner }}
          # Options: game.svg (recommended) or game.gif
          output_path: game.svg
          # Options: classic | fire | ice | lightning | poison
          ball_skin: classic
          # Options: dark | sky | synthwave | matrix
          theme: dark
          # Options: default | laser | retro | mecha | cyber
          paddle_skin: default

      - name: Commit and Push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add -A
          git diff --staged --quiet || git commit -m "chore: update brick breaker assets"
          git pull --rebase origin main || true
          git push origin main
```

#### Ball Skin Options (`ball_skin`)
| Option | Preview |
| :---: | :---: |
| `classic` (default) | <img src="assets/preview/sample_classic.svg" width="340" alt="classic" /> |
| `fire` | <img src="assets/preview/sample_fire.svg" width="340" alt="fire" /> |
| `ice` | <img src="assets/preview/sample_ice.svg" width="340" alt="ice" /> |
| `lightning` | <img src="assets/preview/sample_lightning.svg" width="340" alt="lightning" /> |
| `poison` | <img src="assets/preview/sample_poison.svg" width="340" alt="poison" /> |

#### Paddle Skin Options (`paddle_skin`)
| Option | Preview |
| :---: | :---: |
| `default` | Primary theme color |
| `laser` | <img src="assets/preview/sample_paddle_laser.svg" width="340" alt="paddle laser" /> |
| `retro` | <img src="assets/preview/sample_paddle_retro.svg" width="340" alt="paddle retro" /> |
| `mecha` | <img src="assets/preview/sample_paddle_mecha.svg" width="340" alt="paddle mecha" /> |
| `cyber` | <img src="assets/preview/sample_paddle_cyber.svg" width="340" alt="paddle cyber" /> |

#### Board Theme Options (`theme`)
| Option | Preview |
| :---: | :---: |
| `dark` (default) | <img src="assets/preview/sample_theme_dark.svg" width="340" alt="dark theme" /> |
| `sky` | <img src="assets/preview/sample_theme_sky.svg" width="340" alt="sky theme" /> |
| `synthwave` | <img src="assets/preview/sample_theme_synthwave.svg" width="340" alt="synthwave theme" /> |
| `matrix` | <img src="assets/preview/sample_theme_matrix.svg" width="340" alt="matrix theme" /> |

2. Enable workflow permissions: Repo **Settings** > **Actions** > **General** > **Workflow permissions** > select **Read and write permissions** > **Save**.

3. Add image to your profile `README.md` (use `.svg` or `.gif` matching your `output_path`):
```markdown
<p align="center">
  <img src="game.svg" alt="Brick Breaker Game" />
</p>
```

> **Note on Image Caching:** GitHub caches profile images through its Camo CDN. If you update settings and the animation does not change immediately, do a hard refresh (`Ctrl + F5` or `Cmd + Shift + R`), open your profile in an Incognito window, or allow 5–15 minutes for the CDN cache to clear.

### 2. Local Usage (CLI)

```bash
git clone https://github.com/MakdumIbrohim/generate-brick-breaker.git
cd generate-brick-breaker
pip install pillow
python generate.py <username> [output.svg | output.gif] [skin] [theme] [paddle_skin]
```

Examples:
```bash
# Output SVG (recommended: lightweight vector animation)
python generate.py MakdumIbrohim game.svg

# Output GIF
python generate.py MakdumIbrohim game.gif fire dark laser
```

---

## Bahasa Indonesia

### 1. Pasang di Profil GitHub (Otomatis)

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

      - uses: MakdumIbrohim/generate-brick-breaker@main
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          github_user: ${{ github.repository_owner }}
          # Opsi: game.svg (disarankan) atau game.gif
          output_path: game.svg

          # Opsi: classic | fire | ice | lightning | poison
          ball_skin: classic

          # Opsi: dark | sky | synthwave | matrix
          theme: dark
          
          # Opsi: default | laser | retro | mecha | cyber
          paddle_skin: default

      - name: Commit and Push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add -A
          git diff --staged --quiet || git commit -m "chore: update brick breaker assets"
          git pull --rebase origin main || true
          git push origin main
```

#### Pilihan Skin Paddle (`paddle_skin`)
| Opsi | Preview |
| :---: | :---: |
| `default` | Warna primer tema aktif |
| `laser` | <img src="assets/preview/sample_paddle_laser.svg" width="340" alt="paddle laser" /> |
| `retro` | <img src="assets/preview/sample_paddle_retro.svg" width="340" alt="paddle retro" /> |
| `mecha` | <img src="assets/preview/sample_paddle_mecha.svg" width="340" alt="paddle mecha" /> |
| `cyber` | <img src="assets/preview/sample_paddle_cyber.svg" width="340" alt="paddle cyber" /> |

#### Pilihan Tema Papan (`theme`)
| Opsi | Preview |
| :---: | :---: |
| `dark` (default) | <img src="assets/preview/sample_theme_dark.svg" width="340" alt="dark theme" /> |
| `sky` | <img src="assets/preview/sample_theme_sky.svg" width="340" alt="sky theme" /> |
| `synthwave` | <img src="assets/preview/sample_theme_synthwave.svg" width="340" alt="synthwave theme" /> |
| `matrix` | <img src="assets/preview/sample_theme_matrix.svg" width="340" alt="matrix theme" /> |

2. Beri izin write: buka repo **Settings** > **Actions** > **General** > **Workflow permissions** > pilih **Read and write permissions** > **Save**.

3. Tampilkan di `README.md` profil Anda (sesuaikan ekstensi `.svg` atau `.gif` dengan `output_path` Anda):
```markdown
<p align="center">
  <img src="game.svg" alt="Brick Breaker Game" />
</p>
```

> **Catatan Cache Gambar:** GitHub menyimpan cache gambar profil melalui server Camo CDN. Jika Anda baru saja mengubah pengaturan tema/skin dan animasinya belum langsung berubah di profil, lakukan *hard refresh* (`Ctrl + F5` atau `Cmd + Shift + R`), buka lewat tab *Incognito*, atau tunggu 5–15 menit hingga cache CDN GitHub terperbarui otomatis.

### 2. Penggunaan di Lokal

```bash
git clone https://github.com/MakdumIbrohim/generate-brick-breaker.git
cd generate-brick-breaker
pip install pillow
python generate.py <username_github> [output.svg | output.gif] [skin] [theme] [paddle_skin]
```

Contoh pemakaian:
```bash
# Output SVG (ringan & tajam di layar resolusi tinggi)
python generate.py MakdumIbrohim game.svg

# Output GIF
python generate.py MakdumIbrohim game.gif fire dark laser
```
