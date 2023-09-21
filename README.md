# Where & When - Server-side README

## Project Description

**Where & When** is the server-side component of a project developed for Al-Anon Family Services (AFS) of Middle Tennessee, a non-profit organization that maintains a directory of local support group meetings known as "Where & When." Currently, AFS manages this database manually using Google Sheets. Group representatives update their meeting details by filling out a Google Form, which is then manually transferred by the office manager from the responses Google Sheet to a private Google Sheet. This private Google Sheet is the source for a public Google Sheet listing meetings by day and time. Manual updates are required whenever new meetings are added or existing ones are removed. This process is cumbersome and time-consuming, often requiring Excel proficiency, posing challenges in hiring new office managers for the Board.

The objective is to replace AFS's current interconnected Google Docs system with a robust database solution. This involves migrating data from spreadsheets into a database and creating a user-friendly interface. The interface will enable group representatives to easily add, edit, update, and delete meeting details. Additionally, it will allow the office manager to manage meetings on behalf of group representatives. Site visitors will have a user-friendly way to search for meetings.

## Project Links

- [ERD (Entity-Relationship Diagram)](https://dbdiagram.io/d/64f2483502bd1c4a5ed3c41a)
- [Wireframe](https://sketchboard.me/HDY973P3tdLQ)

## Installation

To set up the server-side of the application, you will need:

- Python
- Django

Make sure you have Python installed on your machine. You can then install Django using pip:

```bash
pip install django

## Database Setup

The application uses a local database. Please configure the database settings in your Django project's settings file.

## API Documentation

The server provides data via JSON API endpoints. Here are some of the key endpoints:

- `/meetings`: Manages meeting data.
- `/days`: Manages days of the week for meeting schedules.
- `/types`: Manages meeting types.
- `/groupreps`: Manages group representatives.
- `/areas`: Manages meeting areas.
- `/districts`: Manages meeting districts.

You can use these endpoints to interact with the data in the system.

## Configuration

Configuration details are not specified in this document. Configuration settings may vary depending on your deployment environment.

## Usage

To start the server, you can use npm:

```bash
npm start

**Before Starting the Server:**

Make sure you have all the required dependencies installed and the database properly configured before starting the server.

Thank you for using **Where & When**! If you have any questions or encounter issues, please don't hesitate to reach out.
