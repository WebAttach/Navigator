from flask import Flask, render_template_string, request, jsonify
import sqlite3
import yaml

app = Flask(__name__)

DB_NAME = 'nav.nv'
db_config = {
    "nav.nv": {
        "commands": "CREATE TABLE IF NOT EXISTS commands (id INTEGER PRIMARY KEY, commandtitle TEXT, command TEXT, commandlog TEXT)"
    }
}
    
def init_db():
    for db_name, tables in db_config.items():
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        for table_name, create_query in tables.items():
            cursor.execute(create_query)
        conn.commit()
        conn.close()

init_db() 


CONFIG_YAML = """
app:
  title: "Analyst Navigator - City Gov Edition"
  theme: "light"
DOM:
  top-bar:
    h4: "Analyst Navigator - City Gov Edition"
    user-circle: "CA"
  bottom-bar:
    text: "Analyst Navigator  2025"
  left-section:
    views:
      Set Up:
        items:
          - "Getting Started"
          - "Site Survey"
          - "Layout"
          - "Auto Actions"
      Roles:
        items:
          - "Budget"
          - "Payroll"
          - "Stores Warehouse"
          - "Add Role"
  main-section:
    views:
      Getting Started:
        descripton: "Introduction to Set Up Steps leading to Role-based menus and functionality."
        headline: "Welcome"
        textline:
          - Set Up a couple Roles for demo can take between 10-30 minutes.
          - Implementation of a Role is a 2-4 week process including testing.
"""

config = yaml.safe_load(CONFIG_YAML)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analyst Navigator - Fund Edition</title>
    <style>
         body { font-family: Arial, sans-serif; margin: 0; padding: 0; box-sizing: border-box;overflow-x: hidden;}
          .top-bar { background-color: #222; color: white; padding: 10px; border-radius: 10px 10px 0 0;display: flex;justify-content: space-between;align-items: center;}
          .user-circle {width: 40px;height: 40px;background-color: #b22222;color: #fff;border-radius: 50%;display: flex;justify-content: center;align-items: center;font-weight: bold;font-size: 16px;cursor: pointer;}
          .left-section { background-color: #e0e0e0; padding: 10px; width: 20%; float: left; height: 100vh;box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);}
           .left-section a {text-decoration: none; color: inherit; cursor: pointer; }        
           .main-section { padding: 10px; margin-left: 20%; overflow: hidden; }
            .bottom-bar {background-color: #222;color: white;padding: 5px; border-radius: 0 0 10px 10px; position: fixed;bottom: 0;width: 100%;text-align: center;font-size: 12px;z-index: 10;}
           button { padding: 3px 5px; background-color: #3a7bd5; color: white; border: none; border-radius: 5px; cursor: pointer; }
           button:hover { background-color: #305b94; }
           .hidden{display:none}
           .show{display:block}
    </style>
</head>
<body>
    <div class="top-bar">
        <h4>Analyst Navigator - Fund Edition</h4>
        <div class="user-circle">KM</div>
    </div>
    <div class="left-section">
        <h4>Getting Started</h4>
          <a href="#" event.preventDefault();">Introduction</a><br>
        <h4>Roles</h4>
          <a href="#" event.preventDefault();">Payroll</a><br>
          <a href="#" event.preventDefault();">Budget</a><br>
          <a href="#" event.preventDefault();">System Analyst</a><br>          
          <a href="#" event.preventDefault();">Add Role</a><br>
        <h4>Tasks</h4>
          <a href="#" event.preventDefault();">Produce Report</a><br>
          <a href="#" event.preventDefault();">Process Timecard</a><br>
          <a href="#" event.preventDefault();">Purchase Requisition</a><br>
          <a href="#" event.preventDefault();">Add Task</a><br>
    </div>
    <div class="main-section">
        <div id="results" class="results show"></div>
       <div class="db hidden">
                <div class="db-header">
                    <p><span>Next Dispatch in <span id="cycle-timer">300</span> seconds</span></p>
                </div>
                <div class="db-console">
                    <textarea id="db-request" style="width:50%;" rows=3></textarea><br>
                    <button onclick="executeDBCommand(this)">Dispatch Request</button><br><br>
                    <textarea id="db-response" readonly style="width:50%;" rows=8></textarea><br>
                </div>
        </div>
    </div>
       <div class="bottom-bar">
             <input type=\"text\" id=\"command-input\" >
             <button onclick=\"sendCommand()\">Send</button>
        </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/")
def hello_world():
    return "Hello, World! This is a Dockerized Flask app deployed on Render on 1/21/2025 937am"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
