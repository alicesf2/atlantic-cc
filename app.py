from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/afang8"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# MODELS


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.String(), primary_key=True)
    slug = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    dek = db.Column(db.String(), nullable=False)
    published_date = db.Column(db.DateTime(), nullable=False)
    canonical_url = db.Column(db.String(), nullable=False)
    word_count = db.Column(db.String(), nullable=False)
    tags = db.Column(db.String())
    embeds = db.Column(db.String())

    def __init__(self, article_id, slug, title, dek, published_date, canonical_url, word_count, tags, embeds):
        self.id = article_id
        self.slug = slug
        self.title = title
        self.dek = dek
        self.published_date = published_date
        self.canonical_url = canonical_url
        self.word_count = word_count
        self.tags = tags
        self.embeds = embeds

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Art(db.Model):
    __tablename__ = 'art'

    id = db.Column(db.String(), primary_key=True)
    art_type = db.Column(db.String(), nullable=False)
    article_id = db.Column(db.Integer(), db.ForeignKey(
        'article.id'), nullable=False)

    def __init__(self, art_type, article_id):
        self.art_type = art_type
        self.article_id = article_id

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.String(), primary_key=True)
    slug = db.Column(db.String(), nullable=False)

    def __init__(self, slug):
        self.slug = slug

    def __repr__(self):
        return '<id {}>'.format(self.id)

# ROUTES


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/articles', methods=['GET', 'POST', 'PUT'])
def get_articles():
    if request.method == 'GET':
        articles = Article.query.all()
        results = [
            {
                "id": article.id,
                "slug": article.slug,
                "title": article.title,
                "dek": article.dek,
                "published_date": article.published_date,
                "canonical_url": article.canonical_url,
                "word_count": article.word_count,
                "tags": article.tags,
                "embeds": article.embeds
            } for article in articles
        ]

        return {"count": len(articles), "articles": results}

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_article = Article(
                article_id=data['id'],
                slug=data['slug'],
                title=data['title'],
                dek=data['dek'],
                published_date=data['published_date'],
                canonical_url=data['canonical_url'],
                word_count=data['word_count'],
                tags=data['tags'],
                embeds=data['embeds'])
            db.session.add(new_article)
            db.session.commit()
            return {"message": f"Article {new_article.title} has been created successfully."}
        else:
            return {"error": "The request is not in JSON format."}


if __name__ == '__main__':
    app.run()
