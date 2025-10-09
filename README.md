# PyTasks - Django Task Manager
PyTasks is a **clean, minimalist task management web application** built with Django. Organize your tasks with categories, priorities, and due dates in a simple, intuitive interface.

## Features
- **Task Management** - Create, edit, delete, and mark tasks as complete
- **Category Organization** - Organize tasks into custom categories
- **Smart Defaults** - Automatic "General" category creation for new users, ensuring you can add tasks immediately
- **Priority System** - Set priorities (Critical, High, Normal, Low) with filtering
- **Smart Search** - Search tasks by title and description
- **Archives** - Review completed tasks with permanent deletion options
- **User Authentication** - Secure signup and login system
- **Due Date Validation** - Prevents past due dates with form validation

## Technologies
- **Backend:** Django Python Framework
- **Database:** MySQL
- **Authentication:** Django's built-in auth system
- **Frontend:** HTML5, Bootstrap 5, Custom CSS, JavaScript

<hr>

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone https://github.com/souviksn91/pycontacts.git
   cd pycontacts
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database:**
    Create MySQL database (see DATABASE.md)

5. **Run the app:**
   ```bash
   python app.py
   ```
6. **Access in browser:**
   http://127.0.0.1:5000/
   