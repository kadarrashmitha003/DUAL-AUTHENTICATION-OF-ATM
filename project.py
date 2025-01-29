
from tkinter import *
from tkinter import ttk
import random 
import time
import cv2
import numpy as np
import string

# Sample user data for demonstration purposes
users = {
    '1234567890': {'fingerprint': 'hashed_fingerprint1', 'otp': None, 'otp_time': None, 'invalid_attempts': 0, 'blocked': False, 'balance': 50000},
    '0987654321': {'fingerprint': 'hashed_fingerprint2', 'otp': None, 'otp_time': None, 'invalid_attempts': 0, 'blocked': False, 'balance': 60000},
}

def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join(random.choices('0123456789', k=6))

def capture_fingerprint(image_path=None):
    """Capture fingerprint from an image file"""
    if image_path:
        fingerprint_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if fingerprint_image is None:
            print("Failed to load the image.")
            return None
    else:
        # Dummy fingerprint image if no path is provided
        fingerprint_image = np.random.randint(0, 255, size=(100, 100), dtype=np.uint8)
    
    return fingerprint_image

def generate_otp_with_fingerprint():
    """Generate OTP using fingerprint and image processing (dummy function)"""
    fingerprint_image = capture_fingerprint()
    
    # Generate a random OTP
    otp = ''.join(random.choices(string.digits, k=6))  # 6-digit OTP
    return otp

def authenticate(card_number, fingerprint=None):
    """Authenticate the user and generate OTP"""
    user = users.get(card_number)
    if user and not user['blocked'] and (fingerprint is None or user['fingerprint'] == fingerprint):
        otp = generate_otp()
        user['otp'] = otp
        user['otp_time'] = time.time()
        user['invalid_attempts'] = 0
        print(f"OTP for {card_number}: {otp}")  # For demonstration
        otp_label.config(text=f"OTP for {card_number}: {otp}")  # Update UI for OTP (demo)
        return otp
    else:
        print("Authentication failed. Invalid card number, fingerprint, or account is blocked.")
        return None

def transaction_window():
    window = Toplevel(master)
    window.title("Welcome to the Advanced Security System")
    window.configure(bg="#E6E6FA")  # Lavender
    window.geometry('739x415')

    Label(window, text="Advanced ATM Security System", font=("Arial Bold", 30)).pack(pady=10)

    def otp_verification_window():
        otp_window = Toplevel(window)
        otp_window.title("OTP Verification")
        otp_window.configure(bg="#E6E6FA")  # Lavender
        otp_window.geometry('400x200')

        Label(otp_window, text="Enter OTP:", font=("Arial", 12)).pack(pady=10)
        otp_entry = Entry(otp_window)
        otp_entry.pack(pady=5)

        def verify_otp():
            otp = otp_entry.get()
            current_time = time.time()
            user = users.get(account_number)
            
            if user['blocked']:
                Label(otp_window, text="Account is blocked. Contact your bank.", font=("Arial", 12)).pack(pady=10)
                return

            if user['otp'] == otp and current_time - user['otp_time'] <= 60:
                Label(otp_window, text="OTP Verified. Access Granted!", font=("Arial", 12)).pack(pady=10)
                print("Fingerprint authentication and OTP verification successful.")  # Added statement
                transaction_selection_window()
            else:
                user['invalid_attempts'] += 1
                if user['invalid_attempts'] >= 3:
                    user['blocked'] = True
                    Label(otp_window, text="Account blocked due to multiple invalid attempts.", font=("Arial", 12)).pack(pady=10)
                else:
                    Label(otp_window, text="Invalid OTP. Try Again.", font=("Arial", 12)).pack(pady=10)

        Button(otp_window, text="Verify OTP", command=verify_otp).pack(pady=10)

    def transaction_selection_window():
        transaction_window = Toplevel(window)
        transaction_window.title("Select Transaction")
        transaction_window.configure(bg="#E6E6FA")  # Lavender
        transaction_window.geometry('739x415')

        Label(transaction_window, text="Select Transaction Type", font=("Arial Bold", 20)).pack(pady=20)

        Button(transaction_window, text="Withdrawal", font=("Arial Bold", 18), bg="#FF6347", fg="white", command=withdrawal).pack(pady=10)
        Button(transaction_window, text="Balance", font=("Arial Bold", 18), bg="#4682B4", fg="white", command=balance).pack(pady=10)
        Button(transaction_window, text="Mini statement", font=("Arial Bold", 18), bg="#4682B4", fg="white", command=statement).pack(pady=10)
        Button(transaction_window, text="Fund Transfer", font=("Arial Bold", 18), bg="#4682B4", fg="white", command=fund_transfer).pack(pady=10)
        Button(transaction_window, text="Deposit", font=("Arial Bold", 18), bg="#32CD32", fg="white", command=deposit).pack(pady=10)

    def on_fingerprint():
        fingerprint_image = capture_fingerprint("C:\\Users\\KADARUS\\Desktop\\fingerprint.jpeg")
        if fingerprint_image is not None:
            # Add actual fingerprint processing logic here
            authenticate(account_number, 'hashed_fingerprint1')
            otp_verification_window()

    def on_card():
        authenticate(account_number)
        otp_verification_window()

    account_number = '1234567890'  # For demonstration

    Label(window, text="Choose Access Method", font=("Arial", 18)).pack(pady=10)
    Button(window, text="Fingerprint Access", command=on_fingerprint).pack(pady=10)
    Button(window, text="Card Access", command=on_card).pack(pady=10)

