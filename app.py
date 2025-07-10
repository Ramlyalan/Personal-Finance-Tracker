from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:YourNewPassword123%21@localhost/finance_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Transaction model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    type = db.Column(db.String(10))  # Income or Expense
    category = db.Column(db.String(50))
    date = db.Column(db.DateTime, default=datetime.utcnow)

# Home - show summary and transactions
@app.route('/')
def index():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    income = sum(t.amount for t in transactions if t.type == 'Income')
    expense = sum(t.amount for t in transactions if t.type == 'Expense')
    balance = income - expense
    return render_template('index.html', transactions=transactions, income=income, expense=expense, balance=balance)

# Add transaction
@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        type = request.form['type']
        category = request.form['category']
        new_t = Transaction(amount=amount, type=type, category=category)
        db.session.add(new_t)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_transaction.html')

# Delete transaction
@app.route('/delete/<int:id>')
def delete_transaction(id):
    t = Transaction.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)