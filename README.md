# Aplicatie_SNMP
Licenta Aplicatie SNMP Robert Davidoiu.

Django commands:

python -m django --version
django-admin
python manage.py runserver - Starting Server
python manage.py startapp snmp_app - Create snmp_app application
python manage.py makemigrations
python manage.py migrate
python manage.py shell PythonPromptShell
pip install django-crispy-forms

>>> User.objects.all()
<QuerySet [<User: Robert>, <User: TestUser>]>
>>> User.objects.first()
<User: Robert>
>>> User.objects.filter(username='Robert')
<QuerySet [<User: Robert>]>
>>> User.objects.filter(username='Robert').first()
<User: Robert>
>>> user = User.objects.filter(username='Robert').first()
>>> user.id
1
AttributeError: 'User' object has no attribute 'ok'
>>> user.pk
1

Tabel Adaugare echipament:
Model
Adresa IP
Descriere
