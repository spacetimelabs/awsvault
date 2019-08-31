import json
import os
try:
    from unittest import mock
except:
    import mock

from awsvault import Vault

AWS_SECRETS_MOCK = {
    "EMAIL": {
        'SecretString': json.dumps({
            'EMAIL_USER': 'user-secret',
            'EMAIL_PASS': 'user-pass'
        })
    },
    "DATABASE": {
        'SecretString': json.dumps({
            'HOSTNAME': 'myserver:5432',
            'DB_USER': 'db-user',
            'DB_PASS': 'db-p@ssw0rd',
        })
    }
}

def test_should_return_secrets_from_aws_secrets_manager():
    """
    Test should get the EMAIL keys mocking the AWS Secrets Manager
    """
    with mock.patch('awsvault.core.boto3') as boto3:
        boto3.client().get_secret_value.return_value = AWS_SECRETS_MOCK.get("EMAIL")

        vault = Vault("myproject/email_secrets")

    email_user = vault.get("EMAIL_USER")
    email_password = vault.get("EMAIL_PASS")

    assert email_user == "user-secret"
    assert email_password == "user-pass"


def test_override_secrets():
    """
    Test should get the EMAIL keys from the override dict before the AWS Keys
    """
    # Given an existing AWS Secrets and an override for the EMAIL_USER
    with mock.patch('awsvault.core.boto3') as boto3:
        boto3.client().get_secret_value.return_value = AWS_SECRETS_MOCK.get("EMAIL")

        override = {
            'EMAIL_USER': 'bart.simpsons@example.com'
        }
        vault = Vault("myproject/email_secrets", look_first=override)

    # When we get keys
    email_user = vault.get("EMAIL_USER")
    email_password = vault.get("EMAIL_PASS")

    # Then the overrided key should be returned
    assert email_user == "bart.simpsons@example.com"
    assert email_password == "user-pass"


def test_override_secrets_using_fn():
    """
    Just another way for overriding KEYS method
    """
    with mock.patch('awsvault.core.boto3') as boto3:
        boto3.client().get_secret_value.return_value = AWS_SECRETS_MOCK.get("DATABASE")

        def override(name):
            if name == 'DB_PASS':
                return 'db-password-overrided-fn'

        vault = Vault("myproject/database_secrets", look_first=override)

    db_user = vault.get("DB_USER")
    db_password = vault.get("DB_PASS")

    assert db_user == "db-user"
    assert db_password == "db-password-overrided-fn"


def test_should_work_without_secretmanager_conection():
    """
    Using tests or in the development mode, we might want to
    use environment variables rather than having credentials to access AWS
    It is the default `look_first` method
    """
    # Given an environment
    os.environ["EMAIL_HOST"] = "TEST_ENV"

    # When we use vault
    no_secrets = None
    vault = Vault(no_secrets)

    # Then
    assert vault.get("EMAIL_HOST") == "TEST_ENV"


def test_should_get_the_environment_secrets_first():
    """
    The environment variables (or the look_first parameter) MUST be the first option
    for returning the key ALWAYS
    """

    # Given an environment
    os.environ["EMAIL_USER"] = "MY-ENVIRONMENT-USER"

    # When we use vault to get an existing AWS KEY
    with mock.patch('awsvault.core.boto3') as boto3:
        boto3.client().get_secret_value.return_value = AWS_SECRETS_MOCK.get("EMAIL")

        vault = Vault("myproject/email_secrets")

    email_user = vault.get("EMAIL_USER")

    # Then we should get the ENVIRONMENT one
    assert email_user == "MY-ENVIRONMENT-USER"
