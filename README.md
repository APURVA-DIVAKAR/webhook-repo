# GitHub Webhook Event Tracker (Flask + MongoDB)

A real-time GitHub webhook listener built with Flask and MongoDB that captures repository activity such as pushes, pull requests, and merges, stores them in a database, and exposes the data through APIs and a simple UI.

---

## What This Project Does

When activity occurs in a GitHub repository (push, pull request, merge), GitHub sends a webhook event to this server.

The application:
- Receives GitHub webhook events
- Identifies the event type using request headers
- Extracts meaningful information
- Stores processed events in MongoDB
- Exposes recent activity via REST APIs
- Displays events in a browser UI

---

## Architecture Overview

GitHub Repository  
→ Webhook Event  
→ ngrok (public HTTPS tunnel)  
→ Flask Application  
→ MongoDB  

The server reacts to events instead of polling.

---

## Tech Stack

Backend: Flask (Blueprints, App Factory Pattern)  
Database: MongoDB (PyMongo)  
Tunneling: ngrok  
Frontend: HTML  
Version Control: Git and GitHub Webhooks  

---

## Project Structure

webhook-repo/
│
├── app/
│ ├── init.py # Flask app factory
│ ├── extensions.py # MongoDB initialization
│ ├── webhook/
│ │ ├── init.py
│ │ └── routes.py # Webhook logic
│ └── templates/
│ └── index.html # UI
│
├── run.py # Application entry point
├── requirements.txt
├── .env.example
└── README.md

---

## Supported GitHub Events

- Push events
- Pull request
- Pull request merged

Unsupported or irrelevant events are ignored without crashing the server.

---

## Setup Instructions

###  Clone the Repository

```bash
git clone https://github.com/APURVA-DIVAKAR/webhook-repo.git
cd webhook-repo

---

## Create and Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate

---

## Install Dependencies

```bash
pip install -r requirements.txt

---

## Environment Configuration

Create a .env file in the project root and add the MongoDB connection string.

MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database_name>


---

## Running the Application

Start the Flask development server using the entry file.

```bash
python run.py

---

## Exposing Local Server Using ngrok

GitHub webhooks require a public HTTPS endpoint. Use ngrok to expose localhost.

```bash
ngrok http 5000

You will get a public HTTPS URL like:

https://<ngrok-id>.ngrok-free.dev

Use this URL in GitHub webhook settings:

https://<ngrok-id>.ngrok-free.dev/events


---

## GitHub Webhook Configuration

Navigate to:

Repository → Settings → Webhooks → Add Webhook

Configuration:

Payload URL: https://<ngrok-id>.ngrok-free.dev/events
Content type: application/json
Events:
Push
Pull requests
SSL verification: Enabled

Save the webhook and use the Redeliver option for testing.

---

## API Endpoints

Receive Webhook Events
POST /events


This endpoint receives webhook events from GitHub and stores processed data in MongoDB.

---

## Fetch Recent Events

GET /events

Returns the most recent events from MongoDB in JSON format.

---


## UI Dashboard

http://localhost:5000/

Displays stored GitHub events in a simple browser UI.

---

## Database Details

Database Name: techstax
Collection: events

---








