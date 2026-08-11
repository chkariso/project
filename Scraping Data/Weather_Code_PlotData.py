# ==========================================================
# File        : Weather_Code_PlotData.py
# Project     : Project - Weather Data Scraping
# Author      : Christian Kariso
# Created     : 10/08/2026
# Language    : Python
# Description : How to plot the weather data from an Excel file using Matplotlib.
# ==========================================================


import pandas as pd
import matplotlib.pyplot as plt

nama_file = "Kembes_Dua_Indonesia_10_day_forecast_1345.xlsx" 
df = pd.read_excel(nama_file)

nama_daerah = df['Location'].iloc[0]

plt.style.use('bmh')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
fig.suptitle(f"Laporan Prakiraan Cuaca 10 Hari\nLokasi: {nama_daerah}", 
             fontsize=10, fontweight='bold', y=0.96)


ax1.plot(df['Tanggal'], df['Max Temp (°C)'], marker='o', color='#d62728', linewidth=2.5, label='Suhu Maks (C)')
ax1.plot(df['Tanggal'], df['Min Temp (°C)'], marker='o', color='#1f77b4', linewidth=2.5, label='Suhu Min (C)')

ax1.set_title('Pergerakan Suhu Udara', fontsize=10, pad=10)
ax1.set_ylabel('Suhu (°C)', fontsize=10)
ax1.legend(loc='upper right', frameon=True, shadow=True)
ax1.grid(True, linestyle='--', alpha=0.7)

bars = ax2.bar(df['Tanggal'], df['Precipitation (mm)'], color='#3498db', edgecolor='#2980b9', width=0.6)

ax2.set_title('Prakiraan Curah Hujan', fontsize=10, pad=10)
ax2.set_xlabel('Tanggal', fontsize=10)  
ax2.set_ylabel('Curah Hujan (mm)', fontsize=10)
ax2.grid(axis='y', linestyle='--', alpha=0.7)

for bar in bars:
    yval = bar.get_height()
    if yval > 0: 
        ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.5, 
                 f'{yval}', ha='center', va='bottom', fontsize=10, fontweight='bold')


plt.setp(ax1.get_xticklabels(), rotation=15, ha='right')
plt.setp(ax2.get_xticklabels(), rotation=15, ha='right')

plt.tight_layout()
plt.subplots_adjust(top=0.88, hspace=0.3)

plt.show()