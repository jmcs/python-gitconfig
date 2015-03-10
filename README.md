Git Config
==========

Overview
--------
``gitconfig`` is a small wrapper around the git cli to expose git configuration as a mapping.
 
Usage
-----

``gitconfig`` is pretty straight forward:

    >>> import gitconfig
    >>> config = gitconfig.GitConfig()
    >>> config['test.test'] = 'test value'
    >>> config['test.test']
    'test value'
    >>> del config['test.test']
    >>> config['test.test']
    Traceback (most recent call last):
        ...
    KeyError
    
By default values are set locally (keeping the behaviour of ``git config KEY VALUE``), you can also store the values
for the user or the system by providing the right space when initializing ``GitConfig``:
    
    >>> config = gitconfig.GitConfig('local')
    >>> config = gitconfig.GitConfig('global')
    >>> config = gitconfig.GitConfig('system')
    
Key are always read from every available configuration, and will respect the same rules as ``git config`` to get the
key values.