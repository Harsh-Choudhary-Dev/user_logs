from flask import Flask, render_template, request, jsonify
import psycopg2
from flask_cors import CORS
app = Flask(__name__)
connection_url = "postgresql://user_activity_user:IdBVTkwEAlvrWV8dSeDZGbsI0HsFAmuh@dpg-cskcb8pu0jms73b9ijf0-a.oregon-postgres.render.com/user_activity"
CORS(app)

def get_db_connection():
    connection = psycopg2.connect(connection_url)
    return connection

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        refreshment = data.get('refreshment')
        meeting_date = data.get('date')
        message = data.get('message')
        

        # Insert data into the database
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            insert_query = '''
            INSERT INTO meeting_invite (name, refreshment, meeting_date, message)
            VALUES (%s, %s, %s, %s);
            '''
            cursor.execute(insert_query, (name, refreshment, meeting_date, message))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({'message': 'Activity logged successfully'}), 201
        except Exception as error:
            return f"An error occurred: {error}"

if __name__ == '__main__':
    app.run(debug=False, port=5000)