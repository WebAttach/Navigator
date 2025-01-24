from flask import Flask, render_template_string, request, jsonify
import sqlite3


app = Flask(__name__)

DB_NAME = 'nav.nv'
db_config = {
    "nav.nv": {
        "commands": "CREATE TABLE IF NOT EXISTS commands (id INTEGER PRIMARY KEY, commandtitle TEXT, command TEXT, commandlog TEXT)",
        "glba": "CREATE TABLE IF NOT EXISTS glba (id INTEGER PRIMARY KEY, uniquekey TEXT, fqastring TEXT, commandlog TEXT)"
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
    <script src="https://videopal.me/js/vp_player.min.js?v=1.1.29" data-cfasync="false"></script>
    <script>
        var vpPlayer = new VpPlayer({
        embedId: "xazm5GauH3JT"
        });
     </script>
     <script>
           function sendCommand() {
                const commandInput = document.getElementById('command-input');
                const command = commandInput.value.trim();
                if (command === "content") {
                }else if(command == 'erp'){
                    window.open('/erp', '_blank');
                }else if(command == 'maps'){
                    window.open('/maps', '_blank');  
                }else if (command ==='tasks') {
                    showTasks()
                }else if (command === 'cls') {
                    document.getElementById('main-section').innerHTML = '';
                }else if (command.startsWith('lang-')) {
                    const langCommand = command.slice(5);
                    fetch(`/lang?input=${encodeURIComponent(langCommand)}`)
                    .then(response => {
                        if (!response.ok) throw new Error("Failed to fetch the language result.");
                            return response.text();
                        })
                        .then(data => {
                            document.getElementById('main-section').innerHTML = data;
                        })
                        .catch(error => {
                            document.getElementById('main-section').innerHTML = `<p>Error: ${error.message}</p>`;
                        });
                }else if (command.startsWith('omni-')) {
                     const langCommand = command.slice(5); 
                     fetch(`/omni?input=${encodeURIComponent(langCommand)}`)
                     .then(response => {
                        if (!response.ok) throw new Error("Failed to fetch the language result.");
                            return response.text();
                        })
                        .then(data => {
                            document.getElementById('main-section').innerHTML = data;
                        })
                        .catch(error => {
                            document.getElementById('main-section').innerHTML = `<p>Error: ${error.message}</p>`;
                        });
                }else {
                    document.getElementById('main-section').innerHTML = `<p>Unknown command: ${command}</p>`;
                }
            }
            async function showTasks() {
                var panh = `<div class="panel-container" id="panel-container">
               <div class="card"><img src="https://github.com/WebAttach/WebAttach/blob/fd2f9b87483893e7769f07d9f82a4137db73324e/panel_1.jpg?raw=true" alt="Legacy Report"><div class="card-content"><h3>Reports</h3><div class="due-date"><svg class="calendar-icon" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 32 32" aria-hidden="true"><path d="M26,4h-4V2h-2v2h-8V2h-2v2H6C4.9,4,4,4.9,4,6v20c0,1.1,0.9,2,2,2h20c1.1,0,2-0.9,2-2V6C28,4.9,27.1,4,26,4z M26,26H6V12h20V26z M26,10H6V6h4v2h2V6h8v2h2V6h4V10z"></path></svg><span>12/15/2024</span></div></div><div class="card-footer"><a href="#" class="continue-btn" onclick="showIframe()">Proceed</a></div></div>
       <div class="card"><img src="https://github.com/WebAttach/WebAttach/blob/fd2f9b87483893e7769f07d9f82a4137db73324e/panel_2.jpg?raw=true" alt="Legacy Report"><div class="card-content"><h3>Forms</h3><div class="due-date"><svg class="calendar-icon" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 32 32" aria-hidden="true"><path d="M26,4h-4V2h-2v2h-8V2h-2v2H6C4.9,4,4,4.9,4,6v20c0,1.1,0.9,2,2,2h20c1.1,0,2-0.9,2-2V6C28,4.9,27.1,4,26,4z M26,26H6V12h20V26z M26,10H6V6h4v2h2V6h8v2h2V6h4V10z"></path></svg><span>12/15/2024</span></div></div><div class="card-footer"><a href="#" class="continue-btn" onclick="showIframe()">Proceed</a></div></div>
<div class="card"><img src="https://github.com/WebAttach/WebAttach/blob/fd2f9b87483893e7769f07d9f82a4137db73324e/panel_3.jpg?raw=true" alt="Legacy Report"><div class="card-content"><h3>Workflow</h3><div class="due-date"><svg class="calendar-icon" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 32 32" aria-hidden="true"><path d="M26,4h-4V2h-2v2h-8V2h-2v2H6C4.9,4,4,4.9,4,6v20c0,1.1,0.9,2,2,2h20c1.1,0,2-0.9,2-2V6C28,4.9,27.1,4,26,4z M26,26H6V12h20V26z M26,10H6V6h4v2h2V6h8v2h2V6h4V10z"></path></svg><span>12/15/2024</span></div></div><div class="card-footer"><a href="#" class="continue-btn" onclick="showIframe()">Proceed</a></div></div>
    </div>`;
                document.getElementById('main-section').innerHTML = panh; // Assign the HTML string to innerHTML
            }

        </script>
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
          <a href="#" event.preventDefault();">Add Roles</a><br>
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
    
@app.route('/maps')
def maps():
    try:
        # Replace with your ASHX endpoint URL
        ashx_url = "https://earth.google.com/earth/d/1WqAG7imU2pofn12dq-kDE4NoyywNTQ8I?usp=sharing"
        # Redirect to ASHX URL in a new tab
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Viewer</title>
            <script>
                window.onload = function() {{
                    // Open the ASHX URL in a new tab
                    window.open("{ashx_url}", "_blank");
                }};
            </script>
        </head>
        <body>
            <h3>Opening Maps</h3>
        </body>
        </html>
        """
    except Exception as e:
        return jsonify({"error": f"Failed to connect to ASHX: {str(e)}"})
 
@app.route('/erp')
def erp():
    try:
        # Replace with your ASHX endpoint URL
        ashx_url = "https://workflow-viewer.odoo.com/odoo"
        # Redirect to ASHX URL in a new tab
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Viewer</title>
            <script>
                window.onload = function() {{
                    // Open the ASHX URL in a new tab
                    window.open("{ashx_url}", "_blank");
                }};
            </script>
        </head>
        <body>
            <h3>Opening Viewer...featuring Screens, Forms, and Reports with improved functionality</h3>
        </body>
        </html>
        """
    except Exception as e:
        return jsonify({"error": f"Failed to connect to erp: {str(e)}"})
 

@app.route("/")
def hello_world():
    return "Hello, World! This is a Dockerized Flask app deployed on Render on 1/21/2025 937am"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
