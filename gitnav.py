from flask import Flask, render_template_string, request
import sqlite3

app = Flask(__name__)

DB_NAME = 'nav.nv'

# Initialize the database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS commands (id INTEGER PRIMARY KEY,commandtitle TEXT,commandtype TEXT,commandstr TEXT,commandlog TEXT)""")
    conn.commit()
    conn.close()

init_db()

# HTML Template for the simple interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analyst Navigator</title>
    <style>body { font-family: Arial, sans-serif; margin: 0; padding: 0; }.container { padding: 20px; max-width: 800px; margin: auto; }textarea { width: 100%; height: 100px; margin-bottom: 10px; }button { padding: 10px 20px; font-size: 16px; cursor: pointer; }pre { background: #f4f4f4; padding: 10px; border: 1px solid #ddd; }</style>
    <style>body { font-family: Arial, sans-serif; margin: 0; padding: 0; box-sizing: border-box;overflow-x: hidden;} .top-bar { background-color: #222; color: white; padding: 10px; border-radius: 10px 10px 0 0;display: flex;justify-content: space-between;align-items: center;}.user-circle {width: 40px;height: 40px;background-color: #b22222;color: #fff;border-radius: 50%;display: flex;justify-content: center;align-items: center;font-weight: bold;font-size: 16px;cursor: pointer;} .left-section { background-color: #e0e0e0; padding: 10px; width: 20%; float: left; height: 100vh;box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);}.left-section a {text-decoration: none; color: inherit; cursor: pointer; } .main-section { padding: 10px; margin-left: 20%; overflow: hidden; }.bottom-bar {background-color: #222;color: white;padding: 5px; border-radius: 0 0 10px 10px; position: fixed;bottom: 0;width: 100%;text-align: center;font-size: 12px;z-index: 10;}button { padding: 3px 5px; background-color: #3a7bd5; color: white; border: none; border-radius: 5px; cursor: pointer; }button:hover { background-color: #305b94; }.hidden{display:none}.show{display:block}</style>
    <style>.panel-container {display: flex;justify-content: space-evenly;align-items: center;margin: 50px;}.card {background-color: #ffffff;border-radius: 15px;box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);overflow: hidden;width: 240px;text-align: center;}.card img {width: 100%;height: 160px;object-fit: cover;}.card-content {padding: 15px;}.card h3 {font-size: 18px;margin: 15px 0 10px;color: #333;}.due-date {display: flex;align-items: center;justify-content: center;color: #777;font-size: 14px;margin-bottom: 10px;}.calendar-icon {margin-right: 5px;width: 16px;height: 16px;}.card-footer {background-color: #444;padding: 10px;border-radius: 0 0 15px 15px;text-align: center;}.card-footer .continue-btn { color: #fff; text-decoration: none;font-size: 16px; font-weight: bold;display: block;width: 100%; padding: 10px 0; cursor: pointer; border-radius: 0 0 15px 15px;margin: 0;}.card-footer .continue-btn:hover {background-color: #666;text-decoration: underline;}</style>
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
        <div class="container">
            <h4>Request Handler</h4>
            <textarea id="aql-input" placeholder="Enter your Analyst Request here Ex select * from commands, show viewer, fetch glba"></textarea>
            <button onclick="executeSQL()">Dispatch Request</button>
            <pre id="output">Response will appear here</pre>
        </div>
    </div>
    <div class="bottom-bar">
             <input type=\"text\" id=\"command-input\" >
             <button onclick=\"sendCommand()\">Send</button>
    </div>
    <script>
        async function executeSQL() {
            const sqlInput = document.getElementById('aql-input').value.trim();
            const output = document.getElementById('output');

            if (!sqlInput) {
                output.textContent = "Error: SQL command cannot be empty.";
                return;
            }

            output.textContent = "Processing...";

            try {
                if(sqlInput.startsWith('select '))
                {
                const response = await fetch('/execute', {
                    method: 'POST',
                    headers: { 'Content-Type': 'text/plain' },
                    body: sqlInput
                });

                const result = await response.text(); // Expect plain text response
                output.textContent = result;
                }
                else if(sqlInput.startsWith('show '))
                {
                     window.open('/show', '_blank');
                     output.textContent = "";
                }
                else if(sqlInput.startsWith('fetch '))
                {
                    output.textContent = "Bulk Fetch here";
                }
                else if(sqlInput.startsWith('tasks '))
                {
                     showTasks();
                }
                else
                {

                }
            } catch (error) {
                output.textContent = "Error: " + error.message;
            }
        }
        async function showTasks() {
            var panh = `<div class="panel-container" id="panel-container">
               <div class="card"><img src="https://github.com/WebAttach/WebAttach/blob/fd2f9b87483893e7769f07d9f82a4137db73324e/panel_1.jpg?raw=true" alt="Legacy Report"><div class="card-content"><h3>Reports</h3><div class="due-date"><svg class="calendar-icon" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 32 32" aria-hidden="true"><path d="M26,4h-4V2h-2v2h-8V2h-2v2H6C4.9,4,4,4.9,4,6v20c0,1.1,0.9,2,2,2h20c1.1,0,2-0.9,2-2V6C28,4.9,27.1,4,26,4z M26,26H6V12h20V26z M26,10H6V6h4v2h2V6h8v2h2V6h4V10z"></path></svg><span>12/15/2024</span></div></div><div class="card-footer"><a href="#" class="continue-btn" onclick="showIframe()">Proceed</a></div></div>
               <div class="card"><img src="https://github.com/WebAttach/WebAttach/blob/fd2f9b87483893e7769f07d9f82a4137db73324e/panel_2.jpg?raw=true" alt="Legacy Report"><div class="card-content"><h3>Forms</h3><div class="due-date"><svg class="calendar-icon" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 32 32" aria-hidden="true"><path d="M26,4h-4V2h-2v2h-8V2h-2v2H6C4.9,4,4,4.9,4,6v20c0,1.1,0.9,2,2,2h20c1.1,0,2-0.9,2-2V6C28,4.9,27.1,4,26,4z M26,26H6V12h20V26z M26,10H6V6h4v2h2V6h8v2h2V6h4V10z"></path></svg><span>12/15/2024</span></div></div><div class="card-footer"><a href="#" class="continue-btn" onclick="showIframe()">Proceed</a></div></div>
                <div class="card"><img src="https://github.com/WebAttach/WebAttach/blob/fd2f9b87483893e7769f07d9f82a4137db73324e/panel_3.jpg?raw=true" alt="Legacy Report"><div class="card-content"><h3>Workflow</h3><div class="due-date"><svg class="calendar-icon" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 32 32" aria-hidden="true"><path d="M26,4h-4V2h-2v2h-8V2h-2v2H6C4.9,4,4,4.9,4,6v20c0,1.1,0.9,2,2,2h20c1.1,0,2-0.9,2-2V6C28,4.9,27.1,4,26,4z M26,26H6V12h20V26z M26,10H6V6h4v2h2V6h8v2h2V6h4V10z"></path></svg><span>12/15/2024</span></div></div><div class="card-footer"><a href="#" class="continue-btn" onclick="showIframe()">Proceed</a></div></div>
            </div>`;
           document.querySelector(".main-section").innerHTML = panh; 
        }	
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/show')
def viewer():
    try:
        # Replace with your ASHX endpoint URL
        ashx_url = "https://www.google.com"
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
        return jsonify({"error": f"Failed to connect to ASHX: {str(e)}"})

@app.route('/execute', methods=['POST'])
def execute_sql():
    sql_query = request.data.decode().strip()  # Get raw SQL query from request body

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        if sql_query.lower().startswith("select"):
            cursor.execute(sql_query)
            results = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]

            # Format results as a table-like structure
            formatted_results = ', '.join(column_names) + '\n'
            formatted_results += '\n'.join([', '.join(map(str, row)) for row in results])

            conn.close()
            return formatted_results
        else:
            cursor.execute(sql_query)
            conn.commit()
            affected_rows = cursor.rowcount
            conn.close()
            return f"Query executed successfully. Rows affected: {affected_rows}"
    except sqlite3.Error as e:
            return f"SQL Error: {str(e)}", 400

if __name__ == '__main__':
    app.run(debug=True)
