# Django: Creare Endpoint API

## Indice

### Flow Base
1. [Model](#1-model-modelspy)
2. [Migrazione](#2-migrazione)
3. [View](#3-view-viewspy)
4. [URL dell'app](#4-url-dellapp-nome_appurlspy)
5. [URL del progetto](#5-url-del-progetto-progettourlspy)
6. [Risultato](#6-risultato)

### Flow con Django REST Framework
7. [Installazione DRF](#7-installazione-drf)
8. [Model DRF](#8-model-drf-modelspy)
9. [Migrazione DRF](#9-migrazione-drf)
10. [Serializer](#10-serializer-serializerspy)
11. [ViewSet](#11-viewset-viewspy)
12. [Router e URL dell app](#12-router-e-url-dell-app-nome_appurlspy)
13. [URL del progetto DRF](#13-url-del-progetto-drf-progettourlspy)
14. [Risultato DRF](#14-risultato-drf)

---

# Flow Base

```
Model → migrate → View → urls.py (app) → urls.py (progetto)
```

---

## 1. Model (`models.py`)

[↑ Torna all'indice](#indice)

Definisci la struttura dei dati.

```python
from django.db import models

class Articolo(models.Model):
    titolo = models.CharField(max_length=200)
    testo = models.TextField()
```

---

## 2. Migrazione

[↑ Torna all'indice](#indice)

Sincronizza il model con il database.

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 3. View (`views.py`)

[↑ Torna all'indice](#indice)

Legge i dati dal model e restituisce una risposta JSON.

```python
from django.http import JsonResponse
from .models import Articolo

def lista_articoli(request):
    dati = list(Articolo.objects.values())
    return JsonResponse(dati, safe=False)
```

---

## 4. URL dell'app (`nome_app/urls.py`)

[↑ Torna all'indice](#indice)

Mappa il path alla view.

```python
from django.urls import path
from . import views

urlpatterns = [
    path('articoli/', views.lista_articoli, name='lista-articoli'),
]
```

---

## 5. URL del progetto (`progetto/urls.py`)

[↑ Torna all'indice](#indice)

Include le URL dell'app nel progetto principale.

```python
from django.urls import path, include

urlpatterns = [
    path('api/', include('nome_tua_app.urls')),
]
```

---

## 6. Risultato

[↑ Torna all'indice](#indice)

Avvia il server:

```bash
python manage.py runserver
```

Visita: `http://localhost:8000/api/articoli/`

Risposta attesa:

```json
[
  { "id": 1, "titolo": "Primo articolo", "testo": "..." }
]
```

---
---

# Flow con Django REST Framework

```
Model → migrate → Serializer → ViewSet → Router → urls.py (progetto)
```

---

## 7. Installazione DRF

[↑ Torna all'indice](#indice)

```bash
pip install djangorestframework
```

```python
# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

---

## 8. Model DRF (`models.py`)

[↑ Torna all'indice](#indice)

Identico al flow base.

```python
from django.db import models

class Articolo(models.Model):
    titolo = models.CharField(max_length=200)
    testo = models.TextField()
```

---

## 9. Migrazione DRF

[↑ Torna all'indice](#indice)

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 10. Serializer (`serializers.py`)

[↑ Torna all'indice](#indice)

Converte le istanze del model in JSON (e viceversa). Gestisce anche la validazione in input.

```python
from rest_framework import serializers
from .models import Articolo

class ArticoloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articolo
        fields = '__all__'  # oppure lista esplicita: ['id', 'titolo', 'testo']
```

---

## 11. ViewSet (`views.py`)

[↑ Torna all'indice](#indice)

Un `ModelViewSet` genera automaticamente tutte le azioni CRUD: `list`, `retrieve`, `create`, `update`, `destroy`.

```python
from rest_framework import viewsets
from .models import Articolo
from .serializers import ArticoloSerializer

class ArticoloViewSet(viewsets.ModelViewSet):
    queryset = Articolo.objects.all()
    serializer_class = ArticoloSerializer
```

---

## 12. Router e URL dell app (`nome_app/urls.py`)

[↑ Torna all'indice](#indice)

Il `DefaultRouter` genera automaticamente tutti i path dal ViewSet registrato.

```python
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'articoli', views.ArticoloViewSet)

urlpatterns = router.urls
```

---

## 13. URL del progetto DRF (`progetto/urls.py`)

[↑ Torna all'indice](#indice)

```python
from django.urls import path, include

urlpatterns = [
    path('api/', include('nome_tua_app.urls')),
]
```

---

## 14. Risultato DRF

[↑ Torna all'indice](#indice)

Avvia il server:

```bash
python manage.py runserver
```

Il Router registra automaticamente questi endpoint:

| Metodo   | URL                   | Azione           |
|----------|-----------------------|------------------|
| GET      | `/api/articoli/`      | Lista tutti      |
| POST     | `/api/articoli/`      | Crea nuovo       |
| GET      | `/api/articoli/{id}/` | Dettaglio singolo|
| PUT      | `/api/articoli/{id}/` | Aggiorna completo|
| PATCH    | `/api/articoli/{id}/` | Aggiorna parziale|
| DELETE   | `/api/articoli/{id}/` | Elimina          |

DRF include anche una **Browsable API** visitabile dal browser su `http://localhost:8000/api/articoli/`.

