export DJANGOPORT := 8000
export DEBUG := True
export  PGHOST := localhost
export  PGDATABASE := polideportivo_db
export  PGUSER := alumnodb
export  PGPASSWORD := alumnodb
PSQL = psql
CMD = python manage.py
APP = polideportivo api
export DATABASE_URL = postgres://alumnodb:alumnodb@localhost/$(PGDATABASE)

clear_db:
	@echo Clear Database
	dropdb --if-exists $(PGDATABASE)
	createdb

create_super_user:
	$(CMD) shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('polideportivo_user', 'admin@myproject.com', 'user1', first_name='polideportivo_user')"

runserver:
	$(CMD) runserver $(DJANGOPORT)

update_models:
	$(CMD) makemigrations $(APP)
	$(CMD) migrate

static:
	@echo manage.py collectstatic
	python3 ./manage.py collectstatic

force_update_db: clear_db
	@echo del migrations and make migrations and migrate
	rm -rf */migrations
	python3 ./manage.py makemigrations $(APP) 
	python3 ./manage.py migrate

populate:
	python3 ./manage.py populate
	