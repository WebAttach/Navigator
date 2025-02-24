from flask import Flask, render_template_string, send_from_directory, redirect, url_for
import os
import pdfplumber

app = Flask(__name__)

# Serve the PDF from the static folder
@app.route('/static/<filename>')
def serve_static_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

# Function to extract text from PDF
def extract_pdf_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

@app.route('/')
def index():
    # Simple layout with a header, left menu, and main content
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Fund Masters</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                height: 100vh;
            }
            .header, .footer {
                background-color: #222;
                color: white;
                padding: 10px;
                text-align: center;
            }
            .main-content {
                display: flex;
                height: 100%;
            }
            .left-section {
                width: 200px;
                background-color: #f4f4f4;
                padding: 10px;
                box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
            }
            .left-section a {
                text-decoration: none;
                color: black;
                display: block;
                padding: 5px;
            }
            .left-section a:hover {
                background-color: #ddd;
            }
            .right-section {
                flex: 1;
                padding: 20px;
                overflow-y: scroll;
            }
            .footer input {
                width: 80%;
                padding: 5px;
                margin-right: 10px;
            }
            .footer button {
                padding: 5px 10px;
                background-color: #444;
                color: white;
                border: none;
                cursor: pointer;
            }
            .footer button:hover {
                background-color: #555;
            }
            pre {
                white-space: pre-wrap;       /* CSS3 */
                white-space: -moz-pre-wrap;  /* Mozilla */
                white-space: -pre-wrap;      /* Opera 4-6 */
                word-wrap: break-word;       /* Internet Explorer 5.5+ */
            }
            textarea {
                width: 100%;
                height: 300px;
                padding: 10px;
                font-family: monospace;
                border: 1px solid #ccc;
                resize: none;
            }
        </style>
    </head>
    <body>

        <div class="header">
            <h1>Fund Masters</h1>
        </div>

        <div class="main-content">
            <div class="left-section">
                <h3>Menu</h3>
                <a href="#">Get Coaching</a>
                <a href="{{ url_for('serve_static_file', filename='SampleSummary.pdf') }}" target="_blank">View Funds</a>
                <a href="{{ url_for('shopping_cart') }}">Shop Solutions</a>
            </div>
            <div class="right-section">
                <h3>PDF Content:</h3>
                <!-- Textarea for PDF content, initially empty -->
                <textarea id="pdf-content" readonly></textarea>
            </div>
        </div>

        <div class="footer">
            <input type="text" id="command-input" placeholder="Enter command...">
            <button onclick="alert('Command sent')">Run Command</button>
        </div>

        <script>
            // JavaScript to load PDF content dynamically when the "Shop Solutions" link is clicked
            document.querySelector('a[href="{{ url_for('shopping_cart') }}"]').addEventListener('click', function(event) {
                event.preventDefault();  // Prevent default link behavior
                fetch('/shopping_cart')  // Fetch the content dynamically
                    .then(response => response.text())
                    .then(data => {
                        document.getElementById('pdf-content').value = data;  // Insert content into textarea
                    })
                    .catch(error => console.error('Error fetching PDF content:', error));
            });
        </script>

    </body>
    </html>
    """)

@app.route('/shopping_cart')
def shopping_cart():
    # Extract content from PDF when the shopping cart is clicked
    pdf_path = os.path.join(app.root_path, 'static', 'SampleSummary.pdf')
    pdf_content = extract_pdf_text(pdf_path)
    
    # Return the extracted content directly as plain text
    return pdf_content

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
