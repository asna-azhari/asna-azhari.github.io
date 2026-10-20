@echo off
REM Menjalankan portofolio di server kecil. Viewer 3D butuh ini,
REM sebab browser melarang fetch berkas lewat file://
cd /d "%~dp0"
start "" http://localhost:8000/
python -m http.server 8000
