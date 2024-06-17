""" Module to find best combinations of shares to be purchased using Brute Force Algorithm"""
import time
import sys
from itertools import combinations
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
        if float(shares_df.iloc[i, 1]) > 0:
            profit_in_euro = (float(shares_df.iloc[i, 1]) * float(shares_df.iloc[i, 2]))/100
            shares_list.append([shares_df.iloc[i, 0], shares_df.iloc[i, 1], round(profit_in_euro, 2)])
    return shares_list


def generate_combination(shares_data):
    """ Function to generate different combinations of Shares to invest based on brute force algorithm"""
    max_budget = 500  # pre-defined budget
    max_profit = 0
    best_deal_list = []
    # iterate through length of the Shares data list
    for k in range(len(shares_data)):
        # generate combinations of different size
        temp_list = combinations(shares_data, len(shares_data)-k)
        for item in temp_list:
            cost_of_combination = 0
            profit_of_combination = 0
            for i, value in enumerate(item):
                # find cost and profit par combination
                cost_of_combination += int(value[1])
                profit_of_combination += int(value[2])
                # compare profit of combination with maximum profit
                if profit_of_combination >= max_profit and cost_of_combination <= max_budget:
                    max_profit = profit_of_combination

                # if combination satisfies the condition of 500 euros budget and
                # gains maximum profit add to the list
                if cost_of_combination in range(495, max_budget) and profit_of_combination >= max_profit:
                    # print(max_profit, profit_of_combination, cost_of_combination)
                    best_deal_list.append([item, cost_of_combination, profit_of_combination])
    return best_deal_list


def display_output(best_deal_list):
    """ Function to display(formatted) the best deal to invest """
    # sort list by descending order of profit
    best_deal_list = sorted(best_deal_list, key=lambda x: x[2], reverse=True)
    print(fontstyle.apply("Best Investment Strategy is:", "bold"))
    # for k in range(2):
    print("-"*30)
    # print(fontstyle.apply(f"\tOption-{k+1}", "bold"))
    # print("-"*30)
    print(" Name\t\tPrice\tProfit(in euros)")
    print("-"*30)
    deal = best_deal_list[0][0]
    for i, name in enumerate(deal):
        print(name[0] + " \t" + str(name[1]) + "\t" + str(name[2]))
    print(fontstyle.apply(f" Total Cost: {best_deal_list[0][1]} euros", "bold"))
    print(fontstyle.apply(f" Total Profit: {best_deal_list[0][2]} euros\n", "bold"))


def main():
    """ Main function to start execution"""
    start = time.time()
    memory_before = sys.getallocatedblocks()
    shares_data = readfile()
    best_deal = generate_combination(shares_data)
    display_output(best_deal)
    end = time.time()
    time_diff = (end - start)
    memory_after = sys.getallocatedblocks() - memory_before
    print(f"Time taken by Bruteforce Algorithm = {time_diff:.02f} seconds")
    print(f"The space allocated = {memory_after} blocks")


main()
