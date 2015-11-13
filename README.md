# reeltalk-backend

## Development

Create a clean `virtualenv`, then

    pip install -r requirements_base.txt

    python manage.py collectstatic

Create at least two users (temporary). For example:

    python manage.py createsuperuser

And finally,

    # initialize db and load fixture data
    python manage.py migrate


To run the backend:

    python manage.py runserver


Visit [/graphiql](http://localhost:8000/graphiql) for an interactive playground and documentation page.
