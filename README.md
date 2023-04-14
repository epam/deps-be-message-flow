# Message Flow

## Description
Message Flow - is a messaging framework designed to facilitate communication between microservices through different messaging types, such as events, commands, and sagas. Message Flow supports a variety of messaging technologies, including Kafka, RabbitMQ, and cloud message buses, allowing you to choose the messaging system that best suits your needs. With MessageFlow, you can easily connect your microservices and ensure smooth, continuous messaging flows for your applications.

## Local development

### General workflow

By default, the dependencies are managed with [Poetry](https://python-poetry.org/), go there and install it.

You can install all the dependencies with:

```console
$ poetry install
```

Before installing dependencies poetry creates virtual environment.
Then you can activate venv using next command:

```console
$ poetry shell
```

Now you are ready to develop project locally.
