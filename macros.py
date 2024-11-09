def calculate_macros(age):
    """Returns recommended macros based on age."""
    if age >= 19:
        return {'protein': 50, 'carbs': 130, 'fats': 70}  # Adult requirements per day
    elif age >= 9:
        return {'protein': 34, 'carbs': 130, 'fats': 60}  # Child requirements per day
    else:
        return {'protein': 20, 'carbs': 90, 'fats': 40}   # Younger child requirements

# Example usage:
if __name__ == "__main__":
    age = int(input("Enter age: "))
    print(calculate_macros(age))
