from flask import Flask
from flask import render_template, redirect, url_for
from flask import request
from api import *

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		lender = request.form['lender']
		borrower = request.form['borrower']
		amount = request.form['amount']
		inputTransaction(name=lender, to_whom=borrower, amount=amount )
		return redirect(url_for('index'))
 
	
	return render_template('index.html')

@app.route('/checking', methods=['GET'])
def check():
	results = check_blockchain()
	return render_template('index.html', results=results)

if __name__ == '__main__':
	app.run(debug=True)