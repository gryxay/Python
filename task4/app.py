from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def display_cafes():
    connection = sqlite3.connect('./database/database.db')
    cursor = connection.cursor()

    if request.method == 'POST':
        query = request.form.get('query', '')
        if query:
            cursor.execute("SELECT id, name, location FROM cafes WHERE name LIKE ? OR id IN "
                           "(SELECT cafeId FROM reviews WHERE author LIKE ?)", ('%' + query + '%', '%' + query + '%'))
        else:
            cursor.execute("SELECT id, name, location FROM cafes")
    else:
        query = request.args.get('query', '')
        if query:
            cursor.execute("SELECT id, name, location FROM cafes WHERE name LIKE ? OR id IN "
                           "(SELECT cafeId FROM reviews WHERE author LIKE ?)", ('%' + query + '%', '%' + query + '%'))
        else:
            cursor.execute("SELECT id, name, location FROM cafes")

    cafes = cursor.fetchall()
    connection.close()

    return render_template('cafes.html', cafes=cafes, query=query)


@app.route('/cafe/<int:cafe_id>')
def display_cafe_details(cafe_id):
    connection = sqlite3.connect('./database/database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM cafes WHERE id=?", (cafe_id,))
    cafe = cursor.fetchone()

    cursor.execute("SELECT * FROM reviews WHERE cafeId=?", (cafe_id,))
    reviews = cursor.fetchall()

    cursor.execute("SELECT * FROM beverages WHERE cafeId=?", (cafe_id,))
    beverages = cursor.fetchall()

    connection.close()
    return render_template('cafe_details.html', cafe=cafe, reviews=reviews, beverages=beverages)


@app.route('/delete_review/<int:cafe_id>/<int:review_id>', methods=['POST'])
def delete_review(cafe_id, review_id):
    connection = sqlite3.connect('./database/database.db')
    cursor = connection.cursor()

    cursor.execute("DELETE FROM reviews WHERE id=?", (review_id,))
    connection.commit()

    connection.close()
    return redirect(f'/cafe/{cafe_id}')


@app.route('/update_review/<int:cafe_id>/<int:review_id>', methods=['GET', 'POST'])
def update_review(cafe_id, review_id):
    if request.method == 'POST':
        author = request.form['author']
        rating = request.form['rating']
        description = request.form['description']
        date = request.form['date']

        connection = sqlite3.connect('./database/database.db')
        cursor = connection.cursor()

        cursor.execute("UPDATE reviews SET author=?, rating=?, description=?, date=? WHERE id=?",
                       (author, rating, description, date, review_id))
        connection.commit()
        connection.close()

        return redirect(f'/cafe/{cafe_id}')
    else:
        connection = sqlite3.connect('./database/database.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM reviews WHERE id=?", (review_id,))
        review = cursor.fetchone()

        connection.close()
        return render_template('update_review.html', review=review, review_id=review_id, cafe_id=cafe_id)


@app.route('/add_review/<int:cafe_id>', methods=['GET', 'POST'])
def add_review(cafe_id):
    if request.method == 'POST':
        author = request.form['author']
        rating = request.form['rating']
        description = request.form['description']
        date = request.form['date']

        connection = sqlite3.connect('./database/database.db')
        cursor = connection.cursor()

        cursor.execute("INSERT INTO reviews (cafeId, author, rating, description, date) VALUES (?, ?, ?, ?, ?)",
                       (cafe_id, author, rating, description, date))
        connection.commit()
        connection.close()

        return redirect(f'/cafe/{cafe_id}')
    else:
        return render_template('add_review.html', cafe_id=cafe_id)


if __name__ == '__main__':
    app.run(debug=True)
