# I-need-my-coffee-fast...api
A Dockerized FASTApi API with PostgreSQL and PGAdmin. Featuring full CRUD on a one-to-many entity relationship (Roaster -< Coffee)
Additionally:
- Custom validations
- JWT based authorization (ToDo)


Run Migrations in docker
`$ docker-compose run api alembic revision --autogenerate -m "New Migration"`
`$ docker-compose run api alembic upgrade head`
