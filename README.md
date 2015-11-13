# reeltalk-backend

## Development

Create a clean `virtualenv`, then

    pip install -r requirements_base.txt

    python manage.py collectstatic

You'll get an error running this but that's fine

    python manage.py migrate

Now, create at least two users (temporary). For example:

    python manage.py createsuperuser

And finally, run migrate again

    python manage.py migrate

To run the backend:

    python manage.py runserver


Visit [/graphiql](http://localhost:8000/graphiql) for an interactive playground and documentation page.
