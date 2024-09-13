from flask import Flask, render_template, request, redirect, flash
import subprocess

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Index page
@app.route('/')
def index():
    return render_template('index.html')

# Reset Password page
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash("Passwords do not match!")
            return redirect('/reset_password')

        # Change password on Windows
        try:
            subprocess.run(['net', 'user', username, new_password], check=True)
            flash("Password reset successful!")
        except subprocess.CalledProcessError:
            flash("Failed to reset password.")
        return redirect('/reset_password')
    
    return render_template('reset_password.html')

# Create User page
@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        permissions = request.form.getlist('permissions')

        if new_password != confirm_password:
            flash("Passwords do not match!")
            return redirect('/create_user')

        # Create the user on Windows
        try:
            subprocess.run(['net', 'user', new_username, new_password, '/add'], check=True)
            for permission in permissions:
                subprocess.run(['net', 'localgroup', permission, new_username, '/add'], check=True)
            flash(f"User {new_username} created successfully!")
        except subprocess.CalledProcessError:
            flash(f"Failed to create user {new_username}.")
        return redirect('/create_user')

    return render_template('create_user.html')

if __name__ == '__main__':
    app.run(debug=True, host='192.168.17.109', port=5000)

