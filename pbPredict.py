import pandas as pd
import random
import itertools

# Prompt the user to choose an Excel file
file_choice = input("Choose a game (1 for 'Powerball' or 2 for 'Mega Millions'): ")

if file_choice == '1':
    excel_file = 'powerball.xlsx'
elif file_choice == '2':
    excel_file = 'megamillions.xlsx'
else:
    print("Invalid choice. Exiting the program.")
    exit()

# Read data from the selected Excel file into a DataFrame
xls = pd.ExcelFile(excel_file)
df = pd.read_excel(xls, 'winners')

# Create an empty dictionary to store the frequency of each number for winning numbers
frequency_dict_winning = {}
# Create an empty dictionary to store the frequency of each number for Powerball numbers
frequency_dict_powerball = {}

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    # Extract the winning numbers and Powerball number from the row
    winning_numbers_str = row['Winning Numbers']  # Replace 'Winning Numbers' with the actual column name for winning numbers
    powerball_number = row['Powerball']  # Replace 'Powerball' with the actual column name for Powerball numbers
    
    # Split the winning numbers string into a list of individual numbers
    winning_numbers = [int(num) for num in winning_numbers_str.split()]

    # Iterate through winning numbers
    for number in winning_numbers:
        # Convert number to a string
        number_str = str(number)
        
        # Check if the number is a single-digit number and pad it with '0'
        if len(number_str) == 1:
            number_str = f'0{number_str}'
        
        # Check if the number is already in the dictionary for winning numbers
        if number_str in frequency_dict_winning:
            frequency_dict_winning[number_str] += 1
        else:
            frequency_dict_winning[number_str] = 1
    
    # Process the Powerball number
    # Check if the Powerball number is already in the dictionary for Powerball numbers
    if powerball_number in frequency_dict_powerball:
        frequency_dict_powerball[powerball_number] += 1
    else:
        frequency_dict_powerball[powerball_number] = 1

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

# Print the six most frequently drawn winning numbers
print("Six Most Frequently Drawn Winning Numbers:")
for number, frequency in sorted(frequency_dict_winning.items(), key=lambda item: item[1], reverse=True)[:6]:
    print(f"Winning Number {number} appears {frequency} times")

# Print the five most frequently drawn Powerball numbers
print("\nFive Most Frequently Drawn Powerball/Megaball Numbers:")
for number, frequency in sorted(frequency_dict_powerball.items(), key=lambda item: item[1], reverse=True)[:5]:
    print(f"Powerball/Megaball Number {number} appears {frequency} times")

# Generate combinations of 5 numbers from the 6 most frequent winning numbers
most_frequent_winning_numbers = [number for number, _ in sorted(frequency_dict_winning.items(), key=lambda item: item[1], reverse=True)[:6]]
combinations = generate_combinations(most_frequent_winning_numbers)

# Print or use the combinations as needed
print("\nUnique Combinations of 5 Numbers from the 6 Most Frequent Winning Numbers:")
for combination in combinations:
    print(combination)

# Predict the next set of winning numbers based on frequencies
predicted_winning_numbers = predict_next_numbers(frequency_dict_winning)
print(f"\nPredicted Next Winning Numbers: {predicted_winning_numbers}")

# Predict the next Powerball number based on frequencies
predicted_powerball_number = predict_next_numbers(frequency_dict_powerball, num_numbers=1)[0]
print(f"Predicted Next PowerballMegaball Number: {predicted_powerball_number}")
