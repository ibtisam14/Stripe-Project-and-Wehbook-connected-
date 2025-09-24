🛒 Small Product Selling Website (Django + Stripe Integration)

This is a simple Django-based e-commerce website that demonstrates selling products online with Stripe integration for secure payment processing. The project includes features like product listing, checkout, Stripe webhook handling, and environment variable configuration for secure key management.



🚀 Features





Django-based product selling website with a clean and simple interface



Stripe Checkout Session integration for seamless payment processing



Webhook handling for processing successful payments and updating order status



Secure management of sensitive keys using a .env file



Basic product management (add, view, and purchase products)



Responsive design for accessibility across devices



📂 Project Structure

The project follows a standard Django structure with additional configurations for Stripe integration. Below is an overview of the key directories and files:

small_product_selling/
├── manage.py                 # Django management script
├── small_product_selling/    # Project configuration directory
│   ├── __init__.py
│   ├── settings.py          # Django settings (includes Stripe and .env config)
│   ├── urls.py              # Main URL configurations
│   └── wsgi.py              # WSGI entry point for deployment
├── products/                 # App for product management
│   ├── migrations/           # Database migration files
│   ├── __init__.py
│   ├── admin.py             # Admin panel configurations
│   ├── apps.py              # App configuration
│   ├── models.py            # Product and order models
│   ├── views.py             # Views for product listing and checkout
│   ├── urls.py              # App-specific URL routes
│   └── templates/           # HTML templates for product pages
├── templates/                # Base templates (e.g., base.html)
├── static/                   # Static files (CSS, JS, images)
├── .env                      # Environment variables (Stripe keys, etc.)
├── requirements.txt          # Project dependencies
└── README.md                 # This file



🛠️ Prerequisites

Before setting up the project, ensure you have the following installed:





Python 3.8 or higher



pip (Python package manager)



Virtualenv (optional but recommended)



Git



A Stripe account with API keys (test mode recommended for development)



📥 How to Clone the Project

To get started, clone the repository to your local machine:





Open your terminal and run:

git clone https://github.com/your-username/small_product_selling.git



Navigate to the project directory:

cd small_product_selling



🌐 Setting Up the Environment

Follow these steps to set up the project environment:





Create a Virtual Environment (recommended to isolate dependencies):

python -m venv venv



Activate the Virtual Environment:





On Windows:

venv\Scripts\activate



On macOS/Linux:

source venv/bin/activate



Install Dependencies: Install the required Python packages listed in requirements.txt:

pip install -r requirements.txt



Set Up Environment Variables:





Create a .env file in the project root directory.



Add the following environment variables (replace with your actual Stripe keys):

STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret
SECRET_KEY=your_django_secret_key
DEBUG=True



You can obtain Stripe keys from the Stripe Dashboard.



Apply Database Migrations: Run the following commands to set up the database:

python manage.py makemigrations
python manage.py migrate



Create a Superuser (optional, for admin access):

python manage.py createsuperuser



🚀 Running the Project

To run the project locally:





Ensure the virtual environment is activated.



Start the Django development server:

python manage.py runserver



Open your browser and navigate to http://127.0.0.1:8000 to view the website.



Access the admin panel at http://127.0.0.1:8000/admin (log in with the superuser credentials).



💳 Configuring Stripe Webhooks

To handle payment events (e.g., successful payments), configure Stripe webhooks:





Log in to your Stripe Dashboard.



Create a new webhook endpoint pointing to:

http://127.0.0.1:8000/webhooks/stripe/



Select the events you want to listen for (e.g., checkout.session.completed).



Copy the webhook secret and add it to your .env file as STRIPE_WEBHOOK_SECRET.



Test the webhook locally using a tool like ngrok to expose your local server:

ngrok http 8000

Update the webhook URL in Stripe with the ngrok-provided URL.



🧪 Testing Payments

To test payments:





Use Stripe's test card numbers (e.g., 4242 4242 4242 4242, expiry: any future date, CVC: any 3 digits).



Navigate to the product page, select a product, and proceed to checkout.



Verify webhook functionality by checking the order status in the database or admin panel after a successful payment.



📚 Additional Notes





Security: Never commit the .env file to version control. Ensure it is listed in .gitignore.



Deployment: For production, configure a production-ready server (e.g., Gunicorn + Nginx) and set DEBUG=False in settings.py.



Customization: Extend the products app to add more features like cart functionality, user authentication, or product categories.



🤝 Contributing

Contributions are welcome! To contribute:





Fork the repository.



Create a new branch (git checkout -b feature/your-feature).



Make your changes and commit (git commit -m "Add your feature").



Push to the branch (git push origin feature/your-feature).



Open a pull request.



📬 Contact

For questions or issues, please open an issue on the repository or contact [your-email@example.com].