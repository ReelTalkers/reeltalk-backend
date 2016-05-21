# reeltalk-backend

## Development

Create a clean `virtualenv`, then

    pip install -r requirements_base.txt

    python manage.py collectstatic

You'll get an error running this but that's fine

    python manage.py migrate

    python manage.py loaddata data_dump

To run the backend:

    python manage.py runserver


Make it available to CORS:

`export CORS_WHITELIST="localhost:<other_port_num>,localhost:<again>"`

And run it again


Visit [/graphiql](http://localhost:8000/graphiql) for an interactive playground and documentation page.
