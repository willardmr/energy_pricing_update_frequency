import random
import matplotlib.pyplot as plt
import numpy as np

simulation_length = 100


def simulate_profits(retail_prices, hedge_prices, customers):
    final_profits = []
    unhedged_customers = []
    unhedged_customer_prices = []
    for index, customer_count in enumerate(customers):
        if sum(unhedged_customers) >= 10:
            hedge_cost = hedge_prices[index] * sum(unhedged_customers)
            customer_revenue = 0
            for i, unhedged_customer_count in enumerate(unhedged_customers):
                customer_revenue += (
                    unhedged_customer_count * unhedged_customer_prices[i]
                )
            final_profits.append(customer_revenue - hedge_cost)
            unhedged_customers = []
            unhedged_customer_prices = []
        else:
            unhedged_customers.append(customer_count)
            unhedged_customer_prices.append(retail_prices[index])
    return sum(final_profits)


def prices_updated_every_x_days(x, hedge_prices):
    retail_prices_updated_every_x_days = []
    current_retail_price = hedge_prices[0]
    for i in range(simulation_length):
        if i != 0 and i % x == 0:
            current_retail_price = hedge_prices[i - 1]
        retail_prices_updated_every_x_days.append(current_retail_price)
    return retail_prices_updated_every_x_days


flat_retail_prices = [1] * simulation_length
flat_hedge_prices = [1] * simulation_length
flat_customers = [1] * simulation_length
print("All flat")
print(simulate_profits(flat_retail_prices, flat_hedge_prices, flat_customers))

increasing_hedge_prices = []
for i in range(simulation_length):
    increasing_hedge_prices.append(i + 1)
print("Increasing hedge costs")
print(simulate_profits(flat_retail_prices, increasing_hedge_prices, flat_customers))

retail_prices_updated_every_10_days = prices_updated_every_x_days(
    10, increasing_hedge_prices
)
print("Increasing hedge costs, retail_price updated every 10 days")
print(
    simulate_profits(
        retail_prices_updated_every_10_days, increasing_hedge_prices, flat_customers
    )
)

retail_prices_updated_every_5_days = prices_updated_every_x_days(
    5, increasing_hedge_prices
)
print("Increasing hedge costs, retail_price updated every 5 days")
print(
    simulate_profits(
        retail_prices_updated_every_5_days, increasing_hedge_prices, flat_customers
    )
)

retail_prices_updated_every_1_days = prices_updated_every_x_days(
    1, increasing_hedge_prices
)
print("Increasing hedge costs, retail_price updated every 1 days")
print(retail_prices_updated_every_1_days)
print(
    simulate_profits(
        retail_prices_updated_every_1_days, increasing_hedge_prices, flat_customers
    )
)

increase_then_decreasing_hedge_prices = []
current_hedge_price = -25
for i in range(simulation_length):
    if i < simulation_length / 2:
        current_hedge_price += 1
    elif i == simulation_length / 2:
        continue
    else:
        current_hedge_price -= 1

    increase_then_decreasing_hedge_prices.append(current_hedge_price)
print("Increasing then decreasing hedge costs")
print(
    simulate_profits(
        flat_retail_prices, increase_then_decreasing_hedge_prices, flat_customers
    )
)

random_simulation_length = 10000

day_1_profits = []
for i in range(random_simulation_length):
    hedge_prices = [random.uniform(0.97, 1.03) for x in range(simulation_length)]
    customers = [random.randint(1, 3) for x in range(simulation_length)]

    retail_prices_updated_every_1_days = prices_updated_every_x_days(1, hedge_prices)
    day_1_profits.append(
        simulate_profits(
            retail_prices_updated_every_1_days, hedge_prices, flat_customers
        )
    )
std_dev_1 = np.std(day_1_profits)

day_5_profits = []
for i in range(random_simulation_length):
    hedge_prices = [random.uniform(0.97, 1.03) for x in range(simulation_length)]
    customers = [random.randint(1, 3) for x in range(simulation_length)]

    retail_prices_updated_every_5_days = prices_updated_every_x_days(5, hedge_prices)
    day_5_profits.append(
        simulate_profits(
            retail_prices_updated_every_5_days, hedge_prices, flat_customers
        )
    )
std_dev_5 = np.std(day_5_profits)

day_10_profits = []
for i in range(random_simulation_length):
    hedge_prices = [random.uniform(0.97, 1.03) for x in range(simulation_length)]
    customers = [random.randint(1, 3) for x in range(simulation_length)]

    retail_prices_updated_every_10_days = prices_updated_every_x_days(10, hedge_prices)
    day_10_profits.append(
        simulate_profits(
            retail_prices_updated_every_10_days, hedge_prices, flat_customers
        )
    )
std_dev_10 = np.std(day_10_profits)

print(std_dev_1, std_dev_5, std_dev_10)

a = day_1_profits
b = day_5_profits
c = day_10_profits

common_params = dict(
    bins=30,
    density=False,
    label=["Update every 1 day", "Update every 5 days", "Update every 10 days"],
)

plt.title("Profit outcome distribution")
plt.hist((a, b, c), **common_params)

plt.legend()
plt.savefig("3hist.png", dpi=300)
plt.show()
