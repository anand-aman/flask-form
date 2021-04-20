from flask import Flask, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
db = SQLAlchemy(app)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    nickname = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.String(200), nullable=False)
    review = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Review ' + str(self.id)


@app.route('/')
def welcome():
    return '<h2>Todo App: <br>/add --> to add data  <br>/reviews --> to see the list</h2>'


@app.route('/add', methods=["POST", "GET"])
def add_review():
    if request.method == "POST":
        review_rating = request.form['rating']
        review_nickname = request.form['nickname']
        review_summary = request.form['summary']
        review_detail = request.form['review']

        # For SQLite Database
        new_review = Review(
            rating=review_rating,
            nickname=review_nickname,
            summary=review_summary,
            review=review_detail
        )

        db.session.add(new_review)
        db.session.commit()

    return render_template('form.html')


@app.route('/reviews')
def get_reviews():
    all_reviews = Review.query.order_by(Review.date).all()
    return render_template('reviews.html', reviews=all_reviews)


@app.route('/reviews/delete/<int:review_id>')
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    return redirect('/reviews')


@app.route('/reviews/api')
def get_reviews_api():
    review_list = []
    reviews = Review.query.all()
    for review in reviews:
        review_list.append({
            "id": review.id,
            "rating": review.rating,
            "nickname": review.nickname,
            "summary": review.summary,
            "review": review.review
        })

    return jsonify(review_list)


# @app.route('/todo/<int:index>', methods=['POST'])
# def delete_element(index):
#     if index < len(reviews):
#         del reviews[index]
#     return render_template('reviews.html', todoList=reviews, size=len(reviews))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
