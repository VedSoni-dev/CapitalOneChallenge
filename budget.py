def allocate_budget(weekly_budget):
    """Splits weekly budget into daily amounts."""
    return weekly_budget / 7

# Example usage:
if __name__ == "__main__":
    weekly_budget = 100  # Example weekly budget of $100
    print(f"Daily Budget: ${allocate_budget(weekly_budget):.2f}")
