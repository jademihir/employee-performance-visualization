import sys
import csv
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout, QHeaderView, QGroupBox
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

USERS = {"admin": "password123"}
DATA_FILE = "employees.csv"

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(300, 150)
        layout = QFormLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        layout.addRow("Username:", self.username)
        layout.addRow("Password:", self.password)
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.try_login)
        layout.addWidget(self.login_btn)
        self.setLayout(layout)
        self.accepted = False

    def try_login(self):
        user = self.username.text()
        pwd = self.password.text()
        if USERS.get(user) == pwd:
            self.accepted = True
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials.")

class EmployeeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Performance Entry & Visualization (PyQt5)")
        self.setGeometry(100, 100, 1000, 600)
        self.employees_data = {}
        self.load_from_csv()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        header = QLabel("Employee Performance Entry & Visualization System")
        header.setStyleSheet("font-size: 22px; font-weight: bold; background: #3399ff; color: white; padding: 10px;")
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        content_layout = QHBoxLayout()

        # Input Section
        input_group = QGroupBox("Enter Employee Details")
        input_layout = QFormLayout()
        self.name_edit = QLineEdit()
        self.score_edit = QLineEdit()
        self.dept_edit = QLineEdit()
        input_layout.addRow("Employee Name:", self.name_edit)
        input_layout.addRow("Performance Score (0-100):", self.score_edit)
        input_layout.addRow("Department:", self.dept_edit)
        self.submit_btn = QPushButton("Submit/Update")
        self.submit_btn.clicked.connect(self.submit)
        input_layout.addWidget(self.submit_btn)
        input_group.setLayout(input_layout)
        content_layout.addWidget(input_group, 1)

        # Table Section
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Name", "Score", "Department"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellClicked.connect(self.on_row_select)
        content_layout.addWidget(self.table, 2)

        # Chart Section
        chart_group = QGroupBox("Charts")
        chart_layout = QVBoxLayout()
        self.fig, (self.ax_pie, self.ax_bar) = plt.subplots(2, 1, figsize=(4, 6))
        plt.tight_layout()
        self.canvas = FigureCanvas(self.fig)
        chart_layout.addWidget(self.canvas)
        chart_group.setLayout(chart_layout)
        content_layout.addWidget(chart_group, 2)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)
        self.update_table()
        self.update_charts()

    def submit(self):
        name = self.name_edit.text().strip()
        try:
            score = int(self.score_edit.text())
            if not (0 <= score <= 100):
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Score must be an integer between 0 and 100.")
            return
        dept = self.dept_edit.text().strip()
        if not name or not dept:
            QMessageBox.warning(self, "Invalid Input", "Name and Department cannot be empty.")
            return
        self.employees_data[name] = (score, dept)
        self.save_to_csv()
        self.update_table()
        self.update_charts()

    def update_table(self):
        self.table.setRowCount(0)
        for name, (score, dept) in self.employees_data.items():
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(str(score)))
            self.table.setItem(row, 2, QTableWidgetItem(dept))

    def update_charts(self):
        self.ax_pie.clear()
        self.ax_bar.clear()
        # Pie chart: total score by department
        dept_totals = {}
        for name, (score, dept) in self.employees_data.items():
            dept_totals[dept] = dept_totals.get(dept, 0) + score
        if dept_totals:
            depts = list(dept_totals.keys())
            totals = [dept_totals[dept] for dept in depts]
            color_map = plt.get_cmap('tab20')
            dept_colors = {dept: color_map(i) for i, dept in enumerate(depts)}
            colors = [dept_colors[dept] for dept in depts]
            self.ax_pie.pie(totals, labels=depts, autopct='%1.1f%%', colors=colors)
            self.ax_pie.set_title("Total Score Distribution by Department")
        else:
            self.ax_pie.text(0.5, 0.5, "No data", ha='center')
        # Bar chart: all employees' scores
        names = list(self.employees_data.keys())
        scores_list = [self.employees_data[n][0] for n in names]
        bar_colors = [dept_colors.get(self.employees_data[n][1], "#3399ff") for n in names] if dept_totals else "#3399ff"
        self.ax_bar.bar(names, scores_list, color=bar_colors)
        self.ax_bar.set_title("All Employees' Scores")
        self.ax_bar.set_ylabel("Score")
        self.ax_bar.set_xticklabels(names, rotation=45, ha='right')
        self.canvas.draw()

    def on_row_select(self, row, col):
        name = self.table.item(row, 0).text()
        score = self.table.item(row, 1).text()
        dept = self.table.item(row, 2).text()
        self.name_edit.setText(name)
        self.score_edit.setText(score)
        self.dept_edit.setText(dept)

    def save_to_csv(self):
        with open(DATA_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Score", "Department"])
            for name, (score, dept) in self.employees_data.items():
                writer.writerow([name, score, dept])

    def load_from_csv(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.employees_data[row["Name"]] = (int(row["Score"]), row["Department"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginDialog()
    if login.exec_() == QDialog.Accepted and login.accepted:
        window = EmployeeApp()
        window.show()
        sys.exit(app.exec_())