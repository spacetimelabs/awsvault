import pytest
import mock
from botocore.exceptions import NoCredentialsError
from awsvault.secrets import Vault


def test_should_return_None_for_invalid_aws_credentials():
    """
    Environment has no AWS credentials (cannot connect to secretsmanager)
    """
    vault = Vault("myproject/email_secrets")
    email_password = vault.get("EMAIL_PASS")  # no error

    assert email_password is None


def test_should_return_get_from_env_with_no_aws_credentials():
    """
    Environment has no AWS credentials (cannot connect to secretsmanager)
    """
    with mock.patch('os.getenv', return_value='MY_ENV_PASSWORD'):
        vault = Vault("myproject/email_secrets")
        email_password = vault.get("EMAIL_PASS")  # no error

    assert email_password == 'MY_ENV_PASSWORD'


def test_should_return_fail_without_aws_credentials():
    """
    Environment has no AWS credentials (cannot connect to secretsmanager)
    """
    with pytest.raises(NoCredentialsError):
        vault = Vault("myproject/email_secrets", fail=True)
        email_password = vault.get("EMAIL_PASS")
