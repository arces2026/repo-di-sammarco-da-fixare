>>> scarpe_objects = [Scarpe(**data) for data in scarpe_data] #convertire dizionari in istanze di Scarpe
>>> Scarpe.objects.bulk_create(scarpe_objects)

docker exec -it django-backend python manage.py dumpdata > dump.json

# Carica TUTTI i dati dal file
python manage.py loaddata dump.json

# Oppure usa sed per rimuovere i caratteri non stampabili
sed 's/^[^a-zA-Z]*//' dump_vue_django.sql > dump_pulito.sql