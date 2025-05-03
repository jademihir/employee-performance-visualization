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

## File Structure


## Requirements

- Python 3.x
- PyQt5
- matplotlib

Install dependencies with:
```bash
pip install PyQt5 matplotlib

## Usage
1. Run the Application :
   
   bash
   
   Run
   
   Open Folder
   
   1
   
   python employee.py
2. Login :
   
   - Default credentials:
     - Username: admin
     - Password: password123
3. Add or Update Employee :
   
   - Enter the employee's name, score (0-100), and department.
   - Click "Submit/Update" to save.
4. View & Edit :
   
   - Click any row in the table to load its data into the entry fields for editing.
5. Visualizations :
   
   - The right panel displays a pie chart (departmental score distribution) and a bar chart (all employees' scores).
## Data Format
The employees.csv file stores employee records in the following format:

Name Score Department Mihir 90 Data Scientist Harry 84 Software Developer Jennie 53 Devops Katie 91 Data Scientist Ben 73 Backend Developer Charlie 80 Linux Administrator

## Customization
- Add More Users : Edit the USERS dictionary in employee.py to add more login credentials.
- Change Data File : Modify the DATA_FILE variable in employee.py if you want to use a different CSV file.
## Notes
- The application is intended for local, single-user use and does not provide advanced security.
- All data is stored locally in the CSV file.
## License
This project is provided for educational purposes. No specific license.