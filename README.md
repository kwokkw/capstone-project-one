# Springboard - Capstone Project One (Real Estate Dashboard)

<!-- TODO: do I need Restful APIs? -->
It is focused on building a database-driven website powered by an external API, using technologies like Python/Flask, PostgreSQL, SQLAlchemy, Jinja, RESTful APIs, JavaScript, HTML, and CSS. The project will integrate features related to real estate. 

## Table of contents

- [Springboard - Capstone Project One (Real Estate Dashboard)](#springboard-capstone---project-one-real-estate-dashboard)
  - [Table of contents](#table-of-contents)
  - [Overview](#overview)
    - [The challenge](#the-challenge)
    - [Links](#links)
  - [My process](#my-process)
    - [Built with](#built-with)
    - [What I learned](#what-i-learned)
    - [Continued development](#continued-development)
    - [Useful resources](#useful-resources)
  - [Author](#author)
  - [Acknowledgments](#acknowledgments)
  - [Time estimate](#time-estimate)

## Overview

1.  Purpose and Scope

  The project aims to provides users with a way to explore real estate listings, save favorite properties, and potentially personalize their seach experience. Core functionalities will focus on:

  - Displaying property information sourced from an external real estate API.
  - Managing user accounts and their interactions with property data.
  - Enabling search, filtering, and saving of property listings. 

2.  Key Features

  - User Authentication
  - Property Listings and Details
  - Favorites

3.  Database Design

  - Users Table
  - Properties Table
  - Favorites Table

4.  User Flow

  A user's journey might look like this:

  1.  Authentication: The user signs up or logs in.
  2.  Property Search: They search for properties by specifying criteria like location, price range, or proerty type. 
  3.  View Details: Clicking a propety opens a detailed view with additional information.
  4.  Favorites Management: They can save properties to theri favorites, accessible from a dedicated page. 


### The challenge

- API integration
- User Experience
- Database Performance

### Links

## My process

1.  Planning & Research
  - Goal Setting: Set project goals focused on creating a database-driven real estate dashboard.
  - Feature Requirements: Prioritized core functionalities, such as user authentication, property listings, and saving favorites.
  - API Selection

2.  Setting Up the Environment

3.  Database Modeling
  - Models Defined: Designed `User`, `Property`, and `Favorite` tables in `models.py`
  - Relationships: Created relationships between tables to link users with their favorite properties.
  - Data Seeding: Seeded sample data for testing purposes. 

4.  Building Core Features

5.  Testing & Debugging 

### Built with

Tech Stack Breakdown

  - Languages:
    - Python: Backend scripting and logic
    - JavaScirpt: Client-side scripting
    - HTML: Markup for structuring web pages
    - CSS: Styling web pages

  - Framworks and Libraries:
    - Flask: Web framework for routing, views, and backend functionality
    - SQLAlchemy: ORM (Object Relational Mapper) for handling database interactions
    - Jinja: Templating engine for rendering dynamic HTML
    - WTForms: Form validation and handling in Flask

  - Database:
    - PostgreSQL: Relational database to store and manage property and user data

  - API Integration:
    - <!-- TODO: A real estate API that supply the property data -->
    - External Real Estate API: provides property data

  - Tools and Platforms:
    - Git: Version control system to manage and track code changes
    - GitHub: Repository hosting service for collaboration and version tracking
    - <!-- TODO: Do I need Supabase database service? -->

### What I learned


### Continued development


### Useful resources


## Author


## Acknowledgments


## Time estimate 

Springboard: 41 - 57 Hours

Project Timeline

### Day 1: Backend Development & Database Setup

#### **Goal**: Establish backend structure, database setup, and API integration.

- **Session 1**

  - **Task 1**: Set up Flask application and project structure (1 hour)
    - Create necessary directories and files (`app.py`, `README.md`, etc.).
    - Initialize virtual environment and install dependencies. 
  
  - **Task 2**: Database Design & Implementation (2 hours)
    - Define schema for `Users`, `Properties`, and `Favorites` tables.
    - Set up PostgreSQL database and create tables.

- **Session 2**

  - **Task 3**: Build Data Models with SQLAlchemy (1-2 hours)
    - Create SQLAlchemy models for `Users`, `Properties`, and `Favorites`.
    - Define relationships and basic validations.

  - **Task 4**: Integrate External API (2 hours)
    - Connect to the real estate API and retrieve property data.
    - Write helper functions to process and store API data in the database.

- **Session 3**

  - **Task 5**: Basic CRUD Routes for Properties (2 hours)
    - Set up routes for displaying property listings and details.
    - Implement functions to query data from the database.

  - **Task 6**: Initial Testing of API and Database Integration (1 hour)
    - Verify API data retrieval and ensure correct data storage.
    - Test CRUD routes and database connections.

---

### Day 2: Frontend, Authentication, and Finalization

#### **Goal**: Implement frontend, user authentication, and finalize documentation and testing.

- **Session 1**
  - **Task 7**: Build User Authentication (2 hours)
    - Set up registration, login, and logout routes using Flask-WTF and Flask-Bcrypt.
    - Create session management and protect user-only routes.

  - **Task 8**: Develop Property Listing and Detail Views (2 hours)
    - Build HTML templates using Jinja for property listings and details.
    - Incorporate dynamic data from Flask routes into templates.

- **Session 2**

  - **Task 9**: Implement User Favorites Functionality (2 hours)
    - Create “Add to Favorites” feature, linking properties to users.
    - Build out favorites view to display saved properties.

  - **Task 10**: CSS Styling and Basic JavaScript (2 hours)
    - Apply styling for layouts and responsive design.
    - Add JavaScript for interactions, like button clicks on favorites.

- **Session 3**

  - **Task 11**: Testing & Debugging (1 hour)
    - Test all routes, forms, and database actions for smooth functionality.
    - Debug any issues in the user flow or API integration.

  - **Task 12**: Deployment & Documentation (1 hour)
    - Deploy the application to a platform like Heroku or Vercel.
    - Complete README with installation steps, usage instructions, and "Built With" section.
