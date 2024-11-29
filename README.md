# Form Submission and Management System

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [User Dashboard](#user-dashboard)
6. [Form Customization](#form-customization)
7. [Subscription Management](#subscription-management)
8. [Security](#security)
9. [API Endpoints](#api-endpoints)
10. [Contributing](#contributing)
11. [License](#license)


## Project Overview

This Django-based web application allows users to create customizable form submission pages and manage the submitted data. It is designed for businesses or individuals who need to collect and manage sensitive information securely.

---

## Features

- User registration and authentication
- Customizable public form pages for data submission
- User dashboard for managing form submissions
- Form template customization
- Subscription-based access control
- Secure handling of sensitive information
- Notification system for new submissions
- Pagination and search functionality for form entries
- Edit and delete capabilities for form submissions
- Responsive design for mobile and desktop use

---

## Installation

### Step 1: Clone the Repository

To clone the `Beta-Form` branch of the repository, run the following command:

```bash
git clone --branch Beta-Form https://github.com/brandnova/Pulling-Form.git
```

Then navigate into the project directory:

```bash
cd Pulling-Form
```

### Step 2: Create and Activate a Virtual Environment

Create a virtual environment and activate it:

On macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

Install the required packages using `pip`:

```bash
pip install -r requirements.txt
```

### Step 4: Set Up the Database

Apply the database migrations:

```bash
python manage.py migrate
```

### Step 5: Create a Superuser

Create an admin account:

```bash
python manage.py createsuperuser
```

### Step 6: Run the Development Server

Start the development server:

```bash
python manage.py runserver
```

---

## Usage

After installation, you can access the application at `http://localhost:8000`.

### Key Functionalities:
- **Register** a new account or log in with existing credentials.
- Access your **dashboard** to view and manage form submissions.
- Share your unique **form URL** with others to collect submissions.

---

## User Dashboard

The user dashboard provides a comprehensive interface for managing form submissions, including:

- Viewing all form submissions
- Editing or deleting individual submissions
- Searching and filtering submissions
- Accessing form analytics
- Managing subscription status
- Customizing the form template

---

## Form Customization

Users can personalize their form's appearance by selecting from predefined templates or creating custom ones. To customize your form:

1. Navigate to the **Dashboard**.
2. Click on the **Form Template** section.
3. Choose from the available templates or create a new one.
4. Preview the template.
5. Apply the selected template to your form.

---

## Subscription Management

This application includes a subscription-based access system that allows users to unlock additional features. Key subscription functionalities:

- View subscription status on the dashboard.
- Upgrade or manage your subscription plan.
- Notifications for subscription expiry or renewal.

---

## Security

Security is a top priority. This application implements the following measures:
- Password hashing for user accounts.
- Encrypted database fields for sensitive information.
- CSRF protection for forms.
- Secure HTTPS implementation (in production).

---

## API Endpoints

This system includes RESTful APIs for integration with other systems. Key endpoints:
- **Authentication APIs**: Register, Login, Logout
- **Form Management APIs**: Create, Update, Delete forms
- **Submission APIs**: Fetch, Search, Update submissions
- Full API documentation is available in the project repository.

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push to your fork.
4. Create a pull request to the main repository.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
