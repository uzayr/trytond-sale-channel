# -*- coding: utf-8 -*-
"""
    __init__.py

"""
from trytond.pool import Pool
from channel import (
    SaleChannel, ReadUser, WriteUser, ChannelException, ChannelOrderState
)
from wizard import (
    ImportDataWizard, ImportDataWizardStart, ImportDataWizardSuccess,
    ImportDataWizardProperties, ImportOrderStatesStart, ImportOrderStates,
    ExportPricesStatus, ExportPricesStart, ExportPrices
)
from product import (
    ProductSaleChannelListing, Product, AddProductListing,
    AddProductListingStart
)
from sale import Sale
from user import User


def register():
    Pool.register(
        SaleChannel,
        ReadUser,
        WriteUser,
        ChannelException,
        ChannelOrderState,
        User,
        Sale,
        ProductSaleChannelListing,
        Product,
        ImportDataWizardStart,
        ImportDataWizardSuccess,
        ImportDataWizardProperties,
        ImportOrderStatesStart,
        ExportPricesStatus,
        ExportPricesStart,
        AddProductListingStart,
        module='sale_channel', type_='model'
    )
    Pool.register(
        AddProductListing,
        ImportDataWizard,
        ImportOrderStates,
        ExportPrices,
        module='sale_channel', type_='wizard'
    )
