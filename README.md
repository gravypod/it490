# IT 490 Project Monorepo

This is a monorepo for my IT490 class project.

# Project Setup

1. Install [Docker](https://docs.docker.com/install/#supported-platforms)
2. Install [Docker Compose](https://docs.docker.com/compose/install/)
3. Set up hosts file
4. Run `docker-compose up -d --build`


## Set Up Hosts File

Because the development environment does not have a DNS name you'll need to 
edit your hosts file so your system resolves to local host for all DNS
queries. This is not needed to run the code, this is just useful for debugging
because you will be able to interract with the site as if it is a full production
environment.

To find a list of domains do the following:

```
$ grep '.localhost' docker-compose.yml
...
      VIRTUAL_HOST: rabbitmq.it490.localhost
...
$ sudo nano /etc/hosts # Inside the editor make a line that looks like: 127.0.0.1 rabbitmq.it490.localhost
```

This will create a DNS name for each service that needs one. You can now go to 
http://rabbitmq.it490.localhost (and any other domain) in your browser to debug things.
