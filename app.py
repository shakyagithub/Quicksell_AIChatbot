from flask import Flask, request, render_template
import os
from rapidfuzz import process
import pdfplumber

app = Flask(__name__)

# Folder to store uploaded PDFs
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Function to extract text from a PDF
def extract_pdf_content(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


# Home Route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get file and query from the form
        file = request.files.get("pdf")
        query = request.form.get("query")

        # Validate uploaded file
        if file and file.filename.endswith(".pdf"):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)  # Save the file to uploads folder

            # Extract text and search for query
            content = extract_pdf_content(file_path)
            matches = process.extract(query, content.split("\n"), limit=1)
            result = matches[0][0] if matches else "No match found."

            return render_template("index.html", query=query, result=result)

    return render_template("index.html", query="", result="")


# Run the application
if __name__ == "__main__":
    app.run(debug=True)
