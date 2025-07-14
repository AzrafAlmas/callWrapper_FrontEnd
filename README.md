# callWrapper Front-End

## Overview

This project serves as the **front-end web application** for the customer service AI agent system. It allows customers to **upload documents** that are then processed and stored in a **MongoDB database** for later access by a back-end LLM system (via the `call_gpt.py` backend logic).

The main purpose is to **automate customer service** using AI and reduce operational costs by offloading much of the data handling to the local server.

### Key Features
- Built using **Django's native framework**
- Uses Django’s **default admin panel** and **authentication system**
- **MongoDB (via PyMongo)** used to store user uploads and content contextually
- No `djongo` or ORM models; uses **raw PyMongo** for full control
- Signals connect Django’s User model to a **MongoDB user profile**
- **Minimal Django setup** (1 app, no models, 1 admin field extension)
- Simple file flow: `manage.py → urls.py → views.py → HTML/CSS/JavaScript`

## APIs Used
 - MongoDB Atlas

## Make sure to setup using
"pip install -r requirements.txt"

## Last updated: 2025-07-14


The back-end AI agent (LLM) parses uploaded content for context and responds via Twilio voice.

---

## Data Flow

```text
User → Uploads Content → Stored in MongoDB → Parsed by back-end → LLM response via Twilio

NOW THE DATA FLOW FOR ADMIN MODEL
Admin creates user → Django User created → MongoDB document created → UserProfile created → Admin enters phone → MongoDB updated with phone
