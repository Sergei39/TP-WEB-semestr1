from django.apps import AppConfig
import os


class ForumConfig(AppConfig):
    name = 'askme'
    forum_name = 'AskYou'

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        self.forum_name = os.environ.get('FORUM_NAME', 'AskMe')
