import pandas as pd
import csv
from datetime import datetime
import os
from prettytable import PrettyTable
from colorama import Fore,Style
import matplotlib.pyplot as plt


class BudgetManager:

    BUDGET_FILE = "budget_data.csv"
    
    
    @classmethod
    def initialize_budget_file(cls):
        # Ensure the budget file exists
        if not os.path.exists(cls.BUDGET_FILE):
            df = pd.DataFrame(columns=["category","budget","spent"])
            df.to_csv(cls.BUDGET_FILE,index=False)

    
    @classmethod
    def set_budget(cls,category,budget_amount):
        cls.initialize_budget_file()
        df = pd.read_csv(cls.BUDGET_FILE)

        if category in df["category"].values:
            df.loc[df["category"]==category,"budget"]=budget_amount
            print(f"Updated budget for {category} to ₹{budget_amount}.")
        else:
            new_row = pd.DataFrame([{"category": category, "budget": budget_amount, "spent": 0}])
            df = pd.concat([df, new_row], ignore_index=True)
            print(f"Budget of ₹{budget_amount} set for {category}.")


        df.to_csv(cls.BUDGET_FILE,index=False)
        print("Entry added sucessfully 😊\n")

    @classmethod
    def update_spent(cls,category,amount):
        cls.initialize_budget_file()
        df = pd.read_csv(cls.BUDGET_FILE)

        if category in df["category"].values:
            df.loc[df["category"]==category,"spent"]+=amount
            df.to_csv(cls.BUDGET_FILE,index=False)
        else:
            print(f"No budget found for category {category}. Please set a budget first.")


    
    @classmethod
    def check_budget(cls):
        cls.initialize_budget_file()
        df = pd.read_csv(cls.BUDGET_FILE)

        if df.empty:
            print("No budgets set.")
            return
        
        print(Fore.BLUE + "\n|| 🏦 Budget Summary ||" + Style.RESET_ALL)
        table = PrettyTable()
        table.field_names = ["Category", "Budget (₹)", "Spent (₹)", "Remaining (₹)", "Status"]

        for _, row in df.iterrows():
            remaining = row["budget"] - row["spent"]
            status = "Within Budget" if remaining >= 0 else "Exceeded"
            table.add_row([row["category"], row["budget"], row["spent"], max(0, remaining), status])

        print(table)



    @classmethod
    def visualize_budget(cls):
        cls.initialize_budget_file()
        df = pd.read_csv(cls.BUDGET_FILE)

        if df.empty:
            print("No budgets to Visualize.")
            return
        
        categories = df["category"]
        spent = df["spent"]
        remaining = df["budget"]-df["spent"]

        plt.bar(categories,spent,label="Spent",color="red")
        plt.bar(categories,remaining,bottom=spent,label="Remaining")
        plt.xlabel("Categories")
        plt.ylabel("Amount(₹)")
        plt.title("Budget vs Spending")
        plt.legend()
        plt.show()


