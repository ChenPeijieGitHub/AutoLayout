# system import
import os
from collections import defaultdict as ddt


class Dict2Obj(dict):
    def __init__(self, *args, **kwargs):
        super(Dict2Obj, self).__init__(*args, **kwargs)

    def __getattr__(self, key):
        value = self[key]
        if isinstance(value, dict):
            value = Dict2Obj(value)
        return value




class StarLink:
    def __init__(self):
        self.dict_id = ddt(list)

    def addNode(self, m_id, prop):
        node = Node(m_id, prop)