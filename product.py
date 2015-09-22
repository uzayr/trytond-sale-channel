# -*- coding: utf-8 -*-
"""
    product.py

"""
from trytond.pool import PoolMeta
from trytond.transaction import Transaction
from trytond.model import ModelView, fields, ModelSQL

__metaclass__ = PoolMeta
__all__ = ['ProductSaleChannelListing', 'Product']


class Product:
    "Product"
    __name__ = "product.product"

    channel_listings = fields.One2Many(
        'product.product.channel_listing', 'product', 'Channel Listings',
    )

    @classmethod
    def create_from(cls, channel, product_data):
        """
        Create the product for the channel
        """
        raise NotImplementedError(
            "create_from is not implemented in product for %s channels"
            % channel.source
        )


class ProductSaleChannelListing(ModelSQL, ModelView):
    '''Product - Sale Channel
    This model keeps a record of a product's association with Sale Channels.
    A product can be listed on multiple marketplaces
    '''
    __name__ = 'product.product.channel_listing'

    # TODO: Only show channels where this ability is there. For example
    # showing a manual channel is pretty much useless
    channel = fields.Many2One(
        'sale.channel', 'Sale Channel',
        domain=[('source', '!=', 'manual')],
        required=True, select=True,
        ondelete='RESTRICT'
    )
    product = fields.Many2One(
        'product.product', 'Product', required=True, select=True,
        ondelete='CASCADE'
    )
    product_identifier = fields.Char("Product Identifier")
    state = fields.Selection([
        ('active', 'Active'),
        ('disabled', 'Disabled'),
    ], 'State', required=True, select=True)
    channel_source = fields.Function(
        fields.Char("Channel Source"),
        getter="on_change_with_channel_source"
    )

    @fields.depends('channel')
    def on_change_with_channel_source(self, name=None):
        return self.channel and self.channel.source

    @classmethod
    def __setup__(cls):
        '''
        Setup the class and define constraints
        '''
        super(ProductSaleChannelListing, cls).__setup__()
        cls._sql_constraints += [
            (
                'channel_product_unique',
                'UNIQUE(channel, product)',
                'Each product can be linked to only one Sale Channel!'
            )
        ]

    @staticmethod
    def default_state():
        return 'active'

    @classmethod
    def create_from(cls, channel, product_data):
        """
        Create a listing for the product from channel and data
        """
        raise NotImplementedError(
            "create_from is not implemented in channel listing for %s channels"
            % channel.source
        )

    def export_inventory(self):
        """
        Export listing.product inventory to listing.channel

        Since external channels are implemented by downstream modules, it is
        the responsibility of those channels to implement exporting or call
        super to delegate.
        """
        raise NotImplementedError(
            "Export inventory is not implemented for %s channels"
            % self.channel.source
        )

    @classmethod
    def export_bulk_inventory(cls, listings):
        """
        Export listing.product inventory to listing.channel in bulk

        Since external channels are implemented by downstream modules, it is
        the responsibility of those channels to implement bulk exporting for
        respective channels.
        Default behaviour is to export inventory individually.
        """
        for listing in listings:
            listing.export_inventory()

    def get_availability_context(self):
        """
        Allow overriding the context used to compute availability of
        products.
        """
        return self.channel.get_availability_context()

    def get_availability(self):
        """
        Return the availability of the product for this listing
        """
        with Transaction().set_context(**self.get_availability_context()):
            rv = {'type': 'bucket'}
            quantity = Product.get_quantity(
                [self.product], 'quantity'
            )[self.product.id]
            if quantity > 0:
                rv['value'] = 'in_stock'
            else:
                rv['value'] = 'out_of_stock'
            return rv
