# I-need-my-coffee-fast...api
A Docker-containerized fullstack application with: a RESTFUL FASTApi API, React.js and Bootstrap frontend, PostgreSQL database, and PGAdmin database administration.


Interact with the client at port:3000 URL "/" Home Page:

<img src="./images/Home_Page.jpg" alt="coffee erd" width="1000" height=auto>


Featuring full CRUD on a one-to-many entity relationship (Roaster -< Coffee) created by Victor Haynes

<img src="./images/Coffee_ERD.jpg" alt="coffee erd" width="400" height=auto>

Additional Features:
- JWT for authentication & admin-specific actions
- Custom Model validations
- Custom Response Serializers & attributes

To build:
- `$ docker-compose up`

To create databse tables run these commands from the project root after building. This will run the alembic commands for the "api" service (the Python-FastAPI application):
- `$ docker-compose run api alembic revision --autogenerate -m "New Migration"`
- `$ docker-compose run api alembic upgrade head`


Discover this API at port:8000 URL "/docs":

<img src="./images/FastAPI_docs.jpg" alt="docs page" width="1000" height=auto>


React.js Installations
- Bootstrap `$ npm install react-bootstrap bootstrap`
- React Router `$ npm install react-router-dom@6`