"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from programy.utils.logging.ylogger import YLogger

from programy.config.container import BaseContainerConfigurationData
from programy.config.bot.bot import BotConfiguration
from programy.config.client.scheduler import SchedulerConfiguration

class ClientConfigurationData(BaseContainerConfigurationData):

    def __init__(self, name):
        BaseContainerConfigurationData.__init__(self, name)
        self._bot_configs = []
        self._bot_configs.append(BotConfiguration("bot"))
        self._license_keys = None
        self._bot_selector = None
        self._scheduler = SchedulerConfiguration()
        self._renderer = None

    @property
    def configurations(self):
        return self._bot_configs

    @property
    def license_keys(self):
        return self._license_keys

    @property
    def bot_selector(self):
        return self._bot_selector

    @property
    def scheduler(self):
        return self._scheduler

    @property
    def renderer(self):
        return self._renderer

    def load_configuration(self, configuration_file, section, bot_root):
        if section is not None:
            bot_names = configuration_file.get_multi_option(section, "bot", missing_value="bot")
            first = True
            for name in bot_names:
                if first is True:
                    config = self._bot_configs[0]
                    first = False
                else:
                    config = BotConfiguration(name)
                    self._bot_configs.append(config)
                config.load_configuration(configuration_file, bot_root)

            self._license_keys = configuration_file.get_option(section, "license_keys")
            if self._license_keys is not None:
                self._license_keys = self.sub_bot_root(self._license_keys, bot_root)

            self._bot_selector = configuration_file.get_option(section, "bot_selector")

            self._scheduler.load_config_section(configuration_file, section, bot_root)

            self._renderer = configuration_file.get_option(section, "renderer")

        else:
            YLogger.warning(self, "No bot name defined for client [%s], defaulting to 'bot'.", self.section_name)
            self._bot_configs[0]._section_name = "bot"
            self._bot_configs[0].load_configuration(configuration_file, bot_root)


