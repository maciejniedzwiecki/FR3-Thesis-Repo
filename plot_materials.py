import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm


# Funkcja do filtrowania plików na podstawie kryteriów
def filter_files(files, suffix, includes=None, excludes=None):
    if includes:
        return [f for f in files if f.endswith(suffix) and any(inc in f for inc in includes)]
    elif excludes:
        return [f for f in files if f.endswith(suffix) and f not in excludes]
    return [f for f in files if f.endswith(suffix)]


# Ścieżki do folderów
input_folder = "edit_files/Measurement Campaigns/avg_files"
output_folder = "edit_files/Measurement Campaigns/plots/materials_campaigns"

# Lista dostępnych markerów
markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h', 'x', '+']

# Kolory z palety (np. tab10)
#colors = cm.tab10.colors
#colors = ["blue", "orange", "green", "red", "purple", "brown", "pink", "gray", "lime", "turquoise"]
#colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
colors = ["#1f77b4", "orange", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]


# Mapowanie nazw plików na etykiety w legendzie
labels_mapping = {
    "avg_DREWNO_pierwszy.CSV": "Wooden wall",
    "avg_DREWNO_drugi.CSV": "Wooden wall",
    "avg_KASETONY_pierwszy.CSV": "Ceiling Tiles",
    "avg_KASETONY_drugi.CSV": "Ceiling Tiles",
    "avg_LAZIENKA_pierwszy.CSV": "Interior wall",
    "avg_LAZIENKA_drugi.CSV": "Interior wall",
    "avg_MIEDZ_pierwszy.CSV": "Copper sheet",
    "avg_MIEDZ_drugi.CSV": "Copper sheet",
    "avg_OSB_pierwszy.CSV": "OSB board",
    "avg_OSB_drugi.CSV": "OSB board",
    "avg_PLEKSI_pierwszy.CSV": "Polycarbonate",
    "avg_PLEKSI_drugi.CSV": "Polycarbonate",
    "avg_PUSTAK_pierwszy.CSV": "External wall",
    "avg_PUSTAK_drugi.CSV": "External wall",
    "avg_SZKLO_pierwszy.CSV": "Glass",
    "avg_SZKLO_drugi.CSV": "Glass",
    "avg_ZESPOLONA_pierwszy.CSV": "IRR glass",
    "avg_ZESPOLONA_drugi.CSV": "IRR glass",
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
    print()  # Pusta linia przed folderem wyjściowym

# Sprawdzenie folderu wyjściowego
if not os.path.exists(output_folder):
    print(f"Folder wyjściowy '{output_folder}' nie istnieje! Tworzenie folderu...")
    os.makedirs(output_folder)
    print(f"Folder '{output_folder}' został utworzony.")
else:
    print(f"Folder wyjściowy '{output_folder}' istnieje i jest dostępny.\n")

# Pliki referencyjne (do całkowitego wykluczenia)
reference_files = [
    "avg_REFERENCYJNY_pierwszy.CSV",
    "avg_REFERENCYJNY_drugi.CSV"
]

# Filtrowanie plików
pierwszy_files = filter_files(files, "_pierwszy.CSV",
                              excludes=reference_files + ["avg_MIEDZ_pierwszy.CSV", "avg_ZESPOLONA_pierwszy.CSV"])
drugi_files = filter_files(files, "_drugi.CSV",
                           excludes=reference_files + ["avg_MIEDZ_drugi.CSV", "avg_ZESPOLONA_drugi.CSV"])

excluded_pierwszy_files = filter_files(files, "_pierwszy.CSV", includes=["MIEDZ", "ZESPOLONA"])
excluded_drugi_files = filter_files(files, "_drugi.CSV", includes=["MIEDZ", "ZESPOLONA"])

# Zakresy osi Y
y_min, y_max = -65, -29  # Dla podstawowych
excluded_y_min, excluded_y_max = -105, -70  # Dla wykluczonych


# Funkcja do rysowania wykresów
def draw_plot(files, title, filename, output_folder, y_min, y_max):
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
    max_items_per_row = 4  # Maksymalna liczba elementów w jednym wierszu
    ncol = min(len(files), max_items_per_row)

    plt.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.11),
        ncol=ncol,
        fontsize='10',
        frameon=False
    )

    # Zapis wykresu
    plt.savefig(os.path.join(output_folder, filename), bbox_inches='tight')
    plt.close()


# Generowanie wykresów dla plików podstawowych
print("Tworzę wykresy dla plików podstawowych")
draw_plot(pierwszy_files, "Received Power (First Measurement Campaign)", "series_pierwszy.png", output_folder, y_min,
          y_max)
draw_plot(drugi_files, "Received Power (Second Measurement Campaign)", "series_drugi.png", output_folder, y_min, y_max)

# Generowanie wykresów dla plików wykluczonych
print("Tworzę wykresy dla plików wykluczonych")
draw_plot(excluded_pierwszy_files, "Received Power (First Measurement Campaign)",
          "excluded_series_pierwszy.png", output_folder, excluded_y_min, excluded_y_max)
draw_plot(excluded_drugi_files, "Received Power (Second Measurement Campaign)",
          "excluded_series_drugi.png", output_folder, excluded_y_min, excluded_y_max)

print("Proces generowania wykresów zakończony.")
