
-- Create the database
CREATE DATABASE HospitalDB;
GO

-- Use the created database
USE HospitalDB;
GO

-- Patients table
CREATE TABLE Patients (
    PatientID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100) NOT NULL,
    Age INT,
    Gender NVARCHAR(10),
    Contact NVARCHAR(20)
);
GO

-- Doctors table
CREATE TABLE Doctors (
    DoctorID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100) NOT NULL,
    Specialization NVARCHAR(100),
    Contact NVARCHAR(20)
);
GO

-- Appointments table
CREATE TABLE Appointments (
    AppointmentID INT PRIMARY KEY IDENTITY(1,1),
    PatientID INT FOREIGN KEY REFERENCES Patients(PatientID) ON DELETE CASCADE,
    DoctorID INT FOREIGN KEY REFERENCES Doctors(DoctorID) ON DELETE CASCADE,
    AppointmentDate DATE,
    AppointmentTime TIME
);
GO

-- Prescriptions table
CREATE TABLE Prescriptions (
    PrescriptionID INT PRIMARY KEY IDENTITY(1,1),
    PatientID INT FOREIGN KEY REFERENCES Patients(PatientID) ON DELETE CASCADE,
    DoctorID INT FOREIGN KEY REFERENCES Doctors(DoctorID) ON DELETE CASCADE,
    Diagnosis NVARCHAR(200),
    Medication NVARCHAR(200)
);
GO

-- Bills table
CREATE TABLE Bills (
    BillID INT PRIMARY KEY IDENTITY(1,1),
    PatientID INT FOREIGN KEY REFERENCES Patients(PatientID) ON DELETE CASCADE,
    Amount DECIMAL(10,2),
    BillDate DATE DEFAULT GETDATE(),
    Status NVARCHAR(20) DEFAULT 'Pending'
);
GO

-- Medicines table
CREATE TABLE Medicines (
    MedicineID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100) NOT NULL,
    Quantity INT,
    Price DECIMAL(10,2)
);
GO

