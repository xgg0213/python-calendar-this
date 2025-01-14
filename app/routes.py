from flask import Blueprint, render_template, redirect, url_for
from .templates import *
import os
import sqlite3
from datetime import datetime
from .forms import AppointmentForm

# Create the Blueprint
bp = Blueprint(
    "main",  # Name of the Blueprint
    __name__,  # Import name (required for locating resources)
    url_prefix="/"  # Top-level route
)

DB_FILE = os.environ.get("DB_FILE")

@bp.route("/")
def main():
    d = datetime.now()
    return redirect(url_for(".daily", year=d.year, month=d.month, day=d.day))

@bp.route("/<int:year>/<int:month>/<int:day>",methods=["GET", "POST"])
def daily(year, month, day):
    form = AppointmentForm()

    # Convert year, month, and day into a datetime object for querying
    current_date = datetime(year, month, day).strftime("%Y-%m-%d")

    # Handle POST requests: add a new appointment
    if form.validate_on_submit():
        # Extract from data
        params = {
            'name': form.name.data,
            'start_datetime': datetime.combine(form.start_date.data, form.start_time.data),
            'end_datetime': datetime.combine(form.end_date.data, form.end_time.data),
            'description': form.description.data,
            'private': form.private.data
        }

        # create a connection to the database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # insert new appointment into the database
        cursor.execute("""
           INSERT INTO appointments (name, start_datetime, end_datetime, description, private)
           VALUES (?, ?, ?, ?, ?);           
        """, (params['name'], params['start_datetime'], params['end_datetime'], params['description'], params['private']))

        # commit changes and close connection
        conn.commit()
        conn.close()

        # redirect to the same page to avoid form resubmission
        return redirect(url_for(".daily", year=year, month=month, day=day))

    # handle GET request: fetch and display all appointments
    # Create a connection to the database
    conn = sqlite3.connect(DB_FILE)

    # Create a cursor
    cursor = conn.cursor()

    # Execute the SQL query to fetch all records from the appointments table
    cursor.execute("""
        SELECT id, name, start_datetime, end_datetime, description, private
        FROM appointments
        WHERE DATE(start_datetime) = ? 
        ORDER BY start_datetime;
    """, (current_date,))

    # Fetch all results
    appointments_data = cursor.fetchall()

    # Process data: Convert start_datetime and end_datetime to Python datetime objects
    formatted_appointments = []
    for appointment in appointments_data:
        formatted_appointments.append({
            "id": appointment[0],
            "name": appointment[1],
            "start_datetime": datetime.strptime(appointment[2], "%Y-%m-%d %H:%M:%S"),
            "end_datetime": datetime.strptime(appointment[3], "%Y-%m-%d %H:%M:%S"),
            "description": appointment[4],
            "private": appointment[5]
        })

    # Close the database connection
    conn.close()

    # Pass the appointments to the template
    return render_template("main.html", rows=formatted_appointments, form=form)