def calculate_current_savings(initial_savings_rate, total_cost, annual_salary, semi_annual_raise, annual_investment_rate, down_payment_portion=0.25, target_months=36):
    portion_down_payment = down_payment_portion * total_cost
    monthly_salary = annual_salary / 12
    monthly_investment_rate = annual_investment_rate / 12
    monthly_saving = initial_savings_rate * monthly_salary

    current_savings = 0
    for month in range(target_months):
        current_savings += monthly_saving
        current_savings *= (1 + monthly_investment_rate)
        if month % 6 == 0 and month != 0:
            monthly_saving = monthly_saving * (1 + semi_annual_raise)

    return current_savings, portion_down_payment


def find_best_saving_rate_binary_search(total_cost, annual_salary, semi_annual_raise, annual_investment_rate, target_months, down_payment_portion=0.25, epsilon=0.0001, max_iterations=100):
    low = 0.0
    high = 1.0
    best_rate = None
    rounds = 0
    for _ in range(max_iterations):
        rounds += 1
        mid_rate = (low + high) / 2
        current_savings, portion_down_payment = calculate_current_savings(
            mid_rate, total_cost, annual_salary, semi_annual_raise, annual_investment_rate, down_payment_portion
        )

        if abs(current_savings - portion_down_payment) < epsilon:
            return mid_rate, rounds

        if current_savings < portion_down_payment:
            low = mid_rate
        else:
            best_rate = mid_rate
            high = mid_rate

    return best_rate, rounds


total_cost = 1000000
semi_annual_raise = 0.07
annual_investment_rate = 0.04
down_payment_portion = 0.25
target_months = 36

starting_salary = float(input("Enter your starting salary: "))

best_rate, rounds = find_best_saving_rate_binary_search(
    total_cost,
    starting_salary,
    semi_annual_raise,
    annual_investment_rate,
    target_months,
    down_payment_portion
)

if best_rate is not None:
    initial_monthly_salary = starting_salary / 12
    required_initial_monthly_saving = best_rate * initial_monthly_salary
    down_payment_amount = down_payment_portion * total_cost

    print(f"\nTo reach the down payment of ${down_payment_amount:,.2f} in {target_months} months,")
    print(f"the required initial monthly saving rate is approximately {best_rate:.4f}")
    print(f"This was found in {rounds} rounds of binary search.")
    print(f"This means you need to save about ${required_initial_monthly_saving:,.2f} of your initial monthly salary.")
else:
    print("Could not find a suitable saving rate within the iterations.")

