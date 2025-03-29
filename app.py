from flask import Flask, render_template, request, jsonify 
import pandas as pd
import psycopg2

app = Flask(__name__, template_folder='html')

# Function taking the name of a table and returning a dataframe with its contents
def query_table(table_name, animal_type = None):
    conn = None
    cursor = None
    try:
        # Database connection
        conn = psycopg2.connect(
            dbname="Zoo",
            user="postgres",
            password="mike12189",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        if animal_type:
            query = f"SELECT * FROM {table_name} WHERE animal = %s;"
            cursor.execute(query, (animal_type,))
        else:
            cursor.execute(f"SELECT * FROM {table_name};")
            
        data = cursor.fetchall()

        

        # Execute query to get data from the specified table
        # cursor.execute(f"SELECT * FROM {table_name};")
        # data = cursor.fetchall()

        # check for data retrieval
        if not data:
            return None

        # Create DataFrame from fetched data
        columns = [desc[0] for desc in cursor.description]  # get and apply column names
        df = pd.DataFrame(data, columns=columns)

        return df

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        # Ensure connection is closed
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route('/')
def home():
    return render_template('index.html') # index page


@app.route('/employees.html')
def employees():
    # Query data from the 'employees' table
    employees_df = query_table('employees')

    if employees_df is None:
        return render_template('error.html', error_message="No data found in the 'employees' table.")

    # Convert the DataFrame to an HTML table
    employees_html = employees_df.to_html(classes='table table-bordered table-striped')

    # Return the HTML table embedded in the page's template
    return render_template('employees.html', table_html=employees_html, title="Employees Table")

@app.route('/animals.html')
def animals():
    # Query data from the 'animals' table
    animals_df = query_table('animals')
    

    if animals_df is None:
        return render_template('error.html', error_message="No data found in the 'animals' table.")

    # Convert the DataFrame to an HTML table
    animals_html = animals_df.to_html(classes='table table-bordered', index=False)

    # Return the HTML table embedded in the page's template
    return render_template('animals.html', table_html=animals_html, title="Animals Table")
# This code is used to received the js request to filter out the animal table by query. 
@app.route('/filter_animals', methods=['POST'])
def filter_animals():
    try:
        data = request.get_json()
        if not data or "animal_type" not in data:
            return jsonify({'table_html': "<p>Error: Missing animal type.</p>"}), 400

        animal_type = data["animal_type"]
        filtered_df = query_table('animals', animal_type)

        if filtered_df is None or filtered_df.empty:
            return jsonify({'table_html': "<p>No animals found for this type.</p>"})

        table_html = filtered_df.to_html(classes='table table-bordered', index=False)
        return jsonify({'table_html': table_html})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/events.html')
def events():
    # Query data from the 'events' table
    events_df = query_table('events')

    if events_df is None:
        return render_template('error.html', error_message="No data found in the 'events' table.")

    # Convert the DataFrame to an HTML table
    events_html = events_df.to_html(classes='table table-bordered')

    # Return the HTML table embedded in the page's template
    return render_template('events.html', table_html=events_html, title="Events Table")

@app.route('/event_attendance.html')
def event_attendance():
    # Query data from the 'eventattendance' table
    event_attendance_df = query_table('eventattendance')

    if event_attendance_df is None:
        return render_template('error.html', error_message="No data found in the 'event-attendance' table.")

    # Convert the DataFrame to an HTML table
    event_attendance_html = event_attendance_df.to_html(classes='table table-bordered')

    # Return the HTML table embedded in the page's template
    return render_template('event_attendance.html', table_html=event_attendance_html, title="Event-Attendance Table")

@app.route('/guests.html')
def guests():
    # Query data from the 'guests' table
    guests_df = query_table('guests')

    if guests_df is None:
        return render_template('error.html', error_message="No data found in the 'guests' table.")

    # Convert the DataFrame to an HTML table
    guests_html = guests_df.to_html(classes='table table-bordered')

    # Return the HTML table embedded in the page's template
    return render_template('guests.html', table_html=guests_html, title="Guests Table")

@app.route('/habitats.html')
def habitats():
    # Query data from the 'habitats' table
    habitats_df = query_table('habitats')

    if habitats_df is None:
        return render_template('error.html', error_message="No data found in the 'habitats' table.")

    # Convert the DataFrame to an HTML table
    habitats_html = habitats_df.to_html(classes='table table-bordered')

    # Return the HTML table embedded in the page's template
    return render_template('habitats.html', table_html=habitats_html, title="Habitats Table")

@app.route('/inventory.html')
def inventory():
    # Query data from the 'inventory' table
    inventory_df = query_table('inventory')

    if inventory_df is None:
        return render_template('error.html', error_message="No data found in the 'inventory' table.")

    # Convert the DataFrame to an HTML table
    inventory_html = inventory_df.to_html(classes='table table-bordered')

    # Return the HTML table embedded in the page's template
    return render_template('inventory.html', table_html=inventory_html, title="Inventory Table")

@app.route('/membership.html')
def membership():
    # Query data from the 'membership' table
    membership_df = query_table('memberships')

    if membership_df is None:
        return render_template('error.html', error_message="No data found in the 'membership' table.")

    # Convert the DataFrame to an HTML table
    membership_html = membership_df.to_html(classes='table table-bordered')

    # Return the HTML table embedded in the page's template
    return render_template('membership.html', table_html=membership_html, title="Membership Table")


if __name__ == '__main__':
    app.run(debug=True)