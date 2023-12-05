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

