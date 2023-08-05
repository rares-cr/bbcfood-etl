from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Connect to the database
conn = psycopg2.connect(
    host="postgres",
    database="bbcdb",
    user="postgres",
    password="mysecretpassword",
    port="5432"
)

# route for getting all recipes
@app.route('/recipes')
def get_recipes():
    cur = conn.cursor()
    cur.execute("SELECT * FROM bbcfood.recipes")
    rows = cur.fetchall()
    recipes = []
    for row in rows:
        recipes.append({
            'uuid': row[0],
            'href': row[1],
            'title': row[2],
            'author': row[3],
            'category': row[4],
            'preparation_time': row[5],
            'cooking_time': row[6],
            'servings': row[7],
            'ingredients': row[8],
            'methods': row[9]
        })
    cur.close()
    return jsonify(recipes)

@app.route('/methods')
def get_methods():
    cur = conn.cursor()
    cur.execute("SELECT * FROM bbcfood.methods")
    rows = cur.fetchall()
    recipes = []
    for row in rows:
        recipes.append({
            'uuid': row[0],
            'href': row[1],
            'title': row[2],
            'step': row[3]
        })
    cur.close()
    return jsonify(recipes)


@app.route('/ingredients')
def get_ingredients():
    cur = conn.cursor()
    cur.execute("SELECT * FROM bbcfood.ingredients")
    rows = cur.fetchall()
    recipes = []
    for row in rows:
        recipes.append({
            'uuid': row[0],
            'href': row[1],
            'title': row[2],
            'ingredient': row[3]
        })
    cur.close()
    return jsonify(recipes)

# run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

