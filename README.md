# Gradja

> Containerized grade and message management system using Django and Docker

## Instalacja

Krótki opis jak pracować z projektem.

### Gałęzie (Branches):

Projekt dzielimy na 3 rodzaje gałęzi:
1. **Master** - Działający projekt (Tego nie ruszamy pod żadnym pozorem. Tylko za moją komendą -> Damian )
2. **Dev** - Tu są wszystkie zmergowane nasze zmiany
3. **User** (dokładniej swoje imie) - Tu pracujemy

**WSZYSTKIE ZMIANY WYKONUJEMY NA SWOICH BRANCHACH!!!**

Jak przygotować sobie środowisko z gitem:

1. Klonujemy projekt:
```
git clone <url>
```
2. Przełączamy się na dev i pullujemy:
```
git checkout dev
git pull
```
3. Tworzymy własnego brancha (w miejsce <user> podajcie swoje imie albo coś dzięki czemu będziecie mogli odznaczyć że to wasze)
```
git checkout -b <user>
```
4. Pushujemy swojego brancha:
```
git push --set-upstream origin <user>
```

Dobrze żeby każde małe zmiany commitować (niekoniecznie trzeba pushować, mogą zostać lokalnie). Potem łatwiej zmiany konkretne znaleźć.

Jeżeli nasz projekt jest gotów to można do mnie napisać, żeby zrobić merga albo samemu dać merge requesta.

### Django:

*W kwestii dockeryzacji jest prośba aby Igor opisał to w tym albo przed tym paragrafem (względnie coś zmienił)*

Na start należy pobrać Django (polecam do tego stworzyć przedtem venv i tam pracować, ja mam w tym samym katalogu co .git):
```
pip install Django
```

Kolejne kroki aby skonfigurować środowisko:

1. Dokonać migracji bazy:
```
python manage.py makemigrations
python manage.py migrate
```
2. Stworzyć superusera (nieważne jakie id i hasło, e-maila można nie podawać):
```
python manage.py createsuperuser
```
3. Uruchomić środowisko:
```
python manage.py runserver
```

W konsoli powinien pojawić się link do którego wchodzimy. Można się logować normalnie w apce superkontem.

### Grupy (dawniej role):

Wykorzystując możliwości django.contrib połączyliśmy tabele Users z tabelą contrib.auth.User. Teraz możemy wykorzystać mechanizm grup, jaki daje nam framework, zastępujący przy tym role (tabelka w przyszłości zniknie). Prośba jest teraz aby stworzyć 4 grupy i nadać im pełne uprawnienia (po prostu choose all). Grupy te to (z małych liter):

- admin
- student
- parent
- teacher

Co więcej warto nadać grupę admin swojemu superuserowi (będzie łatwiej obsługiwać się nim w apce potem).

### Widoki:

Najważniejsza część to budowa widoków (oczywiście przy obsłudze bazy itd.). Nasza praca będzie głównie opierała się o folder GradjaApp. Natomiast każdy taki widok pojawia się jako funkcja w views.py w mniej więcej taki sposób:
```
def widok(request):
    # ...
    return render(request, "url.html", context)
```
Gdzie:
- request - ten sam co argument funkcji
- url.html - widok do wygenerowania
- context - dictionary zawierające wszelakie zmienne potrzebne do wygenerowania widoku (np. lista osób)

To wy powiniście stwierdzić, czy widok potrzebuje dodatkowych parametrów, czy trzeba coś wywołać w inny sposób, itd.

Dla takiego widoku należy stworzyć plik .html który bedzie szablonem do wygenerowania. Należy umieścić go w folderze template. Oto struktura:
```
{% extends 'base.html' %}

{% block title %} Tytul strony {% endblock %}

{% block content %}
...
{% endblock %}
```
Gdzie:
- extends 'base.html' - odwołanie do szablonu z bootstrapem
- block title - Miejsce do podania tytułu strony
- block content - miejsce do modelowania widoku

Kolejna część to dodanie ścieżki. W pliku urls.py (WAŻNE: wewnątrz GradjaApp) należy do urlpatterns dodać path w następujący sposób:
```
urlpatterns = [
    ...
    path('url_widoku', views.widok, name='nazwa widoku'),
    ...
]
```
Gdzie:
- 'url_widoku' - URL w przeglądarce
- views.widok - Funkcja widoku w views.py
- name='nazwa widoku' - Nazwa widoku

Na koniec należy dodać link do widoku w pasku obok. Możemy to zrobić wewnątrz base.html. Należy znaleźć tam div z komentarzem Sidebar (i moimi uwagami) i wewnątrz diva z klasą "list-group list-group-flush" dodać odpowiedniego htmla:
```
<div class="list-group list-group-flush">
    <a class="list-group-item list-group-item-action list-group-item-light p-3" href="/">Home</a>

    <!-- Tu dodajemy elementy, które nie wymagają autentykacji -->

    {% if user.is_authenticated %}
        {% if request.user|has_group:"admin" %} 
            <a class="list-group-item list-group-item-action list-group-item-light p-3" href="/admin">Panel admina</a>
        {% endif %}
        {% if request.user|has_group:"teacher" %} 
            <a class="list-group-item list-group-item-action list-group-item-light p-3" href="/set_grades">Dodaj oceny</a>
        {% endif %}

        <!-- Tu dodajemy elementy, które wymagają autentykacji -->

    {% endif %}
</div>
```
Nalepiej skorzystać ze schematu jak zrobiono pozostałe linki:
```
<a class="list-group-item list-group-item-action list-group-item-light p-3" href="/url">Nazwa</a>
```





