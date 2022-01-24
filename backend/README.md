# Dashboard API

This project requires Python 3.6 and above. Dashboard API uses Flask framework for serving API.

## Installation

Setup the virtualenv on the project folder.

```sh
$ git clone https://github.com/Qwikwire/dashboards-api
$ cd dashboards-api
$ python3.6 -m venv venv
$ . ./venv/bin/activate
```

Use `pip` to install the required project dependencies.

```sh
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

To exit from virtualenv on your terminal, use `deactivate` command.

## Running dashboards-api 

#### Using python

Using python requires virtualenv for Python 3.6.

```
$ python app.py
```

#### Debugging on Visual Studio Code

Add the following .vscode configuration to your `launch.json`. This would provide a Flask-specific debugger with the default port at 8021.

```
{
    "name": "flask",
    "type": "python",
    "request": "launch",
    "module": "flask",
    "env": {
        "FLASK_APP": "app.py",
        "FLASK_ENV": "development",
        "FLASK_DEBUG": "0"
    },
    "args": ["run", "--no-debugger", "--no-reload", "--port", "8021"],
    "jinja": true
}
```

#### Serving with NGINX

> Due to CORS policy on the browser, it does not allow REST API calls between localhost with different ports. 

Add the following environment variables to your config. Either on `/etc/environment` or `~/.bash_profile`. For Windows, use the System Variables.

```
REACT_APP_API_BASE_URL=http://localhost/v1/xqwapi
```

The NGINX configuration differs per system, depending on the system you must determine the location of the configuration:

- MacOS (brew): `/usr/local/etc/nginx/nginx.conf`
- Ubuntu 16.04: `/etc/nginx/sites-available/default`


```
server {
    server_name localhost;
    root /Users/<username>/projects;
    listen 80;

    # dashboard-api backend
    location /v1/ {
        rewrite /v1(.*) $1 break;
        proxy_pass http://127.0.0.1:8021;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_cache_bypass $http_upgrade;
    }

    # black-widow served by yarn dev
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_cache_bypass $http_upgrade;
    }
}
```

If you are stuck with issue of restarting nginx but have trouble with stopping the instance, use `lsof` to find the NGINX that is using the port and using `kill` to stop it.

```sh
$ lsof -n -i4TCP:<port>
$ kill -9 <pid>
```

## Testing

#### Linting

The app uses pylint for linting and maintaining code quality. To run it manually on your terminal

```
$ pylint --rcfile=.pylintrc server/**/*.py tests/**/*.py *.py
```

Use `--errors-only` to check only for errors.

```
$ pylint --rcfile=.pylintrc --errors-only server/**/*.py tests/**/*.py *.py
```

#### Integration Tests

The project uses pytest for testing Flask application API endpoints. All the test files are located in `tests/` folder.

Make sure you have a running Mongodb instance. Run the following command to run the integration tests.

```
$ pytest
```

You can also specify the file(s) that you wanted to test. Add `-s` to output the stdout and stderr messages on the terminal.

```
$ pytest -s tests/api/test_auth_controller.py
```
