@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/api/list' , methods=['GET'])
def index():
    list = Content.query \
        .order_by(Content.name) \
        .all()
    content_schema = ContentSchema(many=True)
    return content_schema.dump(list).data    

@app.route('/api/cartoons/<int:cartoon_id>' , methods=['GET'])
def show_cartoon(cartoon_id):
    result = []
    for cartoon in cartoons:
        if cartoon['id'] == cartoon_id:
            result.append(cartoon)
    return jsonify(result)

@app.route('/api/cartoons/<int:cartoon_id>' , methods=['PUT'])
def update_cartoon(cartoon_id):
    return 'update'

@app.route('/api/cartoons/<int:cartoon_id>' , methods=['DELETE'])
def delete_cartoon(cartoon_id):
    return 'delete'


app = flask.Flask(__name__)
app.config["DEBUG"] = True



app.run()