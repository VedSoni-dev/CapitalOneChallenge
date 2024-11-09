from budget import allocate_budget
from macros import calculate_macros
from savings import track_savings, estimate_saving_duration

def main():
    # Gather user input
    weekly_budget = float(input("Enter your weekly food budget: $"))
    num_people = int(input("Enter the number of people you're buying food for: "))
    ages = [int(input(f"Enter the age of person {i+1}: ")) for i in range(num_people)]
    desired_item_cost = float(input("Enter the cost of the item you want to save for (optional): $") or 0)

    # Step 1: Allocate Budget
    daily_budget = allocate_budget(weekly_budget)
    print(f"Daily Budget: ${daily_budget:.2f}")

    # Step 2: Calculate Macros for each person based on age
    total_macros = {'protein': 0, 'carbs': 0, 'fats': 0}
    for age in ages:
        macros = calculate_macros(age)
        total_macros['protein'] += macros['protein']
        total_macros['carbs'] += macros['carbs']
        total_macros['fats'] += macros['fats']

    print(f"Total daily macronutrient needs: {total_macros}")

    # Step 3: Track Savings (example usage)
    actual_spent = float(input(f"How much did you spend today? $"))
    daily_savings = track_savings(daily_budget, actual_spent)
    print(f"Savings Today: ${daily_savings:.2f}")

    # Step 4: Estimate saving duration for desired item
    if desired_item_cost > 0:
        days_to_save = estimate_saving_duration(desired_item_cost, daily_savings)
        print(f"It will take {days_to_save:.0f} days to save enough money for your item.")

if __name__ == "__main__":
    main()
