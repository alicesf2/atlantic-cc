from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/postgres"
db = SQLAlchemy(app)

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
    article_id = db.Column(db.String(), db.ForeignKey(
        'articles.id'), nullable=False)

    def __init__(self, art_id, art_type, article_id):
        self.id = art_id
        self.art_type = art_type
        self.article_id = article_id

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.String(), primary_key=True)
    slug = db.Column(db.String(), nullable=False)

    def __init__(self, author_id, slug):
        self.id = author_id
        self.slug = slug

    def __repr__(self):
        return '<id {}>'.format(self.id)


class ArticleAuthor(db.Model):
    __tablename__ = 'articles_authors'

    article_id = db.Column(db.String(), db.ForeignKey(
        'articles.id'), nullable=False)
    author_id = db.Column(db.String(), db.ForeignKey(
        'authors.id'), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint(
            article_id, author_id,
        ),
    )

    def __init__(self, article_id, author_id):
        self.article_id = article_id,
        self.author_id = author_id

    def __repr__(self):
        return '<id {}>'.format(self.id)


# ROUTES


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/art', methods=['GET'])
def get_art():
    art = Art.query.all()
    results = [
        {
            "id": item.id,
            "type": item.art_type
        } for item in art
    ]
    return {"count": len(art), "art": results}


@app.route('/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    results = [
        {
            "id": author.id,
            "slug": author.slug
        } for author in authors
    ]
    return {"count": len(authors), "authors": results}


@app.route('/articles', methods=['GET', 'POST', 'PUT'])
def articles():
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

            # update article if article already exists
            articles = Article.query.all()
            found_article = None
            for article in articles:
                if article.id == data['id'] and article.canonical_url == data['canonical_url']:
                    found_article = article
                    break
            if found_article:
                found_article.slug = data['slug']
                found_article.title = data['title']
                found_article.dek = data['dek']
                found_article.published_date = data['published_date']
                found_article.word_count = data['word_count']
                found_article.tags = data['tags']
                found_article.embeds = data['embeds']
                db.session.commit()
                return {"message": f"Article {found_article.id} has been updated successfully."}
            else:
                # create new article with given id and canonical_url
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

                # update art, authors, and articleauthors
                new_art = Art(
                    art_id=data['lead_art']['id'],
                    art_type=data['lead_art']['type'],
                    article_id=data['id'])
                db.session.add(new_art)
                db.session.commit()

                authors = []
                article_authors = []
                for author in data['authors']:
                    authors.append(
                        Author(author_id=author['id'], slug=author['slug']))
                    article_authors.append(ArticleAuthor(
                        article_id=data['id'], author_id=author['id']))
                db.session.bulk_save_objects(authors)
                db.session.commit()
                db.session.bulk_save_objects(article_authors)
                db.session.commit()
                return {"message": f"Article {new_article.id} has been created successfully."}
        else:
            return {"error": "The request is not in JSON format."}


if __name__ == '__main__':
    app.run()
