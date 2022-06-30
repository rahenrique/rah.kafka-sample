# FastAPI with Kafka Sample

Este projeto é uma demonstração de como utilizar **Kafka** como message broker com uma API web em **FlaskAPI**. Este repositório tem como objetivo ser um ponto de partida para um ambiente de desenvolvimento local.

## Pré requisitos

Antes de iniciar, você irá precisar das seguintes ferramentas instaladas em sua máquina local:
* [Git](https://git-scm.com)
* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/install/)

## Instalação (Desenvolvimento Local)

```bash
# Clone this repository
$ git clone https://github.com/rahenrique/rah.kafka-sample.git

# Run the application
$ docker-compose up
```

Ist'irá criar duas aplicações FastAPI, uma atuando como produtora, e outra atuando como consumidora de mensagens. Ambas podem ser acessadas pelos seus endpoints via requisições REST. Além disso, serão criados mais dois containers: Kafka e Zookeeper. 

Para acessar cada uma das aplicações FastAPI:
* Producer: <http://localhost:7000/docs/>
* Consumer: <http://localhost:8000/docs/>
