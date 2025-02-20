from flask import Flask, render_template_string, request, jsonify
import sqlite3
import yaml

app = Flask(__name__)

# Sample YAML content for header, sections, and command prompt
CONFIG_YAML = """
app:
  title: "My Simple Flask App"
  header:
    label: "App Header"
    progress: "50%"
    user_circle: "Admin"
  left_section:
    items:
      - "Step 1: Setup"
      - "Step 2: Database"
      - "Step 3: Testing"
  main_section:
    content: "This is the content area, dynamically populated based on the YAML configuration."
  bottom_bar:
    command_prompt: "Enter SQL commands to populate the database."
"""

# Parse the YAML configuration
config = yaml.safe_load(CONFIG_YAML)

@app.route('/')
def index():
    # Extract data from YAML config
    app_title = config['app']['title']
    header = config['app']['header']
    left_section = config['app']['left_section']
    main_section = config['app']['main_section']
    bottom_bar = config['app']['bottom_bar']

    # Render the basic layout with data from YAML
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ app_title }}</title>
        <style>
            body {font-family: Arial, sans-serif; margin: 0; padding: 0;}
            .top-bar {background-color: #333; color: white; padding: 10px; text-align: center;}
            .top-bar .progress {font-size: 14px;}
            .left-section {width: 20%; float: left; background-color: #f4f4f4; padding: 10px; box-sizing: border-box;}
            .main-section {margin-left: 22%; padding: 20px;}
            .bottom-bar {position: fixed; bottom: 0; width: 100%; background-color: #333; color: white; padding: 10px;}
            .command-input {width: 100%; padding: 10px; margin-top: 10px;}
        </style>
    </head>
    <body>
        <div class="top-bar">
            <h1>{{ header['label'] }}</h1>
            <div class="progress">Progress: {{ header['progress'] }}</div>
            <div class="user-circle">{{ header['user_circle'] }}</div>
        </div>
        
        <div class="left-section">
            <ul>
                {% for item in left_section['items'] %}
                    <li>{{ item }}</li>
                {% endfor %}
            </ul>
        </div>

        <div class="main-section">
            <h2>Main Section</h2>
            <p>{{ main_section['content'] }}</p>
        </div>

        <div class="bottom-bar">
            <p>{{ bottom_bar['command_prompt'] }}</p>
            <input type="text" class="command-input" id="command-input" placeholder="Enter SQL here">
            <button onclick="sendCommand()">Run Command</button>
        </div>

        <script>
            function sendCommand() {
                const commandInput = document.getElementById('command-input').value;
                alert('Executing: ' + commandInput);  // For now, just alert the SQL command entered
                // You can add logic to send the command to the backend for SQL execution
            }
        </script>
    </body>
    </html>
    """, app_title=app_title, header=header, left_section=left_section, main_section=main_section, bottom_bar=bottom_bar)


@app.route('/execute_sql', methods=['POST'])
def execute_sql():
    """Endpoint to execute SQL commands from the command input."""
    command = request.json.get('command')
    if not command:
        return jsonify({"error": "No SQL command provided"}), 400

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(command)
        conn.commit()
        conn.close()
        return jsonify({"message": "SQL executed successfully"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
