import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QMessageBox, QLabel, QInputDialog, QDialog, QLineEdit, QHBoxLayout, QComboBox, QDateEdit
from PyQt5.QtCore import Qt, QDate


class AddExpenseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Expense")
        self.setWindowModality(Qt.ApplicationModal)

        self.name_label = QLabel("Expense Name:")
        self.name_input = QLineEdit()

        self.amount_label = QLabel("Amount:")
        self.amount_input = QLineEdit()

        self.quantity_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit()

        self.date_label = QLabel("Date:")
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())

        self.category_label = QLabel("Category:")
        self.category_input = QComboBox()
        self.category_input.addItems(["Food", "Transportation", "Utilities", "Entertainment", "Others"])

        self.add_button = QPushButton("Add Expense")
        self.add_button.setStyleSheet("QPushButton { background-color: #007bff; color: white; border: none; padding: 10px 20px; }"
                                      "QPushButton:hover { background-color: #0056b3; }")
        self.add_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.quantity_input)
        layout.addWidget(self.date_label)
        layout.addWidget(self.date_input)
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_input)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def get_expense_info(self):
        name = self.name_input.text()
        amount = float(self.amount_input.text())
        date = self.date_input.date().toString("yyyy-MM-dd")
        category = self.category_input.currentText()
        return name, amount, date, category


class ExpenseTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(200, 200, 500, 400)

        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        self.expense_display = QTextEdit()
        layout.addWidget(self.expense_display)

        self.add_expense_btn = QPushButton("Add Expense")
        self.add_expense_btn.setCursor(Qt.PointingHandCursor)
        self.add_expense_btn.setStyleSheet("QPushButton { background-color: #007bff; color: white; border: none; padding: 10px 20px; }"
                                           "QPushButton:hover { background-color: #0056b3; }")
        self.add_expense_btn.clicked.connect(self.show_add_expense_dialog)
        layout.addWidget(self.add_expense_btn)

        self.view_expenses_btn = QPushButton("View Expenses")
        self.view_expenses_btn.setCursor(Qt.PointingHandCursor)
        self.view_expenses_btn.setStyleSheet("QPushButton { background-color: #007bff; color: white; border: none; padding: 10px 20px; }"
                                              "QPushButton:hover { background-color: #0056b3; }")
        self.view_expenses_btn.clicked.connect(self.view_expenses)
        layout.addWidget(self.view_expenses_btn)

        self.delete_expense_btn = QPushButton("Delete Expense")
        self.delete_expense_btn.setCursor(Qt.PointingHandCursor)
        self.delete_expense_btn.setStyleSheet("QPushButton { background-color: #007bff; color: white; border: none; padding: 10px 20px; }"
                                               "QPushButton:hover { background-color: #0056b3; }")
        self.delete_expense_btn.clicked.connect(self.delete_expense)
        layout.addWidget(self.delete_expense_btn)

        self.quit_btn = QPushButton("Quit")
        self.quit_btn.setCursor(Qt.PointingHandCursor)
        self.quit_btn.setStyleSheet("QPushButton { background-color: #dc3545; color: white; border: none; padding: 10px 20px; }"
                                     "QPushButton:hover { background-color: #c82333; }")
        self.quit_btn.clicked.connect(self.close)
        layout.addWidget(self.quit_btn)

        self.central_widget.setLayout(layout)

    def show_add_expense_dialog(self):
        dialog = AddExpenseDialog()
        if dialog.exec_():
            expense_info = dialog.get_expense_info()
            expense_text = "Name: {}, Amount: RS{:.2f}, Date: {}, Category: {}".format(*expense_info)
          #  self.expense_display.append(expense_text)
            self.add_expense(*expense_info)

    def add_expense(self, name, amount, date, category):
        # Logic to add expense
        expense_text = f"Name: {name}, Amount: RS{amount:.2f}, Date: {date}, Category: {category}"
        self.expense_display.append(expense_text)
        with open("expenses.txt", "a") as file:
            file.write(expense_text + "\n")

    def view_expenses(self):
        # Logic to view expenses
        self.expense_display.clear()
        try:
            with open("expenses.txt", "r") as file:
                expenses = file.readlines()
            self.expense_display.append("Expenses:\n")
            for expense in expenses:
                self.expense_display.append(expense.strip())
        except FileNotFoundError:
            self.expense_display.append("No expenses recorded.")

    def delete_expense(self):
        # Logic to delete expense
        expense_to_delete, ok = QInputDialog.getText(self, "Delete Expense", "Enter expense to delete:")
        if ok and expense_to_delete:
            msg = QMessageBox(self)
            msg.setWindowTitle("Confirmation")
            msg.setText(f"Are you sure you want to delete {expense_to_delete}?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)
            msg.setStyleSheet(
                "QMessageBox { background-color: white; }"
                "QPushButton { background-color: #007bff; color: white; border: none; padding: 10px 20px; }"
                "QPushButton:hover { background-color: #0056b3; }"
            )
            if msg.exec_() == QMessageBox.Yes:
                try:
                    with open("expenses.txt", "r") as file:
                        lines = file.readlines()
                    with open("expenses.txt", "w") as file:
                        deleted = False
                        for line in lines:
                            if line.strip() != expense_to_delete:
                                file.write(line)
                            else:
                                deleted = True
                        if deleted:
                            self.expense_display.append(expense_to_delete + " deleted.")
                        else:
                            self.expense_display.append("Expense not found.")
                except FileNotFoundError:
                    self.expense_display.append("No expenses recorded.")

    def get_user_input(self, prompt):
        text, ok = QInputDialog.getText(self, "Expense Tracker", prompt)
        if ok:
            return text.strip()
        return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tracker = ExpenseTracker()
    tracker.show()
    sys.exit(app.exec_())
