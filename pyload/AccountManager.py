#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#   Copyright(c) 2008-2013 pyLoad Team
#   http://www.pyload.org
#
#   This file is part of pyLoad.
#   pyLoad is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   Subjected to the terms and conditions in LICENSE
#
#   @author: RaNaN, mkaay
###############################################################################

from threading import Lock
from random import choice

from pyload.Api import AccountInfo
from pyload.utils import lock, json


class AccountManager:
    """manages all accounts"""

    def __init__(self, core):
        """Constructor"""

        self.core = core
        self.lock = Lock()

        # PluginName mapped to list of account instances
        self.accounts = {}

        self.loadAccounts()

    def _createAccount(self, info, password, options):
        plugin = info.plugin
        loginname = info.loginname
        # Owner != None must be enforced
        if info.owner is None:
            raise ValueError("Owner must not be null")

        klass = self.core.pluginManager.loadClass("accounts", plugin)
        if not klass:
            self.core.log.warning(_("Account plugin %s not available") % plugin)
            raise ValueError("Account plugin %s not available" % plugin)

        if plugin not in self.accounts:
            self.accounts[plugin] = []

        self.core.log.debug("Create account %s:%s" % (plugin, loginname))

        # New account instance
        account = klass.fromInfoData(self, info, password, options)
        self.accounts[plugin].append(account)
        return account

    def loadAccounts(self):
        """loads all accounts available from db"""
        for info, password, options in self.core.db.loadAccounts():
            # put into options as used in other context
            options = json.loads(options) if options else {}
            try:
                self._createAccount(info, password, options)
            except:
                self.core.log.error(_("Could not load account %s") % info)
                self.core.print_exc()

    def iterAccounts(self):
        """ yields login, account  for all accounts"""
        for plugin, accounts in self.accounts.iteritems():
            for account in accounts:
                yield plugin, account

    def saveAccounts(self):
        """save all account information"""
        data = []
        for plugin, accounts in self.accounts.iteritems():
            data.extend(
                [(plugin, acc.loginname, acc.owner, 1 if acc.activated else 0, 1 if acc.shared else 0, acc.password,
                  json.dumps(acc.options)) for acc in
                 accounts])
        self.core.db.saveAccounts(data)

    def getAccount(self, plugin, loginname, user=None):
        """ Find a account by specific user (if given) """
        if plugin in self.accounts:
            for acc in self.accounts[plugin]:
                if acc.loginname == loginname and (not user or acc.owner == user.true_primary):
                    return acc

    @lock
    def updateAccount(self, plugin, loginname, password, user):
        """add or update account"""
        account = self.getAccount(plugin, loginname, user)
        if account:
            if account.setPassword(password):
                self.saveAccounts()
                account.scheduleRefresh(force=True)
        else:
            info = AccountInfo(plugin, loginname, user.true_primary, activated=True)
            account = self._createAccount(info, password, {})
            account.scheduleRefresh()
            self.saveAccounts()

        self.core.eventManager.dispatchEvent("account:updated", account.toInfoData())
        return account

    @lock
    def removeAccount(self, plugin, loginname, uid):
        """remove account"""
        if plugin in self.accounts:
            for acc in self.accounts[plugin]:
                # admins may delete accounts
                if acc.loginname == loginname and (not uid or acc.owner == uid):
                    self.accounts[plugin].remove(acc)
                    self.core.db.removeAccount(plugin, loginname)
                    self.core.evm.dispatchEvent("account:deleted", plugin, loginname)
                    break

    @lock
    def selectAccount(self, plugin, user):
        """ Determines suitable plugins and select one """
        if plugin in self.accounts:
            uid = user.true_primary if user else None
            # TODO: temporary allowed None user
            accs = [x for x in self.accounts[plugin] if x.isUsable() and (x.shared or uid is None or x.owner == uid)]
            if accs: return choice(accs)

    @lock
    def getAllAccounts(self, uid):
        """ Return account info for every visible account """
        # filter by owner / shared, but admins see all accounts
        accounts = []
        for plugin, accs in self.accounts.iteritems():
            accounts.extend([acc for acc in accs if acc.shared or not uid or acc.owner == uid])

        return accounts

    def refreshAllAccounts(self):
        """ Force a refresh of every account """
        for p in self.accounts.itervalues():
            for acc in p:
                acc.getAccountInfo(True)
