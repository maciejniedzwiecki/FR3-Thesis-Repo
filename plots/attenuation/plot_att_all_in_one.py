import os
import pandas as pd
import matplotlib.pyplot as plt

# Ścieżki do folderów
input_folder = "csv_files/attenuation"
output_folder = "plots/attenuation"

# Lista dostępnych markerów
markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h', 'x', '+']

# Kolory
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

# Mapowanie nazw plików na etykiety w legendzie
labels_mapping = {
    "att_mean_modified_DREWNO.CSV": "Wooden wall",
    "att_mean_modified_KASETONY.CSV": "Ceiling Tiles",
    "att_mean_modified_LAZIENKA.CSV": "Interior wall",
    "att_mean_modified_OSB.CSV": "OSB board",
    "att_mean_modified_PLEKSI.CSV": "Polycarbonate",
    "att_mean_modified_PUSTAK.CSV": "External wall",
    "att_mean_modified_SZKLO.CSV": "Glass",
    "att_mean_modified_MIEDZ.CSV": "Copper sheet",
    "att_mean_modified_ZESPOLONA.CSV": "IRR glass",
}

# Sprawdzenie folderu wejściowego
if not os.path.exists(input_folder):
    print(f"Folder wejściowy '{input_folder}' nie istnieje!")
    exit()

# Sprawdzenie folderu wyjściowego
if not os.path.exists(output_folder):
    print(f"Folder wyjściowy '{output_folder}' nie istnieje! Tworzenie folderu...")
    os.makedirs(output_folder)

# Filtrowanie plików
all_files = [f for f in os.listdir(input_folder) if f.startswith("att_mean_modified") and "REFERENCYJNY" not in f]

# Zakres osi Y
y_min, y_max = 0, 65  # Zakres dla tłumienności

# Funkcja do rysowania wykresów
def draw_plot(files, title, filename, y_min, y_max):
    plt.figure(figsize=(10, 6))
    for i, file in enumerate(files):
        file_path = os.path.join(input_folder, file)
        marker = markers[i % len(markers)]
        color = colors[i % len(colors)]
        try:
            data = pd.read_csv(file_path, header=None, sep=";", names=["Frequency", "Attenuation"])
            plt.plot(
                data["Frequency"],
                data["Attenuation"],
                marker=marker,
                color=color,
                label=labels_mapping.get(file, file.replace(".CSV", ""))
            )
        except Exception as e:
            print(f"Błąd podczas wczytywania pliku {file}: {e}")

    plt.title(title)
    plt.xlabel("f [GHz]")
    plt.ylabel("Attenuation [dB]")
    plt.ylim(y_min, y_max)
    plt.yticks(range(y_min, y_max + 1, 5))  # Podziałka co 5 na osi Y
    plt.grid(True)

    # Legenda pod wykresem
    max_items_per_row = 5
    ncol = min(len(files), max_items_per_row)

    plt.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.11),
        ncol=ncol,
        fontsize='10',
        frameon=False
    )

    plt.savefig(os.path.join(output_folder, filename), bbox_inches='tight')
    plt.close()

# Generowanie wykresów
print("Tworzę wykres dla wszystkich materiałów...")
draw_plot(all_files, "Average Material Attenuation", "att_all_in_one.png", y_min, y_max)

print("Proces generowania wykresów zakończony.")
