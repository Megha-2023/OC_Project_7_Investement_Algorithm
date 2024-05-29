""" Module to find best combinations of shares to be purchased using an optimized Algorithm : Knapsack Algorithm"""
import time
import sys
import pandas as pd
import fontstyle


def readfile():
    """ Function to read Shares data stored in csv file"""

    shares_df = pd.read_csv("Shares_List.csv", header=0, delimiter=",")
    shares_list = []

    # make a list of tuples containing name, price and profit in euros
    for i in range(len(shares_df)):
        profit_in_euro = 0
        # convert profit per share in % to euros
        profit_in_euro = (float(shares_df.iloc[i, 1]) * float(shares_df.iloc[i, 2]))/100
        shares_list.append([shares_df.iloc[i, 0], shares_df.iloc[i, 1], round(profit_in_euro, 2)])
    return shares_list


def knapsack(max_budget, shares_data):
    """ Function to execute knapsack optimized algorithm"""

    # sort data in reverse order by profit in euros
    shares_data.sort(reverse=True, key=lambda x: x[2])

    total_price = 0
    total_profit = 0
    best_deal = []

    for share, price, profit in shares_data:
        # check for positive values of price
        if price > 0:
            total_price += price
            # add share to best deal list if price fits into the budget
            if total_price <= max_budget:
                total_profit += profit
                best_deal.append([share, price, profit])
            else:
                total_price -= price
                continue
        
    return best_deal, total_price, total_profit


def display_output(best_deal_list, total_price, total_profit):
    """ Function to display(formatted) the best deal to invest """

    print(fontstyle.apply("Best Investment Strategy is:", "bold"))
    print("-"*30)
    print(" Name\t\tPrice\tProfit(in euros)")
    print("-"*30)
    deal = best_deal_list
    for i, name in enumerate(deal):
        print(name[0] + " \t" + str(name[1]) + "\t" + str(name[2]))
    print(fontstyle.apply(f" \nTotal Cost: {round(total_price, 2)} euros", "bold"))
    print(fontstyle.apply(f"Total Profit: {round(total_profit, 2)} euros\n", "bold"))


def main():
    """ Main function to start execution"""
    start = time.time()  # start time of the program
    memory_blocks = sys.getallocatedblocks()

    # read file containing dataset
    shares_data = readfile()
    # budget pre-defined
    max_budget = 500

    # call method executing the optimized algorithm
    best_deal_list, total_price, total_profit = knapsack(max_budget, shares_data)
    display_output(best_deal_list, total_price, total_profit)

    end = time.time()  # end time of the program

    time_diff = (end - start) * 10**3
    print(f"Time taken by Knapsack Algorithm = {time_diff:.02f} ms")
    print(f"The space allocated is {memory_blocks} ")


main()
