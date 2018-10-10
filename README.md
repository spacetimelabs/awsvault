aws-vault
===============================

![travis-ci](https://api.travis-ci.org/spacetimelabs/awsvault.svg)

version number: 0.1.1
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

pip install requirements-dev.txt
tox

Example
-------

```python
vault = Vault("myproject/email_secrets")
email_user = vault.get("EMAIL_USER")
email_password = vault.get("EMAIL_PASS")
```

```python
OVERRIDE = {
    'EMAIL_USER': 'bart.simpsons@example.com'
}

vault = Vault("myproject/email_secrets", look_first=OVERRIDE)
email_user = vault.get('EMAIL_USER')
assert email_user == 'bart.simpsons@example.com'
```

```python
def my_super_special_get_config_fn(name):
    if name == 'FRUIT':
        return 'avocado'


vault = Vault("myproject/email_secrets", look_first=my_super_special_get_config_fn)
email_user = vault.get('EMAIL_USER')
fruit = vault.get('FRUIT')

assert fruit == 'avocado'
```
