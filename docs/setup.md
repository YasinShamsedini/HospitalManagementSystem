
```markdown
# Installation Guide for Hospital Management System

This guide will walk you through the steps to install and set up the Hospital Management System on your local machine.

## Prerequisites

Make sure you have the following installed:

- **Python 3.x**: You can download it from [python.org](https://www.python.org/downloads/).
- **SQL Server**: This project uses SQL Server as the database. You can download and install SQL Server from [here](https://www.microsoft.com/en-us/sql-server/sql-server-downloads).

### Required Python Libraries

The project uses some external libraries. You can install them using `pip`:

```bash
pip install -r requirements.txt
```

If you don't have the `requirements.txt` file, you can create one by adding the following libraries manually:

- `pyodbc`
- `Pillow`
- `tkcalendar`

Install them individually if needed:

```bash
pip install pyodbc Pillow tkcalendar
```

## Database Setup

This project uses SQL Server for data storage. You will need to create a database and tables for the system to work properly.

By running the SQL code in Ypur SSMS, ypu will be able to access the database and tables and intract with that.


### Remember to Update Connection String

In the `src` folder, open the `database.py` file (or the file where you set up your database connection), and update the connection string to match your local SQL Server instance:

```python
self.conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 18 for SQL Server};'
    r'SERVER=.\SQLEXPRESS;'  # Replace with your SQL Server instance name
    r'DATABASE=HospitalDB;'
    r'TrustServerCertificate=yes;'
    r'Authentication=ActiveDirectoryIntegrated;'  # Or your authentication method
)
```



```markdown
## Running the Application

Once you have the database set up and the dependencies installed, you can run the application.

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/Hospital-Management-System.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd Hospital-Management-System
   ```

3. **Run the application**:

   ```bash
   python src/main.py
   ```

This will start the Hospital Management System with a GUI built using Tkinter.

Alternatively, you can open the project in **PyCharm** or **VS Code**, and run it directly from there.
``


## Troubleshooting

- If you encounter issues with the database connection, check the connection string in the `database.py` file.
- Make sure your SQL Server instance is running and accessible.
- Ensure the `image_path` in the code matches the location of the image file on your device.
<br> <br> 

## Enjoy using the software!

