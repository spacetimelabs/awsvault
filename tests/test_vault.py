import json
try:
    from unittest import mock
except:
    import mock

from awsvault import Vault


def test_should_return_secrets_from_aws_secrets_manager():
    with mock.patch('awsvault.core.boto3') as boto3:
        boto3.client().get_secret_value.return_value = {
            'SecretString': json.dumps({
                'EMAIL_USER': 'user-secret',
                'EMAIL_PASS': 'user-pass'
            })
        }

        vault = Vault("myproject/email_secrets")

    email_user = vault.get("EMAIL_USER")
    email_password = vault.get("EMAIL_PASS")

    assert email_user == "user-secret"
    assert email_password == "user-pass"


def test_override_secrets():
    with mock.patch('awsvault.core.boto3') as boto3:
        boto3.client().get_secret_value.return_value = {
            'SecretString': json.dumps({
                'EMAIL_USER': 'user-secret',
                'EMAIL_PASS': 'user-pass'
            })
        }

        override = {
            'EMAIL_USER': 'bart.simpsons@example.com'
        }
        vault = Vault("myproject/email_secrets", look_first=override)

    email_user = vault.get("EMAIL_USER")
    email_password = vault.get("EMAIL_PASS")

    assert email_user == "bart.simpsons@example.com"
    assert email_password == "user-pass"


def test_override_secrets_using_fn():
    with mock.patch('awsvault.core.boto3') as boto3:
        boto3.client().get_secret_value.return_value = {
            'SecretString': json.dumps({
                'EMAIL_USER': 'user-secret',
                'EMAIL_PASS': 'user-pass'
            })
        }

        def override(name):
            if name == 'EMAIL_PASS':
                return 'test-override-fn'

        vault = Vault("myproject/email_secrets", look_first=override)

    email_user = vault.get("EMAIL_USER")
    email_password = vault.get("EMAIL_PASS")

    assert email_user == "user-secret"
    assert email_password == "test-override-fn"
