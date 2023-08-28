# Knowledge base indexer

## Development environment

### Initial setup

```shell
virtualenv venv
. venv/bin/activate
pip install -r ./app/requirements.txt
```

### Run development server

```shell
while read env; do export $env; done < .env.dev
python app/manage.py runserver
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
