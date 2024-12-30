import tkinter as tk
from tkinter import ttk
from .sensors import SensorSimulator
from .protocols import ServerClient
from .localization import LANGUAGES
from .settings import SETTINGS, UNIT_SYSTEMS
from datetime import datetime

class IoTClientApp:
    def __init__(self, root):
        self.root = root
        self.language = 'uk'
        self.texts = LANGUAGES[self.language]

        self.root.title(self.texts['title'])
        self.simulator = SensorSimulator()
        self.client = ServerClient("http://127.0.0.1:5000")

        self.setup_ui()

    def switch_language(self, lang):
        """Перемикання мови інтерфейсу"""
        self.language = lang
        self.texts = LANGUAGES[self.language]
        self.refresh_ui()

    def refresh_ui(self):
        """Оновлює текст інтерфейсу для поточної мови"""
        self.root.title(self.texts['title'])
        self.server_url_label.config(text=self.texts['server_url'])
        self.elevator_id_label.config(text=self.texts['elevator_id'])
        self.start_button.config(text=self.texts['start_simulation'])
        self.stop_button.config(text=self.texts['stop_simulation'])
        #self.control_panel_label.config(text=self.texts['control_panel'])
        self.power_button.config(text=self.texts['toggle_power'])
        self.stuck_button.config(text=self.texts['toggle_stuck'])
        self.move_button.config(text=self.texts['toggle_move'])
        self.settings_label.config(text=self.texts['settings'])
        self.date_format_label.config(text=self.texts['date_format'])
        self.time_zone_label.config(text=self.texts['time_zone'])
        self.unit_system_label.config(text=self.texts['unit_system'])
        self.save_settings_button.config(text=self.texts['save_settings'])
        self.temp_min_label.config(text=self.texts['temperature_min'])
        self.temp_max_label.config(text=self.texts['temperature_max'])
        self.hum_min_label.config(text=self.texts['humidity_min'])
        self.hum_max_label.config(text=self.texts['humidity_max'])
        self.fixed_weight_label.config(text=self.texts['weight'])
        self.apply_simulation_params_button.config(text=self.texts['apply_simulation_params'])

    def setup_ui(self):
        """Налаштування графічного інтерфейсу"""
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Вибір мови
        language_frame = ttk.Frame(frame)
        language_frame.grid(row=0, column=0, sticky=tk.W, columnspan=2)
        ttk.Button(language_frame, text="EN", command=lambda: self.switch_language('en')).grid(row=0, column=0, padx=5)
        ttk.Button(language_frame, text="UK", command=lambda: self.switch_language('uk')).grid(row=0, column=1, padx=5)

        self.auth_frame = ttk.Frame(frame, padding=10)
        self.auth_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W)
        ttk.Label(self.auth_frame, text="Admin Email:").grid(row=0, column=0, sticky=tk.W)
        self.email_entry = ttk.Entry(self.auth_frame, width=20)
        self.email_entry.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(self.auth_frame, text="Password:").grid(row=1, column=0, sticky=tk.W)
        self.password_entry = ttk.Entry(self.auth_frame, width=20, show="*")
        self.password_entry.grid(row=1, column=1, sticky=tk.W)

        self.auth_button = ttk.Button(self.auth_frame, text="Login", command=self.authenticate)
        self.auth_button.grid(row=2, column=1, sticky=tk.W)

        # Поле введення URL сервера
        self.server_url_label = ttk.Label(frame, text=self.texts['server_url'])
        self.server_url_label.grid(row=3, column=0, sticky=tk.W)
        self.url_entry = ttk.Entry(frame, width=40)
        self.url_entry.insert(0, "http://127.0.0.1:5000")
        self.url_entry.grid(row=3, column=1, sticky=tk.W)

        # Поле введення Elevator ID
        self.elevator_id_label = ttk.Label(frame, text=self.texts['elevator_id'])
        self.elevator_id_label.grid(row=4, column=0, sticky=tk.W)
        self.elevator_id_entry = ttk.Entry(frame, width=10)
        self.elevator_id_entry.grid(row=4, column=1, sticky=tk.W)

        # Налаштування
        self.settings_label = ttk.Label(frame, text=self.texts['settings'])
        self.settings_label.grid(row=5, column=0, sticky=tk.W)

        # Вибір формату дати
        self.date_format_label = ttk.Label(frame, text=self.texts['date_format'])
        self.date_format_label.grid(row=6, column=0, sticky=tk.W)
        self.date_format_entry = ttk.Entry(frame, width=20)
        self.date_format_entry.insert(0, SETTINGS['date_format'])
        self.date_format_entry.grid(row=6, column=1, sticky=tk.W)

        # Група для Time Zone, Unit System і Save Settings
        settings_row_frame = ttk.Frame(frame)
        settings_row_frame.grid(row=5, column=0, columnspan=2, sticky=tk.W)

        # Вибір часової зони
        self.time_zone_label = ttk.Label(settings_row_frame, text=self.texts['time_zone'])
        self.time_zone_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.time_zone_var = tk.StringVar(value=SETTINGS['time_zone'])
        ttk.OptionMenu(settings_row_frame, self.time_zone_var, SETTINGS['time_zone'], "local", "UTC").grid(row=0, column=1, sticky=tk.W)

        # Вибір системи мір
        self.unit_system_label = ttk.Label(settings_row_frame, text=self.texts['unit_system'])
        self.unit_system_label.grid(row=0, column=2, sticky=tk.W, padx=(10, 5))
        self.unit_system_var = tk.StringVar(value=SETTINGS['unit_system'])
        ttk.OptionMenu(settings_row_frame, self.unit_system_var, SETTINGS['unit_system'], "metric", "imperial").grid(row=0, column=3, sticky=tk.W)

        # Кнопка для збереження налаштувань
        self.save_settings_button = ttk.Button(settings_row_frame, text=self.texts['save_settings'], command=self.save_settings)
        self.save_settings_button.grid(row=0, column=4, sticky=tk.W, padx=(10, 0))

        # Кнопка для запуску симуляції
        self.start_button = ttk.Button(frame, text=self.texts['start_simulation'], command=self.start_simulation)
        self.start_button.grid(row=7, column=0, sticky=tk.W)

        # Кнопка для зупинки симуляції
        self.stop_button = ttk.Button(frame, text=self.texts['stop_simulation'], command=self.stop_simulation, state=tk.DISABLED)
        self.stop_button.grid(row=7, column=1, sticky=tk.W)

        # Фрейм для кнопок
        control_buttons_frame = ttk.Frame(frame)
        control_buttons_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E))

        # Кнопки управління аварійними ситуаціями
        self.power_button = ttk.Button(control_buttons_frame, text=self.texts['toggle_power'], command=self.toggle_power)
        self.power_button.grid(row=0, column=0, padx=5, pady=2)

        self.stuck_button = ttk.Button(control_buttons_frame, text=self.texts['toggle_stuck'], command=self.toggle_stuck)
        self.stuck_button.grid(row=0, column=1, padx=5, pady=2)

        self.move_button = ttk.Button(control_buttons_frame, text=self.texts['toggle_move'], command=self.toggle_move)
        self.move_button.grid(row=0, column=2, padx=5, pady=2)

        # Розтягування кнопок по горизонталі
        control_buttons_frame.columnconfigure(0, weight=1)
        control_buttons_frame.columnconfigure(1, weight=1)
        control_buttons_frame.columnconfigure(2, weight=1)

        # Поля для налаштування параметрів генерації
        self.temp_min_label = ttk.Label(frame, text=self.texts['temperature_min'])
        self.temp_min_label.grid(row=9, column=0, sticky=tk.W)
        self.temp_min_entry = ttk.Entry(frame, width=10)
        self.temp_min_entry.insert(0, "-0.5")
        self.temp_min_entry.grid(row=9, column=1, sticky=tk.W)

        self.temp_max_label = ttk.Label(frame, text=self.texts['temperature_max'])
        self.temp_max_label.grid(row=9, column=2, sticky=tk.W)
        self.temp_max_entry = ttk.Entry(frame, width=10)
        self.temp_max_entry.insert(0, "0.5")
        self.temp_max_entry.grid(row=9, column=3, sticky=tk.W)

        self.hum_min_label = ttk.Label(frame, text=self.texts['humidity_min'])
        self.hum_min_label.grid(row=10, column=0, sticky=tk.W)
        self.hum_min_entry = ttk.Entry(frame, width=10)
        self.hum_min_entry.insert(0, "-1.0")
        self.hum_min_entry.grid(row=10, column=1, sticky=tk.W)

        self.hum_max_label = ttk.Label(frame, text=self.texts['humidity_max'])
        self.hum_max_label.grid(row=10, column=2, sticky=tk.W)
        self.hum_max_entry = ttk.Entry(frame, width=10)
        self.hum_max_entry.insert(0, "1.0")
        self.hum_max_entry.grid(row=10, column=3, sticky=tk.W)

        self.fixed_weight_label = ttk.Label(frame, text=self.texts['weight'])
        self.fixed_weight_label.grid(row=11, column=0, sticky=tk.W)
        self.fixed_weight_entry = ttk.Entry(frame, width=10)
        self.fixed_weight_entry.insert(0, "0.0")
        self.fixed_weight_entry.grid(row=11, column=1, sticky=tk.W)

        self.apply_simulation_params_button = ttk.Button(frame, text=self.texts['apply_simulation_params'], 
                                                         command=self.apply_simulation_params)
        self.apply_simulation_params_button.grid(row=12, column=2, sticky=tk.W)

        # Поле для виводу відправлених даних
        self.log_text = tk.Text(self.root, height=15, width=60, state=tk.DISABLED)
        self.log_text.grid(row=13, column=0, columnspan=2, padx=10, pady=10)

    def save_settings(self):
        """Зберігає налаштування"""
        SETTINGS['date_format'] = self.date_format_entry.get()
        SETTINGS['time_zone'] = self.time_zone_var.get()
        SETTINGS['unit_system'] = self.unit_system_var.get()
        self.log(f"Settings updated: {SETTINGS}")

    def log(self, message):
        """Додає повідомлення до логів"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)

    def start_simulation(self):
        """Запуск симуляції роботи сенсорів"""
        if not self.client.token:
            self.log("Error: Please authenticate before starting the simulation.")
            return
        self.simulating = True
        self.client.base_url = self.url_entry.get()
        self.log(self.texts['simulation_started'])
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.simulate()

    def stop_simulation(self):
        """Зупинка симуляції роботи сенсорів"""
        self.simulating = False
        self.log(self.texts['simulation_stopped'])
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def simulate(self):
        """Симуляція даних сенсорів і відправка їх на сервер"""
        if self.simulating:
            data = self.simulator.generate_data()

            # Перетворення формату рядка
            date_format = SETTINGS['date_format']
            timestamp = datetime.strptime(data['timestamp'], "%Y-%m-%d %H:%M:%S")
            timestamp = timestamp.strftime(date_format)

            # Отримати elevator_id з інтерфейсу
            try:
                elevator_id = int(self.elevator_id_entry.get())
                data["elevator_id"] = elevator_id
            except ValueError:
                self.log(self.texts['invalid_elevator_id'])
                self.stop_simulation()
                return
            
            # Конвертація одиниць вимірювання для виводу
            if "temperature" in data and "humidity" in data and "weight" in data:
                converted_data = {
                    "temperature": f"{round(data['temperature'] * 9/5 + 32, 2)} °F" if SETTINGS['unit_system'] == "imperial" else f"{data['temperature']} °C",
                    "humidity": f"{data['humidity']} %",
                    "weight": f"{round(data['weight'] * 2.20462, 2)} lbs" if SETTINGS['unit_system'] == "imperial" else f"{data['weight']} kg",
                    "timestamp": timestamp,
                    "current_floor": data["current_floor"],
                    "is_moving": data["is_moving"],
                    "is_power_on": data["is_power_on"],
                    "is_stuck": data["is_stuck"],
                }   
                self.log(f"{self.texts['sent']}: {converted_data}")
            else:
                converted_data = {
                    "timestamp": timestamp,
                    "is_power_on": data["is_power_on"],
                    "is_moving": data["is_moving"],
                    "is_stuck": data["is_stuck"],
                }
                self.log(f"{self.texts['sent']}: {converted_data}")
            # Надсилання даних
            response = self.client.send_sensor_data(data)
            self.log(f"{self.texts['response']}: {response}")
            self.root.after(1000, self.simulate) # Повторювати кожну секунду

    def log(self, message):
        """Додає повідомлення до логів"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)

    def toggle_power(self):
        """Перемикає стан живлення"""
        self.simulator.is_power_on = not self.simulator.is_power_on
        state = self.texts['state_on'] if self.simulator.is_power_on else self.texts['state_off']
        self.log(self.texts['power_toggled'].format(state=state))

    def toggle_stuck(self):
        """Перемикає стан застрягання"""
        self.simulator.is_stuck = not self.simulator.is_stuck
        state = self.texts['state_stuck'] if self.simulator.is_stuck else self.texts['state_moving_normally']
        self.log(self.texts['stuck_toggled'].format(state=state))

    def toggle_move(self):
        """Перемикає стан руху"""
        self.simulator.is_moving = not self.simulator.is_moving
        state = self.texts['state_moving'] if self.simulator.is_moving else self.texts['state_stopped']
        self.log(self.texts['movement_toggled'].format(state=state))

    def apply_simulation_params(self):
        """Застосовує нові параметри генерації"""
        try:
            temperature_min = float(self.temp_min_entry.get())
            temperature_max = float(self.temp_max_entry.get())
            humidity_min = float(self.hum_min_entry.get())
            humidity_max = float(self.hum_max_entry.get())
            fixed_weight = float(self.fixed_weight_entry.get())

            self.simulator.update_simulation_params(temperature_min, 
                                                    temperature_max, 
                                                    humidity_min, 
                                                    humidity_max, 
                                                    fixed_weight)
            self.log("Simulation parameters updated successfully.")
        except ValueError:
            self.log("Error: Invalid simulation parameter input.")

    def authenticate(self):
        """Авторизація адміністратора"""
        email = self.email_entry.get()
        password = self.password_entry.get()
        if not email or not password:
            self.log("Error: Email and password are required.")
            return

        result = self.client.authenticate(email, password)
        if result["success"]:
            self.log("Authentication successful.")
        else:
            self.log(f"Authentication failed: {result['message']}")


if __name__ == "__main__":
    root = tk.Tk()
    app = IoTClientApp(root)
    root.mainloop()