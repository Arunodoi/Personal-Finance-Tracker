from finance import CSV
from data_entry import get_amount,get_category,get_date,get_description
import matplotlib.pyplot as plt
import os
from colorama import Fore,Style
from budget import BudgetManager



def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of this transcation (dd-mm-yyyy) or Press Enter for today's date : ",allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()

    CSV.add_entry(date,amount,category,description)

def plot_transaction(df):
    df.set_index("date",inplace = True)

    income_df  = (
        df[df["category"]=="Income"]
        .resample("D")
        .sum()
        .reindex(df.index,fill_value=0)
        )
    
    expense_df  = (
        df[df["category"]=="Expense"]
        .resample("D")
        .sum()
        .reindex(df.index,fill_value=0)
        )
    
    plt.figure(figsize=(10,5))
    plt.plot(income_df.index,income_df["amount"],label = "Income",color="g")
    plt.plot(expense_df.index,expense_df["amount"],label="Expense",color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()



def set_budget():
    category = input("Enter the category: ")
    budget = float(input(f"Set the budget for {category} (₹):"))
    BudgetManager.set_budget(category,budget)

def check_budget():
    BudgetManager.check_budget()
    if input("Do you want to visualize the budget (y/n)? ").lower() == "y":
        BudgetManager.visualize_budget()







def main():

    while True:
        
        print(Fore.GREEN + "\n||🤑 PERSONAL FINANCE TRACKER 📈|| "+ Style.RESET_ALL)
        print(Fore.CYAN +"\n1. Add a new Transaction ➕ "+ Style.RESET_ALL)
        print(Fore.YELLOW +"2.🔍 View transcations 🧐 and a summary within a date range"+ Style.RESET_ALL)
        print(Fore.BLUE + "3. Set Budget 💰" + Style.RESET_ALL)
        print(Fore.MAGENTA + "4. View Budget Summary 📊" + Style.RESET_ALL)
        print(Fore.RED + "5. Exit ❌\n"+ Style.RESET_ALL)

        choice = input(Fore.MAGENTA +"💡 Enter your choice (1-5)😊: "+ Style.RESET_ALL)

        if choice=="1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date,end_date)
            if input(Fore.GREEN +"Do you want to see a plot (y/n)"+ Style.RESET_ALL).lower()=="y":
                plot_transaction(df)

        elif choice == "3":
            set_budget()
        elif choice == "4":
            check_budget()

        elif choice=="5":
            print(Fore.RED +"👋 Exiting....🙁"+ Style.RESET_ALL)
            break

        else:
            print(Fore.RED +"❗ Invalid Choice. Enter 1 ,2, 3 or 4."+ Style.RESET_ALL)


if __name__ == "__main__":
    main()