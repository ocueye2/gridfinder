from flask import Flask, render_template, request, Response # Added Response
import submod.imagegen as image
import submod.dbman as dbman
import json

app = Flask("gridfinder")

@app.route("/", methods=['GET'])
def index():
    return render_template("home.html")
    
# api
@app.route("/api/render", methods=['GET'])
def render(): # Removed 'self'
    # It's usually safer to provide defaults or cast these to int/float
    id = int(request.args.get('id'))
    item = dbman.item.getdata(id)
    grid = dbman.grid.getdata(item[2])
    size = json.loads(grid[2])
    points = json.loads(item[3])
    print(item)
    out = image.generate(size["x"], size["y"], points)
    
    return Response(out, mimetype='image/svg+xml')

@app.route("/api/create", methods=['GET'])
def create():
    typ = request.args.get('type')
    match typ:
        case "grid":
            xs = int(request.args.get('xs'))
            ys = int(request.args.get('ys'))
            name = request.args.get('name')
            dbman.grid.create(name,xs,ys)
            return "done"
        case "item":
            points = request.args.get('points')
            grid = request.args.get('gridid')
            name = request.args.get('name')
            dbman.item.create(name,grid,json.loads(points))
            return "done"
    
@app.route("/api/search", methods=['GET'])
def search():
    typ = request.args.get('q')
    return typ
if __name__ == "__main__":
    app.run(debug=True)