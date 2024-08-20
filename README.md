# RECAP: Reviewing Evidence and Categorizing All Procedures

## Overview

**RECAP** is a centralized database application designed to assist employees of the NYPD Compliance Section in efficiently categorizing TRI records. Built with Flask, Python, JavaScript, and SQLite for the backend, and HTML, CSS, and the Bootstrap framework for the front end, RECAP provides a user-friendly interface to streamline the categorization process and ensure accurate record-keeping.

## Features

* **Centralized Database:** Easily manage and categorize TRI records.
* **User-Friendly Interface:** Accessible and intuitive UI built with Bootstrap.
* **Secure Data Handling:** Ensures compliance with NYPD data protection policies.
* **Customizable Reports:** Generate and export categorized data for further analysis.

## Installation

### Prerequisites

* Python 3.x
* Virtual environment setup (optional but recommended)
* Required Python Libraries:

  ```
  altgraph==0.17.4
  Babel==2.15.0
  customtkinter==5.2.2
  darkdetect==0.8.0
  et-xmlfile==1.1.0
  lxml==5.2.2
  numpy==2.0.1
  openpyxl==3.1.5
  packaging==24.1
  pandas==2.2.2
  pefile==2023.2.7
  pillow==10.4.0
  pyinstaller==6.9.0
  pyinstaller-hooks-contrib==2024.7
  python-dateutil==2.9.0.post0
  python-pptx==0.6.23
  pytz==2024.1
  pywin32-ctypes==0.2.2
  six==1.16.0
  tkcalendar==1.6.1
  tzdata==2024.1
  xlsx2csv==0.8.3
  XlsxWriter==3.2.0

  ```

### Setup

---

1. **Install Python 3.x** : Ensure Python 3.x is installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).
2. **Use install_venv.bat:** Run the script to set up the virtual environment automatically.
3. **If there are any issues with the script, follow these steps:**

   1. **Install venv (virtual environment) using Pip:**
      `pip install venv`
   2. **Create and setup the virtual environment:** In the directory, open the terminal and do the following:
      1. **Create** a venv folder:
         `python -m venv venv`
      2. **Open** the venv in powershell:
         `.\venv\Scripts\Activate.ps1`
      3. If there are any **issues** with running scripts being disabled. Use the following command:
         `Set-ExecutionPolicy Unrestricted -Scope Process`
      4. **Install** required libraries: Open a terminal and run the following to install the libraries needed for the program:
         `pip install -r requirements.txt`
4. **Ensure file structure:** Ensure your working directory has the following structure:

### Building the Executable (Windows)

RECAP can be packaged as a standalone executable using `pyinstaller`. A batch file (`make.bat`) has been provided for convenience:

1. **Run the Batch File:**
   `make.bat`

   This will generate a single executable file with the RECAP icon and splash screen.

## Directory Structure

```
.
├── README.md
├── app.py
├── columns.txt
├── database
│   └── bwcDB.db
├── install_venv.bat
├── make.bat
├── make_config.json
├── requirements.txt
├── setup.ipynb
├── setup.py
├── src
│   ├── manage.py
│   └── sqliteObjects.py
├── static
│   ├── PSDLogo.png
│   ├── favicon.ico
│   ├── hardcut.py
│   ├── main.css
│   └── manifest.json
├── templates
│   ├── base.html
│   ├── entry.html
│   ├── manage.html
│   └── review.html
└── venv_pwsh.bat
```

## Usage

1. **Create the database**:
   Use the setup.py or setup.ipynb file to create the database. It will create a database folder and store 'bwcDB.db' in it. This database folder is **needed** in the same directory as the executable in order for it to work.
2. **Accessing the Application:**
   Double click the executable in the dist folder. Once the application is running, it will open up a dedicated browser window.
3. **Categorize TRI Records:**
   Start using the provided forms to categorize and review TRI records.

## Contribution

Contributions to RECAP are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE]() file for details.
