import sys
import os
import cv2
import face_recognition
import smtplib
import random
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox,
    QInputDialog
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class FaceLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏦 GV Bank - Secure Login")
        self.setGeometry(100, 100, 800, 600)

        self.csv_file = "accounts.csv"
        self.face_folder = "faces/"
        if not os.path.exists(self.face_folder):
            os.makedirs(self.face_folder)
        self.otp = None

        self.create_dataset()
        self.data = pd.read_csv(self.csv_file)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel("🏦 GV Bank - Secure Face Login")
        title.setFont(QFont("Arial", 28))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.account_input, ok1 = QInputDialog.getInt(
            self, "Login", "Enter your Account Number:", value=0, min=1
        )
        if not ok1:
            self.close()
            return

        self.pin_input, ok2 = QInputDialog.getInt(
            self, "Login", "Enter your PIN:", value=0, min=1000, max=9999
        )
        if not ok2:
            self.close()
            return

        self.face_login_button = QPushButton("📸 Face Login", self)
        self.style_button(self.face_login_button, "#2196F3")
        self.face_login_button.clicked.connect(self.validate_login)
        layout.addWidget(self.face_login_button)

        self.setLayout(layout)

    def style_button(self, button, color):
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 8px;
                padding: 15px;
                font-size: 18px;
            }}
            QPushButton:hover {{
                background-color: {self.lighten_color(color)};
            }}
        """)

    def lighten_color(self, color, factor=1.2):
        r = min(255, int(int(color[1:3], 16) * factor))
        g = min(255, int(int(color[3:5], 16) * factor))
        b = min(255, int(int(color[5:7], 16) * factor))
        return f"#{r:02X}{g:02X}{b:02X}"

    def create_dataset(self):
        try:
            pd.read_csv(self.csv_file)
        except FileNotFoundError:
            data = {
                "Account Number": [1001],
                "Name": ["User1"],
                "Email": ["your-email@example.com"],
                "Balance (₹)": [50000],
                "PIN": [1234]
            }
            pd.DataFrame(data).to_csv(self.csv_file, index=False)
            print("✅ Created 'accounts.csv' with default data.")

    def validate_login(self):
        acc_number = self.account_input
        pin = self.pin_input

        user = self.data[(self.data["Account Number"] == acc_number) & (self.data["PIN"] == pin)]

        if user.empty:
            QMessageBox.critical(self, "❌ Error", "Invalid Account Number or PIN!")
            return

        QMessageBox.information(self, "✅ Validated", "Login successful. Proceeding to Face Recognition...")
        self.capture_face(user.iloc[0])

    def capture_face(self, user):
        video_capture = cv2.VideoCapture(0)
        QMessageBox.information(self, "📸 Capture", "Look at the camera to verify your identity...")

        ret, frame = video_capture.read()
        video_capture.release()

        if not ret:
            QMessageBox.critical(self, "❌ Error", "Failed to capture image!")
            return

        captured_face = face_recognition.face_encodings(frame)

        if not captured_face:
            QMessageBox.critical(self, "❌ Error", "No face detected. Try again.")
            return

        captured_encoding = captured_face[0]
        image_path = f"{self.face_folder}{user['Account Number']}.jpg"

        try:
            stored_image = face_recognition.load_image_file(image_path)
            stored_encoding = face_recognition.face_encodings(stored_image)[0]

            match = face_recognition.compare_faces([stored_encoding], captured_encoding)[0]
            if match:
                QMessageBox.information(self, "✅ Success", f"Welcome {user['Name']}!")
                self.open_dashboard(user)
                return
        except Exception as e:
            print(f"Error loading face: {e}")
            cv2.imwrite(image_path, frame)
            QMessageBox.information(self, "✅ Registered", "New face registered. Please login again.")
            return

        QMessageBox.warning(self, "⚠️ Face Not Recognized", "Face not matched. Sending OTP to email.")
        self.send_email_otp(user)

    def send_email_otp(self, user):
        recipient_email = user["Email"]
        self.otp = str(random.randint(100000, 999999))

        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "yourmail@gmail.com"
        sender_password = "your-app-passowrd"

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = "GV Bank - OTP Verification"
        body = f"Your GV Bank OTP is: {self.otp}"
        message.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
            server.quit()

            QMessageBox.information(self, "📧 OTP Sent", f"OTP sent to {recipient_email}")
            self.verify_otp(user)

        except Exception as e:
            QMessageBox.critical(self, "❌ Error", f"Failed to send OTP: {e}")

    def verify_otp(self, user):
        otp_input, ok = QInputDialog.getText(self, "OTP Verification", "Enter OTP sent to your email:")
        if ok and otp_input == self.otp:
            QMessageBox.information(self, "✅ Success", "OTP Verified. Access Granted!")
            self.open_dashboard(user)
        else:
            QMessageBox.critical(self, "❌ Error", "Invalid OTP! Access Denied.")

    def open_dashboard(self, user):
        self.dashboard = Dashboard(user, self.csv_file)
        self.dashboard.show()
        self.close()

class Dashboard(QWidget):
    def __init__(self, user, csv_file):
        super().__init__()
        self.setWindowTitle("🏦 GV Bank - Dashboard")
        self.setGeometry(100, 100, 800, 600)

        self.user = user
        self.csv_file = csv_file
        self.data = pd.read_csv(self.csv_file)
        self.user_index = self.data[self.data['Account Number'] == self.user['Account Number']].index[0]

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel(f"🏦 GV Bank - Welcome, {self.user['Name']}!")
        title.setFont(QFont("Arial", 22))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.balance_label = QLabel(f"💰 Balance: ₹{self.user['Balance (₹)']:.2f}")
        self.balance_label.setFont(QFont("Arial", 16))
        layout.addWidget(self.balance_label)

        self.deposit_button = QPushButton("💵 Deposit", self)
        self.style_button(self.deposit_button, "#4CAF50")
        self.deposit_button.clicked.connect(self.deposit_funds)
        layout.addWidget(self.deposit_button)

        self.transfer_button = QPushButton("📤 Transfer", self)
        self.style_button(self.transfer_button, "#2196F3")
        self.transfer_button.clicked.connect(self.transfer_funds)
        layout.addWidget(self.transfer_button)

        self.pin_button = QPushButton("🔒 Change PIN", self)
        self.style_button(self.pin_button, "#FF9800")
        self.pin_button.clicked.connect(self.change_pin)
        layout.addWidget(self.pin_button)

        self.logout_button = QPushButton("🚪 Logout", self)
        self.style_button(self.logout_button, "#F44336")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        self.setLayout(layout)

    def style_button(self, button, color):
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 8px;
                padding: 15px;
                font-size: 18px;
            }}
            QPushButton:hover {{
                background-color: {self.lighten_color(color)};
            }}
        """)

    def lighten_color(self, color, factor=1.2):
        r = min(255, int(int(color[1:3], 16) * factor))
        g = min(255, int(int(color[3:5], 16) * factor))
        b = min(255, int(int(color[5:7], 16) * factor))
        return f"#{r:02X}{g:02X}{b:02X}"

    def deposit_funds(self):
        amount, ok = QInputDialog.getDouble(self, "Deposit", "Enter amount to deposit (₹):", min=1.0)
        if ok:
            self.user['Balance (₹)'] += amount
            self.update_balance()

    def transfer_funds(self):
        recipient_account, ok1 = QInputDialog.getInt(self, "Transfer", "Enter recipient's account number:", min=1)
        if ok1:
            recipient = self.data[self.data["Account Number"] == recipient_account]
            if recipient.empty:
                QMessageBox.critical(self, "❌ Error", "Recipient account not found!")
                return
            amount, ok2 = QInputDialog.getDouble(self, "Transfer", "Enter amount to transfer (₹):", min=1.0)
            if ok2 and amount <= self.user['Balance (₹)']:
                self.user['Balance (₹)'] -= amount
                recipient_index = recipient.index[0]
                self.data.at[recipient_index, 'Balance (₹)'] += amount
                self.update_balance()
            elif ok2:
                QMessageBox.critical(self, "❌ Error", "Insufficient funds!")

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FaceLogin()
    window.show()
    sys.exit(app.exec())
