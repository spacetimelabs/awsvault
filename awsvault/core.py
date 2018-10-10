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
        except (ClientError, BotoCoreError) as exc:
            self._logger.warning('AWS Secrets Manager error', exc_info=True)

    def get(self, name, default=None):
        value = None
        if callable(self._look_first):
            value = self._look_first(name)
        elif isinstance(self._look_first, dict) or hasattr(self._look_first, 'get'):
            value = self._look_first.get(name)

        if value is not None:
            return value

        return self._vault.get(name, default)
