import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pyodbc
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import re  

class Database:
    def __init__(self):
        try:
            self.conn = pyodbc.connect(
                r'DRIVER={ODBC Driver 18 for SQL Server};'
                r'SERVER=.\SQLEXPRESS;'
                r'DATABASE=HospitalDB;'
                r'TrustServerCertificate=yes;'
                r'Authentication=ActiveDirectoryIntegrated;'
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
    
    def __del__(self):
        self.conn.close()

    def execute_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            raise e

    def fetch_patients(self):
        try:
            self.cursor.execute("SELECT PatientID, Name, Age, Gender, Contact FROM Patients")
            return self.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return []

    def fetch_doctors(self):
        try:
            self.cursor.execute("SELECT DoctorID, Name, Specialization, Contact FROM Doctors")
            return self.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return []

    def fetch_medicines(self):
        try:
            self.cursor.execute("SELECT MedicineID, Name, Quantity, Price FROM Medicines")
            return self.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return []


    def fetch_appointments(self):
        try:
            self.cursor.execute("""
                SELECT a.AppointmentID, 
                       p.Name + ' (' + CAST(p.PatientID AS NVARCHAR) + ')', 
                       d.Name + ' (' + CAST(d.DoctorID AS NVARCHAR) + ')', 
                       a.AppointmentDate, 
                       a.AppointmentTime 
                FROM Appointments a
                JOIN Patients p ON a.PatientID = p.PatientID
                JOIN Doctors d ON a.DoctorID = d.DoctorID
            """)
            return self.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return []

    def fetch_prescriptions(self):
        try:
            self.cursor.execute("""
                SELECT pr.PrescriptionID, 
                       p.Name + ' (' + CAST(p.PatientID AS NVARCHAR) + ')', 
                       d.Name + ' (' + CAST(d.DoctorID AS NVARCHAR) + ')', 
                       pr.Diagnosis, 
                       pr.Medication 
                FROM Prescriptions pr
                JOIN Patients p ON pr.PatientID = p.PatientID
                JOIN Doctors d ON pr.DoctorID = d.DoctorID
            """)
            return self.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return []

    def fetch_bills(self):
        try:
            self.cursor.execute("""
                SELECT b.BillID, 
                       p.Name + ' (' + CAST(p.PatientID AS NVARCHAR) + ')', 
                       b.Amount, 
                       FORMAT(b.BillDate, 'yyyy-MM-dd'), 
                       b.Status 
                FROM Bills b
                JOIN Patients p ON b.PatientID = p.PatientID
            """)
            return self.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return []
















class HospitalManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")

        # *** KEY CHANGE 1: Configure root background ***
        self.root.configure(bg='black')  # Or #000000 for black

        self.db = Database()

        # Main Container
        self.main_frame = tk.Frame(root, bg='black') # Added background
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Dashboard Frame
        self.dashboard_frame = tk.Frame(self.main_frame, width=0, bg='#282828')
        self.dashboard_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Content Frame (Right Side)
        self.content_frame = tk.Frame(self.main_frame, bg='#5d6d7e')
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        
        # Dashboard Buttons
        buttons = [
            ('Patients', self.show_patients),
            ('Doctors', self.show_doctors),
            ('Appointments', self.show_appointments),
            ('Prescriptions', self.show_prescriptions),
            ('Medicines', self.show_medicines),
            ('Bills', self.show_bills)
        ]

        # Load and display image
        try:
            image_path = "D:\\Users\\BLACK-RAYANE\\Downloads\\11865203.png"
            original_image = Image.open(image_path)
            resized_image = original_image.resize((200, 200), Image.LANCZOS) # Resize for better fit
            self.money_image = ImageTk.PhotoImage(resized_image)  # Store a reference to prevent garbage collection
            image_label = tk.Label(self.dashboard_frame, image=self.money_image, bg='#282828') # Label on dashboard, same background
            image_label.pack(side=tk.BOTTOM,pady=10,padx=10)  # Add padding above the image

        except FileNotFoundError:
            messagebox.showerror("Error", "Image not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image: {e}")
        
        for text, command in buttons:
            btn = tk.Button(self.dashboard_frame, text=text, width=19, 
                          command=command, bg='#38475c', fg='white',font=('Times New Roman',12))
            btn.pack(pady=12, padx=8)
        
        self.current_manager = None
        


    def clear_content(self):
        if self.current_manager:
            self.current_manager.destroy()
    
    def show_patients(self):
        self.clear_content()
        self.current_manager = PatientManager(self.content_frame)
    
    def show_doctors(self):
        self.clear_content()
        self.current_manager = DoctorManager(self.content_frame)
    
    def show_appointments(self):
        self.clear_content()
        self.current_manager = AppointmentManager(self.content_frame)
    
    def show_prescriptions(self):
        self.clear_content()
        self.current_manager = PrescriptionManager(self.content_frame)
    
    def show_bills(self):
        self.clear_content()
        self.current_manager = BillManager(self.content_frame)
    
    def show_medicines(self):
        self.clear_content()
        self.current_manager = MedicineManager(self.content_frame)


class PlaceholderManager(tk.Frame):
    def __init__(self, parent, section_name):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        lbl = tk.Label(self, text=f"{section_name} Management", font=("Arial", 16))
        lbl.pack(pady=20)








##########################
# PATIENT MANAGER
##########################


class PatientManager(tk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.db = Database()
        self.pack(fill=tk.BOTH, expand=True)
        
        # Configure style for dark theme
        self.style = ttk.Style()
        self.style.theme_use('default')
        
        # General background color
        self.configure(background='#38475c')
        
        # Configure widget styles
        self.style.configure('TFrame', background='#38475c')
        self.style.configure('TLabel', background='#38475c', foreground='white',font=('Times New Roman', 11)),  # Set font family and size)
        self.style.configure('TButton',
                            font=('Arial', 10,'bold'),
                            background='#1976D2', 
                            foreground='white', 
                            borderwidth=1,
                            focuscolor='#2e2e2e')
        self.style.map('TButton',
                    background=[('active', '#2a4e64'), ('pressed', '#6a6a6a')],
                    foreground=[('active', 'white')])
        
        # Treeview style
        self.style.configure('Treeview',
                            background='#38475c',
                            foreground='white',
                            fieldbackground='#38475c',
                            borderwidth=0)
        self.style.configure('Treeview.Heading',
                            font=('Times New Roman', 13),
                            padding=2,               # Adjust padding (optional)
                            background='#232c39',
                            foreground='white',
                            relief='flat')
        self.style.map('Treeview',
                    background=[('selected', '#2d6355')],
                    foreground=[('selected', 'white')])
        
        
        # Entry and Combobox style
        self.style.configure('TEntry',
                            fieldbackground='#e9e9e9',
                            foreground='black')
        self.style.configure('TCombobox',
                            fieldbackground='#e9e9e9',
                            foreground='black')
        
        # Main container
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview Frame
        tree_frame = ttk.Frame(self.main_frame)
        tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Form Frame
        form_frame = ttk.Frame(self.main_frame, width=300)
        form_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        # Treeview
        self.tree = ttk.Treeview(tree_frame, columns=('ID', 'Name', 'Age', 'Gender', 'Contact'), show='headings')
        self.tree.heading('ID', text='Patient ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Age', text='Age')
        self.tree.heading('Gender', text='Gender')
        self.tree.heading('Contact', text='Contact')
        # Align Columns and Set Widths
        self.tree.column('ID', width=80, anchor=tk.CENTER)
        self.tree.column('Name', width=150, anchor=tk.CENTER)
        self.tree.column('Age', width=80, anchor=tk.CENTER)
        self.tree.column('Gender', width=100, anchor=tk.CENTER)
        self.tree.column('Contact', width=150, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Form Fields
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W,padx=10, pady=5)
        self.name_entry = ttk.Entry(form_frame, width=25)
        self.name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Age:").grid(row=1, column=0, sticky=tk.W,padx=10, pady=5)
        self.age_entry = ttk.Entry(form_frame, width=25)
        self.age_entry.grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Gender:").grid(row=2, column=0, sticky=tk.W,padx=10, pady=5)
        self.gender_combobox = ttk.Combobox(form_frame, values=['Male', 'Female', 'Other'], width=23)
        self.gender_combobox.grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Contact:").grid(row=3, column=0, sticky=tk.W,padx=10, pady=5)
        self.contact_entry = ttk.Entry(form_frame, width=25)
        self.contact_entry.grid(row=3, column=1, pady=5)

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Add", command=self.add_patient, width=14).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="Update", command=self.update_patient, width=14).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_patient, width=14).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form, width=14).grid(row=1, column=1, padx=5, pady=5)

        # Load initial data
        self.load_patients()

        # Bind treeview selection
        self.tree.bind('<<TreeviewSelect>>', self.load_selected_patient)

    def load_patients(self):
        # Clear existing data in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            patients = self.db.fetch_patients()
            for patient in patients:
                # Convert all values to strings before inserting
                str_patient = tuple(str(value) for value in patient)
                self.tree.insert('', tk.END, values=str_patient)

        except Exception as e:
            messagebox.showerror("Error", f"Error loading patients: {e}")

    def load_selected_patient(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            if values:
                # Safely access values, handling potential missing elements
                name = values[1] if len(values) > 1 else ""
                age = values[2] if len(values) > 2 else ""
                gender = values[3] if len(values) > 3 else ""
                contact = values[4] if len(values) > 4 else ""

                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, name)
                self.age_entry.delete(0, tk.END)
                self.age_entry.insert(0, age)
                self.gender_combobox.set(gender)
                self.contact_entry.delete(0, tk.END)
                self.contact_entry.insert(0, contact)
            else:
                self.clear_form()


    def add_patient(self):
        try:
            name = self.name_entry.get()
            age = int(self.age_entry.get())
            gender = self.gender_combobox.get()
            contact = self.contact_entry.get()

            if not all([name, age, gender, contact]):
                messagebox.showerror("Error", "All fields are required!")
                return

            self.db.execute_query(
                "INSERT INTO Patients (Name, Age, Gender, Contact) VALUES (?, ?, ?, ?)",
                (name, age, gender, contact)
            )
            self.load_patients()
            self.clear_form()
            messagebox.showinfo("Success", "Patient added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Age must be a number!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_patient(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a patient to update!")
            return

        try:
            values = self.tree.item(selected, 'values')
            if not values or len(values) < 1:
                messagebox.showerror("Error", "No valid selection for update.")
                return

            patient_id = int(values[0])  # Convert to integer IMMEDIATELY

            name = self.name_entry.get()
            age = int(self.age_entry.get())
            gender = self.gender_combobox.get()
            contact = self.contact_entry.get()

            if not all([name, age, gender, contact]):
                messagebox.showerror("Error", "All fields are required!")
                return

            self.db.execute_query(
                "UPDATE Patients SET Name=?, Age=?, Gender=?, Contact=? WHERE PatientID=?",
                (name, age, gender, contact, patient_id)
            )
            self.load_patients()  # Reload to show updated data
            messagebox.showinfo("Success", "Patient updated successfully!")
            self.clear_form()

        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid input: {ve}")  # More general message
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_patient(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a patient to delete!")
            return

        try:
            values = self.tree.item(selected, 'values')
            if not values or len(values) < 1:
                messagebox.showerror("Error", "No valid selection for delete.")
                return

            patient_id = int(values[0])  # Convert to integer IMMEDIATELY

            if messagebox.askyesno("Confirm", "Are you sure you want to delete this patient?"):
                self.db.execute_query("DELETE FROM Patients WHERE PatientID=?", (patient_id,))
                self.load_patients()  # Reload to show updated data
                self.clear_form()
                messagebox.showinfo("Success", "Patient deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.gender_combobox.set('')
        self.contact_entry.delete(0, tk.END)




#####################
# DOCTORS MANAGMENT
#####################

class DoctorManager(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = Database()  # Initialize your database connection
        self.pack(fill=tk.BOTH, expand=True)

        # Configure style for dark theme
        self.style = ttk.Style()
        self.style.theme_use('default')

        # General background color
        self.configure(background='#38475c')

        # Configure widget styles
        self.style.configure('TFrame', background='#38475c')
        self.style.configure('TLabel', background='#38475c', foreground='white', font=('Times New Roman', 11))
        self.style.configure('TButton',
                            font=('Arial', 10, 'bold'),
                            background='#1976D2',
                            foreground='white',
                            borderwidth=1,
                            focuscolor='#2e2e2e')
        self.style.map('TButton',
                       background=[('active', '#2a4e64'), ('pressed', '#6a6a6a')],
                       foreground=[('active', 'white')])

        self.style.configure('Treeview',
                            background='#38475c',
                            foreground='white',
                            fieldbackground='#38475c',
                            borderwidth=0)
        self.style.configure('Treeview.Heading',
                            font=('Times New Roman', 13),
                            padding=2,
                            background='#232c39',
                            foreground='white',
                            relief='flat')
        self.style.map('Treeview',
                       background=[('selected', '#2d6355')],
                       foreground=[('selected', 'white')])


        self.style.configure('TEntry',
                            fieldbackground='#e9e9e9',
                            foreground='black')

        # Main container
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview Frame
        tree_frame = ttk.Frame(self.main_frame)
        tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Form Frame
        form_frame = ttk.Frame(self.main_frame, width=300)
        form_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        # Treeview
        self.tree = ttk.Treeview(tree_frame,
                                columns=('ID', 'Name', 'Specialization', 'Contact'),
                                show='headings')
        self.tree.heading('ID', text='Doctor ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Specialization', text='Specialization')
        self.tree.heading('Contact', text='Contact')
        self.tree.column('ID', width=80, anchor=tk.CENTER)
        self.tree.column('Name', width=150, anchor=tk.CENTER)
        self.tree.column('Specialization', width=200, anchor=tk.CENTER)
        self.tree.column('Contact', width=150, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)


        # Form Fields with Size and Positioning
        ttk.Label(form_frame, text="Name:", width=12).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)  # Added width and padx
        self.name_entry = ttk.Entry(form_frame, width=25)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Specialization:", width=12).grid(row=1, column=0, sticky=tk.W, pady=5, padx=5) # Added width and padx
        self.spec_entry = ttk.Entry(form_frame, width=25)
        self.spec_entry.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Contact:", width=12).grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)  # Added width and padx
        self.contact_entry = ttk.Entry(form_frame, width=25)
        self.contact_entry.grid(row=2, column=1, pady=5, padx=5)

        # Buttons with Size and Positioning
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Add", command=self.add_doctor, width=14).grid(row=0, column=0, padx=5, pady=5) # Added pady
        ttk.Button(btn_frame, text="Update", command=self.update_doctor, width=14).grid(row=0, column=1, padx=5, pady=5) # Added pady
        ttk.Button(btn_frame, text="Delete", command=self.delete_doctor, width=14).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form, width=14).grid(row=1, column=1, padx=5, pady=5)

        # Load initial data (you'll need to implement these methods)
        self.load_doctors()  # Placeholder
        self.tree.bind('<<TreeviewSelect>>', self.load_selected_doctor) # Placeholder

    def load_doctors(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        doctors = self.db.fetch_doctors()
        for doctor in doctors:
            str_doctor = tuple(str(value) for value in doctor)  # Convert to strings!
            self.tree.insert('', tk.END, values=str_doctor)

    def load_selected_doctor(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            if values:
                name = values[1] if len(values) > 1 else ""
                specialization = values[2] if len(values) > 2 else ""
                contact = values[3] if len(values) > 3 else ""

                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, name)
                self.spec_entry.delete(0, tk.END)
                self.spec_entry.insert(0, specialization)
                self.contact_entry.delete(0, tk.END)
                self.contact_entry.insert(0, contact)
            else:
                self.clear_form()

    def add_doctor(self):
        try:
            name = self.name_entry.get()
            specialization = self.spec_entry.get()
            contact = self.contact_entry.get()

            if not all([name, specialization, contact]):
                messagebox.showerror("Error", "All fields are required!")
                return

            self.db.execute_query(
                "INSERT INTO Doctors (Name, Specialization, Contact) VALUES (?, ?, ?)",
                (name, specialization, contact)
            )
            self.load_doctors()
            self.clear_form()
            messagebox.showinfo("Success", "Doctor added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_doctor(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a doctor to update!")
            return

        try:
            values = self.tree.item(selected, 'values')
            if not values or len(values) < 1:
                messagebox.showerror("Error", "No valid selection for update.")
                return

            doctor_id = int(values[0])  # Convert to integer IMMEDIATELY

            name = self.name_entry.get()
            specialization = self.spec_entry.get()
            contact = self.contact_entry.get()

            if not all([name, specialization, contact]):
                messagebox.showerror("Error", "All fields are required!")
                return

            self.db.execute_query(
                "UPDATE Doctors SET Name=?, Specialization=?, Contact=? WHERE DoctorID=?",
                (name, specialization, contact, doctor_id)
            )
            self.load_doctors()  # Reload Treeview
            messagebox.showinfo("Success", "Doctor updated successfully!")
            self.clear_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_doctor(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a doctor to delete!")
            return

        try:
            values = self.tree.item(selected, 'values')
            if not values or len(values) < 1:
                messagebox.showerror("Error", "No valid selection for delete.")
                return

            doctor_id = int(values[0])  # Convert to integer IMMEDIATELY

            if messagebox.askyesno("Confirm", "Are you sure you want to delete this doctor?"):
                self.db.execute_query("DELETE FROM Doctors WHERE DoctorID=?", (doctor_id,))
                self.load_doctors()  # Reload Treeview
                self.clear_form()
                messagebox.showinfo("Success", "Doctor deleted successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.spec_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)





#########################
# APPOINTMENT MANAGER
#########################

class AppointmentManager(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = Database()
        self.pack(fill=tk.BOTH, expand=True)

        # Configure style for dark theme
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.configure(background='#38475c')
        
        # Widget style configurations
        self.style.configure('TFrame', background='#38475c')
        self.style.configure('TLabel', background='#38475c', foreground='white', font=('Times New Roman', 11))
        self.style.configure('TButton',
                            font=('Arial', 10, 'bold'),
                            background='#1976D2',
                            foreground='white',
                            borderwidth=1,
                            focuscolor='#2e2e2e')
        self.style.map('TButton',
                       background=[('active', '#2a4e64'), ('pressed', '#6a6a6a')],
                       foreground=[('active', 'white')])
        self.style.configure('Treeview',
                            background='#38475c',
                            foreground='white',
                            fieldbackground='#38475c',
                            borderwidth=0)
        self.style.configure('Treeview.Heading',
                            font=('Times New Roman', 13),
                            padding=2,
                            background='#232c39',
                            foreground='white',
                            relief='flat')
        self.style.map('Treeview',
                       background=[('selected', '#2d6355')],
                       foreground=[('selected', 'white')])
        self.style.configure('TEntry',
                            fieldbackground='#e9e9e9',
                            foreground='black')
        self.style.configure('TCombobox',
                            fieldbackground='#e9e9e9',
                            foreground='black')

        # Main container
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview Frame
        tree_frame = ttk.Frame(self.main_frame)
        tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Form Frame
        form_frame = ttk.Frame(self.main_frame, width=300)
        form_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        # Treeview
        self.tree = ttk.Treeview(tree_frame, 
                               columns=('ID', 'Patient', 'Doctor', 'Date', 'Time'), 
                               show='headings')
        self.tree.heading('ID', text='Appointment ID')
        self.tree.heading('Patient', text='Patient')
        self.tree.heading('Doctor', text='Doctor')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Time', text='Time')
        self.tree.column('ID', width=100, anchor=tk.CENTER)
        self.tree.column('Patient', width=150, anchor=tk.CENTER)
        self.tree.column('Doctor', width=150, anchor=tk.CENTER)
        self.tree.column('Date', width=120, anchor=tk.CENTER)
        self.tree.column('Time', width=100, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)


        # Form Fields
        ttk.Label(form_frame, text="Patient:", width=12).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.patient_combobox = ttk.Combobox(form_frame, width=21)
        self.patient_combobox.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Doctor:", width=12).grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.doctor_combobox = ttk.Combobox(form_frame, width=21)
        self.doctor_combobox.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Date:", width=12).grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.date_entry = DateEntry(form_frame, width=20, date_pattern='yyyy-mm-dd',
                                  background='#38475c', foreground='white', bordercolor='#38475c')
        self.date_entry.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Time (hh:mm):", width=12).grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.time_entry = ttk.Entry(form_frame, width=23)
        self.time_entry.grid(row=3, column=1, pady=5, padx=5)

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Add", command=self.add_appointment, width=14).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="Update", command=self.update_appointment, width=14).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_appointment, width=14).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form, width=14).grid(row=1, column=1, padx=5, pady=5)

        # Load initial data
        self.load_appointments()
        self.load_combobox_data()
        self.tree.bind('<<TreeviewSelect>>', self.load_selected_appointment)

    def load_combobox_data(self):
        # Load patients
        patients = self.db.fetch_patients()
        patient_list = [f"{p[0]} - {p[1]}" for p in patients]
        self.patient_combobox['values'] = patient_list

        # Load doctors
        doctors = self.db.fetch_doctors()
        doctor_list = [f"{d[0]} - {d[1]}" for d in doctors]
        self.doctor_combobox['values'] = doctor_list

    def load_appointments(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        appointments = self.db.fetch_appointments()
        for appt in appointments:
            # Format the time here to HH:MM for display
            formatted_time = appt[4].strftime("%H:%M") if appt[4] else ""  # Handle potential None values

            # Create a new tuple with the formatted time
            display_appt = (appt[0], appt[1], appt[2], appt[3], formatted_time)

            str_appt = tuple(str(value) for value in display_appt)  # Convert to strings!
            self.tree.insert('', tk.END, values=str_appt)

    def load_selected_appointment(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            if values:
                patient = values[1] if len(values) > 1 else ""
                doctor = values[2] if len(values) > 2 else ""
                date = values[3] if len(values) > 3 else ""
                time = values[4] if len(values) > 4 else ""

                self.patient_combobox.set(patient)
                self.doctor_combobox.set(doctor)
                self.date_entry.set_date(date)  # Use set_date for DateEntry
                self.time_entry.delete(0, tk.END)
                self.time_entry.insert(0, time)
            else:
                self.clear_form()

    def add_appointment(self):
        try:
            patient_id = self.patient_combobox.get().split(' - ')[0]
            doctor_id = self.doctor_combobox.get().split(' - ')[0]
            date = self.date_entry.get_date()
            time = self.time_entry.get()

            if not all([patient_id, doctor_id, date, time]):
                messagebox.showerror("Error", "All fields are required!")
                return

            if not re.match(r'^\d{2}:\d{2}$', time):
                messagebox.showerror("Error", "Time must be in HH:MM format!")
                return

            self.db.execute_query(
                "INSERT INTO Appointments (PatientID, DoctorID, AppointmentDate, AppointmentTime) VALUES (?, ?, ?, ?)",
                (patient_id, doctor_id, date, time)
            )
            self.load_appointments()  # Reload Treeview
            self.clear_form()
            messagebox.showinfo("Success", "Appointment added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_appointment(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select an appointment to update!")
            return

        try:
            values = self.tree.item(selected, 'values')
            if not values or len(values) < 1:
                messagebox.showerror("Error", "No valid selection for update.")
                return

            appointment_id = int(values[0])

            patient_id = self.patient_combobox.get().split('(')[1].split(')')[0]
            doctor_id = self.doctor_combobox.get().split('(')[1].split(')')[0]
            date = self.date_entry.get_date()
            time = self.time_entry.get()

            if not date:  # Check if date is None
                messagebox.showerror("Error", "Date is required!")
                return

            if not time:  # Check if time is empty
                messagebox.showerror("Error", "Time is required!")
                return

            if not re.match(r'^\d{2}:\d{2}$', time):
                messagebox.showerror("Error", "Time must be in HH:MM format!")
                return


            self.db.execute_query(
                "UPDATE Appointments SET PatientID=?, DoctorID=?, AppointmentDate=?, AppointmentTime=? WHERE AppointmentID=?",
                (patient_id, doctor_id, date, time + ":00", appointment_id)  # Add seconds for SQL Server
            )
            self.load_appointments()
            self.clear_form()
            messagebox.showinfo("Success", "Appointment updated successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_appointment(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select an appointment to delete!")
            return

        try:
            values = self.tree.item(selected, 'values')
            if not values or len(values) < 1:
                messagebox.showerror("Error", "No valid selection for delete.")
                return

            appointment_id = int(values[0])  # Convert to integer IMMEDIATELY

            if messagebox.askyesno("Confirm", "Are you sure you want to delete this appointment?"):
                self.db.execute_query("DELETE FROM Appointments WHERE AppointmentID=?", (appointment_id,))
                self.load_appointments()  # Reload Treeview
                self.clear_form()
                messagebox.showinfo("Success", "Appointment deleted successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_form(self):
        self.patient_combobox.set('')
        self.doctor_combobox.set('')
        self.date_entry.set_date(None)
        self.time_entry.delete(0, tk.END)




########################
# PROSCRIPTION MANAGMENT
########################

class PrescriptionManager(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = Database()
        self.pack(fill=tk.BOTH, expand=True)

        # Configure style for dark theme
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.configure(background='#38475c')
        
        # Widget style configurations
        self.style.configure('TFrame', background='#38475c')
        self.style.configure('TLabel', background='#38475c', foreground='white', font=('Times New Roman', 11))
        self.style.configure('TButton',
                            font=('Arial', 10, 'bold'),
                            background='#1976D2',
                            foreground='white',
                            borderwidth=1,
                            focuscolor='#2e2e2e')
        self.style.map('TButton',
                       background=[('active', '#2a4e64'), ('pressed', '#6a6a6a')],
                       foreground=[('active', 'white')])
        self.style.configure('Treeview',
                            background='#38475c',
                            foreground='white',
                            fieldbackground='#38475c',
                            borderwidth=0)
        self.style.configure('Treeview.Heading',
                            font=('Times New Roman', 13),
                            padding=2,
                            background='#232c39',
                            foreground='white',
                            relief='flat')
        self.style.map('Treeview',
                       background=[('selected', '#2d6355')],
                       foreground=[('selected', 'white')])
        self.style.configure('TEntry',
                            fieldbackground='#e9e9e9',
                            foreground='black')
        self.style.configure('TCombobox',
                            fieldbackground='#e9e9e9',
                            foreground='black')

        # Main container
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview Frame
        tree_frame = ttk.Frame(self.main_frame)
        tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Form Frame
        form_frame = ttk.Frame(self.main_frame, width=300)
        form_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        # Treeview
        self.tree = ttk.Treeview(tree_frame, 
                               columns=('ID', 'Patient', 'Doctor', 'Diagnosis', 'Medication'), 
                               show='headings')
        self.tree.heading('ID', text='Prescription ID')
        self.tree.heading('Patient', text='Patient')
        self.tree.heading('Doctor', text='Doctor')
        self.tree.heading('Diagnosis', text='Diagnosis')
        self.tree.heading('Medication', text='Medication')
        self.tree.column('ID', width=150, anchor=tk.CENTER)
        self.tree.column('Patient', width=150, anchor=tk.CENTER)
        self.tree.column('Doctor', width=150, anchor=tk.CENTER)
        self.tree.column('Diagnosis', width=175, anchor=tk.CENTER)
        self.tree.column('Medication', width=175, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Form Fields
        ttk.Label(form_frame, text="Patient:", width=12).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.patient_combobox = ttk.Combobox(form_frame, width=21)
        self.patient_combobox.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Doctor:", width=12).grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.doctor_combobox = ttk.Combobox(form_frame, width=21)
        self.doctor_combobox.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Diagnosis:", width=12).grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.diagnosis_entry = ttk.Entry(form_frame, width=23)
        self.diagnosis_entry.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Medication:", width=12).grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.medication_entry = ttk.Entry(form_frame, width=23)
        self.medication_entry.grid(row=3, column=1, pady=5, padx=5)

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Add", command=self.add_prescription, width=14).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="Update", command=self.update_prescription, width=14).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_prescription, width=14).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form, width=14).grid(row=1, column=1, padx=5, pady=5)

        # Load initial data
        self.load_prescriptions()
        self.load_combobox_data()
        self.tree.bind('<<TreeviewSelect>>', self.load_selected_prescription)

    def load_combobox_data(self):
        # Load patients
        patients = self.db.fetch_patients()
        self.patient_combobox['values'] = [f"{p[1]} ({p[0]})" for p in patients]  # Name (ID) format

        # Load doctors
        doctors = self.db.fetch_doctors()
        self.doctor_combobox['values'] = [f"{d[1]} ({d[0]})" for d in doctors]  # Name (ID) format

    def load_prescriptions(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        prescriptions = self.db.fetch_prescriptions()
        for pres in prescriptions:
            str_pres = tuple(str(value) for value in pres)  # Convert to strings!
            self.tree.insert('', tk.END, values=str_pres)

    def load_selected_prescription(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            if values:
                patient = values[1] if len(values) > 1 else ""
                doctor = values[2] if len(values) > 2 else ""
                diagnosis = values[3] if len(values) > 3 else ""
                medication = values[4] if len(values) > 4 else ""

                self.patient_combobox.set(patient)
                self.doctor_combobox.set(doctor)
                self.diagnosis_entry.delete(0, tk.END)
                self.diagnosis_entry.insert(0, diagnosis)
                self.medication_entry.delete(0, tk.END)
                self.medication_entry.insert(0, medication)
            else:
                self.clear_form()

    def add_prescription(self):
        try:
            patient_str = self.patient_combobox.get()
            doctor_str = self.doctor_combobox.get()

            if not patient_str or not doctor_str:  # Check if comboboxes are empty
                messagebox.showerror("Error", "Please select a patient and a doctor.")
                return

            try:
                patient_id = int(patient_str.split('(')[1].split(')')[0])
                doctor_id = int(doctor_str.split('(')[1].split(')')[0])
            except (IndexError, ValueError):
                messagebox.showerror("Error", "Invalid patient or doctor selection.")
                return


            diagnosis = self.diagnosis_entry.get()
            medication = self.medication_entry.get()

            if not all([diagnosis, medication]):  # Check if diagnosis and medication are empty
                messagebox.showerror("Error", "Diagnosis and Medication fields are required!")
                return


            self.db.execute_query(
                "INSERT INTO Prescriptions (PatientID, DoctorID, Diagnosis, Medication) VALUES (?, ?, ?, ?)",
                (patient_id, doctor_id, diagnosis, medication)
            )
            self.load_prescriptions()
            self.clear_form()
            messagebox.showinfo("Success", "Prescription added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding prescription: {e}")

    def update_prescription(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a prescription to update!")
            return

        try:
            values = self.tree.item(selected, 'values')
            if not values or len(values) < 1:
                messagebox.showerror("Error", "No valid selection for update.")
                return

            prescription_id = int(values[0])

            patient_str = self.patient_combobox.get()
            doctor_str = self.doctor_combobox.get()

            if not patient_str or not doctor_str:  # Check if comboboxes are empty
                messagebox.showerror("Error", "Please select a patient and a doctor.")
                return

            try:
                patient_id = int(patient_str.split('(')[1].split(')')[0])
                doctor_id = int(doctor_str.split('(')[1].split(')')[0])
            except (IndexError, ValueError):
                messagebox.showerror("Error", "Invalid patient or doctor selection.")
                return

            diagnosis = self.diagnosis_entry.get()
            medication = self.medication_entry.get()

            if not all([diagnosis, medication]):  # Check if diagnosis and medication are empty
                messagebox.showerror("Error", "Diagnosis and Medication fields are required!")
                return

            self.db.execute_query(
                "UPDATE Prescriptions SET PatientID=?, DoctorID=?, Diagnosis=?, Medication=? WHERE PrescriptionID=?",
                (patient_id, doctor_id, diagnosis, medication, prescription_id)
            )
            self.load_prescriptions()
            self.clear_form()
            messagebox.showinfo("Success", "Prescription updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating prescription: {e}")

    def delete_prescription(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a prescription to delete!")
            return

        try:
            values = self.tree.item(selected, 'values')
            if not values or len(values) < 1:
                messagebox.showerror("Error", "No valid selection for delete.")
                return

            prescription_id = int(values[0])  # Convert to integer IMMEDIATELY

            if messagebox.askyesno("Confirm", "Are you sure you want to delete this prescription?"):
                self.db.execute_query("DELETE FROM Prescriptions WHERE PrescriptionID=?", (prescription_id,))
                self.load_prescriptions()  # Reload Treeview
                self.clear_form()
                messagebox.showinfo("Success", "Prescription deleted successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_form(self):
        self.patient_combobox.set('')
        self.doctor_combobox.set('')
        self.diagnosis_entry.delete(0, tk.END)
        self.medication_entry.delete(0, tk.END)





#####################
# MEDICINS MANAGMENT
#####################

class MedicineManager(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = Database()
        self.pack(fill=tk.BOTH, expand=True)

        # Configure style for dark theme
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.configure(background='#38475c')
        
        # Widget style configurations
        self.style.configure('TFrame', background='#38475c')
        self.style.configure('TLabel', background='#38475c', foreground='white', font=('Times New Roman', 11))
        self.style.configure('TButton',
                            font=('Arial', 10, 'bold'),
                            background='#1976D2',
                            foreground='white',
                            borderwidth=1,
                            focuscolor='#2e2e2e')
        self.style.map('TButton',
                       background=[('active', '#2a4e64'), ('pressed', '#6a6a6a')],
                       foreground=[('active', 'white')])
        self.style.configure('Treeview',
                            background='#38475c',
                            foreground='white',
                            fieldbackground='#38475c',
                            borderwidth=0)
        self.style.configure('Treeview.Heading',
                            font=('Times New Roman', 13),
                            padding=2,
                            background='#232c39',
                            foreground='white',
                            relief='flat')
        self.style.map('Treeview',
                       background=[('selected', '#2d6355')],
                       foreground=[('selected', 'white')])
        self.style.configure('TEntry',
                            fieldbackground='#e9e9e9',
                            foreground='black')

        # Main container
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview Frame
        tree_frame = ttk.Frame(self.main_frame)
        tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Form Frame
        form_frame = ttk.Frame(self.main_frame, width=300)
        form_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        # Treeview
        self.tree = ttk.Treeview(tree_frame, 
                               columns=('ID', 'Name', 'Quantity', 'Price'), 
                               show='headings')
        self.tree.heading('ID', text='Medicine ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Quantity', text='Quantity')
        self.tree.heading('Price', text='Price')
        self.tree.column('ID', width=80, anchor=tk.CENTER)
        self.tree.column('Name', width=150, anchor=tk.CENTER)
        self.tree.column('Quantity', width=100, anchor=tk.CENTER)
        self.tree.column('Price', width=100, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)


        # Form Fields
        ttk.Label(form_frame, text="Drug Name:", width=12).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.name_entry = ttk.Entry(form_frame, width=23)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Dose:", width=12).grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.quantity_entry = ttk.Entry(form_frame, width=23)
        self.quantity_entry.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Price:", width=12).grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.price_entry = ttk.Entry(form_frame, width=23)
        self.price_entry.grid(row=2, column=1, pady=5, padx=5)

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Add", command=self.add_medicine, width=14).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="Update", command=self.update_medicine, width=14).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_medicine, width=14).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form, width=14).grid(row=1, column=1, padx=5, pady=5)

        # Load initial data
        self.load_medicines()
        self.tree.bind('<<TreeviewSelect>>', self.load_selected_medicine)

    def load_medicines(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        medicines = self.db.fetch_medicines()
        for medicine in medicines:
            str_medicine = tuple(str(value) for value in medicine)  # Convert to strings!
            self.tree.insert('', tk.END, values=str_medicine)

    def load_selected_medicine(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            if values:
                name = values[1] if len(values) > 1 else ""
                quantity = values[2] if len(values) > 2 else ""
                price = values[3] if len(values) > 3 else ""

                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, name)
                self.quantity_entry.delete(0, tk.END)
                self.quantity_entry.insert(0, quantity)
                self.price_entry.delete(0, tk.END)
                self.price_entry.insert(0, price)
            else:
                self.clear_form()

    def add_medicine(self):
        try:
            name = self.name_entry.get()
            quantity = int(self.quantity_entry.get())  # Convert to int!
            price = float(self.price_entry.get())  # Convert to float!

            if not all([name, quantity >= 0, price >= 0]):
                messagebox.showerror("Error", "All fields are required with valid values!")
                return

            self.db.execute_query(
                "INSERT INTO Medicines (Name, Quantity, Price) VALUES (?, ?, ?)",
                (name, quantity, price)
            )
            self.load_medicines()  # Reload Treeview
            self.clear_form()
            messagebox.showinfo("Success", "Medicine added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer and Price must be a number!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_medicine(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a medicine to update!")
            return

        try:
            values = self.tree.item(selected, 'values')
            if not values or len(values) < 1:
                messagebox.showerror("Error", "No valid selection for update.")
                return

            medicine_id = int(values[0])  # Convert to integer IMMEDIATELY

            name = self.name_entry.get()
            quantity = int(self.quantity_entry.get())  # Convert to int!
            price = float(self.price_entry.get())  # Convert to float!

            self.db.execute_query(
                "UPDATE Medicines SET Name=?, Quantity=?, Price=? WHERE MedicineID=?",
                (name, quantity, price, medicine_id)
            )
            self.load_medicines()  # Reload Treeview
            messagebox.showinfo("Success", "Medicine updated successfully!")
            self.clear_form()

        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer and Price must be a number!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_medicine(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a medicine to delete!")
            return

        try:
            values = self.tree.item(selected, 'values')
            if not values or len(values) < 1:
                messagebox.showerror("Error", "No valid selection for delete.")
                return

            medicine_id = int(values[0])  # Convert to integer IMMEDIATELY

            if messagebox.askyesno("Confirm", "Are you sure you want to delete this medicine?"):
                self.db.execute_query("DELETE FROM Medicines WHERE MedicineID=?", (medicine_id,))
                self.load_medicines()  # Reload Treeview
                self.clear_form()
                messagebox.showinfo("Success", "Medicine deleted successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)







########################
# BILL MANAGMENT
########################

class BillManager(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = Database()
        self.pack(fill=tk.BOTH, expand=True)

        # Configure style for dark theme
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.configure(background='#38475c')
        
        # Widget style configurations
        self.style.configure('TFrame', background='#38475c')
        self.style.configure('TLabel', background='#38475c', foreground='white', font=('Times New Roman', 11))
        self.style.configure('TButton',
                            font=('Arial', 10, 'bold'),
                            background='#1976D2',
                            foreground='white',
                            borderwidth=1,
                            focuscolor='#2e2e2e')
        self.style.map('TButton',
                       background=[('active', '#2a4e64'), ('pressed', '#6a6a6a')],
                       foreground=[('active', 'white')])
        self.style.configure('Treeview',
                            background='#38475c',
                            foreground='white',
                            fieldbackground='#38475c',
                            borderwidth=0)
        self.style.configure('Treeview.Heading',
                            font=('Times New Roman', 13),
                            padding=2,
                            background='#232c39',
                            foreground='white',
                            relief='flat')
        self.style.map('Treeview',
                       background=[('selected', '#2d6355')],
                       foreground=[('selected', 'white')])
        self.style.configure('TEntry',
                            fieldbackground='#e9e9e9',
                            foreground='black')
        self.style.configure('TCombobox',
                            fieldbackground='#e9e9e9',
                            foreground='black')

        # Main container
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview Frame
        tree_frame = ttk.Frame(self.main_frame)
        tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Form Frame
        form_frame = ttk.Frame(self.main_frame, width=300)
        form_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        # Treeview
        self.tree = ttk.Treeview(tree_frame, 
                               columns=('ID', 'Patient', 'Amount', 'Date', 'Status'), 
                               show='headings')
        self.tree.heading('ID', text='Bill ID')
        self.tree.heading('Patient', text='Patient')
        self.tree.heading('Amount', text='Amount')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Status', text='Status')
        self.tree.column('ID', width=80, anchor=tk.CENTER)
        self.tree.column('Patient', width=150, anchor=tk.CENTER)
        self.tree.column('Amount', width=100, anchor=tk.CENTER)
        self.tree.column('Date', width=100, anchor=tk.CENTER)
        self.tree.column('Status', width=100, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Form Fields
        ttk.Label(form_frame, text="Patient:", width=12).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.patient_combobox = ttk.Combobox(form_frame, width=21)
        self.patient_combobox.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Amount:", width=12).grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.amount_entry = ttk.Entry(form_frame, width=23)
        self.amount_entry.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Date:", width=12).grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.date_entry = DateEntry(form_frame, width=20, date_pattern='yyyy-mm-dd',
                                   background='#38475c', foreground='white', bordercolor='#38475c')
        self.date_entry.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Status:", width=12).grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.status_combobox = ttk.Combobox(form_frame, values=['Pending', 'Resolved'], width=19)
        self.status_combobox.grid(row=3, column=1, pady=5, padx=5)
        self.status_combobox.set('Pending')

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Add", command=self.add_bill, width=14).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="Update", command=self.update_bill, width=14).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_bill, width=14).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form, width=14).grid(row=1, column=1, padx=5, pady=5)

        # Load initial data
        self.load_bills()
        self.load_patient_combobox()
        self.tree.bind('<<TreeviewSelect>>', self.load_selected_bill)

    def load_patient_combobox(self):
        patients = self.db.fetch_patients()
        self.patient_combobox['values'] = [f"{p[1]} ({p[0]})" for p in patients]  # Name (ID) format


    def load_bills(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        bills = self.db.fetch_bills()
        for bill in bills:
            str_bill = tuple(str(value) for value in bill)  # Convert to strings!
            self.tree.insert('', tk.END, values=str_bill)

    def load_selected_bill(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            if values:
                patient = values[1] if len(values) > 1 else ""
                amount = values[2] if len(values) > 2 else ""
                date = values[3] if len(values) > 3 else ""
                status = values[4] if len(values) > 4 else ""

                self.patient_combobox.set(patient)
                self.amount_entry.delete(0, tk.END)
                self.amount_entry.insert(0, amount)
                self.date_entry.set_date(date)
                self.status_combobox.set(status)
            else:
                self.clear_form()

    def add_bill(self):
        try:
            patient_str = self.patient_combobox.get()
            if not patient_str:
                messagebox.showerror("Error", "Please select a patient.")
                return

            try:
                patient_id = int(patient_str.split('(')[1].split(')')[0])
            except (IndexError, ValueError):
                messagebox.showerror("Error", "Invalid patient selection.")
                return

            try:
                amount = float(self.amount_entry.get())
                if amount <= 0:
                    raise ValueError("Amount must be positive.")
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid amount: {e}")
                return

            date = self.date_entry.get_date()
            status = self.status_combobox.get()

            if not all([date, status]):  # Check if date and status are empty
                messagebox.showerror("Error", "Date and Status fields are required!")
                return


            self.db.execute_query(
                "INSERT INTO Bills (PatientID, Amount, BillDate, Status) VALUES (?, ?, ?, ?)",
                (patient_id, amount, date, status)
            )
            self.load_bills()
            self.clear_form()
            messagebox.showinfo("Success", "Bill added successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Error adding bill: {e}")

    def update_bill(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a bill to update!")
            return

        try:
            values = self.tree.item(selected, 'values')
            if not values or len(values) < 1:
                messagebox.showerror("Error", "No valid selection for update.")
                return

            bill_id = int(values[0])

            patient_str = self.patient_combobox.get()
            if not patient_str:
                messagebox.showerror("Error", "Please select a patient.")
                return

            try:
                patient_id = int(patient_str.split('(')[1].split(')')[0])
            except (IndexError, ValueError):
                messagebox.showerror("Error", "Invalid patient selection.")
                return

            try:
                amount = float(self.amount_entry.get())
                if amount <= 0:
                    raise ValueError("Amount must be positive.")
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid amount: {e}")
                return

            date = self.date_entry.get_date()
            status = self.status_combobox.get()

            if not all([date, status]):  # Check if date and status are empty
                messagebox.showerror("Error", "Date and Status fields are required!")
                return

            self.db.execute_query(
                "UPDATE Bills SET PatientID=?, Amount=?, BillDate=?, Status=? WHERE BillID=?",
                (patient_id, amount, date, status, bill_id)
            )
            self.load_bills()
            self.clear_form()
            messagebox.showinfo("Success", "Bill updated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Error updating bill: {e}")

    def delete_bill(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a bill to delete!")
            return

        try:
            values = self.tree.item(selected, 'values')
            if not values or len(values) < 1:
                messagebox.showerror("Error", "No valid selection for delete.")
                return

            bill_id = int(values[0])  # Convert to integer IMMEDIATELY

            if messagebox.askyesno("Confirm", "Are you sure you want to delete this bill?"):
                self.db.execute_query("DELETE FROM Bills WHERE BillID=?", (bill_id,))
                self.load_bills()  # Reload Treeview
                self.clear_form()
                messagebox.showinfo("Success", "Bill deleted successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_form(self):
        self.patient_combobox.set('')
        self.amount_entry.delete(0, tk.END)
        self.date_entry.set_date(None)
        self.status_combobox.set('Pending')






if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1350x600")
    app = HospitalManagementSystem(root)
    root.mainloop()
