from flask import Flask, render_template, request, redirect, session, url_for
import MySQLdb
from config import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db = MySQLdb.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
cursor = db.cursor()

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        if user:
            session['user'] = user[1]
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        db.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM customers")
    total_customers = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]
    return render_template('dashboard.html', products=total_products, customers=total_customers, orders=total_orders)

@app.route('/products')
def products():
    cursor.execute("SELECT * FROM products")
    items = cursor.fetchall()
    return render_template('products.html', items=items)

@app.route('/customers')
def customers():
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    return render_template('customers.html', customers=customers)

@app.route('/orders')
def orders():
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    return render_template('orders.html', orders=orders)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# ===================== Product CRUD =====================
@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        cursor.execute("INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)", (name, price, quantity))
        db.commit()
        return redirect('/products')
    return render_template('product_form.html', action='Add')

@app.route('/product/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        cursor.execute("UPDATE products SET name=%s, price=%s, quantity=%s WHERE id=%s", (name, price, quantity, id))
        db.commit()
        return redirect('/products')
    cursor.execute("SELECT * FROM products WHERE id=%s", (id,))
    product = cursor.fetchone()
    return render_template('product_form.html', action='Edit', product=product)

@app.route('/product/delete/<int:id>')
def delete_product(id):
    cursor.execute("DELETE FROM products WHERE id=%s", (id,))
    db.commit()
    return redirect('/products')


# ===================== Customer CRUD =====================
@app.route('/customer/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        cursor.execute("INSERT INTO customers (name, phone, email) VALUES (%s, %s, %s)", (name, phone, email))
        db.commit()
        return redirect('/customers')
    return render_template('customer_form.html', action='Add')

@app.route('/customer/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        cursor.execute("UPDATE customers SET name=%s, phone=%s, email=%s WHERE id=%s", (name, phone, email, id))
        db.commit()
        return redirect('/customers')
    cursor.execute("SELECT * FROM customers WHERE id=%s", (id,))
    customer = cursor.fetchone()
    return render_template('customer_form.html', action='Edit', customer=customer)

@app.route('/customer/delete/<int:id>')
def delete_customer(id):
    cursor.execute("DELETE FROM customers WHERE id=%s", (id,))
    db.commit()
    return redirect('/customers')


# ===================== Order CRUD =====================
@app.route('/order/add', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        cursor.execute("INSERT INTO orders (customer_id, product_id, quantity) VALUES (%s, %s, %s)", (customer_id, product_id, quantity))
        db.commit()
        return redirect('/orders')
    cursor.execute("SELECT id FROM customers")
    customers = cursor.fetchall()
    cursor.execute("SELECT id FROM products")
    products = cursor.fetchall()
    return render_template('order_form.html', customers=customers, products=products)

@app.route('/order/delete/<int:id>')
def delete_order(id):
    cursor.execute("DELETE FROM orders WHERE id=%s", (id,))
    db.commit()
    return redirect('/orders')

# ===================== Supplier CRUD =====================
@app.route('/suppliers')
def suppliers():
    cursor.execute("SELECT * FROM suppliers")
    data = cursor.fetchall()
    return render_template('suppliers.html', suppliers=data)

@app.route('/supplier/add', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        cursor.execute("INSERT INTO suppliers (name, contact) VALUES (%s, %s)", (name, contact))
        db.commit()
        return redirect('/suppliers')
    return render_template('supplier_form.html', action='Add')

@app.route('/supplier/edit/<int:id>', methods=['GET', 'POST'])
def edit_supplier(id):
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        cursor.execute("UPDATE suppliers SET name=%s, contact=%s WHERE id=%s", (name, contact, id))
        db.commit()
        return redirect('/suppliers')
    cursor.execute("SELECT * FROM suppliers WHERE id=%s", (id,))
    supplier = cursor.fetchone()
    return render_template('supplier_form.html', action='Edit', supplier=supplier)

@app.route('/supplier/delete/<int:id>')
def delete_supplier(id):
    cursor.execute("DELETE FROM suppliers WHERE id=%s", (id,))
    db.commit()
    return redirect('/suppliers')


# ===================== Inventory CRUD =====================
@app.route('/inventory')
def inventory():
    cursor.execute("SELECT * FROM inventory")
    data = cursor.fetchall()
    return render_template('inventory.html', inventory=data)

@app.route('/inventory/add', methods=['GET', 'POST'])
def add_inventory():
    if request.method == 'POST':
        product_name = request.form['product_name']
        stock = request.form['stock']
        cursor.execute("INSERT INTO inventory (product_name, stock) VALUES (%s, %s)", (product_name, stock))
        db.commit()
        return redirect('/inventory')
    return render_template('inventory_form.html', action='Add')

@app.route('/inventory/edit/<int:id>', methods=['GET', 'POST'])
def edit_inventory(id):
    if request.method == 'POST':
        product_name = request.form['product_name']
        stock = request.form['stock']
        cursor.execute("UPDATE inventory SET product_name=%s, stock=%s WHERE id=%s", (product_name, stock, id))
        db.commit()
        return redirect('/inventory')
    cursor.execute("SELECT * FROM inventory WHERE id=%s", (id,))
    item = cursor.fetchone()
    return render_template('inventory_form.html', action='Edit', item=item)

@app.route('/inventory/delete/<int:id>')
def delete_inventory(id):
    cursor.execute("DELETE FROM inventory WHERE id=%s", (id,))
    db.commit()
    return redirect('/inventory')


# ===================== Sales CRUD =====================
@app.route('/sales')
def sales():
    cursor.execute("SELECT * FROM sales")
    data = cursor.fetchall()
    return render_template('sales.html', sales=data)

@app.route('/sale/add', methods=['GET', 'POST'])
def add_sale():
    if request.method == 'POST':
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        cursor.execute("INSERT INTO sales (product_id, quantity) VALUES (%s, %s)", (product_id, quantity))
        db.commit()
        return redirect('/sales')
    cursor.execute("SELECT id FROM products")
    products = cursor.fetchall()
    return render_template('sale_form.html', products=products)

@app.route('/sale/delete/<int:id>')
def delete_sale(id):
    cursor.execute("DELETE FROM sales WHERE id=%s", (id,))
    db.commit()
    return redirect('/sales')


if __name__ == '__main__':
    app.run(debug=True)
