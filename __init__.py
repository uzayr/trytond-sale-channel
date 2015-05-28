# -*- coding: utf-8 -*-
"""
    __init__.py

    :copyright: (c) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.pool import Pool
from channel import (
    SaleChannel, ReadUser, WriteUser, ChannelException
)
from wizard import (
    ImportDataWizard, ImportDataWizardStart, ImportDataWizardSuccess,
    ImportDataWizardProperties
)
from product import ProductSaleChannelListing, Product
from sale import Sale
from user import User


def register():
    Pool.register(
        SaleChannel,
        ReadUser,
        WriteUser,
        ChannelException,
        User,
        Sale,
        ProductSaleChannelListing,
        Product,
        ImportDataWizardStart,
        ImportDataWizardSuccess,
        ImportDataWizardProperties,
        module='sale_channel', type_='model'
    )
    Pool.register(
        ImportDataWizard,
        module='sale_channel', type_='wizard'
    )
