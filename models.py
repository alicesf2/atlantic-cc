from app import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer(), primary_key=True)
    slug = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    dek = db.Column(db.String(), nullable=False)
    published_date = db.Column(db.DateTime(), nullable=False)
    canonical_url = db.Column(db.String(), nullable=False)
    word_count = db.Column(db.String(), nullable=False)
    tags = db.Column(db.String())
    embeds = db.Column(db.String())

    def __init__(self, slug, title, dek, published_date, canonical_url, word_count, tags, embeds):
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

    id = db.Column(db.Integer(), primary_key=True)
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

    id = db.Column(db.Integer(), primary_key=True)
    slug = db.Column(db.String(), nullable=False)

    def __init__(self, slug):
        self.slug = slug

    def __repr__(self):
        return '<id {}>'.format(self.id)
