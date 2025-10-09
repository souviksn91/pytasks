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



### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/pytasks.git
   cd pytasks
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```


### Database Setup

1. **Create MySQL database and user**
   ```sql
   CREATE DATABASE pytasks;
   CREATE USER 'pytasks_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON pytasks.* TO 'pytasks_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual database credentials
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

### Run the Application
   ```bash
   python manage.py runserver
   ```



