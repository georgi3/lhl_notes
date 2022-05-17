from flask import Flask, jsonify
from flask_restful import reqparse, Resource, Api

app = Flask(__name__)
api = Api(app)


class Greet(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location="args")
        args = parser.parse_args()
        name = args.get('name', None)

        if name:
            greeting = f'Hello {name}'
        else:
            greeting = f'Hello nameless'
        return jsonify(greeting=greeting)


api.add_resource(Greet, '/greet')


@app.route('/')
def home():
    return '<h1>Hello World</h1>'


if __name__ == '__main__':
    app.run(debug=False)
