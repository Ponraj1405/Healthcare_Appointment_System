import os
import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QDate, QTime

from PyQt5.uic import loadUi


API_BASE = "http://127.0.0.1:8000/api"


def fetch_doctors():
    url = f"{API_BASE}/doctors/"
    response = requests.get(url)
    data = response.json()

    if data.get("status") == "success":
        return data["data"]
    return []

def fetch_appointments(patient_username):
    url = f"{API_BASE}/appointments/?patient={patient_username}"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    try:
        data = response.json()
    except ValueError:
        return []

    if data.get("status") == "success":
        return data["data"]

    return []



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        base_path = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(base_path, "ui", "main.ui")
        loadUi(ui_path, self)

        # -------- INIT --------
        self.stackedWidget.setCurrentIndex(0)
        self.dateEdit.setDate(QDate.currentDate())
        self.timeEdit.setTime(QTime.currentTime())

        self.logged_in_username = None
        self.doctor_map = {}

        # -------- BUTTONS --------
        self.loginButton.clicked.connect(self.handle_login)
        self.bookAppointmentButton.clicked.connect(self.go_to_book_appointment)
        self.viewAppointmentsButton.clicked.connect(self.go_to_appointments)
        self.confirmAppointmentButton.clicked.connect(self.handle_confirm_appointment)
        self.backButton0.clicked.connect(self.go_to_login)
        self.logoutButton1.clicked.connect(self.go_to_login)
        self.backButton1.clicked.connect(self.go_to_patient_dashboard)
        self.backButton2.clicked.connect(self.go_to_book_appointment)


        
        self.exitButton.clicked.connect(self.close)

        # Load doctors
        self.load_doctors()

    # -------- NAVIGATION --------
    def go_to_login(self):
        self.stackedWidget.setCurrentIndex(0)

    def go_to_patient_dashboard(self):
        self.stackedWidget.setCurrentIndex(1)

    def go_to_book_appointment(self):
        self.stackedWidget.setCurrentIndex(2)

    def go_to_appointments(self):
        self.stackedWidget.setCurrentIndex(3)
        self.load_appointments()


    # -------- LOGIN --------
    def handle_login(self):
        username = self.usernameLineEdit.text()

        if not username:
            QMessageBox.warning(self, "Error", "Enter username")
            return

        self.logged_in_username = username
        self.stackedWidget.setCurrentIndex(1)

    # -------- LOAD DOCTORS --------
    def load_doctors(self):
        doctors = fetch_doctors()
        self.comboDoctor.clear()
        self.doctor_map.clear()

        for doc in doctors:
            username = doc["user"]["username"]
            specialization = doc["specialization"]
            display = f"{username} ({specialization})"

            self.comboDoctor.addItem(display)
            self.doctor_map[display] = username

    # -------- BOOK APPOINTMENT --------
    def handle_confirm_appointment(self):
        doctor_display = self.comboDoctor.currentText()

        if not doctor_display:
            QMessageBox.warning(self, "Error", "Select doctor")
            return

        doctor_username = self.doctor_map[doctor_display]
        date = self.dateEdit.date().toString("yyyy-MM-dd")
        time = self.timeEdit.time().toString("HH:mm")

        payload = {
            "patient": self.logged_in_username,
            "doctor": doctor_username,
            "date": date,
            "time": time
        }

        response = requests.post(
            f"{API_BASE}/book-appointment/",
            json=payload
        )

        result = response.json()

        if result.get("status") == "success":
            QMessageBox.information(
                self,
                "Success",
                "Appointment booked successfully!"
            )
        else:
            QMessageBox.critical(
                self,
                "Failed",
                result.get("message", "Error")
            )

    def load_appointments(self):
        appointments = fetch_appointments(self.logged_in_username)

        self.appointmentsTable.setRowCount(0)
        self.appointmentsTable.setColumnCount(4)
        self.appointmentsTable.setHorizontalHeaderLabels(
            ["Doctor", "Date", "Time", "Status"]
        )

        for row_idx, appt in enumerate(appointments):
            self.appointmentsTable.insertRow(row_idx)

            # ---- Doctor name handling ----
            doctor_name = ""
            if isinstance(appt.get("doctor"), dict):
                doctor_name = appt["doctor"].get("username", "")
            elif isinstance(appt.get("doctor"), str):
                doctor_name = appt["doctor"]
            else:
                doctor_name = str(appt.get("doctor", ""))

            self.appointmentsTable.setItem(
                row_idx, 0,
                QTableWidgetItem(doctor_name)
            )

            self.appointmentsTable.setItem(
                row_idx, 1,
                QTableWidgetItem(appt["date"])
            )

            self.appointmentsTable.setItem(
                row_idx, 2,
                QTableWidgetItem(appt["time"][:5])
            )

            self.appointmentsTable.setItem(
                row_idx, 3,
                QTableWidgetItem(appt["status"])
            )



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
