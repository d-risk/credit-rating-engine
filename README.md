# Credit Report Service

This project is a microservice that provides credit reports on companies.

## Getting Started

These instructions should get you started on this project.

### Prerequisites

Here are the requirements that you need to have before starting on this project.

* [Git]
* [Docker] and/or
* [Python] 3.7 or higher

### Installing

The first thing is to clone this project to your local machine.
Below is a commandline to do it.

```commandline
git clone https://github.com/d-risk/credit-report-service.git
```

There are two ways to build this project.

#### Using Docker

If you would like to run this project in as a container, there is a `Dockerfile` to create a Docker image.
Below is the commandline to do it.

```commandline
docker build -t d-risk/credit-report-service .
```

#### Using Python

To run this project through Python, first install the dependencies as indicated below.

```commandline
pip install -r requirements.freeze.txt
```

### Running

There are two ways to run this project.

#### Using Docker

Below is the commandline to do it.

```commandline
docker run --name credit-report-service --rm -it d-risk/credit-report-service
```

#### Using Python

Below is the commandline to do it.

```commandline
python manage.py runserver
```

### Deploying

The Docker image is the recommended way to deploy this project.
Once the image is created, it can be uploaded to a repository of your choice.
When the Docker image is uploaded, you can use deploy that image on your preferred platform.

[Git]: https://git-scm.com/
[Docker]: https://www.docker.com/
[Python]: https://www.python.org/