def new_window():
    master.withdraw()
    transaction_window()

def withdrawal():
    withdrawal_window = Toplevel(master)
    withdrawal_window.configure(bg="#E6E6FA")  # Lavender
    withdrawal_window.geometry('739x415')
    Label(withdrawal_window, text="Please enter your amount for withdrawal", font=("Arial Bold", 10)).place(x=50, y=30)
    amount_entry = Entry(withdrawal_window)
    amount_entry.place(x=50, y=80)

    def on_withdraw():
        amount = int(amount_entry.get())
        user = users.get('1234567890')  # Get the current user data
        if user['balance'] >= amount:
            user['balance'] -= amount
            Label(withdrawal_window, text="Amount Successfully Withdrawn", font=("Arial Bold", 8)).place(x=50, y=110)
            Label(withdrawal_window, text=f"New Balance: {user['balance']} rupees", font=("Arial Bold", 10)).place(x=50, y=140)
        else:
            Label(withdrawal_window, text="Insufficient Balance", font=("Arial Bold", 8)).place(x=50, y=110)

    Button(withdrawal_window, text="Enter", command=on_withdraw, bg="#FF6347", fg="white").place(x=50, y=130)

def balance():
    balance_window = Toplevel(master)
    balance_window.configure(bg="#E6E6FA")  # Lavender
    balance_window.geometry('739x415')
    user = users.get('1234567890')  # Get the current user data
    Label(balance_window, text=f"Your balance is {user['balance']} rupees", font=("Arial Bold", 10)).place(x=50, y=30)

def statement():
    statement_window = Toplevel(master)
    statement_window.configure(bg="#E6E6FA")  # Lavender
    statement_window.geometry('739x415')
    Label(statement_window, text="5000 is withdrawn from your account on 10/10/19", font=("Arial Bold", 10)).place(x=50, y=30)

def fund_transfer():
    fund_transfer_window = Toplevel(master)
    fund_transfer_window.configure(bg="#E6E6FA")  # Lavender
    fund_transfer_window.geometry('739x415')
    Label(fund_transfer_window, text="Please enter your amount for transfer", font=("Arial Bold", 10)).place(x=50, y=30)
    z = Entry(fund_transfer_window)
    z.place(x=50, y=80)

    def on_button6():
        Label(fund_transfer_window, text="Amount Successfully Transferred to another account", font=("Arial Bold", 8)).place(x=50, y=110)

    Button(fund_transfer_window, text="Enter", command=on_button6, bg="#4682B4", fg="white").place(x=50, y=130)

def deposit():
    deposit_window = Toplevel(master)
    deposit_window.configure(bg="#E6E6FA")  # Lavender
    deposit_window.geometry('739x415')
    Label(deposit_window, text="Please enter your amount for deposit", font=("Arial Bold", 10)).place(x=50, y=30)
    x = Entry(deposit_window)
    x.place(x=50, y=80)

    def on_button5():
        Label(deposit_window, text="Amount Successfully Deposited", font=("Arial Bold", 8)).place(x=50, y=110)

    Button(deposit_window, text="Enter", command=on_button5, bg="#32CD32", fg="white").place(x=50, y=130)

# Main window
master = Tk()
master.configure(bg="#ADD8E6")  # Light Blue
master.geometry('739x415')
Label(master, text="Please Select Your Bank", font=("Times New Roman", 30)).grid(row=0, column=100)
var1 = IntVar()
Checkbutton(master, text="State Bank of India", font=("Times New Roman", 10), variable=var1).grid(row=1, sticky=W, column=100)
var2 = IntVar()
Checkbutton(master, text="Bank Of India", font=("Times New Roman", 10), variable=var2).grid(row=2, sticky=W, column=100)
var3 = IntVar()
Checkbutton(master, text="Central Bank of India", font=("Times New Roman", 10), variable=var3).grid(row=3, sticky=W, column=100)
var4 = IntVar()
Checkbutton(master, text="Punjab National Bank", font=("Times New Roman", 10), variable=var4).grid(row=4, sticky=W, column=100)
var5 = IntVar()
Checkbutton(master, text="Oriental Bank of Commerce", font=("Times New Roman", 10), variable=var5).grid(row=5, sticky=W, column=100)
var6 = IntVar()
Checkbutton(master, text="Bhartiya Mahila Bank", font=("Times New Roman", 10), variable=var6).grid(row=6, sticky=W, column=100)
var7 = IntVar()
Checkbutton(master, text="State Bank of India", font=("Times New Roman", 10), variable=var7).grid(row=7, sticky=W, column=100)
var8 = IntVar()
Checkbutton(master, text="Andhra Bank", font=("Times New Roman", 10), variable=var8).grid(row=8, sticky=W, column=100)

Button(master, text='Enter', command=new_window).grid(row=9, column=100, pady=20)

otp_label = Label(master, text="", font=("Arial", 12), bg="#ADD8E6")  # Light Blue
otp_label.grid(row=10, column=100)

master.mainloop()
