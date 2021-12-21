import os
import json
import logging
from pprint import pprint

class ConfigDict(object):
    """docstring for Config"""
    def __init__(self, conf_dict):
        super(ConfigDict, self).__init__()
        self.logger = logging.getLogger('ConfigDict')
        self._conf_dict = conf_dict
        self._config = dict()


        for key in self._conf_dict:
            if type(self._conf_dict[key]) == dict:
                self._config[key] = ConfigDict(self._conf_dict[key])
            else:
                self._config[key] = self._conf_dict[key]

    def __getattr__(self, name):
        if name in self._config:
            return self._config[name]
        

    def set(self, name, value, overwrite: bool=True):
        
        if value == None:
            self.logger.debug(f'cannot set {name} with {value}')
            return False

        if name in self._config and not overwrite:
            self.logger.debug(f'do nmot overwrite {name}')
            return False

        if type(value) == dict:
            self.logger.info(f'set {name} as dict')
            self._config[name] = ConfigDict(value)
        else:
            self.logger.info(f'assign {name} with {value}')
            self._config[name] = value
        return True

    def _get(self):
        retVal = dict()
        for key in self._config:
            try:
                retVal[key] = self._config[key]._get()
            except Exception as e:
                retVal[key] = self._config[key]
        return retVal

    @property
    def config(self):
        return self._get()
    

class Config(ConfigDict):
    """docstring for Config"""
    def __init__(self, filename: str):
        self._filename = filename
        self.logger = logging.getLogger('Config')
        self._file, self._loaded_config = self.load_config(self._filename)
        super(Config, self).__init__(conf_dict=self._loaded_config)

    def write(self):
         with open(self._file, 'w') as fd:
             json.dump(self.config, fd, sort_keys=True, indent=4)

    def load_config(self, filename):
        logger = logging.getLogger("loadConfig")
        filetoread = False

        cwdConfig = os.path.join(os.getcwd(), filename)
        cwdSubpathConfig = os.path.join(os.getcwd(), "config", filename)
        codeConfig = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
        codeSubpathConfig = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "config", filename
        )

        logger.debug(cwdConfig)
        logger.debug(cwdSubpathConfig)
        logger.debug(codeConfig)
        logger.debug(codeSubpathConfig)

        if os.path.exists(cwdConfig):
            logger.debug("found Config file {}".format(cwdConfig))
            filetoread = cwdConfig
        elif os.path.exists(cwdSubpathConfig):
            logger.debug("found Config file {}".format(cwdSubpathConfig))
            filetoread = cwdSubpathConfig
        elif os.path.exists(codeConfig):
            logger.debug("found Config file {}".format(codeConfig))
            filetoread = codeConfig
        elif os.path.exists(codeSubpathConfig):
            logger.debug("found Config file {}".format(codeSubpathConfig))
            filetoread = codeSubpathConfig

        logger.info("Use Config file {}".format(filetoread))
        if filetoread:
            with open(filetoread, "r") as filedes:
                return [filetoread, json.load(filedes)]
        return [cwdConfig,{}]

