""" Module to find best combinations of shares to be purchased using an optimized Algorithm:
Knapsack Algorithm using Dynamic Programming"""

import time
import sys
import pandas as pd
import fontstyle


def readfile():
    """ Function to read Shares data stored in csv file"""

    shares_df = pd.read_csv("Shares_List.csv", header=0, delimiter=",")
    shares_list = []

    # make a list of tuples containing name, price(multiplied by 100 to make integer)
    # and profit in euros
    for i in range(len(shares_df)):
        profit_in_euro = 0
        # convert profit per share in % to euros
        if float(shares_df.iloc[i, 1]) > 0:
            profit_in_euro = (float(shares_df.iloc[i, 1]) * float(shares_df.iloc[i, 2]))/100
            shares_list.append([shares_df.iloc[i, 0], int(float(shares_df.iloc[i, 1] * 100)),
                                round(profit_in_euro, 2)])

    return shares_list


def knapsack(max_budget, shares_list):
    """ Function to execute knapsack optimized algorithm"""
    n = len(shares_list)
    # declare knapsack table containing rows(=len of dataset+1) and columns(= max budeget+1)
    knap = [[0 for cols in range(max_budget + 1)] for rows in range(n + 1)]

    # fill knapsack table as per formula 
    for i in range(1, n + 1):
        for price in range(1, max_budget + 1):
            if shares_list[i - 1][1] <= price:
                knap[i][price] = max(round(shares_list[i-1][2] + knap[i - 1][price - shares_list[i-1][1]], 2),
                                     knap[i-1][price])
            else:
                knap[i][price] = round(knap[i-1][price], 2)

    best_deal_list = []
    i = n

    while i >= 0 and max_budget >= 0:
        share = shares_list[i-1]
        # if absolute result of max_budget - previous shares cost is more than shares and knapsack length
        # prevent an error which occurs when max_budget is lower than current shares price
        if abs(max_budget-share[1]) > len(shares_list) and abs(max_budget-share[1]) > len(knap[0]):
            i -= 1
        else:
            # compare best result of current share with previous share results - current share price+its profit,
            # if results are equal, then that share can be added to optimal solution
            if knap[i][max_budget] == round(knap[i-1][max_budget-share[1]] + share[2], 2):
                best_deal_list.append([share[0], share[1], share[2]])
                max_budget -= share[1]
            i -= 1

    return best_deal_list


def display_output(best_deal_list):
    """ Function to display(formatted) the best deal to invest """
    total_price = 0
    total_profit = 0
    print(fontstyle.apply("Best Investment Strategy is:", "bold"))
    print("-"*30)
    print(" Name\t\tPrice\tProfit(in euros)")
    print("-"*30)
    deal = best_deal_list
    for i, name in enumerate(deal):
        print(name[0] + " \t" + str(name[1]/100) + "\t" + str(name[2]))
        total_price += name[1]
        total_profit += name[2]
    print(fontstyle.apply(f"\nNumber of Shares: {len(best_deal_list)}", "bold"))
    print(fontstyle.apply(f"Total Cost: {round(total_price/100, 2)} euros", "bold"))
    print(fontstyle.apply(f"Total Profit: {round(total_profit, 2)} euros\n", "bold"))


def main():
    """ Main function to start execution"""
    start = time.time()  # start time of the program
    memory_before = sys.getallocatedblocks()

    # read file containing dataset
    shares_list = readfile()
    # budget pre-defined, multiplied by 100 to make integer
    max_budget = 50000

    # call method executing the optimized algorithm
    best_deal_list = knapsack(max_budget, shares_list)

    display_output(best_deal_list)

    end = time.time()  # end time of the program
    memory_after = sys.getallocatedblocks() - memory_before
    time_diff = end - start
    print(f"Time taken by Knapsack Algorithm = {time_diff:.02f} seconds")
    print(f"The space allocated = {memory_after} blocks")


main()
