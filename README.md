# Employee Performance Entry & Visualization System

A desktop application built with Python (PyQt5 and Matplotlib) for managing employee performance data, visualizing departmental score distributions, and providing a simple login-protected interface.

![Screenshot](Screenshot%202025-05-03%20190155.png)

## Features

- **Login System**: Simple authentication for access control.
- **Employee Data Entry**: Add or update employee name, performance score (0-100), and department.
- **Data Table**: View all employee records in a sortable, non-editable table.
- **Charts**:
  - **Pie Chart**: Visualizes total score distribution by department.
  - **Bar Chart**: Displays all employees' individual scores.
- **Persistent Storage**: Employee data is saved to and loaded from a CSV file (`employees.csv`).
- **Interactive UI**: Selecting a row in the table populates the entry fields for easy editing.
