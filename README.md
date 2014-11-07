Django boilerplate
==================

INSTALL
-------
 * <pre>apt-get install postgresql python-virtualenv python-crypto ipython python-sqlite python-psycopg2</pre>
 * <pre>git clone <this repo> </pre>
 * <pre>make initenv</pre>
 * <pre>source bin/activate</pre>
 * <pre>make reqs/[dev|test|prod]</pre>



TODO
----

  * Write install instructions [pborky]
  * Fix up database scheme
    * Transaction tables - splits, virtual accounts (funds, user accounts) [WIP]
      * Determine schema update [pborky]
      * Link to logical accounts from bank accounts and buddies, logical transactions from bank transactions and buddyevents [pborky or pasky]
    * Buddy event - add dates "created" and "since", date -> "until"
