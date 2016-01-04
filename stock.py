# -*- coding: utf-8 -*-
"""
    stock.py
"""
from trytond.model import fields
from trytond.pyson import Eval
from trytond.pool import PoolMeta


__all__ = ['StockLocation']
__metaclass__ = PoolMeta


class StockLocation:
    __name__ = 'stock.location'

    subtype = fields.Selection([
        (None, '')
    ], "Sub Type", states={
        'invisible': Eval('type') != 'warehouse'
    }, depends=['type'])
