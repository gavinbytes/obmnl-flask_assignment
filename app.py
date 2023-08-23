# Import libraries
from flask import Flask, request, url_for, redirect, render_template

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
  {'id': 1, 'date': '2023-06-01', 'amount': 100},
  {'id': 2, 'date': '2023-06-02', 'amount': -200},
  {'id': 3, 'date': '2023-06-03', 'amount': 300},
]

# Read operation
@app.route('/')
def get_transactions():
  return render_template('transactions.html', transactions=transactions)

# Create operation
@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
  if request.method == 'GET':
    return render_template('form.html')
  
  transaction = {
    'id': len(transactions) + 1,
    'date': request.form['date'],
    'amount': float(request.form['amount']),
  }
  
  transactions.append(transaction)
  return redirect(url_for('get_transactions'))

# Update operation
@app.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
  if request.method == 'GET':
    for t in transactions:
      if t['id'] == transaction_id:
        return render_template('edit.html', transaction=t)
    
  #if POST
  date = request.form['date']
  amount = float(request.form['amount'])
  
  for t in transactions:
    if t['id'] == transaction_id:
      t['date'] = date
      t['amount'] = amount
      break
  return redirect(url_for('get_transactions'))
  
# Delete operation
@app.route('/delete/<int:transaction_id>')
def delete_transaction(transaction_id):
  for t in transactions:
    if t['id'] == transaction_id:
      transactions.remove(t)
      break
    
  return redirect(url_for('get_transactions'))

# Search operation
@app.route('/search', methods=['GET', 'POST'])
def search_transactions():
  if request.method == 'GET':
    return render_template('search.html')
  
  # if POST
  minamount = float(request.form['min_amount'])
  maxamount = float(request.form['max_amount'])
  filtered_transactions = []
  
  for t in transactions:
    if t['amount'] >= minamount and \
    t['amount'] <= maxamount:
      filtered_transactions.append(t)
  return render_template('transactions.html', transactions=filtered_transactions)

# Total Balance Operation
@app.route('/balance')
def total_balance():
  balance = 0
  for t in transactions:
    balance = balance + t['amount']
    
  return f'Total Balance: {balance}'


# Run the Flask app
if __name__ == '__main__':
  app.run(debug=True)