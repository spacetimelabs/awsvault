# -*- coding: utf-8 -*-
import os
import six
import json
import logging
import boto3
from botocore.exceptions import ClientError, BotoCoreError


class Vault(object):
    """
    Helper for getting secrets from AWS secret manager
    Check the TESTs out for usage examples
    """

    def __init__(self, secrets, look_first=None, **kwargs):
        """
        Usage:
          1. Initialize the vault
          vault = Vault("myaws_project_secrets")
          OR
          vault = Vault("myaws_project_secrets/environment")
          OR
          vault = Vault("myaws_project_secrets/email/prod", "myaws_project_secrets/db/prod")

          2. Get any existing key value
          vault.get("MY_KEY")

        For local or staging usage (without AWS account permission):
          1. Set your keys inside your environment variables
          2. Initialize the vault
            vault = Vault(None)
          3. Get your environment keys
            vault.get("MY_KEY")

        vault = Vault("invalid_secret_name") will raise a ResourceNotFoundException.
        """
        self._logger = logging.getLogger('awsvault.' + __name__)
        self._vault = {}
        self._look_first = look_first or os.environ

        if not secrets:
            self._logger.warning('Empty secrets. Environment will be used instead.', exc_info=True)
            return

        if isinstance(secrets, six.string_types):
            secrets = [secrets]

        try:
            client = boto3.client('secretsmanager', **kwargs)
            for secret in secrets:
                response = client.get_secret_value(SecretId=secret)
                value = response.get('SecretString', '{}')
                self._vault.update(json.loads(value))
        except (ClientError, BotoCoreError):
            self._logger.warning('AWS Secrets Manager error', exc_info=True)

    def get(self, name, default=None):
        """
        Usage:
          vault.get("MY_KEY")
          # The method above will
          # 1. Try to return the environment value for the given KEY
          # 2. Try to return the AWS Secret value for the given KEY
        """
        value = None
        if callable(self._look_first):
            value = self._look_first(name)
        elif isinstance(self._look_first, dict) or hasattr(self._look_first, 'get'):
            value = self._look_first.get(name)

        if value is not None:
            return value

        return self._vault.get(name, default)
