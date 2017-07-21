from __future__ import unicode_literals

import os

from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'app'

    def ready(self):
        # registers some single
        pass
