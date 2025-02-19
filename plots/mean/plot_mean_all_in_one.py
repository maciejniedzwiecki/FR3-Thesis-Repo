import os
import pandas as pd
import matplotlib.pyplot as plt

# Ścieżki do folderów
input_folder = "csv_files/mean"
output_folder = "plots/mean"

# Lista dostępnych markerów
markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h', 'x', '+']

# Kolory
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

# Mapowanie nazw plików na etykiety w legendzie
labels_mapping = {
    "mean_modified_DREWNO.CSV": "Wooden wall",
    "mean_modified_KASETONY.CSV": "Ceiling Tiles",
    "mean_modified_LAZIENKA.CSV": "Interior wall",
    "mean_modified_OSB.CSV": "OSB board",
    "mean_modified_PLEKSI.CSV": "Polycarbonate",
    "mean_modified_PUSTAK.CSV": "External wall",
    "mean_modified_SZKLO.CSV": "Glass",
    "mean_modified_ZESPOLONA.CSV": "IRR glass",
    "mean_modified_MIEDZ.CSV": "Copper sheet",
}

# Sprawdzenie folderu wejściowego
if not os.path.exists(input_folder):
    print(f"Folder wejściowy '{input_folder}' nie istnieje!")
    exit()
else:
    print(f"Folder wejściowy '{input_folder}' istnieje i jest dostępny.")
    print("Pliki w folderze:")
    files = os.listdir(input_folder)
    print(files)
    print()

# Sprawdzenie folderu wyjściowego
if not os.path.exists(output_folder):
    print(f"Folder wyjściowy '{output_folder}' nie istnieje! Tworzenie folderu...")
    os.makedirs(output_folder)
    print(f"Folder '{output_folder}' został utworzony.")
else:
    print(f"Folder wyjściowy '{output_folder}' istnieje i jest dostępny.\n")

# Filtrowanie plików
all_files = [f for f in files if f.startswith("mean_modified") and "REFERENCYJNY" not in f]

# Zakres osi Y
y_min, y_max = -100, -29

# Funkcja do rysowania wykresów
def draw_plot(files, title, filename, y_min, y_max):
    plt.figure(figsize=(10, 6))
    for i, file in enumerate(files):
        file_path = os.path.join(input_folder, file)
        marker = markers[i % len(markers)]
        color = colors[i % len(colors)]
        try:
            data = pd.read_csv(file_path, header=None, sep=";", names=["Frequency", "Power"])
            plt.plot(
                data["Frequency"],
                data["Power"],
                marker=marker,
                color=color,
                label=labels_mapping.get(file, file.replace(".CSV", ""))
            )
        except Exception as e:
            print(f"Błąd podczas wczytywania pliku {file}: {e}")

    plt.title(title)
    plt.xlabel("f [GHz]")
    plt.ylabel("Received Power [dBm]")
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

# Generowanie wykresu dla wszystkich plików
print("Tworzę wykres dla wszystkich materiałów...")
draw_plot(all_files, "Average Received Power (All Materials)", "mean_modified_all_in_one.png", y_min, y_max)

print("Proces generowania wykresów zakończony.")
