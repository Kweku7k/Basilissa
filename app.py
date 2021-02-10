from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title = 'Basillisa')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/maps')
def maps():
    return render_template('maps.html')

@app.route('/explore/<string:itemname>')
def explore(itemname):
    print(itemname)
    return render_template('explore.html')

@app.route('/branches')
def branches():
    return render_template('branches.html')

if __name__ == '__main__':
    app.run(debug=True)