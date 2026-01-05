# CraftCore  
A Marketplace for Local Artisans

---

## Overview

CraftCore is a full-stack web application built using Django that connects local artisans with buyers through a simple and intuitive marketplace.

The platform enables artisans to onboard as sellers, list handmade products, and track orders, while buyers can browse products, place orders, and view order confirmations. The application focuses on real-world marketplace flows, role-based access, and clean backend logic.

This project was built as part of a hackathon and represents a functional MVP (Minimum Viable Product).

---

## Problem Statement

Local artisans often lack access to digital platforms that allow them to showcase and sell their products directly to buyers. Existing marketplaces are either too complex, too expensive, or do not highlight the artisan’s identity and story.

CraftCore aims to:
- Provide artisans with a simple digital storefront
- Enable buyers to discover and support local craftsmanship
- Offer a clean, end-to-end buying and selling experience

---

## Key Features

### Buyer Features
- User authentication (login / signup)
- Browse all available products
- View detailed product pages
- Place orders (single-item checkout flow)
- View order confirmation and order history

### Seller (Artisan) Features
- Become a seller through an onboarding flow
- Seller dashboard with analytics
- Add, edit, and deactivate products
- View orders received for their products
- Track total orders and total earnings
- Update artisan profile
- Deactivate seller account while preserving historical data

### Platform Features
- Role-based UI (buyer vs seller)
- Product availability handling (active, inactive, out of stock)
- Historical analytics that do not change when products are deactivated
- Custom error handling (404, access control)
- Responsive UI

---

## Tech Stack

### Backend
- Python
- Django
- SQLite (for development and demo)

### Frontend
- HTML
- CSS
- JavaScript
- Bootstrap

### Deployment
- Render (Python Web Service)
- Gunicorn (WSGI server)

### Version Control
- Git
- GitHub

---

## Application Flow

### Buyer Flow
1. User logs in or signs up
2. Browses products
3. Views product details
4. Places an order
5. Sees order confirmation
6. Views orders in profile

### Seller Flow
1. User logs in
2. Completes onboarding
3. Becomes a seller
4. Adds products
5. Views seller dashboard
6. Tracks orders and earnings
7. Manages product availability

---

## Data Integrity & Design Decisions

- Products are never hard-deleted; they are deactivated to preserve order history
- Orders and earnings analytics are event-based and immutable
- Product stock controls availability without affecting past orders
- Seller deactivation does not alter historical data
- Onboarding is enforced globally to prevent inconsistent user states

---

## Setup Instructions (Local)

### Prerequisites
- Python 3.10+
- Git
- Virtual environment (recommended)

### Steps

```bash
git clone https://github.com/rageenidawale/craftcore-hackathon
cd craftcore
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open:
```
http://127.0.0.1:8000/
```

---

## Environment Variables

The following environment variables are required for deployment:

```
SECRET_KEY
DEBUG
ALLOWED_HOSTS
```

These values are configured on the hosting platform (Render) and are not included in the repository.

---

## Deployment

The application is deployed using Render as a Python Web Service.

- Build command:
```bash
pip install -r requirements.txt
```

- Start command:
```bash
gunicorn craftcore.wsgi:application
```

---

## Demo & Screenshots

- A demo video showcasing key flows is included in the submission
- Screenshots of the application are provided for reference

---

## Limitations & Future Scope

This project is an MVP and can be extended with:
- Product reviews and ratings by verified buyers
- Secure payment gateway integration
- OAuth based login (Google authentication)
- Multi-item cart functionality
- Advanced seller analytics
- Admin dashboards
- Search and recommendation features
- Cloud storage for media files

---

## Author

CraftCore was built as a hackathon project with a focus on clean architecture, real-world marketplace logic, and user experience.
