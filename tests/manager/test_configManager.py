# -*- coding: utf-8 -*-

from unittest import TestCase
from collections import defaultdict

from nose.tools import raises

from tests.helper.Stubs import Core, adminUser, normalUser

from module.Api import InvalidConfigSection
from module.database import DatabaseBackend
from module.config.ConfigParser import ConfigParser
from module.config.ConfigManager import ConfigManager

class TestConfigManager(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.core = Core()
        cls.db = DatabaseBackend(cls.core)
        cls.core.db = cls.db
        cls.db.manager = cls.core
        cls.db.manager.statusMsg = defaultdict(lambda: "statusmsg")
        cls.parser = ConfigParser()
        cls.config = ConfigManager(cls.core, cls.parser)
        cls.db.setup()

    def setUp(self):
        self.db.clearAllConfigs()
        # used by some tests, needs to be deleted
        self.config.delete("plugin", adminUser)


    def addConfig(self):
        self.config.addConfigSection("plugin", "Name", "desc", "something",
            [("value", "str", "label", "desc", "default")])

    def test_db(self):

        self.db.saveConfig("plugin", "some value", 0)
        self.db.saveConfig("plugin", "some other value", 1)

        assert self.db.loadConfig("plugin", 0) == "some value"
        assert self.db.loadConfig("plugin", 1) == "some other value"

        d = self.db.loadAllConfigs()
        assert d[0]["plugin"] == "some value"
        assert self.db.loadConfigsForUser(0)["plugin"] == "some value"

        self.db.deleteConfig("plugin", 0)

        assert 0 not in self.db.loadAllConfigs()
        assert "plugin" not in self.db.loadConfigsForUser(0)

        self.db.deleteConfig("plugin")

        assert not self.db.loadAllConfigs()
        assert self.db.loadConfig("plugin") == ""

    def test_parser(self):
        assert self.config.get("general", "language")
        self.config["general"]["language"] = "de"
        assert self.config["general"]["language"] == "de"
        assert self.config.get("general", "language", adminUser) == "de"

    def test_user(self):
        self.addConfig()

        assert self.config["plugin"]["value"] == "default"
        assert self.config.get("plugin", "value", adminUser) == "default"
        assert self.config.get("plugin", "value", normalUser) == "default"

        assert self.config.set("plugin", "value", False, user=normalUser)
        assert self.config.get("plugin", "value", normalUser) is False
        assert self.config["plugin"]["value"] == "default"

        assert self.config.set("plugin", "value", True, user=adminUser)
        assert self.config.get("plugin", "value", adminUser) is True
        assert self.config["plugin"]["value"] is True
        assert self.config.get("plugin", "value", normalUser) is False

        self.config.delete("plugin", normalUser)
        assert self.config.get("plugin", "value", normalUser) == "default"

        self.config.delete("plugin")
        assert self.config.get("plugin", "value", adminUser) == "default"
        assert self.config["plugin"]["value"] == "default"

        # should not trigger something
        self.config.delete("foo")


    def test_sections(self):
        self.addConfig()

        i = 0
        # there should be only one section, with no values
        for name, config, values in self.config.iterSections(adminUser):
            assert name == "plugin"
            assert values == {}
            i +=1
        assert i == 1

        assert self.config.set("plugin", "value", True, user=adminUser)

        i = 0
        # now we assert the correct values
        for name, config, values in self.config.iterSections(adminUser):
            assert name == "plugin"
            assert values == {"value":True}
            i +=1
        assert i == 1


    @raises(InvalidConfigSection)
    def test_restricted_access(self):
        self.config.get("general", "language", normalUser)

    @raises(InvalidConfigSection)
    def test_error(self):
        self.config.get("foo", "bar")

    @raises(InvalidConfigSection)
    def test_error_set(self):
        self.config.set("foo", "bar", True)