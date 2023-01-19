FROM node:17-alpine
WORKDIR /client
# COPY ./client/package.json /client
COPY ./client /client

RUN npm i --silent
RUN npm i -g react-scripts@5.0.1

# COPY ./client /client

CMD ["npm", "start"]