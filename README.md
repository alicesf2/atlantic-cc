# atlantic-cc

### Database Schema:
```
Article: {
    String id,
    String slug,
    String title,
    String dek,
    Date published_date,
    String canonical_url,
    Integer word_count,
    String tags,
    String embeds,
}

Art: {
    String id,
    String article_id,
    String art_type,
}

Author: {
    String id,
    String slug,
}

ArticleAuthor: {
    String article_id,
    String author_id
}

```
### Setup/Installation:
1. Activate the virtual environment
    `python3 -m pip install --user virtualenv`
    `python3 -m venv env`
    `source env/bin/activate`
2. Install the `requirements.txt` file
    `pip install -r requirements.txt`
3. Connect to local postgresql database (I used Postico for this: https://eggerapps.at/postico/docs/v1.0.3/install-postgresapp.html)
4. To run the Flask app, type `python app.py`

### What I was able to complete:
- GET requests for articles, art, and authors
- POST request for articles that handles adding new articles and updating existing ones
- Attempt to add new art, authors, and article_author relations to the database upon article creation


### What I would do if I had more time:
- I would display the lead_art id and array of author ids for each article in the GET /articles response
- I would debug the addition of art, authors, and article_author relations to the database (it was working somewhat initially, now it does not)
- I would add tests, irregularity detection, and dockerization of the app.
- I would separate out the code into different files (i.e. models.py for the object classes. I could not import the files properly so I put everything in app.py)