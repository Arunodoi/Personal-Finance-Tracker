import pandas as pd
import csv
from datetime import datetime
import os
from prettytable import PrettyTable
from colorama import Fore,Style
from budget import BudgetManager




class CSV:

    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"




    @classmethod
    def initialize_csv(cls):

       
        try:
           
            pd.read_csv(cls.CSV_FILE)

        except FileNotFoundError:
            print(" File not found, creating a new one...")
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)
       
    @classmethod
    def add_entry(cls,date,amount,category,description):
        #store entry in dictionary
        new_entry = {

            "date" : date,
            "amount" : amount,
            "category": category,
            "description" : description
        }

        with open(cls.CSV_FILE, "a",newline="") as csvfile:
            # Create a DictWriter object with the specified columns
            writer = csv.DictWriter(csvfile,fieldnames=cls.COLUMNS)
            # Write the new entry as a row
            writer.writerow(new_entry)
        
        print("Entry added sucessfully 😊\n")

        if category == "Expense":
            BudgetManager.update_spent(description, amount)

        


    @classmethod
    def get_transactions(cls,start_date,end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"],format=CSV.FORMAT)
        start_date = datetime.strptime(start_date,CSV.FORMAT)
        end_date = datetime.strptime(end_date,CSV.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df =  df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given data range")

        else:
            print(
                Fore.BLUE+f"\n 💰 Transcations from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)} 💰"
            + Style.RESET_ALL)
            table = PrettyTable()

            table.field_names = ["Date","Amount","Category","Description"]

            for _, row in filtered_df.iterrows():
                table.add_row([
                    row["date"].strftime(CSV.FORMAT),
                    row["amount"],
                    row["category"],
                    row["description"]
                ])

            print(table)

            # print(filtered_df.to_string(
            #     index = False,formatters={"date": lambda x: x.strftime(CSV.FORMAT)})
            #     )
            
            total_income = filtered_df[filtered_df["category"]=="Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"]=="Expense"]["amount"].sum()
            
            
            print(Fore.BLUE+"\n || SUMMARY ||"+ Style.RESET_ALL)

            print(Fore.GREEN+f"Total Income:  ₹{total_income:.2f}"+ Style.RESET_ALL)
            print(Fore.RED+f"Total Expense:  ₹{total_expense:.2f}"+ Style.RESET_ALL)
            print(Fore.YELLOW+f"Net Savings:  ₹{(total_income-total_expense):.2f}\n"+ Style.RESET_ALL)

        return filtered_df