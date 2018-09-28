import pytest
import mock
import boto3
from awsvault.secrets import Vault
from tests.mocks import secrets_mock, boto_mock


@mock.patch('awsvault.secrets.Vault._get_aws_retrieve_secrets', side_effect=secrets_mock)
def test_should_return_secrets_for_one_vault(secrets_mock):
    """
    Usage sample 1:
    --------------
    1 aws secret that contains ALL project's keys

    # settings.py
    vault = Vault("myproject/email_secrets")
    MYPROJECT_EMAIL_USER = vault.get("MYPROJECT_EMAIL_USER")
    MYPROJECT_EMAIL_PASS = vault.get("MYPROJECT_EMAIL_PASS")
    """
    vault = Vault("myproject/email_secrets")
    email_user = vault.get("EMAIL_USER")
    email_password = vault.get("EMAIL_PASS")

    assert email_user == "user-secret"
    assert email_password == "user-pass"


@mock.patch('awsvault.secrets.Vault._get_aws_retrieve_secret', side_effect=boto_mock)
def test_should_return_secrets_for_multiple_vaults(boto_mock):
    """
    Usage sample 2:
    --------------
    the project uses multiple aws secrets

    # settings.py
    vault = Vault(["resource1/prod", "resource2/prod"])
    SECRET_FROM_RESOURCE1 = vault.get("SECRET_FROM_RESOURCE1")
    SECRET_FROM_RESOURCE2 = vault.get("SECRET_FROM_RESOURCE2")
    """
    all_project_secrets = 'database/project1/prod,celery/project1/prod'.split(',')
    vault = Vault(all_project_secrets)
    db_pass = vault.get("DB_PASS")
    broker_url = vault.get("BROKER_URL")

    assert db_pass == "YyxOC"
    assert broker_url == "amqp://user:pwd@server1"


@pytest.mark.env("stage1")
@mock.patch('awsvault.secrets.Vault._get_aws_retrieve_secrets', side_effect=secrets_mock)
def test_should_get_secret_from_env_before_aws(secrets_mock):
    """
    Usage sample 3:
    --------------
    Uses ENVIRONMENT VARIABLES over AWS SECRET MANAGER SECRETS
    """
    vault = Vault("myproject/email_secrets")
    email_password = vault.get("EMAIL_PASS")
    assert email_password == "user-pass"

    with mock.patch('os.getenv', return_value='MY_ENV_VALUE_HAS_PRIORITY'):
        email_password = vault.get("EMAIL_PASS")
        assert email_password == "MY_ENV_VALUE_HAS_PRIORITY"
