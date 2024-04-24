from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

# Function to save username, email, and password to a CSV file
def save_to_csv(username, email, password):
    try: 
        with open(r"C:\Users\harsha anand\Desktop\Miniproject\flask\static\uploads\user.csv", 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, email, password])
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return False 

# Function to check if username exists in the CSV file
def username_exists(username):
    with open(r"C:\Users\harsha anand\Desktop\Miniproject\flask\static\uploads\user.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username:
                return True
    return False

# Route to handle the login page
@app.route('/')
def login():
    return render_template("login.html")

# Route to handle the form submission
@app.route("/login", methods=['POST'])
def login_submit():
    username = request.form['username']
    password = request.form['password']

    # Check if the username exists and credentials match
    if username_exists(username):
        # Implement password checking logic here
        return redirect("/preview")  # Redirect to preview page on successful login
    else:
        return redirect("/register")  # Redirect to registration page if username doesn't exist or credentials don't match

# Route to handle the registration page
@app.route("/register")
def register():
    return render_template("register.html")

# Route to handle the registration form submission
@app.route("/register", methods=['POST'])
def register_submit():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    # Check if the username already exists
    if username_exists(username):
        print("Username Exist")
    else:
        save_to_csv(username, email, password)  # Save username, email, and password to CSV
    return redirect('/login')  # Redirect to login page after registration

# Route to handle the preview page
@app.route("/preview")
def preview():
    return render_template("preview.html")  

if __name__ == '__main__':
    app.run(debug=True)
