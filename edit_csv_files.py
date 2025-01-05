import os
import pandas as pd


# Funkcja do generowania zakresu z krokiem float
def frange(start, stop, step):
    while start < stop:
        yield start
        start += step


# Ścieżki do folderów
input_folder = r"raw_files"  # Folder z plikami CSV
output_folder = r"edit_files\avg_files"  # Folder na pliki wynikowe

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

# Zakres wartości Frequency
frequency_values = [round(x, 1) for x in list(frange(7, 15.5, 0.5))]

# Przetwarzanie plików
for i, file_name in enumerate(files):
    if file_name.lower().endswith(".csv"):
        print(f"Przetwarzam plik: {file_name}")
        file_path = os.path.join(input_folder, file_name)

        # Wczytanie danych z pliku CSV
        try:
            data = pd.read_csv(file_path, header=None, sep=";", names=["Frequency", "Power"])
        except Exception as e:
            print(f"Błąd podczas wczytywania pliku {file_name}: {e}")
            continue

        # Usunięcie wierszy zgodnie ze schematem
        filtered_data = data.iloc[2::3].reset_index(drop=True)

        # Zamiana kolumny Frequency na zakres od 7 do 15 z krokiem 0.5
        if len(filtered_data) > len(frequency_values):
            filtered_data = filtered_data.iloc[:len(frequency_values)]

        filtered_data["Frequency"] = frequency_values[:len(filtered_data)]

        # Zapisanie zmodyfikowanego pliku
        new_file_name = f"avg_{file_name}"
        new_file_path = os.path.join(output_folder, new_file_name)

        try:
            filtered_data.to_csv(new_file_path, index=False, header=False, sep=";")
            print(f"Zapisano plik: {new_file_name}")
        except Exception as e:
            print(f"Błąd podczas zapisu pliku {new_file_name}: {e}")

        # Dodanie pustej linii co 2 pliki dla czytelności
        if (i + 1) % 2 == 0:
            print()

print("Proces zakończony.")
