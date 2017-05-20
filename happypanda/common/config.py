import os
import configparser
import pickle

from contextlib import contextmanager

from happypanda.common import exceptions

class Config:

    def __init__(self, path, filename1, filename2):
        self._cfg = configparser.ConfigParser(allow_no_value=True, default_section='common')
        self._cfg_d = {}
        self._current_ns = None
        self._path = path
        self._settings_f = os.path.join(self._path, filename1)
        self._descr_f = os.path.join(self._path, filename2)
        self._load()

    def _load(self):
        assert self._settings_f and self._descr_f

        if os.path.exists(self._settings_f) and os.path.exists(self._descr_f):
            self._cfg.read(self._settings_f)

            with open(self._descr_f, 'rb') as f:
                self._cfg_d = pickle.load(f)

    def save(self):
        assert self._settings_f and self._descr_f

        with open(self._settings_f, 'w') as f:
            self._cfg.write(f)

        with open(self._descr_f, 'wb') as f:
            pickle.dump(self._cfg_d, f, pickle.HIGHEST_PROTOCOL)

    def __contains__(self, key):
        return key.lower().capitalize() in self._cfg

    def key_exists(self, ns, key):
        ""
        ns = ns.lower().capitalize()
        key = key.lower()
        if ns in self._cfg:
            if key in self._cfg[ns]:
                return True
        return False

    @contextmanager
    def namespace(self, ns):
        assert isinstance(ns, str), "Namespace must be str"
        ns = ns.lower().capitalize()
        if not ns in self._cfg:
            self._cfg[ns] = {}
        if not ns in self._cfg_d:
            self._cfg_d[ns] = {}

        self._current_ns = ns
        yield
        self._current_ns = None

    def get(self, ns, key, default=None, description="", create=True):
        ""
        ns = ns.lower().capitalize()
        key = key.lower()
        with self.namespace(ns):
            if not key in self._cfg[ns]:
                if create:
                    self.define(key, default, description)
                return default

            t = self._cfg_d[ns][key]['type']
            if t == bool:
                v = self._cfg.getboolean(ns, key)
            else:
                v = t(self._cfg[ns][key])

            if not t is None and v is None:
                return default

            return v

    def define(self, key, value, description=""):
        assert self._current_ns, "No namespace has been set"
        key = key.lower()
        if description:
            self._cfg.set(self._current_ns, '# {}'.format(description))
        self._cfg.set(self._current_ns, key, str(value))
        self._cfg_d[self._current_ns][key] = {'type':type(value), 'descr':description}

    def doc_render(self):
        """
        # [
        #   [   
        #    [[val1, val2, val3], ...]],
        #    "header descr"
        #   ],
        # ]
        """
        sections = []
        for s in self._cfg:
            con = []
            for key in self._cfg[s]:
                if key and not key.startswith('#'):
                    con.append([key, self._cfg[s][key], self._cfg_d[s][key]['descr']])
            sections.append([con, s])
        return sections
