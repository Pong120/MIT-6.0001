annual_salary = float(input("Enter your starting salary: "))

portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))

total_cost = float(input("Enter the cost of your dream home: "))

semi_annual_raise = float(input("Enter the semi-annual raise, as a decimal: "))

portion_down_payment = 0.25 * total_cost

monthly_salary = annual_salary / 12

current_savings = 0

r = 0.04 / 12

monthly_saving = portion_saved * monthly_salary

months = 0
while current_savings < portion_down_payment:
    current_savings += monthly_saving 
    current_savings += current_savings * r
    months += 1
    if months % 6 == 0 and months != 0:
        monthly_saving = monthly_saving + monthly_saving * semi_annual_raise

print("Number of months:", months)