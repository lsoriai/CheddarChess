# -*- coding: utf-8 -*-
class ClientError(Exception):
    
    def __init__(self, code):
        super().__init__(code)
        self.code = code
