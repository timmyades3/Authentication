# Yetti-Technolgies-Backend-Assessment

## View live
 
 https://authentication-bhoe.onrender.com

## Local Development Setup

Follow these steps to set up and run the Django app locally after cloning it from GitHub:

### 1. Clone the Repository

Clone the GitHub repository to your local machine using the following command:

```bash
git clone https://github.com/timmyades3/Yetti-Technolgies-Backend-Assessment.git
```

### 2. Create a Virtual Environment

Navigate to the project directory and create a virtual environment:

```bash
cd your-django-app
python -m venv venv
```

### 3. Activate the Virtual Environment

Activate the virtual environment:

**On Windows:**

```bash
venv\Scripts\activate
```

**On macOS and Linux:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

change the `.envexample` file in the project root  to `.env`, it contains necessary environment variables. You can usually find these settings in your project's `settings.py` file.



### 6. Apply Database Migrations

Apply the database migrations to create the database schema:

```bash
python manage.py migrate
```

### 7. Create a Superuser (Optional)

If your app has user authentication and you want to create an admin user, run:

```bash
python manage.py createsuperuser
```

### 8. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The server should be accessible at `http://localhost:8000/` in your web browser.

## Basic Register, Login, and Logout

### Register

1. Open your web browser and go to `http://localhost:8000/Register/` to access the register page.
2. Fill out the Register form with the required information, such as username, email, and password.
3. Click the "Register" button to create a new user account.

### Login

1. Open your web browser and go to `http://localhost:8000/login/` to access the login page.
2. Enter your username and password in the login form.
3. Click the "Login" button to log in to your user account.

### Logout

1. If you are logged in, you will be redirected to a hello world page where you can log out by clicking on the logout button by going to `http://localhost:8000`.
2. Click the "Logout" button to log out from your user account.

## Running Tests 

To run tests, follow these steps:

### 1. Run Tests

Use the following command to run tests:

```bash
python manage.py test
```


That's it! You should now have your Django app up and running locally, and you can run tests.


