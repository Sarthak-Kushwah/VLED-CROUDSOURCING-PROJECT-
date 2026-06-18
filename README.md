# FAQFusion AI 🚀

An AI-powered Smart FAQ Management System that automatically answers repeated questions using Natural Language Processing (NLP) and a centralized FAQ knowledge base.

---

## 📌 Project Overview

FAQFusion AI is designed to reduce repetitive queries by intelligently matching user questions with existing FAQs. If a similar question already exists, the system instantly returns the answer. Otherwise, the question is forwarded to the administrator for review and approval.

The approved questions and answers are added to the FAQ repository, allowing the system to continuously grow its knowledge base over time.

---

## 🎯 Problem Statement

Students and interns frequently ask the same questions regarding:

- Certificates
- Attendance
- Reports
- Deadlines
- Resources
- Guidelines

This increases administrative workload and often leads to inconsistent responses.

---

## 💡 Proposed Solution

FAQFusion AI uses NLP-based similarity detection to identify previously answered questions.

### Workflow

User Question
↓
AI Similarity Engine
↓
┌───────────────────┐
│ Similar FAQ Found │
└───────────────────┘
↓
Display Answer

OR

┌──────────────────┐
│ No Match Found   │
└──────────────────┘
↓
Admin Review
↓
Approval & Answer
↓
Add to FAQ Repository

---

## ✨ Features

### User Features

- User Registration
- User Login & Logout
- Ask Questions
- Search FAQs
- View Instant Answers
- Question History

### Admin Features

- Admin Dashboard
- View Pending Questions
- Approve Questions
- Add Answers
- Manage FAQs
- Delete FAQs
- Analytics Dashboard

### AI Features

- Semantic Question Matching
- Similarity Detection
- Knowledge Base Expansion
- Automated FAQ Retrieval

---

## 🛠 Technology Stack

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Backend

- Flask
- Flask-SQLAlchemy
- Flask-Login

### Database

- MySQL

### AI / NLP

- Sentence Transformers
- Scikit-Learn
- Pandas
- NumPy

---

## 📂 Project Structure

```text
FAQFusion-AI/
│
├── frontend/
├── backend/
├── ai_engine/
├── database/
├── docs/
├── tests/
│
├── requirements.txt
├── config.py
├── run.py
└── README.md
