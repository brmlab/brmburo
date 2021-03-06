Django boilerplate
==================

INSTALL
-------
 * install distribuiton dependencies
  <pre>apt-get install postgresql python-virtualenv python-dev python-crypto ipython python-sqlite python-psycopg2 python-yaml python-passlib</pre>
 * clone this repository and set up dependencies
  <pre>git clone <this repo> </pre>
  <pre>make initenv</pre>
  <pre>source bin/activate</pre>
  <pre>make reqs/[dev|test|prod]</pre>

 * create, import database and set up DATABASES in brmburo/settings/local.py

        from .dev import *

        BANK_TOKENS = [
          'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
          'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
          'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',
          'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD',
          'EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE',
        ]

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

        DOKUWIKI_USERS_FILE = '/path/to/users.auth.php' #config file where dokuwiki has login data, usually in /var/www/conf

  you can create user and empty postgres database using:
  <pre>
sudo -u postgres psql &lt;&lt;-EOF
CREATE ROLE brmbureaucrat WITH LOGIN PASSWORD 'my choosen password';
CREATE DATABASE brmburo;
GRANT ALL PRIVILEGES ON DATABASE brmburo TO brmbureaucrat;
EOF
  </pre>
  and import data from database dump if desired (data must be acquired by pg\_dump first):
  <pre>sudo -u postgres psql brmburo &lt; brmburo.dump.sql</pre>

 * run setup
  <pre>make setup/[dev|test|prod]</pre>

 * if you start with blank database, you must at least load static data
  <pre>make load</pre>


TODO
----

  * ~~Write install instructions [pborky]~~
  * Fix up database scheme
    * Transaction tables - splits, virtual accounts (funds, user accounts) [WIP]
      * ~~Determine schema update [pborky]~~
      * ~~Link to logical accounts from bank accounts and buddies, logical transactions from bank transactions and buddyevents [pborky or pasky]~~
    * Buddy event - add dates "created" and "since", date -> "until"
