import json
from datetime import datetime

shows = []
all_the_people = {}
people_pk = 1

with open('../omdbFull1115/omdbFullUTF8.txt', encoding='utf-8') as f:
    schema = []
    for i, show_string in enumerate(f):
        if i > 50:
            break
        if i == 0:
            schema = show_string.strip('\r\n').split('\t')[1:] # exclude ID
            schema = list(map(lambda field: field[0].lower() + field[1:], schema))
            schema = [field + 's' if field in ['director', 'writer'] else field for field in schema]
            continue
        fields = show_string.strip('\r\n').split('\t')[1:]
        if len(fields) != 21:
            continue
        show_fields = {field: fields[i] for i, field in enumerate(schema)}
        directors = [person.strip() for person in show_fields['directors'].split(',')]
        writers = [person.strip() for person in show_fields['writers'].split(',')]
        cast = [person.strip() for person in show_fields['cast'].split(',')]
        people = directors + writers + cast
        people_ids = {}
        for person in people:
            if person == '':
                continue
            print(person)
            if not all_the_people.get(person):
                all_the_people[people_pk] = person
                people_ids[person] = people_pk
                people_pk += 1

        show_fields['directors'] = [people_ids[person] for person in directors if person != '']
        show_fields['writers'] = [people_ids[person] for person in writers if person != '']
        show_fields['cast'] = [people_ids[person] for person in cast if person != '']
        show_fields['created'] = str(datetime.now()).replace(' ', 'T')
        show_fields['edited'] = str(datetime.now()).replace(' ', 'T')
        show = {
            "fields": show_fields,
            "model": "reeltalk.show",
            "pk": i
        }
        shows.append(show)

with open('./fixtures/shows.json', 'w', encoding='utf-8') as f:
    json.dump(shows, f, indent=4)
