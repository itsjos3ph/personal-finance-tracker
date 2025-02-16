from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/finance.db'  # Database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db = SQLAlchemy(app)

# Transaction model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    date = db.Column(db.String(50), nullable=False)

# Home route: Display all transactions
@app.route('/')
def index():
    transactions = Transaction.query.all()  # Fetch all transactions
    return render_template('index.html', transactions=transactions)

# Add transaction route
@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        category = request.form['category']
        date = request.form['date']
        
        new_transaction = Transaction(name=name, amount=amount, category=category, date=date)
        db.session.add(new_transaction)
        db.session.commit()
        
        return redirect(url_for('index'))  # Redirect to the home page after adding

    return render_template('add_transaction.html')  # Show the form to add a transaction

# Delete transaction route
@app.route('/delete/<int:id>', methods=['POST'])
def delete_transaction(id):
    transaction = Transaction.query.get(id)
    if transaction:
        db.session.delete(transaction)
        db.session.commit()
    
    return redirect(url_for('index'))  # Redirect back to the home page

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
