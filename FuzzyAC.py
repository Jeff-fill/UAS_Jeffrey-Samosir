import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend to avoid Tkinter issues
import matplotlib.pyplot as plt

# Parameter sistem
temperature = ctrl.Antecedent(np.arange(16, 36, 1), 'temperature')  # Suhu dalam °C
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')       # Kelembapan dalam %
fan_speed = ctrl.Consequent(np.arange(0, 101, 1), 'fan_speed')     # Kecepatan kipas dalam %

# Fungsi keanggotaan untuk suhu
temperature['cold'] = fuzz.trimf(temperature.universe, [16, 16, 24])
temperature['comfortable'] = fuzz.trimf(temperature.universe, [20, 25, 30])
temperature['hot'] = fuzz.trimf(temperature.universe, [26, 36, 36])

# Fungsi keanggotaan untuk kelembapan
humidity['dry'] = fuzz.trimf(humidity.universe, [0, 0, 50])
humidity['normal'] = fuzz.trimf(humidity.universe, [30, 50, 70])
humidity['humid'] = fuzz.trimf(humidity.universe, [60, 100, 100])

# Fungsi keanggotaan untuk kecepatan kipas
fan_speed['low'] = fuzz.trimf(fan_speed.universe, [0, 0, 50])
fan_speed['medium'] = fuzz.trimf(fan_speed.universe, [30, 50, 70])
fan_speed['high'] = fuzz.trimf(fan_speed.universe, [50, 100, 100])

# Aturan fuzzy
rule1 = ctrl.Rule(temperature['cold'] & humidity['dry'], fan_speed['low'])
rule2 = ctrl.Rule(temperature['comfortable'] & humidity['normal'], fan_speed['medium'])
rule3 = ctrl.Rule(temperature['hot'] | humidity['humid'], fan_speed['high'])

# Sistem kontrol
fan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
fan_simulation = ctrl.ControlSystemSimulation(fan_ctrl)

# Fungsi untuk menerima input
def get_input(prompt, min_value, max_value):
    while True:
        try:
            value = float(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Masukkan angka antara {min_value}-{max_value}.")
        except ValueError:
            print("Masukkan angka yang valid.")

# Input dari pengguna
print("Sistem Pengaturan AC Otomatis")
temperature_value = get_input("Masukkan Suhu Ruangan (°C, antara 16-36): ", 16, 36)
humidity_value = get_input("Masukkan Kelembapan (%, antara 0-100): ", 0, 100)

# Memberikan input ke sistem fuzzy
fan_simulation.input['temperature'] = temperature_value
fan_simulation.input['humidity'] = humidity_value

# Menghitung hasil
fan_simulation.compute()

# Output hasil
fan_speed_output = fan_simulation.output['fan_speed']
if fan_speed_output <= 33:
    speed_level = "Low"
elif fan_speed_output <= 66:
    speed_level = "Medium"
else:
    speed_level = "High"

print(f"\nKecepatan Kipas AC: {fan_speed_output:.2f}%")
print(f"Kategori: {speed_level}")

# Visualisasi dan menyimpan grafik sebagai file
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Visualisasi untuk suhu
temperature.view(ax=axs[0, 0])
axs[0, 0].set_title("Fungsi Keanggotaan: Temperature")

# Visualisasi untuk kelembapan
humidity.view(ax=axs[0, 1])
axs[0, 1].set_title("Fungsi Keanggotaan: Humidity")

# Visualisasi untuk kecepatan kipas
fan_speed.view(sim=fan_simulation, ax=axs[1, 0])
axs[1, 0].set_title("Fungsi Keanggotaan: Fan Speed")

plt.tight_layout()
plt.savefig("output_plot.png")  # Menyimpan plot ke file
print("Grafik telah disimpan sebagai 'output_plot.png'")
