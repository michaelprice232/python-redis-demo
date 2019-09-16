# Sample python-redis application

Used to further my understanding of using Redis alongside Python as a simple key-value store

This first iteration simulates a number of users playing a game, each of which generates a score. The score is recorded into Redis, retrieved as well as checked to see if a key exists (a user is a new player etc). Next steps would be to add Flask functionality to allow interactive input from end users in order to record real scores

## Run locally:
This will launch the `app` Python as well as the `redis` container:
`docker-compose up --build`

You can also connect to the Redis container from your host machine using your IDE/local code or via `redis-cli`


## Running in a Kubernetes cluster:
Redis is deployed as a deployment/service, and the Python app as a batch job, which currently just runs and completes once it has added and then retrieved the user scores from Redis:

`kubectl apply -f kubernetes/`
