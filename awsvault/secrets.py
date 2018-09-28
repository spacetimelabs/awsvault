# -*- coding: utf-8 -*-
import os
import six
import json
import boto3


class Vault(object):
    """
    Helper for getting secrets from AWS secret manager
    Check the TESTs out for usage examples
    """

    def __init__(self, secrets, fail=False, **kwargs):
        if not secrets:
            return
        if isinstance(secrets, six.text_type):
            secrets = [secrets]
        self._fail = fail
        self._client = self._get_secretsmanager_connection(**kwargs)
        self._vault = self._get_aws_retrieve_secrets(secrets)

    def _get_secretsmanager_connection(self, **kwargs):
        return boto3.client('secretsmanager', **kwargs)

    def _get_aws_retrieve_secret(self, secret):
        response = {}
        try:
            response = self._client.get_secret_value(SecretId=secret)
        except Exception as error:
            if self._fail:
                raise error
        return response.get('SecretString', '{}')

    def _get_aws_retrieve_secrets(self, secrets):
        _vaults = {}
        for secret in secrets:
            _vaults.update(json.loads(self._get_aws_retrieve_secret(secret)))
        return _vaults

    def get(self, name, default=None):
        return os.getenv(name, self._vault.get(name, default))
