# Django Budget Tracker

A personal finance management web application built with Django.  
The application allows users to track income and expenses, manage categories, visualize financial data, and export records.

---

## Features

- User authentication (register, login, logout)
- Password reset via console (development-friendly)
- Create, edit and delete transactions (income & expenses)
- Category management with protection against accidental deletion
- Dashboard overview with total income and expenses
- Interactive charts (income vs. expenses, category breakdown)
- CSV export of transactions
- Pagination for large datasets
- Form validation and clear error handling
- Fully tested models and views

---

## Tech Stack

- **Backend:** Django
- **Database:** SQLite (default)
- **Frontend:** HTML, CSS, Bootstrap 5
- **Charts:** Plotly
- **Authentication:** Django Auth
- **Testing:** Django Test Framework

---

## Project Structure

## Setup & Installation

### Clone the repository

```
  git clone https://github.com/your-username/django-budget-tracker.git
  cd django-budget-tracker
```

### Create & activate a virtual environment

```
   python -m venv env
```

#### Activation:

Windows: `env\Scripts\activate`

macOS / Linux: `source env/bin/activate`

### Install dependencies

```
   pip install -r requirements.txt
```

### Environment variables

Create a `.env` file in the project root and define the following variables:

`SECRET_KEY = your-secret-key`

`DEBUG=True`

### Run migrotions

```
    python manage.py migrate
```

### Start the development server

```
   python manage.py runserver
```

### Open the application in your browser:

http://127.0.0.1:8000/

---

## Licence

MIT
