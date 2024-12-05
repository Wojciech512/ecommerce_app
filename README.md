# 🛒 E-commerce Application Project

## Table of Contents
1. [About the Project](#-about-the-project)
2. [Key Features](#-key-features)
3. [Technologies](#-technologies)
4. [Key Features and Components](#-key-features-and-components)
5. [Main Feature Sequence Diagram](#-main-feature-sequence-diagram)
6. [Setup](#-setup)
7. [Configuring a Google Account for Sending Emails](#-Configuring-a-Google-Account-for-Sending-Emails)
8. [License](#-license)

---

## 📝 About the Project

This project is a fully functional e-commerce application developed using the **Django framework**. It integrates core features such as:

- **Secure payment processing**
- **Responsive design**
- **Robust user account management**

Hosting and data storage are powered by **Azure services**, ensuring scalability and reliability. The application is designed to handle high user traffic and provide a seamless shopping experience for both end-users and administrators.

---

## 🚀 Key Features

### 🔑 End-user Features:
- **Shopping Cart**: Add, remove, and update products with session-based retention.
- **Order Processing**: Full checkout flow with shipping options.
- **User Account**: Registration, login, password reset, and account management.
- **Payment Integration**: Secure payments via PayPal and other platforms.

### 🛠️ Admin Features:
- **Product Management**: Add, update, and remove products.
- **User Management**: Manage user accounts and permissions.
- **Order Insights**: Review purchase history and manage logs.

### 🔒 Security:
- **SQL Injection protection**, CSRF, and session security.
- **Secure communication** with SSL/TLS enforcement.
- Validation of all user inputs to ensure data integrity.

---

## 💻 Technologies

### Backend
- **Django Framework**: Efficient management of core application logic, user authentication, and API integrations.

### Frontend
- **Django Views**: Seamless integration between backend logic and UI.
- **Bootstrap**: Responsive design for mobile and desktop optimization.

### Hosting and Data Storage
- **Azure App Service**: High availability, scalability, and easy deployment.
- **Azure Database for PostgreSQL**: Reliable and secure database for user, product, and transaction data.

### Payment Integration
- **PayPal**: Secure and widely accepted payment gateway.

### Version Control
- **GitHub**: Collaboration, version control, and CI/CD workflows.

---

## 📊 Key Features and Components

| Id | Feature                     | Description                                                                                   |
|----|------------------------------|-----------------------------------------------------------------------------------------------|
| 1  | Shopping Cart                | Add, remove, and update products in the cart with session management to retain items.         |
| 2  | Order Process and Shipping   | Complete order processing, including adding to cart, checkout, and selection of shipping.     |
| 3  | User Registration & Login    | Account creation, login, and password reset with email verification for added security.       |
| 4  | User Account Management      | Update account details, view order history, and manage billing addresses.                     |
| 5  | Admin Account                | Manage users, logs, and products, including adding, updating, and viewing purchase history.   |
| 6  | Payment Integration          | Secure online payments with PayPal and other platforms, integrated into the order process.    |
| 7  | Security                     | Multiple layers of protection against attacks, secure data transmission, and user validation. |
| 8  | Data Validation              | Frontend and backend data validation for correct and compliant data entry.                    |

---

## 📈 Main Feature Sequence Diagram
![diagram sekwencji.png](static%2Fmedia%2Fdiagram%20sekwencji.png)

---

## ⚙️ Setup

Follow these steps to set up the project in your preferred development environment:

1. **Clone the Repository**:
   - Use your IDE's version control integration or run the following commands:
     ```bash
     git clone https://github.com/your-repo-name.git
     cd your-repo-name
     ```

2. **Create a Virtual Environment**:
   - Run the following commands in the terminal:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```

3. **Install Dependencies**:
   - Install the project dependencies:
     ```bash
     pip install -r requirements.txt
     ```

4. **Set Up Environment Variables**:
   - Create a `.env` file in the project root directory (if not already provided) with the following content:
     ```
     SECRET_KEY=your-django-secret-key
     DB_HOST=your-database-host
     DB_NAME=your-database-name
     DB_USER=your-database-user
     DB_PASSWORD=your-database-password
     ```
   - Alternatively, configure environment variables directly in your IDE's run/debug configuration settings.

5. **Apply Database Migrations**:
   - Run the following command:
     ```bash
     python manage.py migrate
     ```

6. **Run the Development Server**:
   - Start the server:
     ```bash
     python manage.py runserver
     ```
   - By default, the application will be available at `http://127.0.0.1:8000`.

7. **Optional - Set Debugging**:
   - Configure your IDE to support Django debugging. Most IDEs support setting breakpoints and running a debug configuration.
---
### 📧 Configuring a Google Account for Sending Emails

To configure your application to send emails using a Google account, follow these steps:

1. **Enable 2-Step Verification for Your Google Account**:
   - Go to your Google Account's [Security Settings](https://myaccount.google.com/security).
   - Enable **2-Step Verification** if it is not already active.

2. **Generate an App Password**:
   - After enabling 2-Step Verification, go to the [App Passwords](https://myaccount.google.com/apppasswords) page.
   - Select "Mail" as the app and "Other" as the device, then give it a name (e.g., `Django App`).
   - Click **Generate**. A password will be displayed—copy it securely.

3. **Set Up Your Environment Variables**:
   - Open your `.env` file and add the following lines:
     ```env
     EMAIL_HOST_USER=your-app-email
     EMAIL_HOST_PASSWORD=your-app-password
     ```
   - Replace `your-app-email` and `your-app-password` with the account email and app password you generated in Step 2.

4. **Ensure Security**:
   - Do not commit the `.env` file containing sensitive information to your version control system.
   - Add `.env` to your `.gitignore` file to protect it.

By following these steps, your application will be able to send emails using your configured Google account.

---
## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). You are free to use, modify, and distribute this project under the terms of the license.
