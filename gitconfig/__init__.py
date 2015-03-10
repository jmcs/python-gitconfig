#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import MutableMapping
import subprocess


class GitConfig(MutableMapping):

    """
    Simple wrapper around git config
    """

    def __init__(self, level='local'):
        """
        :param level: where to store the configuration keys. Can be global, local or system see "man git config"
        """

        if level not in ['global', 'local', 'system']:
            raise ValueError('Level has to be local, global or system')
        self.level = level

    def __iter__(self):
        """
        Iterate over git config keys
        """

        try:
            cmd = ['git', 'config', '--list', '-z']
            lines = subprocess.check_output(cmd, universal_newlines=True).split('\0')
            keys = (line.split()[0] for line in lines if line)
            return keys
        except subprocess.CalledProcessError:
            return []

    def __contains__(self, key):
        try:
            self[key]
            return True
        except KeyError:
            return False

    def __delitem__(self, key):
        """
        Equivalent to 'git config --unset key'
        """

        try:
            cmd = ['git', 'config', '--unset', key]
            return subprocess.check_call(cmd, universal_newlines=True)
        except subprocess.CalledProcessError:
            raise KeyError

    def __getitem__(self, key):
        """
        Equivalent to 'git config --get key'
        """

        try:
            cmd = ['git', 'config', '--get', key]
            return subprocess.check_output(cmd, universal_newlines=True).strip()
        except subprocess.CalledProcessError:
            raise KeyError

    def __len__(self):
        """
        Counts number git config keys
        """

        try:
            cmd = ['git', 'config', '--list', '-z']
            lines = subprocess.check_output(cmd, universal_newlines=True).split('\0')
            # the last line is empty so doesn't count
            return len(lines) - 1
        except subprocess.CalledProcessError:
            return 0

    def __setitem__(self, key, value):
        """
        Equivalent to git config --LEVEL key value
        """

        level = '--' + self.level
        try:
            cmd = [
                'git',
                'config',
                level,
                key,
                str(value),
            ]
            subprocess.check_output(cmd, universal_newlines=True).strip()
        except subprocess.CalledProcessError as e:
            if e.returncode == 1:
                raise ValueError
            elif e.returncode == 2:
                print(cmd)
                raise KeyError
            else:
                # I don't know what happened to get here, so just raise the error
                raise
