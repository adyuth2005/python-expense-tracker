from expense import Expense
import calendar
import datetime
import csv


def main():
    print(f"Running Expense Tracker!")
    expense_file_path = "expenses.csv"
    budget = 50000.0

    while True:
        print("\n--- Expense Tracker Menu ---")
        print("  1. Add a new expense")
        print("  2. View summary for this month")
        print("  3. Exit")

        choice = input("Enter your choice [1-3]: ")

        if choice == '1':
            # Get user expense and save it
            expense = get_user_expense()
            save_expense_to_file(expense, expense_file_path)
        elif choice == '2':
            # Read file and summarize expenses for the current month
            summarize_expenses(expense_file_path, budget)
        elif choice == '3':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def get_user_expense():
    print(f"\nGetting User Expense")

    # get expense name
    expense_name = input("Enter expense name: ")

    # get expense amount with validation
    expense_amount = 0.0
    while True:
        try:
            expense_amount = float(input("Enter expense amount: "))
            if expense_amount <= 0:
                print("Amount must be greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Define category
    expense_categories = [
        "Food",
        "Home",
        "Work",
        "Fun",
        "Transport",
        "Other"
    ]

    # get category choice with validation
    while True:
        print("\nSelect a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"    {i + 1}.  {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        try:
            selected_index = int(
                input(f"Enter a category number {value_range}: ")) - 1

            if selected_index in range(len(expense_categories)):
                selected_category = expense_categories[selected_index]

                # create the expenseobject with todays date
                new_expense = Expense(
                    name=expense_name,
                    category=selected_category,
                    amount=expense_amount,
                    date=datetime.date.today()
                )
                print(
                    f"Expense added: {new_expense.name}, {new_expense.category}, {new_expense.amount:.2f}")
                return new_expense
            else:
                print("Invalid category. Please try again!")
        except ValueError:
            print("Invalid input. Pkease enter a number.")


def save_expense_to_file(expense: Expense, expense_file_path: str):
    print(f"Saving User Expense to {expense_file_path}")
    with open(expense_file_path, "a", newline="", encoding="utf-8") as f:
        # Create a csv writer object
        writer = csv.writer(f)

        # Write the expense data as a new row
        # Format dateas YYYY-MM-DD
        writer.writerow(
            [expense.name, expense.amount, expense.category,
                expense.date.strftime("%Y-%m-%d")]
        )


def summarize_expenses(expense_file_path: str, budget: float):
    """Reads all expenses from the file, filters for the the current month, and prints a summary."""
    print(f"\nSummarize User Expenses for this Month")

    now = datetime.datetime.now()
    current_month = now.month
    current_year = now.year

    expenses_this_month: list[Expense] = []

    try:
        with open(expense_file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)

            for row in reader:
                try:
                    # Check if row has the expected number of columns
                    if len(row) == 4:
                        expense_name = row[0]
                        expense_amount = float(row[1])
                        expense_category = row[2]
                        expense_date = datetime.datetime.strptime(
                            row[3], "%Y-%m-%d").date()

                        # Filter: only add if its from the current month and year
                        if (expense_date.month == current_month and
                                expense_date.year == current_year):

                            line_expense = Expense(
                                name=expense_name,
                                amount=expense_amount,
                                category=expense_category,
                                date=expense_date
                            )
                            expenses_this_month.append(line_expense)
                    else:
                        print(f"Warning: Skipping malformed row: {row}")

                except Exception as e:
                    print(f"Warning: Skipping bad data in row: {row} ({e})")
    except FileNotFoundError:
        print("No expenses file found. Add an expense to get started.")
        return
    except Exception as e:
        print(f"An error occured while reading the file: {e}")
        return

    if not expenses_this_month:
        print("No expenses recorded for this month yet.")
        return

    # Calculate and Print Summary
    # 1. Group by category

    amount_by_category = {}
    for expense in expenses_this_month:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("\nExpense By Category (This Month)")
    for key, amount in sorted(amount_by_category.items()):
        print(f"  {key}: ${amount:2f}")

    # 2. Total spent
    total_spent = sum([x.amount for x in expenses_this_month])
    print(f"\nTotal spent (This Month): ${total_spent:2f}")

    # 3. Budget Calculation
    remaining_budget = budget - total_spent
    print(f"Budget Remaining (This Month): ${remaining_budget:.2f}")

    # 4. Daily budget calculation
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    if remaining_days > 0:
        daily_budget = remaining_budget / remaining_days
        print(
            green(f"Budget Per Day  (for rest of month): ${daily_budget:.2f}"))
    elif remaining_days == 0:
        print(green(
            f"This is the last day of thr month! Remaining budget: ${remaining_budget:.2f}"))
    else:
        print(green("The month is over. This summary is for the past month."))


def green(text: str):
    return f"\033[92m{text}\033[0m"


if __name__ == "__main__":
    main()
