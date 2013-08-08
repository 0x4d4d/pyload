# -*- coding: utf-8 -*-

from unittest import TestCase

from tests.helper.Stubs import Core, adminUser, normalUser

from pyload.database import DatabaseBackend
from pyload.AccountManager import AccountManager


class TestAccountManager(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core = Core()
        cls.db = DatabaseBackend(cls.core)
        cls.core.db = cls.db
        cls.db.setup()

    @classmethod
    def tearDownClass(cls):
        cls.db.shutdown()

    def setUp(self):
        self.db.purgeAccounts()
        self.manager = AccountManager(self.core)

    def test_access(self):
        account = self.manager.updateAccount("Http", "User", "somepw", adminUser)

        assert account is self.manager.updateAccount("Http", "User", "newpw", adminUser)
        self.assertEqual(account.password, "newpw")

        assert self.manager.getAccount("Http", "User") is account
        assert self.manager.getAccount("Http", "User", normalUser) is None

    def test_config(self):
        account = self.manager.updateAccount("Http", "User", "somepw", adminUser)
        info = account.toInfoData()

        self.assertEqual(info.config[0].name, "domain")
        self.assertEqual(info.config[0].value, "")
        self.assertEqual(account.getConfig("domain"), "")

        account.setConfig("domain", "df")

        info = account.toInfoData()
        self.assertEqual(info.config[0].value, "df")

        info.config[0].value = "new"

        account.updateConfig(info.config)
        self.assertEqual(account.getConfig("domain"), "new")


    def test_shared(self):
        account = self.manager.updateAccount("Http", "User", "somepw", adminUser)

        assert self.manager.selectAccount("Http", adminUser) is account
        assert account.loginname == "User"

        assert self.manager.selectAccount("Something", adminUser) is None
        assert self.manager.selectAccount("Http", normalUser) is None

        account.shared = True

        assert self.manager.selectAccount("Http", normalUser) is account
        assert self.manager.selectAccount("sdf", normalUser) is None



