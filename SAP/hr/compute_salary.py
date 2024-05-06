# #https://taxcalculatorphilippines.com/
# monthly_base_salary = 40000
# overtime = 9
# total_workingday = 20
# # The variable `payoutby2weeks` is calculating half of the `monthly_base_salary`. It is dividing the
# # monthly base salary by 2 to determine the amount that would be paid out every two weeks.
# payoutby2weeks = monthly_base_salary/2
# actual_workingday = 20
# workinghours = 8


# dailypay = monthly_base_salary/total_workingday
# hourlypay = dailypay/workinghours


# print(f"{dailypay=}")

# print(f"{hourlypay=}")
# overtimepay = overtime*hourlypay

# print(f"{overtimepay=}")


# initial_pay = actual_workingday*dailypay
# monthly_salary = initial_pay + overtimepay
monthly_salary = 37777

print(f"{monthly_salary=}")
monthly_contrib = 2394.43
taxable_income = monthly_salary - monthly_contrib
print(f"{taxable_income=}")
# 18250 semi-monthly is in bracket 3
if taxable_income < 20833:
    compensation_level = 0
    fixed_tax = 0
    percentage = 0
if taxable_income >= 20833 and taxable_income <= 33333:
    fixed_tax = 0
    percentage = 15
    compensation_level = 20833
elif taxable_income >= 33333 and taxable_income <= 66666:
    fixed_tax = 3125
    percentage = 20
    compensation_level = 33333
# diff = taxable_income - compensation_level
# print(f"{diff=}")
# percentage_over_compensation_level = (diff) * (percentage/100)
percentage_over_compensation_level = (taxable_income - compensation_level) *(percentage/100)


income_tax = fixed_tax + percentage_over_compensation_level
print(f"{percentage_over_compensation_level=}")
print(f"{income_tax=}")

Net_salary =  monthly_salary - (monthly_contrib + income_tax)

print(f"{Net_salary=}")

# prescribed_minimum_tax = constant +


# print(payoutby2weeks)
# print(f"{net_pay=}")


# monthly_base_salary = 40000
# overtime = 9
# total_workingday = 20
# payoutby2weeks = monthly_base_salary/2
# actual_workingday = 20
# workinghours = 8

# dailypay = monthly_base_salary/total_workingday
# hourlypay = dailypay/workinghours

# overtimepay = overtime * 1.5 * hourlypay

# initial_pay = actual_workingday * dailypay
# monthly_salary = initial_pay + overtimepay

# monthly_contrib = 2506.25
# taxable_income = monthly_salary - monthly_contrib

# compensation_level = 33333

# if taxable_income > compensation_level:
#     percentage_over_compensation_level = (taxable_income - compensation_level) * 0.30
# else:
#     percentage_over_compensation_level = 0

# income_tax = 2500 + percentage_over_compensation_level

# Net_salary = monthly_salary - (monthly_contrib + income_tax)

# print(f"Net salary: {Net_salary}")