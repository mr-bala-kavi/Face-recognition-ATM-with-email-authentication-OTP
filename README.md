# 🏦 Face Recognition ATM with Email Authentication OTP 🔐

A secure ATM simulation system that uses **face recognition** and **OTP verification via email** for double-layered authentication. Built with Python.

---

## 🔁 COMPLETE FLOW OF THE PROJECT

Use **Python 3.8 – 3.11**  
✅ *Tested with Python 3.10*

---

## 🪜 STEP-BY-STEP PROCEDURE (For Windows)

### 1️⃣ Create the Project Folder
Create a folder for your project:
```
your_folder_name/
```

### 2️⃣ Inside It, Create a `faces/` Folder
This is where captured face images will be stored.

### 3️⃣ Create a Virtual Environment
Open CMD and run:
```bash
python -m venv your_venv_name
```

### 4️⃣ Activate the Virtual Environment
```bash
your_venv_name\Scripts\activate
```

### 5️⃣ Install Required Packages
Either:
```bash
pip install -r requirements.txt
```
Or install packages manually:
```bash
pip install package_name
```

### 6️⃣ Move Project Files into Your Folder
Copy the following into your `your_folder_name/`:
- `faces/` folder  
- `accounts.csv`  
- `app.py`  
- `capture_face.py`  
- `requirements.txt`  

### 7️⃣ Configure Email Authentication
In `app.py`, **replace** the email and app password variables with your own.

### 8️⃣ Generate App Password for Email
1. Go to **[Google My Account](https://myaccount.google.com/)**  
2. Search for **"App Passwords"**  
3. Create an app name (e.g., `ATM App`)  
4. Copy the auto-generated password  
5. Paste it in `app.py` as your app password

### 9️⃣ Run the Face Recognition ATM
- To **capture and save your face**:
```bash
python capture_face.py
```

- To **run the GUI ATM interface**:
```bash
python app.py
```

---

## 💡 Features
- 🎭 Face recognition-based login  
- 📧 OTP authentication via email (Gmail)  
- 🧾 CSV-based account storage  
- 💻 PyQt5-based simple GUI interface  
- 🔒 Two-factor authentication (2FA)

---

## 📁 Folder Structure

```
your_folder_name/
│
├── faces/                # Captured user face images
├── accounts.csv          # Stores user account data (name, pin, email)
├── app.py                # Main GUI ATM application
├── capture_face.py       # Used to capture and store user faces
├── requirements.txt      # Python dependencies
```

---

## 📧 Contact
**Author**: Mr-Bala-Kavi  
📧 **Email**: [balakavi64@gmail.com](mailto:balakavi64@gmail.com)  
🌐 **GitHub**: [github.com/mr-bala-kavi](https://github.com/mr-bala-kavi)

---

Let me know if you want to add:
- 🔖 Screenshots of the GUI
- 🎥 A demo video/GIF
- ✅ Status badges (like Python version, license, etc.)
