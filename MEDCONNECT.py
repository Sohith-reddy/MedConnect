import os
import json
import time
import re
import pyttsx3

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def mainmenu():
    while True:
        print('\t\t\tMEDCONNECT\n\t\t\t WELCOME\n')
        time.sleep(1)
        print(
            'Select User Type:\n\t1.Doctor\n\t2.Patient\n\t3.Calculate BMI\n\t4.Upcoming '
            'updates\n\t5.Feedback\n\t0.Exit')
        speak("Select User Type")
        n = input("\t  Enter your option: ")
        if n == '1':
            doclogin()
            break
        elif n == '2':
            patientlogin()
            break
        elif n == '4':
            updates()
            os.system('cls')
        elif n == '3':
            calculatebmi()
        elif n == '5':
            print("\n\nYour Feedback is very important to us\nPlease Enter Your Feedback:\n")
            speak("Your Feedback is very important to us\nPlease Enter Your Feedback:\n")
            name = input("Enter Your Name:")
            phno = input("Enter Your Contact details(phno/mail id):")
            feed = input("Write Your Suggestions or Queries Here:")
            feedback(name, phno, feed)
        elif n == '0':
            time.sleep(1)
            print("Closing The Application...")
            speak("Closing the Application")
            return False
            os.system('cls')
        else:
            print("\nOops...\nWrong Option Selected\nRedirecting to the main menu\n\n\n")
            speak("\nOops...\nWrong Option Selected\nRedirecting to the main menu\n\n\n")
            time.sleep(2)
            os.system('cls')


def feedback(name, phno, feed):
    feedback_data = {'name': name, 'contact': phno, 'Feedback': feed}
    with open('feedback.json', 'a') as file:
        json.dump(feedback_data, file)
        file.write('\n')

    print("Okay", name, "!", "Your feedback is valuable to us...")
    time.sleep(2)
    speak("Thank You For giving your feedback")
    print("Thank You For giving your feedback\n\n")
    time.sleep(4)
    os.system('cls')


def validate():
    while True:
        c = 0
        password = input("Enter password:")
        if 6 > len(password) > 14:
            print("Pass length must be greater than 6 ")
            speak("Incorrect password format")
            speak("Pass length must be greater than 6 ")
            c = 1
        if not re.search(r"[a-z]", password):
            print("Password must contain one lowercase alphabet")
            speak("Password must contain one lowercase alphabet")
            c = 1
        if not re.search(r"\d", password):
            print("Password must have digit in it")
            speak("Password must have digit in it")
            c = 1
        if not password[0].isupper():
            print("Password must start with uppercase alphabet")
            speak("Password must start with uppercase alphabet")
            c = 1
        if not re.search(r"[!@#$]", password):
            print("Password must contain at least one special Character")
            speak("Password must contain at least one special Character")
            c = 1
        if c == 1:
            print("Enter password again!\n")
        else:
            while 1:
                confirm_password = input("confirm password:")
                if password == confirm_password:
                    print("password matched")
                    break
                else:
                    print("password did not matched")
            break
    return password


def load_data(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)
            return data
    else:
        return {}


def save_data(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)


def doclogin():
    print("\n..........DOCTOR LOGIN PAGE..........\n")
    doctor_details = {"Doctor123$": "Password123$"}
    username = input("Enter username: ")
    password = input("Enter password: ")
    if username in doctor_details and doctor_details[username] == password:
        print("Details Matched\n")
        doctor_menu()
    else:
        print("\nInvalid Details :(\nRedirecting to the main menu...\n\n")
        time.sleep(2)
        mainmenu()


def patientlogin():
    print("\n..........PATIENT LOGIN PAGE..........\n")
    print("SELECT BELOW OPTION")
    print("\t1. Existing User\n\t2. New User")
    option = input("Enter your option: ")
    if option == '1':
        existingpatient()
    elif option == '2':
        newpatient()
    else:
        print("\nInvalid Details :(\nRedirecting to the main menu...\n\n")
        time.sleep(2)
        mainmenu()


def existingpatient():
    print("..........EXISTING PATIENT LOGIN PAGE..........")
    username = input("Enter username: ")
    password = input("Enter password: ")
    data = load_data('patients.json')
    if username in data and data[username]['password'] == password:
        print("Login successful!\n")
        patient_menu(username)
    else:
        print("Invalid credentials or user does not exist.\n")
        time.sleep(2)
        mainmenu()


