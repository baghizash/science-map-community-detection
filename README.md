# Deteksi Komunitas pada Peta Ilmu dan Jaringan Football

Perbandingan algoritma deteksi komunitas memakai NetworkX: Girvan Newman,
label propagation, greedy modularity, dan fluid communities. Diterapkan pada
peta ilmu pengetahuan Wikipedia dan jaringan pertandingan football kampus.

Proyek ini adalah Module 2 dari kursus Network Modeling and Analysis in Python
(University of Michigan).

## Data

Folder `data` berisi dua jaringan nyata dalam format GML:

* `MapOfScience.gml`: 677 topik Wikipedia, 6517 edge. Setiap topik punya nama
  dan kelas ilmu: Applied (92), Formal (193), Natural (168), Social (224).
* `football.gml`: 115 tim football kampus, 613 pertandingan, lengkap dengan
  nama tim.

## Yang dikerjakan

1.  Empat algoritma dijalankan pada Map of Science. Hasil modularity:
    fluid communities (k=11) = 0.5909, label propagation = 0.5842 (28
    komunitas), Girvan Newman = 0.5807 (35 komunitas), greedy modularity =
    0.5504 (14 komunitas). Lihat `charts/02_algorithm_comparison.png`.
2.  Kualitas partisi Girvan Newman: coverage = 0.8153, performance = 0.8887.
    Lihat `charts/03_partition_quality.png`.
3.  Visualisasi Map of Science dengan warna per komunitas hasil label
    propagation. Lihat `charts/04_science_communities.png`.
4.  Girvan Newman pada jaringan football menghasilkan modularity = 0.5996.
    Salah satu komunitas yang terdeteksi berisi 18 tim di wilayah barat,
    termasuk NewMexico, Arizona, Utah, dan ColoradoState.
    Lihat `charts/05_football_newmexico.png`.

## Cara menjalankan

```bash
python analyze_communities.py
```

Script ini memuat data, menjalankan algoritma deteksi komunitas, menyimpan
chart ke folder `charts`, dan menulis ringkasan angka ke `findings.json`.
Catatan: partisi Girvan Newman pada Map of Science memakai hasil terverifikasi
dari tugas kursus karena komputasinya sangat berat.

## Tools

Python, NetworkX, pandas, NumPy, matplotlib.
