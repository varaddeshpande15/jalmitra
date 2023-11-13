import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# For simplicity, we'll use an in-memory list as a placeholder for a database
main_table = []
admin_list = [
    {"admin1": "password1"},
    {"admin2": "password2"},
    # Add more admins as needed
]

user_list = [
    {"user1": "password1"},
    {"user2": "password2"},
    # Add more users as needed
]

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

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username exists in the admin list
        for admin in admin_list:
            if username in admin:
                # Check if the entered password matches the stored password
                if admin[username] == password:
                    # Redirect to the admin_dashboard page
                    return redirect(url_for('admin_dashboard'))

    # If username or password is incorrect, refresh the page
    return render_template('admin_login.html')


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password match any user in the user_list
        for user in user_list:
            if username in user and user[username] == password:
                # Store the username in the session to track the logged-in user
                session['username'] = username
                return redirect(url_for('user_dashboard'))

    return render_template('user_login.html')

@app.route('/user_dashboard')
def user_dashboard():
    # Retrieve the currently logged-in user from the session
    username = session.get('username', None)

    # Redirect to user_login if no user is logged in
    if not username:
        return redirect(url_for('user_login'))

    # Render the user_dashboard.html page with the logged-in user
    return render_template('user_dashboard.html', username=username)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    username = session.get('username', None)
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        severity = request.form['severity']
        location = request.form['location']
        reporter = username

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

    return render_template('upload.html', username=username)

@app.route('/user_signup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username is already taken
        for user in user_list:
            if username in user:
                return render_template('user_signup.html', message='Username already taken. Please choose another.')

        # If username is available, add the new user to the user_list
        user_list.append({username: password})

        # Redirect to user_login page after successful signup
        return redirect(url_for('user_login'))

    return render_template('user_signup.html', message=None)


# Add a route to serve uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)