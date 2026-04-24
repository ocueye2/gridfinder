from flask import Flask, render_template, request, Response, redirect, url_for # Added Response
import submod.imagegen as image
import submod.dbman as dbman
import json
import ast
from waitress import serve



app = Flask(__name__,"/static","static")

@app.route("/", methods=['GET'])
def index():
    return render_template("home.html")

@app.route("/create", methods=['GET'])
def createdir():
    return render_template("create.html")

@app.route("/item/<value>")
def itempage(value):
    if value.startswith("g"):
        value = int(value.removeprefix("g"))
        data = dbman.grid.getdata(value)
        return render_template("item.html",item={"id":value,"name":data[1],"type":"item","isitem":False,"size":data[2]})
    else:
        data = dbman.item.getdata(value)
        plate = dbman.grid.getdata(data[2])
        return render_template("item.html",item={"id":value,"name":data[1],"type":"item","isitem":True,"plate":plate[1]})

@app.route("/delete/<value>")
def delete(value):
    if value.startswith("g"):
        dbman.grid.delete(int(value[1:]))
    else:
         dbman.item.delete(int(value))
    return redirect(url_for('index'))
    
# api
@app.route("/api/render", methods=['GET'])
def render(): # Removed 'self'
    # It's usually safer to provide defaults or cast these to int/float
    id = str(request.args.get('id'))
    if id.startswith("g"):
        id = int(id[1:])
        grid = dbman.grid.getdata(id)
        size = ast.literal_eval(grid[2])
        out = image.generate(size["x"], size["y"], [])
    else:
        id = int(id)
        item = dbman.item.getdata(id)
        grid = dbman.grid.getdata(item[2])
        size = ast.literal_eval(grid[2])
        points = ast.literal_eval(item[3])
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
            
        case "item":
            points = request.args.get('points')
            grid = request.args.get('gridid')
            name = request.args.get('name')
            dbman.item.create(name,grid,json.loads(points))
    return redirect(url_for('index'))
    
@app.route("/api/search", methods=['GET'])
def search():
    query = str(request.args.get('q'))
    if query.startswith("item:"):
        query = query.removeprefix("item: ")
        print("item: " + query)
        items = dbman.item.search(query)
        print(items)
        results = []
        for item in items:
            results.append({"id":item[0],"name":item[1]})
    elif query.startswith("grid:"):
        query = query.removeprefix("grid: ")
        items = dbman.grid.search(query)
        print(items)
        results = []
        for item in items:
            results.append({"id":"g" + str(item[0]),"name":item[1]})
    else:
        itemsa = dbman.item.search(query)
        results = []
        for item in itemsa:
            results.append({"id":item[0],"name":item[1]})

        itemsb = dbman.grid.search(query)
        for item in itemsb:
            results.append({"id":"g" + str(item[0]),"name":item[1]})

    return render_template("search.html",items=results)
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)