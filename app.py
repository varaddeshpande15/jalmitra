import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

# For simplicity, we'll use an in-memory list as a placeholder for a database
main_table = []

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    # Generate data for the main table
    table_data = []
    for index, item in enumerate(main_table):
        # Generate URLs for the images
        image_url = url_for('uploaded_file', filename=item['image'])
        
        # Add more data for each row in the table
        table_data.append({
            'id': index + 1,
            'image': f'<img src="{image_url}" alt="Image" style="max-width: 100px; max-height: 100px;">',
            'problem_title': item['problem_title'],
            'severity': item['severity'],
            'location': item['location'],
            'reporter': item['reporter']
        })

    # Pass the data to the template
    return render_template('admin_dashboard.html', table_data=table_data)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        severity = request.form['severity']
        location = request.form['location']
        reporter = request.form['reporter']

        # Handle file upload
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Update main table with additional information
            main_table.append({
                'image': filename,
                'problem_title': title,
                'severity': severity,
                'location': location,
                'reporter': reporter
            })

            # Refresh the upload page
            return render_template('upload.html')

    return render_template('upload.html')

# Add a route to serve uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
