# Pulling Form

Pulling Form is a subscription-based multi-step form website that allows users to create and manage custom forms. Users can share their unique form URL with others, and the forms are only functional when the user has an active subscription.

## Features

1. **User Registration and Authentication**
   - Users can register with their name, email, and password
   - Secure login and logout functionality
   - Password reset feature

2. **Subscription Management**
   - Integration with Paystack for payment processing
   - Customizable subscription duration and pricing (managed via Django admin)
   - Automatic subscription expiration and renewal reminders

3. **Form Creation and Management**
   - Each user gets a unique, publicly accessible form URL
   - Forms are only functional when the user has an active subscription
   - Users can view, edit, and delete form submissions from their dashboard

4. **Public Form Submission**
   - External users can submit data through the public form URL
   - Form submissions are stored and linked to the user's account

5. **Dashboard**
   - Custom user dashboard displaying:
     - Subscription status and expiry date
     - Unique form URL
     - List of form submissions
     - Basic analytics (total submissions, submissions by date)

6. **Notifications**
   - Email notifications for new form submissions
   - Dashboard notifications for unread form submissions
   - Email reminders for subscription expiration

7. **Admin Interface**
   - Customizable subscription settings (price and duration)
   - User management
   - Form submission monitoring

## Technology Stack

- Backend: Django
- Frontend: HTML, Tailwind CSS
- Database: SQLite (default, can be changed to PostgreSQL for production)
- Task Queue: Celery with Redis as message broker
- Payment Integration: Paystack

## Setup and Installation

1. Clone the repository:
git clone [https://github.com/yourusername/pulling-form.git](https://github.com/yourusername/pulling-form.git)
cd pulling-form

```plaintext

2. Create a virtual environment and activate it:
```

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

```plaintext

3. Install the required packages:
```

pip install -r requirements.txt

```plaintext

4. Set up environment variables:
- Create a `.env` file in the project root
- Add the following variables:
```

SECRET_KEY=your_django_secret_key
PAYSTACK_SECRET_KEY=your_paystack_secret_key
SUPERUSER_EMAIL=[admin@example.com](mailto:admin@example.com)

```plaintext

5. Run migrations:
```

python manage.py makemigrations
python manage.py migrate

```plaintext

6. Create a superuser:
```

python manage.py createsuperuser

```plaintext

7. Create initial subscription settings:
```

python manage.py create_initial_subscription_settings

```plaintext

8. Start the development server:
```

python manage.py runserver

```plaintext

9. In a separate terminal, start the Celery worker:
```

celery -A pulling_form worker -l info

```plaintext

10. In another terminal, start the Celery beat scheduler:
```

celery -A pulling_form beat -l info

```plaintext

## Usage

1. Access the admin interface at `http://localhost:8000/admin/` to configure subscription settings and manage users.
2. Users can register and log in at `http://localhost:8000/register/` and `http://localhost:8000/login/` respectively.
3. Once logged in, users can access their dashboard at `http://localhost:8000/dashboard/`.
4. Users need to subscribe to activate their form and start receiving submissions.
5. The public form can be accessed at `http://localhost:8000/form/<unique-id>/`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
```