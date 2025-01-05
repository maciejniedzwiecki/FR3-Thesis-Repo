import os
import pandas as pd

# Ścieżki do folderów
input_folder = "edit_files/Measurement Campaigns/mean_files"
output_folder = "edit_files/Attenuation/att_files"

# Plik referencyjny
reference_file = os.path.join(input_folder, "mean_avg_REFERENCYJNY.CSV")

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

# Wczytanie danych z pliku referencyjnego
print(f"Wczytuję dane z pliku referencyjnego: {reference_file}")
try:
    ref_data = pd.read_csv(reference_file, header=None, sep=";", names=["Frequency", "RefPower"])
    print("Dane referencyjne wczytano pomyślnie.\n")
except Exception as e:
    print(f"Błąd podczas wczytywania pliku referencyjnego: {e}")
    exit()

# Przetwarzanie pozostałych plików
for file in files:
    if file == "mean_avg_REFERENCYJNY.CSV":
        continue  # Pomijamy plik referencyjny

    file_path = os.path.join(input_folder, file)
    try:
        # Wczytanie danych
        data = pd.read_csv(file_path, header=None, sep=";", names=["Frequency", "Power"])

        # Połączenie danych na podstawie częstotliwości
        merged_data = pd.merge(ref_data, data, on="Frequency")

        # Obliczanie tłumienności
        merged_data["Attenuation"] = merged_data["RefPower"] - merged_data["Power"]

        # Zapis wyników do nowego pliku
        output_file = os.path.join(output_folder, f"att_{file}")
        merged_data[["Frequency", "Attenuation"]].to_csv(output_file, index=False, header=False, sep=";")
        print(f"Wynik zapisano do pliku: {output_file}")
    except Exception as e:
        print(f"Błąd podczas przetwarzania pliku {file}: {e}")

print("Proces obliczania tłumienności zakończony.")
