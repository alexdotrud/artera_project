# **ARTERA**

![Project preview on multiple screens](documentation/responsive.png)
[View live project here!](https://artera-d6829bf39792.herokuapp.com/)

Artera is a digital art e‑commerce platform built with **Django**, **Bootstrap 5**, **JavaScript**, and **Stripe**. Users can browse artworks, choose sizes with dynamic pricing, purchase securely, manage profiles, and access all purchased files through a personal Digital Library. Artists can also submit custom artwork requests or offer sample work.

---

## Content:

* [User Goals](#user-goals)
* [Business Goals](#business-goals)
* [Developer Goals](#developer-goals)
* [User Stories](#user-stories)
* [Agile Methods](#agile-methods)
* [Design Choices](#design-choices)
* [Database Schema](#database-schema)
* [Features](#features)
* [UX Design](#ux-design)
* [Technologies Used](#technologies-used)
* [Testing](#testing)
* [Bugs](#bugs)
* [Future Changes](#future-changes)
* [Deployment](#deployment)
* [Setup Instructions](#setup-instructions)
* [Cloning, Forking and Version Control](#cloning-forking-and-version-control)
* [Credits](#credits)

---

## User Goals

Artera helps users discover high‑quality downloadable art prints and purchase them easily. Users want:

* A clean, modern browsing experience
* Clear artwork previews, sizes, and pricing
* Smooth, secure checkout
* Access to previously purchased files
* Ability to request custom artwork or submit their own

## Business Goals

Artera is designed as a polished, real‑world e‑commerce platform that demonstrates full‑stack development skill and product thinking.
The project aims to:

* Present a professional, portfolio‑ready example of a complete Django e‑commerce application.
* Showcase the ability to design, build, and deploy production‑level features end‑to‑end.
* Deliver a smooth, trustworthy user experience with clean UI and consistent behavior.
* Provide a scalable base for future additions like artist dashboards, subscriptions, or analytics tools.

## Developer Goals

* Build a fully functional e‑commerce platform using Django, Stripe, Bootstrap 5, and custom JavaScript.
* Ensure the site is fully responsive and visually consistent across all devices.
* Write clean, maintainable, and scalable code following best practices.
* Optimize backend and frontend performance for fast rendering and smooth interactions.
* Create a future‑proof structure that can grow with new features, artwork categories, or business models.

---

## User Stories

### 1. Sign-Up  
**User Story:**  
As a new user, I want to create an account so that I can purchase and later access my digital prints.  

**Acceptance Criteria:**  
- Sign-up form with email, username, and password  
- Redirects to home after successful registration  
- Errors shown for duplicate email or mismatched passwords  

---

### 2. Login  
**User Story:**  
As a returning user, I want to log in so I can securely view my purchases and downloads.  

**Acceptance Criteria:**  
- Login with email/username and password  
- Redirects to home on success  
- Error message on invalid credentials  
- Protected pages require login  
- Session persists until logout  
- “Forgot Password?” option sends reset email  

---

### 3. Browse Shop  
**User Story:**  
As a visitor, I want to browse available digital art prints so I can explore what’s for sale.  

**Acceptance Criteria:**  
- Grid of artworks with thumbnails, titles, and prices  
- Clicking an item opens the artwork detail page  
- Category filter  
- Search bar for titles/keywords  

---

### 4. Artwork Detail & Add to Cart  
**User Story:**  
As a user, I want to view artwork details and add them to my cart.  

**Acceptance Criteria:**  
- Large preview, description, and price displayed  
- “Add to Cart” updates cart dynamically  

---

### 5. Cart & Checkout  
**User Story:**  
As a user, I want to review my cart and pay securely.  

**Acceptance Criteria:**  
- Cart lists items with title, price, and remove/update options  
- Total price updates automatically  
- Checkout button redirects to Stripe  
- Success page after payment  
- Cancel page after failed/cancelled payment  

---

### 6. Stripe Payment Confirmation (System)  
**User Story:**  
As the system, I want to confirm payment success so users only access paid items.  

**Acceptance Criteria:**  
- Stripe webhook validates successful payments  
- Order status becomes “paid” on confirmation  
- Failed payments remain “awaiting payment”  

---

### 7. My Library  
**User Story:**  
As a logged-in user, I want to access and download my purchased artworks.  

**Acceptance Criteria:**  
- List of all purchased artworks under paid orders  
- Only the buyer can access download links  

---

### 8. Profile Management  
**User Story:**  
As a logged-in user, I want to update my profile so my information is correct for purchases.  

**Acceptance Criteria:**  
- Editable fields: name, address, city, postal code, country  
- Validation ensures required fields  
- Confirmation message after saving  

---

### 9. Artist Offers  
**User Story:**  
As an artist, I want to offer my artwork to the platform for review.  

**Acceptance Criteria:**  
- Form with title, description, category, price, image upload  
- Submission marked as “pending approval”  
- Admin can approve or reject the submission  

---

### 10. Custom Artwork Requests  
**User Story:**  
As a customer, I want to request custom artwork tailored to my preferences.  

**Acceptance Criteria:**  
- Form with title, description, and reference image  
- Requests linked to user account  
- Displayed in “My Requests”  
- Admin/artist can respond with a quote or offer  

---

### 11. Email Notifications  
**User Story:**  
As a user, I want to receive email notifications for important actions.  

**Acceptance Criteria:**  
- Welcome email after registration  
- Password reset email  
- Order confirmation email after payment  

---

## Agile Methods

This project was planned and developed using Agile methodology to keep development structured, transparent, and iterative.

- **User Stories:**  
  All core features of Artera were defined as user stories with clear acceptance criteria.  
  Each story received a priority label — *Must Have*, *Should Have*, or *Could Have* — ensuring the most important functionality was delivered first.

- **Project Planning:**  
  A GitHub Projects Kanban board was used with columns for **To Do**, **In Progress**, **Done**, and **Future Improvements**.  
  This provided a clear overview of progress and helped maintain development flow.

- **Iterative Development:**  
  Features were built in small, incremental steps.  
  Core e-commerce functionality (shop, bag, checkout, orders) was implemented first, followed by profile management, library features, and service-related tools (requests and offers).

- **Testing & Refinement:**  
  Each feature was manually tested after implementation.  
  Issues were addressed immediately before moving on to the next task, ensuring stable builds at every stage.

**Project Planning Screenshots**

![GitHub Projects Board](documentation/todo-list.png)  
![Example User Stories](documentation/task-planning.png)
