import sys
import pandas as pd
import random
import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QTextEdit, QInputDialog
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

# Utility function for styling buttons (Shared by both classes)
def style_button(button, color):
    button.setStyleSheet(f"""
        QPushButton {{
            background-color: {color};
            color: white;
            border-radius: 8px;
            padding: 10px;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {lighten_color(color)};
        }}
    """)

def lighten_color(color, factor=1.2):
    r = min(255, int(int(color[1:3], 16) * factor))
    g = min(255, int(int(color[3:5], 16) * factor))
    b = min(255, int(int(color[5:7], 16) * factor))
    return f"#{r:02X}{g:02X}{b:02X}"

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏦 GV Bank - Secure Login")
        self.setGeometry(100, 100, 400, 300)

        self.csv_file = "accounts.csv"
        self.transaction_file = "transactions.csv"

        # Ensure CSV files exist
        self.create_dataset()
        self.data = pd.read_csv(self.csv_file)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Bank Title
        title = QLabel("🏦 GV Bank - AMT System")
        title.setFont(QFont("Arial", 20))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Account Number Input
        self.account_input = QLineEdit(self)
        self.account_input.setPlaceholderText("Enter Account Number")
        layout.addWidget(self.account_input)

        # PIN Input
        self.pin_input = QLineEdit(self)
        self.pin_input.setPlaceholderText("Enter PIN")
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.pin_input)

        # Login Button
        self.login_button = QPushButton("🔑 Login", self)
        style_button(self.login_button, "#2196F3")
        self.login_button.clicked.connect(self.authenticate)
        layout.addWidget(self.login_button)

        # Balance Inquiry Button
        self.check_balance_button = QPushButton("💰 Balance Inquiry", self)
        style_button(self.check_balance_button, "#4CAF50")
        self.check_balance_button.clicked.connect(self.check_balance)
        layout.addWidget(self.check_balance_button)

        self.setLayout(layout)

    def authenticate(self):
        try:
            account_number = int(self.account_input.text())
            pin = int(self.pin_input.text())

            # Validate credentials
            user = self.data[(self.data['Account Number'] == account_number) & (self.data['PIN'] == pin)]

            if not user.empty:
                QMessageBox.information(self, "✅ Success", f"Welcome {user.iloc[0]['Name']}!")
                self.open_dashboard(user.iloc[0])
            else:
                QMessageBox.warning(self, "❌ Error", "Invalid Account Number or PIN!")

        except ValueError:
            QMessageBox.warning(self, "❌ Error", "Invalid input! Please enter numeric values.")

    def open_dashboard(self, user):
        self.hide()
        self.dashboard = Dashboard(user, self.csv_file, self.transaction_file)
        self.dashboard.show()

    def check_balance(self):
        account_number, ok = QInputDialog.getInt(self, "Check Balance", "Enter your Account Number:")

        if ok:
            user = self.data[self.data['Account Number'] == account_number]
            if not user.empty:
                QMessageBox.information(self, "💰 Balance Inquiry", f"Your Balance: ₹{user.iloc[0]['Balance (₹)']:.2f}")
            else:
                QMessageBox.warning(self, "❌ Error", "Account not found!")

    def create_dataset(self):
        try:
            pd.read_csv(self.csv_file)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "⚠️ 'accounts.csv' not found. Please provide it.")

        try:
            pd.read_csv(self.transaction_file)
        except FileNotFoundError:
            pd.DataFrame(columns=["Date", "From", "To", "Amount (₹)"]).to_csv(self.transaction_file, index=False)


class Dashboard(QWidget):
    def __init__(self, user, csv_file, transaction_file):
        super().__init__()
        self.setWindowTitle("🏦 GV Bank - Dashboard")
        self.setGeometry(100, 100, 600, 600)

        self.user = user
        self.csv_file = csv_file
        self.transaction_file = transaction_file

        self.data = pd.read_csv(self.csv_file)
        self.user_index = self.data[self.data['Account Number'] == self.user['Account Number']].index[0]

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Bank Title
        title = QLabel(f"🏦 GV Bank - Welcome, {self.user['Name']}!")
        title.setFont(QFont("Arial", 22))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Balance Display
        self.balance_label = QLabel(f"💰 Balance: ₹{self.user['Balance (₹)']:.2f}")
        self.balance_label.setFont(QFont("Arial", 16))
        layout.addWidget(self.balance_label)

        # Deposit Button
        self.deposit_button = QPushButton("💵 Deposit", self)
        style_button(self.deposit_button, "#4CAF50")
        self.deposit_button.clicked.connect(self.deposit_funds)
        layout.addWidget(self.deposit_button)

        # Transfer Button
        self.transfer_button = QPushButton("📤 Transfer", self)
        style_button(self.transfer_button, "#2196F3")
        self.transfer_button.clicked.connect(self.transfer_funds)
        layout.addWidget(self.transfer_button)

        # PIN Change Button
        self.pin_button = QPushButton("🔒 Change PIN", self)
        style_button(self.pin_button, "#FF9800")
        self.pin_button.clicked.connect(self.change_pin)
        layout.addWidget(self.pin_button)

        # Logout Button
        self.logout_button = QPushButton("🚪 Logout", self)
        style_button(self.logout_button, "#F44336")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        self.setLayout(layout)

    def deposit_funds(self):
        amount, ok = QInputDialog.getDouble(self, "Deposit", "Enter amount to deposit (₹):", min=1.0)
        if ok:
            self.user['Balance (₹)'] += amount
            self.update_balance()

    def transfer_funds(self):
        recipient_account, ok = QInputDialog.getInt(self, "Transfer", "Enter recipient's account number:")
        if ok:
            amount, ok = QInputDialog.getDouble(self, "Transfer", "Enter amount to transfer (₹):", min=1.0)
            if ok and amount <= self.user['Balance (₹)']:
                self.user['Balance (₹)'] -= amount
                self.update_balance()

    def change_pin(self):
        new_pin, ok = QInputDialog.getInt(self, "Change PIN", "Enter new 4-digit PIN:", min=1000, max=9999)
        if ok:
            self.data.at[self.user_index, 'PIN'] = new_pin
            self.update_balance()

    def update_balance(self):
        self.data.at[self.user_index, 'Balance (₹)'] = self.user['Balance (₹)']
        self.data.to_csv(self.csv_file, index=False)
        self.balance_label.setText(f"💰 Balance: ₹{self.user['Balance (₹)']:.2f}")

    def logout(self):
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())
