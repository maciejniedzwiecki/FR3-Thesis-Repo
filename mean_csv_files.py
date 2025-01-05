# średnie z 2 serii

import os
import pandas as pd

# Ścieżki do folderów
input_folder = "edit_files/Measurement Campaigns/avg_files"
output_folder = "edit_files/Measurement Campaigns/mean_files"

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

# Grupowanie plików według prefixów
prefixes = set(f.split("_pierwszy")[0] for f in files if "_pierwszy" in f)

for prefix in prefixes:
    print(f"Przetwarzam pliki dla prefiksu: {prefix}")

    # Ścieżki do plików '_pierwszy' i '_drugi'
    pierwszy_file = os.path.join(input_folder, f"{prefix}_pierwszy.CSV")
    drugi_file = os.path.join(input_folder, f"{prefix}_drugi.CSV")

    # Sprawdzenie, czy oba pliki istnieją
    if not os.path.exists(pierwszy_file) or not os.path.exists(drugi_file):
        print(f"Brakuje jednego z plików dla prefiksu {prefix}:")
        print(f"{pierwszy_file} lub {drugi_file} nie istnieje!\n")
        continue

    # Wczytanie danych
    try:
        data_pierwszy = pd.read_csv(pierwszy_file, header=None, sep=";", names=["Frequency", "Power1"])
        data_drugi = pd.read_csv(drugi_file, header=None, sep=";", names=["Frequency", "Power2"])
    except Exception as e:
        print(f"Błąd podczas wczytywania plików dla prefiksu {prefix}: {e}")
        continue

    # Połączenie danych na podstawie częstotliwości
    try:
        merged_data = pd.merge(data_pierwszy, data_drugi, on="Frequency")
        merged_data["Average"] = merged_data[["Power1", "Power2"]].mean(axis=1)
    except Exception as e:
        print(f"Błąd podczas łączenia danych dla prefiksu {prefix}: {e}")
        continue

    # Zapis wyników do nowego pliku
    output_file = os.path.join(output_folder, f"mean_{prefix}.CSV")
    merged_data[["Frequency", "Average"]].to_csv(output_file, index=False, header=False, sep=";")
    print(f"Wynik zapisano do pliku: {output_file}\n")

print("Proces zakończony.")
