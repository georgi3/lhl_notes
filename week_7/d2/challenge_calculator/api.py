from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse


app = Flask(__name__)
api = Api(app)


class Calculator(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('action', type=str, location='args')
        parser.add_argument('x', type=int, location='args')
        parser.add_argument('y', type=int, location='args')
        args = parser.parse_args()
        action = args.get('action', '')
        x = args.get('x', 0)
        y = args.get('y', 0)
        if action == 'add':
            return jsonify(sum=x+y)
        elif action == 'substract':
            return jsonify(difference=x-y)
        elif action == 'multiply':
            return jsonify(product=x*y)
        elif action == 'divide':
            try:
                division = x / y
            except ZeroDivisionError as err:
                division = f'Error: {err}'
            return jsonify(division=division)
        return 'Start using it!'

api.add_resource(Calculator, '/calculator')

html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Calculator</title>
</head>
<body>
<h1>Welcome to my Calculator API</h1>
<h4>To proceed to calculator, click <a href="http://192.168.0.175:5678/calculator">here</a></h4>
<h2>Documentation</h2>
<ul>
  <li>url=http://192.168.0.175:5678/calculator&action=[add, subtract, multiply, divide]&x=int&y=int</li>
  <li><h3>Parameters</h3></li>
  <li>action, type=string, values(add, subtract, multiply, divide), Description: operation you would like to perform</li>
  <li>x, type=int, Description: first number</li>
  <li>y, type=int, Description: second number</li>
</ul>
</body>
</html>"""


@app.route('/')
def home():
    return html


if __name__ == '__main__':
    app.run(debug=True)  # host='0.0.0.0', port=5678)
