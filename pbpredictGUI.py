import pandas as pd
import random
import itertools
import tkinter as tk
from tkinter import filedialog

# Define functions for your existing code
def predict_next_numbers(frequency_dict, num_numbers=5):
    total_frequency = sum(frequency_dict.values())
    weights = [total_frequency / (frequency_dict[num] * num_numbers) for num in frequency_dict.keys()]
    predicted_numbers = random.choices(list(frequency_dict.keys()), weights=weights, k=num_numbers)
    return predicted_numbers

def generate_combinations(numbers):
    if len(numbers) < 5:
        raise ValueError("At least five numbers are required.")
    combinations = list(itertools.combinations(numbers, 5))
    return combinations

def load_data():
    file_choice = choice_var.get()
    if file_choice == '1':
        excel_file = 'powerball.xlsx'
    elif file_choice == '2':
        excel_file = 'megamillions.xlsx'
    else:
        result_label.config(text="Invalid choice. Exiting the program.")
        return
    
    xls = pd.ExcelFile(excel_file)
    df = pd.read_excel(xls, 'winners')
    return df

def analyze_data():
    df = load_data()
    
    frequency_dict_winning = {}
    frequency_dict_powerball = {}
    
    for index, row in df.iterrows():
        winning_numbers_str = row['Winning Numbers']  
        powerball_number = row['Powerball']
        
        winning_numbers = [int(num) for num in winning_numbers_str.split()]
    
        for number in winning_numbers:
            number_str = str(number)
        
            if len(number_str) == 1:
                number_str = f'0{number_str}'
        
            if number_str in frequency_dict_winning:
                frequency_dict_winning[number_str] += 1
            else:
                frequency_dict_winning[number_str] = 1
    
        if powerball_number in frequency_dict_powerball:
            frequency_dict_powerball[powerball_number] += 1
        else:
            frequency_dict_powerball[powerball_number] = 1
    
    return frequency_dict_winning, frequency_dict_powerball

def predict_numbers():
    frequency_dict_winning, frequency_dict_powerball = analyze_data()
    
    most_frequent_winning_numbers = [number for number, _ in sorted(frequency_dict_winning.items(), key=lambda item: item[1], reverse=True)[:6]]
    combinations = generate_combinations(most_frequent_winning_numbers)
    
    predicted_winning_numbers = predict_next_numbers(frequency_dict_winning)
    predicted_powerball_number = predict_next_numbers(frequency_dict_powerball, num_numbers=1)[0]
    
    result_label.config(text="Six Most Frequently Drawn Winning Numbers:\n")
    for number, frequency in sorted(frequency_dict_winning.items(), key=lambda item: item[1], reverse=True)[:6]:
        result_label.config(text=result_label.cget("text") + f"Winning Number {number} appears {frequency} times\n")
    
    result_label.config(text=result_label.cget("text") + "\nFive Most Frequently Drawn Powerball/Megaball Numbers:\n")
    for number, frequency in sorted(frequency_dict_powerball.items(), key=lambda item: item[1], reverse=True)[:5]:
        result_label.config(text=result_label.cget("text") + f"Powerball/Megaball Number {number} appears {frequency} times\n")
    
    result_label.config(text=result_label.cget("text") + "\nUnique Combinations of 5 Numbers from the 6 Most Frequent Winning Numbers:\n")
    for combination in combinations:
        result_label.config(text=result_label.cget("text") + f"{combination}\n")
    
    result_label.config(text=result_label.cget("text") + f"\nPredicted Next Winning Numbers: {predicted_winning_numbers}\n")
    result_label.config(text=result_label.cget("text") + f"Predicted Next Powerball/Megaball Number: {predicted_powerball_number}\n")

# Create the main GUI window
root = tk.Tk()
root.title("Lottery Number Analyzer")

# Create a label and radio buttons for file choice
file_choice_label = tk.Label(root, text="Choose a game:")
file_choice_label.pack()
choice_var = tk.StringVar(value="1")
powerball_radio = tk.Radiobutton(root, text="Powerball", variable=choice_var, value="1")
megamillions_radio = tk.Radiobutton(root, text="Mega Millions", variable=choice_var, value="2")
powerball_radio.pack()
megamillions_radio.pack()

# Create a button to load and analyze data
load_analyze_button = tk.Button(root, text="Load and Analyze Data", command=predict_numbers)
load_analyze_button.pack()

# Create a label to display the results
result_label = tk.Label(root, text="", justify="left")
result_label.pack()

# Start the GUI main loop
root.mainloop()
