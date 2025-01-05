import os
import pandas as pd
import matplotlib.pyplot as plt

# Ścieżki do folderów
input_folder = "edit_files/Measurement Campaigns/mean_files"
output_folder = "edit_files/Measurement Campaigns/plots/materials_means"

# Lista dostępnych markerów
markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h', 'x', '+']

# Kolory
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

# Mapowanie nazw plików na etykiety w legendzie
labels_mapping = {
    "mean_avg_DREWNO.CSV": "Wooden wall",
    "mean_avg_KASETONY.CSV": "Ceiling Tiles",
    "mean_avg_LAZIENKA.CSV": "Interior wall",
    "mean_avg_OSB.CSV": "OSB board",
    "mean_avg_PLEKSI.CSV": "Polycarbonate",
    "mean_avg_PUSTAK.CSV": "External wall",
    "mean_avg_SZKLO.CSV": "Glass",
    "mean_avg_ZESPOLONA.CSV": "IRR glass",
    "mean_avg_MIEDZ.CSV": "Copper sheet",
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
all_files = [f for f in files if f.startswith("mean_avg") and all(x not in f for x in ["REFERENCYJNY", "MIEDZ", "ZESPOLONA"])]
excluded_files = [f for f in files if f.startswith("mean_avg") and any(x in f for x in ["MIEDZ", "ZESPOLONA"])]

# Zakresy osi Y
y_min, y_max = -60, -29  # Dla podstawowych
excluded_y_min, excluded_y_max = -100, -75  # Dla wykluczonych

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
    max_items_per_row = 4
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
print("Tworzę wykresy...")
draw_plot(all_files, "Average received power (without Copper sheet & IRR glass)", "all_measurements.png", y_min, y_max)
draw_plot(excluded_files, "Average received power (Copper sheet & IRR glass)", "excluded_measurements.png", excluded_y_min, excluded_y_max)

print("Proces generowania wykresów zakończony.")
