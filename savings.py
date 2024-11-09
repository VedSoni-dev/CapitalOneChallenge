def track_savings(daily_budget, actual_spent):
    """Calculates savings from unspent grocery money."""
    return max(daily_budget - actual_spent, 0)

def estimate_saving_duration(item_cost, daily_savings):
    """Estimates how many days it takes to save enough money."""
    if daily_savings == 0:
        return float('inf')  # Can't save if no savings are made daily!
    return item_cost / daily_savings

# Example usage:
if __name__ == "__main__":
    daily_budget = 14.29   # Example daily budget of $14.29
    actual_spent = float(input("How much did you spend today? $"))
    
    savings_today = track_savings(daily_budget, actual_spent)
    
    item_cost = float(input("Enter cost of desired item: $"))
    
    days_needed = estimate_saving_duration(item_cost, savings_today)
    
    print(f"Savings Today: ${savings_today:.2f}")
    print(f"It will take {days_needed:.0f} days to save enough money.")