def newpatient():
    print("\n..........NEW PATIENT REGISTRATION..........\n")
    username = input("Enter username: ")
    print(
        "\n\n 1. Password should be at least 6 characters.\n 2. Password should start with an uppercase character.\n "
        "3. Password should have at least one number.\n 4. Password should have at least one special character ("
        "!@#$).\n\n"
    )
    password = validate()
    data = load_data('patients.json')
    if username in data:
        print("Username already exists. Please choose a different username.")
        time.sleep(2)
        mainmenu()
    else:
        name = input("Enter your name: ")
        age = input("Enter your age: ")
        gender = input("Enter your gender: ")
        data[username] = {'password': password, 'name': name, 'age': age, 'gender': gender, 'issues': ''}
        save_data(data, 'patients.json')
        print("Account created successfully!\n")
        patient_menu(username)


def patient_menu(username):
    while True:
        print(f"Welcome, {username}!")
        speak("Welcome")
        print("1. Enter your health issues")
        speak("1. Enter your health issues")
        print("2. Logout")
        speak("2. Logout")
        print("3. Prescription")
        speak("3. Prescription")
        speak("Enter your choice: ")
        choice = input("Enter your choice: ")
        if choice == '1':
            enter_health_issues(username)
        elif choice == '2':
            print("Logging out...")
            speak("Logging out...")
            time.sleep(2)
            mainmenu()
        elif choice == '3':
            print("Doctor prescription\n")
            speak("Doctor prescription")
            display_prescription(username)
        else:
            print("Invalid choice!")
            speak("Invalid choice!")


def enter_health_issues(username):
    data = load_data('patients.json')
    if username in data:
        issues = input("Please enter your health issues: ")
        data[username]['issues'] = issues
        save_data(data, 'patients.json')
        print("Health issues saved successfully!")
        time.sleep(2)
        patient_menu(username)
    else:
        print("Patient not found. Redirecting to the main menu...")
        time.sleep(2)
        mainmenu()


def doctor_menu():
    while True:
        print("\n..........DOCTOR MENU..........")
        print("1. View patients")
        print("2. Write prescription")
        print("3. Logout")
        choice = input("Enter your choice: ")
        if choice == '1':
            view_patients()
        elif choice == '2':
            write_prescription()
        elif choice == '3':
            print("Logging out...")
            time.sleep(2)
            mainmenu()
        else:
            print("Invalid choice!")


def view_patients():
    data = load_data('patients.json')
    print("\n\nPATIENTS:\n")
    for username, details in data.items():
        print("Username:", username)
        print("Name:", details['name'])
        print("Age:", details['age'])
        print("Health Issues:", details['issues'])
        print("-------------------------")
    time.sleep(2)
    doctor_menu()


def write_prescription():
    data = load_data('patients.json')
    username = input("Enter patient's username: ")
    if username in data:
        prescription = input("Write prescription for " + username + ": ")
        data[username]['prescription'] = prescription
        save_data(data, 'patients.json')
        print("Prescription saved successfully!")
        time.sleep(2)
        doctor_menu()
    else:
        print("Patient not found. Redirecting to the doctor menu...")
        time.sleep(2)
        doctor_menu()


def display_prescription(username):
    print("Prescription:")
    with open('patients.json', 'r') as f:
        data = json.load(f)
        print(data[username]['prescription'])
        print('\n\n\n')


def calculatebmi():
    x = float(input("Enter the weight:"))
    y = float(input("Enter the height in meters:"))
    bmi = x / (y ** 2)
    bmi1 = format(bmi, ".2f")
    print("BMI:", bmi1)
    a = categorize_bmi(bmi)
    print("Category:", a)
    time.sleep(4)
    os.system('cls')


def categorize_bmi(bmi):
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal"
    elif 25 <= bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    return category


def updates():
    print("Upcoming updates:\n\tOnline booking for medicines\n\tBook Physical Appointment\n\tCalories Tracker\n\n")
    speak("Upcoming updates:\n\tOnline booking for medicines\n\tBook Physical Appointment\n\tCalories Tracker\n\n")


def Exit():
    print("Closing The Application")
    speak("Closing the Application")
    return False


def main():
    mainmenu()


main()
