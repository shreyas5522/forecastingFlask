app = Flask(__name__)

@app.route('/')
def home():
    name = request.args.get("name", "World")
    return render_template('index.html')
@app.route('/about')
def hello2():
    return render_template('about.html')

app.run(debug=True)