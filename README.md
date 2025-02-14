# 🏥 **Hospital Management System**

This project is a **Hospital Management System** designed to manage various hospital functions including patient records, doctor profiles, appointments, prescriptions, medications, and bills. The system features a clean and intuitive **dark-themed** user interface built using **Tkinter** and Python, enabling easy management of hospital data.

---

## 🚀 **Features**

### 1. **Patient Management** 👩‍⚕️👨‍⚕️
- Add, update, and manage patient information such as **name**, **age**, **gender**, and **contact details**.
- View all patient records in a simple table format.
  <br> <br>

  ![image1](https://github.com/YasinShamsedini/HospitalManagementSystem/blob/main/images/patientshospital.JPG)

### 2. **Doctor Management** 🩺
- Manage doctor profiles including **name**, **specialization**, and **contact information**.
- Easily filter doctors based on their specialization.
  <br> <br>

  ![image1](https://github.com/YasinShamsedini/HospitalManagementSystem/blob/main/images/doctorshospital.JPG)
  
### 3. **Appointment Management** 🗓️
- Schedule and manage patient appointments with doctors.
- View a list of appointments, including **doctor**, **patient**, **date**, and **time**.

### 4. **Prescription Management** 📝
- Specify **diagnosis** and **prescribed medications** for patients.
- Manage patient prescriptions with ease.

### 5. **Bill Management** 🧾
- Generate and manage bills for patients.
- Calculate total bill amounts based on **services rendered**, **appointments**, and **medications**.
- View and update **payment status** for each bill.

### 6. **Medicine Management** 💊
- Keep track of available medicines, including **quantity**, **price**, and **medication details**.
- Add and remove medicines as necessary.
  <br> <br>

  ![image1](https://github.com/YasinShamsedini/HospitalManagementSystem/blob/main/images/doctorshospital.JPG)


## 🖥️ **User Interface & Design**

- The system uses a **dark theme** suitable for a hospital environment, reducing strain on the eyes.
- The main screen features a **left-side dashboard** for easy navigation between sections like Patients, Doctors, Appointments, Prescriptions, Medicines, and Bills.
- A **custom Tkinter GUI** provides a modern, clean, and intuitive interface for users.
- The interface includes **combo boxes** linked to the database for easy access to data such as doctor and patient information.



## 💡 **Strengths**

- **Modular Design**: Each entity (patients, doctors, appointments, etc.) has its own dedicated section, which ensures ease of use and maintainability.
- **CRUD Functionality**: Complete **Create**, **Read**, **Update**, and **Delete** (CRUD) operations for managing data in all sections.
- **Database Integration**: The system is connected to a **SQL Server** database using **PyODBC**, ensuring smooth data handling and storage.
- **Search & Filter**: Combo boxes and search functionality make it easy to filter and find specific data (e.g., doctors, patients).
- **Responsive Layout**: The GUI layout automatically adapts to window resizing, providing a responsive design.



## ⚠️ **Weaknesses**

While this system is well-suited for smaller hospitals or clinics, it may not scale effectively for **larger hospitals** due to the following limitations:

- **Billing System**: The current billing system does not handle complex billing scenarios (e.g., service-based billing, segmented charges for departments). Larger hospitals may require more granular billing features.
- **Medication Management**: The medication system lacks advanced search functionality for large inventories. A search bar or categorization by **medicine type** could improve efficiency.
- **Doctor Shift Scheduling**: Currently, the system displays all doctors, which may not be suitable for large-scale operations. Implementing a shift-based doctor selection system could be beneficial for bigger hospitals.
- **Extended Features**: More advanced features like **patient history**, **appointments by department**, or **automatic reminders** could be added to improve usability.



## 🔧 **Technologies Used**

- **Python**
- **Tkinter**
- **PyODBC**
- **SQL Server**
- **PIL (Pillow)**



## 📂 **Installation**

To get the project up and running on your local machine, follow the steps that mentioned in docs > setup.md


   This will launch the Hospital Management System with a Tkinter-based GUI.



## 🔧 **Troubleshooting**

If you run into issues while using the application, here are some common troubleshooting steps:

- **Database Connection Issues**: Double-check the database connection string in the `database.py` file. Ensure the server and database credentials are correct.
- **SQL Server**: Make sure that your **SQL Server instance** is running and accessible.
- **Image Path**: If you're getting an error related to missing images, ensure the `image_path` in the code points to the correct location of the image file on your system.



## 📝 **License**

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.



## 🙏 **Acknowledgements**

- Special thanks to my parents, who work in the healthcare industry, for testing the system and providing valuable feedback.
- The project benefited from AI-powered suggestions that enhanced the functionality and design.
  
---

##  **Enjoy using the Software!**

Feel free to explore the project, contribute, and share your feedback. If you have any questions or suggestions, feel free to open an issue or a pull request.
