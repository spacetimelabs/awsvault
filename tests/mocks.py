# -*- coding: utf-8 -*-


def secrets_mock(secrets):
    return {
        "EMAIL_USER": "user-secret",
        "EMAIL_PASS": "user-pass",
    }


def boto_mock(SecretId):
    secrete_manager = {
        "database/project1/prod": {
            "Name": 'database/project1/prod',
            "SecretString": '{"DB_USER":"user1","DB_PASS":"YyxOC"}'
        },
        "database/project1/test": {
            "Name": 'database/project1/test',
            "SecretString": '{"DB_USER":"user1","DB_PASS":"12345"}'
        },
        "celery/project1/prod": {
            "Name": 'celery/project1/prod',
            "SecretString": '{"BROKER_URL":"amqp://user:pwd@server1"}'
        },
        "celery/project1/test": {
            "Name": 'celery/project1/test',
            "SecretString": '{"BROKER_URL":"amqp://user:12345@localhost"}'
        },
    }
    result = secrete_manager.get(SecretId, {}).get("SecretString", '{}')
    return result