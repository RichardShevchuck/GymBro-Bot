GymBro Telegram Bot

Simple Telegram bot for tracking workouts.

Description

This bot allows users to log their workouts step by step.
Each workout can contain multiple exercises with weight, reps and sets.
All data is stored in a PostgreSQL database.

⸻

Features
	•	Add exercises one by one
	•	Multiple exercises in one workout
	•	Finish workout with /stop
	•	View recent workouts history
	•	Data persistence with PostgreSQL
	•	Database migrations with Alembic

⸻

Tech Stack
	•	Python
	•	aiogram
	•	PostgreSQL
	•	SQLAlchemy
	•	Alembic
	•	Docker

⸻

How it works

User starts a workout and enters:
	1.	Exercise name
	2.	Weight
	3.	Reps
	4.	Sets

After that, user can add another exercise or finish the workout with /stop.

Each workout is stored as a session with multiple entries.

⸻

Database Structure
	•	users — Telegram users
	•	workouts — workout sessions
	•	workout_entries — exercises inside workouts

⸻

Notes
	•	Bot uses FSM (Finite State Machine) for handling user input
	•	/stop command works at any step
	•	Data is stored in Docker volume

⸻

Author

Learning project