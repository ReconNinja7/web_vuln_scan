#  Web Application Vulnerability Scanner

##  Overview
This project is a **basic web application vulnerability scanner** built with Python and Flask.  
It crawls target websites, finds forms, and tests them for **XSS, SQL Injection, and CSRF vulnerabilities**.  
Findings are stored in a SQLite database and displayed in a web interface.

⚠ **Disclaimer:** This tool is for educational purposes only.  
Do **not** use it on websites you don’t own or have explicit permission to test.

---

## Tools & Technologies
- Python 3
- Flask
- Requests
- BeautifulSoup
- SQLite

---

##  How to Run

1. Clone this repo:
   ```bash
   git clone https://github.com/YOUR-USERNAME/web-vuln-scanner.git
   cd web-vuln-scanner


2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate   # (Linux/Mac)
   venv\Scripts\activate      # (Windows)

   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python app.py
   ```

4. Open in your browser:

   ```
   http://127.0.0.1:5050
   ```

---

##  Project Report

A detailed **2-page PDF report** is included:
 [Web\_Application\_Vulnerability\_Scanner\_Report.pdf](Web_Application_Vulnerability_Scanner_Report.pdf)

---

## Future Improvements

* Add detection for more vulnerabilities (File Upload, Open Redirects, Command Injection).
* Export results to PDF/CSV.
* Multi-threaded scanning for faster results.
* Authentication support to scan protected pages.

---

 **Author:** Mohammad Farhan Hussain
 **Date:** September 2025

```
 

Do you also want me to give you the **.gitignore content** in the same way (so you can copy–paste that too)?
```
