Django boilerplate
==================

INSTALL
-------
 * install distribuiton dependencies
  <pre>apt-get install postgresql python-virtualenv python-crypto ipython python-sqlite python-psycopg2</pre>
 * clone this repository and set up dependencies
  <pre>git clone <this repo> </pre>
  <pre>make initenv</pre>
  <pre>source bin/activate</pre>
  <pre>make reqs/[dev|test|prod]</pre>

 * create, import database and set up DATABASES in project/settings/local.py
  <pre>
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'brmburo', 
        'USER': 'brmbureaucrat',
        'PASSWORD': 'my choosen password',
        'HOST': '127.0.0.1',
        'PORT': '',
        }
}
  </pre>
 * run update
  <pre>make update</pre>



TODO
----

  * ~~Write install instructions [pborky]~~
  * Fix up database scheme
    * Transaction tables - splits, virtual accounts (funds, user accounts) [WIP]
      * ~~Determine schema update [pborky]~~
      * Link to logical accounts from bank accounts and buddies, logical transactions from bank transactions and buddyevents [pborky or pasky]
    * Buddy event - add dates "created" and "since", date -> "until"
