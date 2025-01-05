import os
import pandas as pd
import matplotlib.pyplot as plt

# Ścieżki do plików CSV
input_folder = "edit_files/avg_files"
output_folder = "edit_files/plots"
file1 = os.path.join(input_folder, "avg_REFERENCYJNY_pierwszy.CSV")
file2 = os.path.join(input_folder, "avg_REFERENCYJNY_drugi.CSV")

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

# Wczytanie danych z plików CSV
print(f"Wczytuję dane z plików: {file1} i {file2}")
try:
    data1 = pd.read_csv(file1, header=None, sep=";", names=["Frequency", "Power"])
    data2 = pd.read_csv(file2, header=None, sep=";", names=["Frequency", "Power"])
    print("Dane wczytano pomyślnie.\n")
except Exception as e:
    print(f"Błąd podczas wczytywania plików: {e}")
    exit()

# Zakres osi Y
y_min, y_max = -38, -28

# Wykres 1: avg_REFERENCYJNY_pierwszy
print("Tworzę wykres: avg_REFERENCYJNY_pierwszy")
plt.figure(figsize=(10, 6))
plt.plot(data1["Frequency"], data1["Power"], marker='o', label="First Measurement Campaign")
plt.title("FSL (First Measurement Campaign)")
plt.xlabel("f [GHz]")
plt.ylabel("Received Power [dBm]")
plt.ylim(y_min, y_max)  # Ustalony zakres osi Y
plt.yticks(range(y_min, y_max + 1, 1))  # Podziałka co 1 na osi Y
plt.grid(True)
plt.legend(loc='upper left')  # Legenda w lewym górnym rogu
plt.savefig(os.path.join(output_folder, "avg_REFERENCYJNY_pierwszy.png"))
plt.close()
print("Wykres avg_REFERENCYJNY_pierwszy zapisano.\n")

# Wykres 2: avg_REFERENCYJNY_drugi
print("Tworzę wykres: avg_REFERENCYJNY_drugi")
plt.figure(figsize=(10, 6))
plt.plot(data2["Frequency"], data2["Power"], marker='o', color='orange', label="Second Measurement Campaign")
plt.title("FSL (Second Measurement Campaign)")
plt.xlabel("f [GHz]")
plt.ylabel("Received Power [dBm]")
plt.ylim(y_min, y_max)  # Ustalony zakres osi Y
plt.yticks(range(y_min, y_max + 1, 1))  # Podziałka co 1 na osi Y
plt.grid(True)
plt.legend(loc='upper left')  # Legenda w lewym górnym rogu
plt.savefig(os.path.join(output_folder, "avg_REFERENCYJNY_drugi.png"))
plt.close()
print("Wykres avg_REFERENCYJNY_drugi zapisano.\n")

# Wykres 3: Oba pliki na jednym wykresie
print("Tworzę wykres: avg_REFERENCYJNY_combined")
plt.figure(figsize=(10, 6))
plt.plot(data1["Frequency"], data1["Power"], marker='o', label="First Measurement Campaign")
plt.plot(data2["Frequency"], data2["Power"], marker='o', color='orange', label="Second Measurement Campaign")
plt.title("Free-Space Loss Measurement")
plt.xlabel("f [GHz]")
plt.ylabel("Received Power [dBm]")
plt.ylim(y_min, y_max)  # Ustalony zakres osi Y
plt.yticks(range(y_min, y_max + 1, 1))  # Podziałka co 1 na osi Y
plt.grid(True)
plt.legend(loc='upper left')  # Legenda w lewym górnym rogu
plt.savefig(os.path.join(output_folder, "avg_REFERENCYJNY_combined.png"))
plt.close()
print("Wykres avg_REFERENCYJNY_combined zapisano.\n")

print("Proces generowania wykresów zakończony.")
