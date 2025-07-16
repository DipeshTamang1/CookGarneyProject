from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# MySQL config (adjust with your own settings)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'dipesh'
app.config['MYSQL_DB'] = 'recipe_db'

mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM recipes ORDER BY id DESC")
    recipes = cursor.fetchall()
    cursor.close()
    return render_template('index.html', recipes=recipes)

@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        recipe_id = request.form['id']
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']

        cursor = mysql.connection.cursor()
        try:
            cursor.execute(
                'INSERT INTO recipes (id, title, ingredients, instructions) VALUES (%s, %s, %s, %s)',
                (recipe_id, title, ingredients, instructions)
            )
            mysql.connection.commit()
            flash('Recipe added successfully!', 'success')
            return redirect(url_for('index'))
        except MySQLdb.IntegrityError:
            flash('Error: Recipe ID already exists. Please use a different ID.', 'danger')
            return render_template('add.html', id=recipe_id, title=title, ingredients=ingredients, instructions=instructions)
    else:
        return render_template('add.html')

@app.route('/view/<int:id>')
def view(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM recipes WHERE id = %s", (id,))
    recipe = cursor.fetchone()
    cursor.close()
    return render_template('view.html', recipe=recipe)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        cursor.execute("UPDATE recipes SET title=%s, ingredients=%s, instructions=%s WHERE id=%s",
                       (title, ingredients, instructions, id))
        mysql.connection.commit()
        cursor.close()
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM recipes WHERE id = %s", (id,))
    recipe = cursor.fetchone()
    cursor.close()
    return render_template('edit.html', recipe=recipe)

@app.route('/delete/<int:id>')
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM recipes WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
