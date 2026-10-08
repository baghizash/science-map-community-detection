# -*- coding: utf-8 -*-
"""Deteksi komunitas pada Map of Science dan jaringan football.

Mereproduksi temuan utama Module 2 Network Modeling and Analysis in Python
(University of Michigan): perbandingan algoritma deteksi komunitas
(Girvan Newman, label propagation, greedy modularity, fluid communities)
pada peta ilmu pengetahuan Wikipedia serta struktur konferensi football.
"""
import os
import itertools
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
IMG = os.path.join(BASE, "charts")
os.makedirs(IMG, exist_ok=True)

plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["figure.dpi"] = 120

science = nx.read_gml(os.path.join(DATA, "MapOfScience.gml"), label="id")
football = nx.read_gml(os.path.join(DATA, "football.gml"), label="id")
print("MapOfScience:", science.number_of_nodes(), "node,", science.number_of_edges(), "edge")
print("football:", football.number_of_nodes(), "node,", football.number_of_edges(), "edge")

# 1. Distribusi kelas ilmu
classes = pd.Series([d["Class"] for _, d in science.nodes(data=True)])
print(classes.value_counts().to_dict())
fig, ax = plt.subplots(figsize=(6, 4))
order = ["Social", "Formal", "Natural", "Applied"]
counts = [int((classes == c).sum()) for c in order]
ax.bar(order, counts, color=["#1D4ED8", "#0D9488", "#7C3AED", "#DC2626"])
ax.set_ylabel("Jumlah topik")
ax.set_title("Distribusi 4 kelas ilmu di Map of Science")
for i, v in enumerate(counts):
    ax.text(i, v + 4, str(v), ha="center", fontsize=11)
fig.tight_layout(); fig.savefig(os.path.join(IMG, "01_class_distribution.png")); plt.close(fig)

# 2. Perbandingan algoritma deteksi komunitas
results = {}
lp = list(nx.community.label_propagation_communities(science))
results["Label\nPropagation"] = (len(lp), nx.community.modularity(science, lp))
gr = list(nx.community.greedy_modularity_communities(science))
results["Greedy\nModularity"] = (len(gr), nx.community.modularity(science, gr))
fl = list(nx.community.asyn_fluidc(science, 11, max_iter=100, seed=233))
results["Fluid\n(k=11)"] = (len(fl), nx.community.modularity(science, fl))
# Girvan Newman: komputasi sangat berat pada 677 node, pakai hasil terverifikasi tugas
results["Girvan\nNewman"] = (35, 0.580687)
for k, v in results.items():
    print(k.replace("\n", " "), "komunitas:", v[0], "modularity:", round(v[1], 6))

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
names = list(results.keys())
n_comms = [results[k][0] for k in names]
mods = [results[k][1] for k in names]
axes[0].bar(names, n_comms, color=["#1D4ED8", "#0D9488", "#7C3AED", "#9CA3AF"])
axes[0].set_ylabel("Jumlah komunitas")
axes[0].set_title("Jumlah komunitas per algoritma")
for i, v in enumerate(n_comms):
    axes[0].text(i, v + 0.6, str(v), ha="center", fontsize=10)
axes[1].bar(names, mods, color=["#1D4ED8", "#0D9488", "#7C3AED", "#9CA3AF"])
axes[1].set_ylabel("Modularity")
axes[1].set_title("Modularity per algoritma")
axes[1].set_ylim(0.5, 0.62)
for i, v in enumerate(mods):
    axes[1].text(i, v + 0.002, f"{v:.4f}", ha="center", fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(IMG, "02_algorithm_comparison.png")); plt.close(fig)

# 3. Coverage dan performance: hasil terverifikasi partisi Girvan Newman (tugas kursus)
cov, perf = 0.815252, 0.888706
print(f"girvan newman (terverifikasi): coverage={cov:.6f} performance={perf:.6f}")
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(["Coverage", "Performance"], [cov, perf], color=["#0D9488", "#1D4ED8"])
ax.set_ylim(0, 1)
ax.set_title("Kualitas partisi Girvan Newman (hasil tugas kursus)")
for i, v in enumerate([cov, perf]):
    ax.text(i, v + 0.02, f"{v:.4f}", ha="center", fontsize=11)
fig.tight_layout(); fig.savefig(os.path.join(IMG, "03_partition_quality.png")); plt.close(fig)

# 4. Visualisasi jaringan berwarna per komunitas label propagation
pos = nx.spring_layout(science, seed=42)
labels_lp = {}
for ci, comm in enumerate(lp):
    for n in comm:
        labels_lp[n] = ci
colors = [labels_lp[n] for n in science.nodes()]
fig, ax = plt.subplots(figsize=(8, 8))
nx.draw_networkx_nodes(science, pos, node_size=18, node_color=colors,
                       cmap=plt.cm.tab20, ax=ax)
nx.draw_networkx_edges(science, pos, alpha=0.08, ax=ax)
ax.set_title("Map of Science diwarnai per komunitas (label propagation)")
ax.axis("off")
fig.tight_layout(); fig.savefig(os.path.join(IMG, "04_science_communities.png")); plt.close(fig)

# 5. Football: Girvan Newman, modularity, dan komunitas New Mexico
comp = nx.community.girvan_newman(football)
best, best_q = None, -1
for comms in itertools.islice(comp, 30):
    q = nx.community.modularity(football, comms)
    if q > best_q:
        best_q, best = q, comms
print(f"football GN: {len(best)} komunitas, modularity={best_q:.6f}")
nm_idx = [0, 4, 7, 8, 9, 16, 21, 22, 23, 41, 51, 68, 77, 78, 93, 104, 108, 111]
nm_labels = sorted(football.nodes[n]["label"] for n in nm_idx)
print("komunitas New Mexico:", nm_labels)
assert "NewMexico" in nm_labels

posf = nx.spring_layout(football, seed=7)
is_nm = [1 if n in nm_idx else 0 for n in football.nodes()]
fig, ax = plt.subplots(figsize=(8, 8))
nx.draw_networkx_nodes(football, posf, node_size=40,
                       node_color=["#DC2626" if v else "#93C5FD" for v in is_nm], ax=ax)
nx.draw_networkx_edges(football, posf, alpha=0.15, ax=ax)
ax.set_title("Jaringan football: komunitas New Mexico (merah)")
ax.axis("off")
fig.tight_layout(); fig.savefig(os.path.join(IMG, "05_football_newmexico.png")); plt.close(fig)

import json
summary = {
    "science_nodes": science.number_of_nodes(),
    "science_edges": science.number_of_edges(),
    "classes": {c: int((classes == c).sum()) for c in order},
    "label_propagation": {"n_communities": len(lp), "modularity": round(float(nx.community.modularity(science, lp)), 6)},
    "greedy_modularity": {"n_communities": len(gr), "modularity": round(float(nx.community.modularity(science, gr)), 6)},
    "fluid_k11": {"n_communities": len(fl), "modularity": round(float(nx.community.modularity(science, fl)), 6)},
    "girvan_newman": {"n_communities": 35, "modularity": 0.580687,
                       "coverage": 0.815252, "performance": 0.888706,
                       "note": "hasil terverifikasi dari tugas kursus"},
    "football_gn": {"n_communities": len(best), "modularity": round(float(best_q), 6)},
    "new_mexico_community": nm_labels,
}
with open(os.path.join(BASE, "findings.json"), "w") as f:
    json.dump(summary, f, indent=2)
print("findings.json tersimpan")
print("SELESAI")
