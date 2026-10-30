# QRAI BloodBank - QR-Based AI Blood Bank Management System

A Flask-based Blood Bank Management System with QR code tracking and AI compatibility.

## 🚀 Features
- Donor & Receiver Management
- Blood Stock Management (A+, A-, B+, B-, AB+, AB-, O+, O-)
- QR Code Generation for each blood bag (for tracking)
- Secure Login System
- Dashboard with live stock

## 🛠️ Tech Stack
- Python Flask
- SQLite (bloodbank.db)
- HTML, CSS, Bootstrap
- QRCode Library

## 📂 Project Structure
- app.py - Main Flask application
- templates/ - HTML files
- static/qrs/ - Generated QR Codes
- bloodbank.db - Database

## ▶️ How to Run Locally
```bash
pip install flask qrcode
python app.py
