# I-need-my-coffee-fast...api
A Docker-containerized application with: a RESTFUL FASTApi API, PostgreSQL database, and PGAdmin. Featuring full CRUD on a one-to-many entity relationship (Roaster -< Coffee) created by Victor Haynes

<img src="./images/Coffee_ERD.jpg" alt="coffee erd" width="400" height=auto>

Additionally:
- Custom validations
- Custom Serializers & attributes
- JWT for authentication & admin-specific actions


Run Migrations in docker:
- `$ docker-compose run api alembic revision --autogenerate -m "New Migration"`
- `$ docker-compose run api alembic upgrade head`

To run:
- `$ docker-compose up`

Discover this API at URL: /docs:

<img src="./images/FastAPI_docs.jpg" alt="docs page" width="1000" height=auto>