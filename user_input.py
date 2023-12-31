import tkinter as tk
from tkinter import simpledialog
import random
import pickle


try:
    with open("user_input_data.pkl", "rb") as f:
        loaded_defaults = pickle.load(f)
        defaults = {
            'num_preds': loaded_defaults.get('num_preds', 100),
            'num_prey': loaded_defaults.get('num_prey', 200),
            'pred_hunger': loaded_defaults.get('pred_hunger', 200),
            'prey_hunger': loaded_defaults.get('prey_hunger', 100),
            'size': loaded_defaults.get('size', 150),
            'food_rate': loaded_defaults.get('food_rate', 1),
            'initial_food': loaded_defaults.get('initial_food', 200),
            'randomness_error': loaded_defaults.get('randomness_error', 200),
            'spoil_date': loaded_defaults.get('spoil_date', 50)  # Added this line
        }
except FileNotFoundError:
    defaults = {
        'num_preds': 100,
        'num_prey': 200,
        'pred_hunger': 200,
        'prey_hunger': 100,
        'size': 150,
        'food_rate': 1,
        'initial_food': 200,
        'randomness_error': 200,
        'spoil_date': 50  # Added this line
    }


class ParameterDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Number of Predators:").grid(row=0, sticky='W', padx=10, pady=5)
        tk.Label(master, text="Number of Preys:").grid(row=1, sticky='W', padx=10, pady=5)
        tk.Label(master, text="Predator Initial Hunger:").grid(row=2, sticky='W', padx=10, pady=5)
        tk.Label(master, text="Prey Initial Hunger:").grid(row=3, sticky='W', padx=10, pady=5)
        tk.Label(master, text="Size:").grid(row=4, sticky='W', padx=10, pady=5)
        tk.Label(master, text="Food Rate:").grid(row=5, sticky='W', padx=10, pady=5)
        tk.Label(master, text="Initial Food:").grid(row=6, sticky='W', padx=10, pady=5)
        tk.Label(master, text="Randomness Error (%):").grid(row=7, sticky='W', padx=10, pady=5)
        tk.Label(master, text="Food Spoil Date:").grid(row=8, sticky='W', padx=10, pady=5)

        self.pred_entry = tk.Entry(master)
        self.pred_entry.insert(0, defaults['num_preds'])
        self.pred_entry.grid(row=0, column=1, padx=10, pady=5)

        self.prey_entry = tk.Entry(master)
        self.prey_entry.insert(0, defaults['num_prey'])
        self.prey_entry.grid(row=1, column=1, padx=10, pady=5)

        self.pred_hunger_entry = tk.Entry(master)
        self.pred_hunger_entry.insert(0, defaults['pred_hunger'])
        self.pred_hunger_entry.grid(row=2, column=1, padx=10, pady=5)

        self.prey_hunger_entry = tk.Entry(master)
        self.prey_hunger_entry.insert(0, defaults['prey_hunger'])
        self.prey_hunger_entry.grid(row=3, column=1, padx=10, pady=5)

        self.size_entry = tk.Entry(master)
        self.size_entry.insert(0, defaults['size'])
        self.size_entry.grid(row=4, column=1, padx=10, pady=5)

        self.food_rate_entry = tk.Entry(master)
        self.food_rate_entry.insert(0, defaults['food_rate'])
        self.food_rate_entry.grid(row=5, column=1, padx=10, pady=5)

        self.initial_food_entry = tk.Entry(master)
        self.initial_food_entry.insert(0, defaults['initial_food'])
        self.initial_food_entry.grid(row=6, column=1, padx=10, pady=5)

        self.randomness_error_entry = tk.Entry(master)
        self.randomness_error_entry.insert(0, 0)  # 5% by default
        self.randomness_error_entry.grid(row=7, column=1, padx=10, pady=5)

        self.spoil_date_entry = tk.Entry(master)
        self.spoil_date_entry.insert(0, defaults['spoil_date'])
        self.spoil_date_entry.grid(row=8, column=1, padx=10, pady=5)


        return self.pred_entry  # initial focus

    def buttonbox(self):
        box = tk.Frame(self)

        ok_button = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        ok_button.pack(side=tk.LEFT, padx=5, pady=5)

        cancel_button = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def apply(self):
        num_preds = int(self.pred_entry.get())
        num_prey = int(self.prey_entry.get())
        pred_hunger = int(self.pred_hunger_entry.get())
        prey_hunger = int(self.prey_hunger_entry.get())
        size = int(self.size_entry.get())
        food_rate = float(self.food_rate_entry.get())
        initial_food = int(self.initial_food_entry.get())
        spoil_date = int(self.spoil_date_entry.get())

        randomness_error = int(self.randomness_error_entry.get()) / 100.0

        num_preds += random.randint(-int(randomness_error * num_preds), int(randomness_error * num_preds))
        num_prey += random.randint(-int(randomness_error * num_prey), int(randomness_error * num_prey))
        pred_hunger += random.randint(-int(randomness_error * pred_hunger), int(randomness_error * pred_hunger))
        prey_hunger += random.randint(-int(randomness_error * prey_hunger), int(randomness_error * prey_hunger))
        size += random.randint(-int(randomness_error * size), int(randomness_error * size))
        food_rate += random.uniform(-randomness_error * food_rate, randomness_error * food_rate)
        initial_food += random.randint(-int(randomness_error * initial_food), int(randomness_error * initial_food))
        spoil_date += random.randint(-int(randomness_error * spoil_date), int(randomness_error * spoil_date))

        self.result = num_preds, num_prey, size, pred_hunger, prey_hunger, food_rate, initial_food, spoil_date, randomness_error

        # Write user inputs to the pickle file
        with open("user_input_data.pkl", "wb") as f:
            data = {
                "num_preds": num_preds,
                "num_prey": num_prey,
                "size": size,
                "pred_hunger": pred_hunger,
                "prey_hunger": prey_hunger,
                "food_rate": food_rate,
                "initial_food": initial_food,
                "randomness_error": randomness_error,
                "spoil_date": spoil_date,
            }
            pickle.dump(data, f)

        # Update default values
        defaults.update(
            num_preds=num_preds, num_prey=num_prey, size=size, pred_hunger=pred_hunger,
            prey_hunger=prey_hunger, food_rate=food_rate, initial_food=initial_food, randomness_error=randomness_error,
            spoil_date=spoil_date
        )



def get_user_input():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    dialog = ParameterDialog(root)
    root.destroy()  # Destroy the root window
    return dialog.result
