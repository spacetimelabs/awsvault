aws-vault
===============================

version number: 0.0.1
author: Spacetime Labs

Overview
--------

AWS Secrets Manager helper

Installation / Usage
--------------------

To install use pip:

    $ pip install awsvault


Or clone the repo:

    $ git clone https://github.com/spacetimelabs/awsvault.git
    $ python setup.py install
    
Contributing
------------

pip install requirements.txt
tox

Example
-------

    # settings.py
    vault = Vault("myproject/email_secrets")
    email_user = vault.get("EMAIL_USER")
    email_password = vault.get("EMAIL_PASS")
