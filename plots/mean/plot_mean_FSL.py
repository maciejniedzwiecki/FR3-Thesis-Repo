import os
import pandas as pd
import matplotlib.pyplot as plt

# Ścieżki do pliku CSV
input_folder = "csv_files/mean"
output_folder = "plots/mean"
input_file = os.path.join(input_folder, "mean_modified_REFERENCYJNY.CSV")

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

# Wczytanie danych z pliku CSV
print(f"Wczytuję dane z pliku: {input_file}")
try:
    data = pd.read_csv(input_file, header=None, sep=";", names=["Frequency", "Power"])
    print("Dane wczytano pomyślnie.\n")
except Exception as e:
    print(f"Błąd podczas wczytywania pliku: {e}")
    exit()

# Zakres osi Y
y_min, y_max = -38, -28

# Tworzenie wykresu
print("Tworzę wykres FSL dla mean_avg_REFERENCYJNY")
plt.figure(figsize=(10, 6))
plt.plot(data["Frequency"], data["Power"], marker='o', color="#1f77b4", label="FSL")
plt.title("Average Free-Space Loss")
plt.xlabel("f [GHz]")
plt.ylabel("Received Power [dBm]")
plt.ylim(y_min, y_max)  # Ustalony zakres osi Y
plt.yticks(range(y_min, y_max + 1, 1))  # Podziałka co 1 na osi Y
plt.grid(True)
plt.legend(loc='upper left')  # Legenda w lewym górnym rogu
plt.savefig(os.path.join(output_folder, "mean_modified_REFERENCYJNY.png"))
plt.close()
print("Wykres mean_modified_REFERENCYJNY zapisano.\n")

print("Proces generowania wykresu zakończony.")
