# Setting Dev Environment
Credit: originally written by undead, edited by samjo

## Introduction
By default, `[WEB_PORT]` and `[API_PORT]` are set as `8080` and `8000` by the frameworks. You may change these settings, but you must also make the required changes (e.g. in SPARCS SSO Test Service), if you choose to do so.

1. You need to setup [SPARCS SSO](https://sparcssso.kaist.ac.kr/dev/main/) configurations for development.
2. You need to run both the API Server (Django) and Web (Vue.js) in development configurations.
3. **NEVER commit these changes to remote repository!!!**


## SPARCS SSO

**Add a SPARCS SSO Test Service**

 - Main URL: http://localhost:[WEB_PORT]
 - Login Callback URL: http://localhost:[WEB_PORT]/auth/login_callback
 - Unregister URL: http://localhost:[WEB_PORT]/api/users/unregister (NOT implemented yet)

## Web (Vue.js)
- config/index.js:

```javascript
module.exports = {
  ...
  dev: {
    ...
    port: [WEB_PORT],
    ...
    proxyTable: {
      "/api": {
        target: "http://localhost:[API_PORT]/api",
        ...
      }
    }
  }
}
```

- config/dev.env.js

```javascript
module.export = merge(prodEnv, {
  NODE_ENV: '"development"',
  SSO_CLIENT_ID: '""',            // Enter Client Id for your SPARCS SSO test service
  SPARCS09_API_DOMAIN: '"http://127.0.0.1:[WEB_PORT]/api/"',
}
```

**Install NPM Dependencies**

```bash
$ npm install
```

**Run Vue.js**

```bash
$ npm run dev
node build/dev-server.js

[HPM] Proxy created: /api  ->  http://localhost:16134/api
[HPM] Proxy rewrite rule created: "^/api" ~> ""
> Starting dev server...

| DONE | Compiled successfully in 7662 ms                                               15:29:06


> Listening at http://localhost:[WEB_PORT]
```

On Windows, you may encounter this error:
`Expected linebreaks to be 'LF' but found 'CRLF'  linebreak-style`

In this case, just turn off `linebreak-style` option from eslint for simplicity.
```javascript
module.export = {
  ...
  'rules': {
    "linebreak-style": 0,
    ...
  }
}
```


## API (Django)

- settings.py:

```python
SSO_ID =                    # Enter Client Id for your SPARCS SSO test service
SSO_KEY =                   # Enter Secret Key for your SPARCS SSO test service

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]
```

**Create Virtual Python Environment**

Download [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/install.html)

```bash
$ mkvirtualenv -p python3 sparcs09
$ workon sparcs09
```

Check your local machine's python version if `mkvirtualenv -p` option fails. For instance,

```bash
$ which python3
/usr/bin/python3
```

**Install Python Dependencies (if haven't done so)**

```bash
(sparcs09) $ pip install -r requirements.txt
```

**API Database Migrate**

```bash
(sparcs09) $ python manage.py makemigrations
(sparcs09) $ python manage.py migrate
```

**Run API Server**

```bash
(sparcs09) $ python manage.py runserver 0.0.0.0:[API_PORT]
Performing system checks...

System check identified no issues (0 silenced).
July 18, 2017 - 15:20:28
Django version 1.11.2, using settings 'sparcs09.settings'
Starting development server at http://0.0.0.0:[API_PORT]/
Quit the server with CTRL-BREAK.
```
