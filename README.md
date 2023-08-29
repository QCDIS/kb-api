
# Knowledge base API

## Docker image

[![Build, test and publish container](https://github.com/QCDIS/kb-api/actions/workflows/build-test-publish.yaml/badge.svg)](https://github.com/QCDIS/kb-api/actions/workflows/build-test-publish.yaml)

### Environment variables

| Name                     | Description                                              | Required                  | Default value        |
|--------------------------|----------------------------------------------------------|---------------------------|----------------------|
| `ELASTICSEARCH_URL`      | URL of the Elasticsearch instance holding the KB indexes | Yes                       |                      |
| `ELASTICSEARCH_USERNAME` | Elasticsearch username                                   | Yes                       |                      |
| `ELASTICSEARCH_PASSWORD` | Elasticsearch password                                   | Yes                       |                      |
| `BASE_PATH`              | Base path of the application                             | No                        | `""`                 |
| `DEBUG`                  | Enable Django debug mode                                 | No                        | `False`              |
| `SECRET_KEY`             | Django secret key                                        | Optional if `DEBUG==True` | Generated at runtime |

### Ports

| Port | Description |
|------|-------------|
| 8000 | HTTP        |


## Development environment

### Initial setup

Create virtualenv and install Python packages:

```shell
virtualenv venv
venv/bin/pip install -r ./app/requirements.txt
```

Install npm packages:

```shell
npm ci
```

Setup pre-commit secret scanning ([doc](https://docs.gitguardian.com/ggshield-docs/integrations/git-hooks/pre-commit)):

```shell
pip install pre-commit ggshield
pre-commit install
ggshield auth login
```

### Run development server

Start Elasticsearch:

```shell
docker run --rm \
  -e "discovery.type=single-node" \
  -e "xpack.security.http.ssl.enabled=false" \
  -e "ELASTIC_PASSWORD=elastic" \
  -p 9200:9200 \
  docker.elastic.co/elasticsearch/elasticsearch:8.8.1
```

Load fixtures (wait for Elasticsearch)

```shell
venv/bin/python fixtures/load_fixtures.py
```

Start Django

```shell
. venv/bin/activate
while read env; do export $env; done < .env.dev
python app/manage.py runserver
```

### Run tests

API tests are generated and run with [Portman](http://getportman.com).
To get started:

```shell
npx portman --cliOptionsFile portman/portman-cli.yaml
```


## License

Copyright 2023 University of Amsterdam / LifeWatch ERIC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
