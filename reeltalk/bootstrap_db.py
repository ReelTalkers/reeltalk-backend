import json
from datetime import datetime
import re

shows = []
people_list = []
all_the_people = {}
people_pk = 1
num_saved = 0

def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

with open('../omdbFull1115/omdbFullUTF8.txt', encoding='utf-8') as f:
    schema = []
    show_id = 1
    for i, show_string in enumerate(f):
        if num_saved % 10000 == 0 or i % 100000 == 0:
            print('Num Saved: {}, Num Processed: {}'.format(num_saved, i))
        if i == 0:
            schema = show_string.strip('\r\n').split('\t')[1:] # exclude ID
            schema = list(map(lambda field: field[0].lower() + field[1:], schema))
            schema = [field + 's' if field in ['director', 'writer'] else field for field in schema]
            continue

        fields = show_string.strip('\r\n').split('\t')[1:]
        if len(fields) != 21:
            continue

        show_fields = {}
        for i, field_name in enumerate(schema):
            snake_field_name = to_snake_case(field_name)
            field_value = fields[i]
            if len(field_value) > 0:
                show_fields[snake_field_name] = field_value
            elif field_name in ['directors', 'writers', 'cast']:
                show_fields[snake_field_name] = []
            else:
                show_fields[snake_field_name] = None

        if not show_fields['poster'] or not show_fields['imdb_rating'] or not show_fields['metacritic']:
            continue

        directors = show_fields['directors']
        if isinstance(directors, str):
            directors = [person.strip() for person in show_fields['directors'].split(',')]
        writers = show_fields['writers']
        if isinstance(writers, str):
            writers = [person.strip() for person in show_fields['writers'].split(',')]
        cast = show_fields['cast']
        if isinstance(cast, str):
            cast = [person.strip() for person in show_fields['cast'].split(',')]

        people = directors + writers + cast
        people_ids = {}
        for person in people:
            if person == '':
                continue
            if not all_the_people.get(person):
                all_the_people[people_pk] = person
                people_ids[person] = people_pk
                people_list.append({
                  "pk": people_pk,
                  "model": "reeltalk.person",
                  "fields": {
                    "full_name": person,
                    "created": str(datetime.now()).replace(' ', 'T'),
                    "edited": str(datetime.now()).replace(' ', 'T')
                    }
                })
                people_pk += 1

        show_fields['directors'] = [people_ids[person] for person in directors if person != '']
        show_fields['writers'] = [people_ids[person] for person in writers if person != '']
        show_fields['cast'] = [people_ids[person] for person in cast if person != '']
        show_fields['created'] = str(datetime.now()).replace(' ', 'T')
        show_fields['edited'] = str(datetime.now()).replace(' ', 'T')
        show_fields['banner'] = show_fields['poster']
        show_fields['imdb_rating'] = float(show_fields['imdb_rating']) if show_fields['imdb_rating'] is not None else None
        show_fields['imdb_votes'] = float(show_fields['imdb_votes']) if show_fields['imdb_votes'] is not None else None
        show_fields['metacritic'] = float(show_fields['metacritic']) if show_fields['metacritic'] is not None else None
        show = {
            "fields": show_fields,
            "model": "reeltalk.show",
            "pk": show_id
        }
        shows.append(show)
        show_id += 1

        num_saved += 1

with open('./fixtures/people.json', 'w', encoding='utf-8') as f:
    json.dump(people_list, f)

with open('./fixtures/shows.json', 'w', encoding='utf-8') as f:
    json.dump(shows, f)
