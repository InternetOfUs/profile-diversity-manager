# WeNet - Profile Diversity Manager


## Introduction

This project is an extension of the profile manager to allow it to calculate
the similarity between strings.

The component to manage the diversity of the user profiles.

## Setup and configuration

First of all, you must install the next software.

 - [docker](https://docs.docker.com/install/)
 - [docker compose](https://docs.docker.com/compose/install/)

### Development

First of all you need to installl the [docker](https://docker.io),
and after that you can run the script **startDevelopmentEnvironment.sh**
to start the development environment.
On this environment you have access to the commands:

 - **start-reload.sh** start a development server that detect the changes
  on the files and start again.
 - **start.sh** start a server similar to the production one. This server
  Not detect the changes, so to be effective you must stop and start again.
 
In both casses you can interact with the stertaed server
at **http://localhost/doc** or at **http://localhost/redoc**.
Also you can stop the server with keys combinations **Control-C**.

If you go to the **tests** directory and execute the command `pytest --cov=../app`
to run all test and obtain a coverage measure of them.

If you not **exit** from the development environment, may be the next time
you try to start it will fail. In this case before to start again try
the next commands:

```
docker stop profile_diversity_manager_dev
docker rm profile_diversity_manager_dev
```

### Create docker image

You can create the docker container with the script **buildDockerImage.sh**.
The created container has the next parameters:

 - **HOST** it is the host to bind the server. By default is set to **0.0.0.0**.
 - **PORT** it is set port to bind teh server. By default is set to **80**.
 - **MAX_EXECUTOR_WORKERS** it is set to the number of backgound threads that
   the server will use. By default is set to **4**.
 - **LOG_LEVEL** the logging level (debug,info,warning,error or critical).
   By default is set to **info**.
 
   
Also you can use the environment veriables of [fatsapi base docker image](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker).

After that you can run the service with the command: 

```
docker run -t internetofus/profile-diversity-manager:VERSION
```

Where **VERSION** is the version of the **profile-diversity-manager** you want to run.


## License

This software is under the [Apache V2 license](LICENSE)


## Interaction with other WeNet components

## Contact

### Researcher

 - [Nardine Osman](http://www.iiia.csic.es/~nardine/) ( [IIIA-CSIC](https://www.iiia.csic.es/~nardine/) ) nardine (at) iiia.csic.es
 - [Carles Sierra](http://www.iiia.csic.es/~sierra/) ( [IIIA-CSIC](https://www.iiia.csic.es/~sierra/) ) sierra (at) iiia.csic.es

### Developers

 - Joan Jené ( [UDT-IA, IIIA-CSIC](https://www.iiia.csic.es/people/person/?person_id=19) ) jjene (at) iiia.csic.es
 - Bruno Rosell i Gui ( [UDT-IA, IIIA-CSIC](https://www.iiia.csic.es/people/person/?person_id=27) ) rosell (at) iiia.csic.es
