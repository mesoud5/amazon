from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta
import mysql.connector

# Function to connect to the MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="amazon",
        password="amazon123",
        database="amazon"
    )


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Define hardcoded admin and employee credentials
admin_username = "mesoud"
admin_password = "mesoud@123"
employee_username = "ekram"
employee_password = "ekram123"

# Define empty list to store sold products
sold_products = []


class Product:
    def __init__(self, id, name, category, quantity, buying_price, selling_price):
        self.id = id
        self.name = name
        self.category = category
        self.quantity = quantity
        self.buying_price = buying_price
        self.selling_price = selling_price

# Define routes
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if the entered username and password match the admin credentials
    if username == admin_username and password == admin_password:
        session['username'] = username
        session['role'] = 'admin'
        return redirect(url_for('admin_dashboard'))

    # Check if the entered username and password match the employee credentials
    elif username == employee_username and password == employee_password:
        session['username'] = username
        session['role'] = 'employee'
        return redirect(url_for('employee_dashboard'))

    # If the entered credentials do not match any predefined accounts, show an error message
    else:
        return render_template('login.html', error='Invalid credentials')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        if session['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif session['role'] == 'employee':
            return redirect(url_for('employee_dashboard'))
    else:
        return redirect(url_for('index'))


@app.route('/admin_dashboard')
def admin_dashboard():
    if 'username' in session and session['role'] == 'admin':
        # Connect to the database
        db_connection = connect_to_database()
        cursor = db_connection.cursor()

        try:
            # Fetch categories from the database
            cursor.execute("SELECT name FROM categories")
            categories = [row[0] for row in cursor.fetchall()]

            # Retrieve all sales data
            cursor.execute("SELECT * FROM sales_report")
            sales_data = cursor.fetchall()

        except Exception as e:
            # Handle any exceptions
            print("Error:", e)
            categories = []
            sales_data = []

        finally:
            # Close the cursor and database connection
            cursor.close()
            db_connection.close()

        return render_template('admin_dashboard.html', categories=categories, sales_data=sales_data)
    else:
        return redirect(url_for('index'))




@app.route('/employee_dashboard')
def employee_dashboard():
    if 'username' in session and session['role'] == 'employee':
        return render_template('employee_dashboard.html')
    else:
        return redirect(url_for('index'))

@app.route('/add_sale', methods=['POST'])
def add_sale_route():
    if 'username' in session and session['role'] == 'employee':
        product_name = request.form['product_name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        total = quantity * price
        sale_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get current date and time
        
        # Connect to the database
        db_connection = connect_to_database()
        cursor = db_connection.cursor()

        try:
            # Execute SQL query to insert the sale data into the sales_report table
            sql = "INSERT INTO sales_report (product_name, quantity, price, total, sale_date) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (product_name, quantity, price, total, sale_date))
            db_connection.commit()
            flash('Sale added successfully', 'success')
        except Exception as e:
            # Handle any exceptions
            print("Error:", e)
            flash('An error occurred while adding the sale', 'error')
        finally:
            # Close the cursor and database connection
            cursor.close()
            db_connection.close()

        return redirect(url_for('employee_dashboard'))
    else:
        return redirect(url_for('index'))





# Route to add a new category
@app.route('/add_category', methods=['POST'])
def add_category():
    if 'username' in session and session['role'] == 'admin':
        category_name = request.form['category_name']
        
        # Connect to the database
        db_connection = connect_to_database()
        cursor = db_connection.cursor()

        try:
            # Execute SQL query to insert the new category
            sql = "INSERT INTO categories (name) VALUES (%s)"
            cursor.execute(sql, (category_name,))
            db_connection.commit()
            flash('Category added successfully', 'success')
        except Exception as e:
            # Handle any exceptions
            print("Error:", e)
            flash('An error occurred while adding the category', 'error')
        finally:
            # Close the cursor and database connection
            cursor.close()
            db_connection.close()

        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('index'))
    
@app.route('/add_product', methods=['POST'])
def add_product_route():
    if 'username' in session and session['role'] == 'admin':
        product_name = request.form['product_name']
        category = request.form['category']
        quantity = int(request.form['quantity'])
        buying_price = float(request.form['buying_price'])
        selling_price = float(request.form['selling_price'])
        
        # Connect to the database
        db_connection = connect_to_database()
        cursor = db_connection.cursor()

        try:
            # Execute SQL query to insert the new product
            sql = "INSERT INTO products (name, category, quantity, buying_price, selling_price) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (product_name, category, quantity, buying_price, selling_price))
            db_connection.commit()
            flash('Product added successfully', 'success')
        except Exception as e:
            # Handle any exceptions
            print("Error:", e)
            flash('An error occurred while adding the product', 'error')
        finally:
            # Close the cursor and database connection
            cursor.close()
            db_connection.close()

        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('index'))


@app.route('/remove_product', methods=['POST'])
def remove_product():
    if 'username' in session and session['role'] == 'admin':
        product_id = request.form['product_id']
        
        # Connect to the database
        db_connection = connect_to_database()
        cursor = db_connection.cursor()

        try:
            # Execute SQL query to delete the product
            sql = "DELETE FROM products WHERE id = %s"
            cursor.execute(sql, (product_id,))
            db_connection.commit()
            flash('Product removed successfully', 'success')
        except Exception as e:
            # Handle any exceptions
            print("Error:", e)
            flash('An error occurred while removing the product', 'error')
        finally:
            # Close the cursor and database connection
            cursor.close()
            db_connection.close()

        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
