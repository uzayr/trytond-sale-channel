# -*- coding: utf-8 -*-
"""
    sale

"""
from trytond.model import fields
from trytond.transaction import Transaction
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval, Or, Bool

__all__ = ['Sale']
__metaclass__ = PoolMeta


class Sale:
    __name__ = 'sale.sale'

    channel = fields.Many2One(
        'sale.channel', 'Channel', required=True, select=True, domain=[
            ('id', 'in', Eval('context', {}).get('allowed_read_channels', [])),
        ],
        states={
            'readonly': Or(
                (Eval('id', 0) > 0),
                Bool(Eval('lines', [])),
            )
        }, depends=['id']
    )

    channel_type = fields.Function(
        fields.Char('Channel Type'), 'on_change_with_channel_type'
    )

    has_channel_exception = fields.Function(
        fields.Boolean('Has Channel Exception ?'), 'get_has_channel_exception',
        searcher='search_has_channel_exception'
    )

    exceptions = fields.One2Many(
        "channel.exception", "origin", "Exceptions"
    )

    @classmethod
    def view_attributes(cls):
        return super(Sale, cls).view_attributes() + [
            ('//page[@id="exceptions"]', 'states', {
                'invisible': Eval('source') == 'manual'
            })]

    @classmethod
    def search_has_channel_exception(cls, name, clause):
        """
        Returns domain for sale with exceptions
        """
        if clause[2]:
            return [('exceptions.is_resolved', '=', False)]
        else:
            return [
                'OR',
                [('exceptions', '=', None)],
                [('exceptions.is_resolved', '=', True)],
            ]

    def get_channel_exceptions(self, name=None):
        ChannelException = Pool().get('channel.exception')

        return map(
            int, ChannelException.search([
                ('origin', '=', '%s,%s' % (self.__name__, self.id)),
                ('channel', '=', self.channel.id),
            ], order=[('is_resolved', 'desc')])
        )

    @classmethod
    def set_channel_exceptions(cls, exceptions, name, value):
        pass

    def get_has_channel_exception(self, name):
        """
        Returs True if sale has exception
        """
        ChannelException = Pool().get('channel.exception')

        return bool(
            ChannelException.search([
                ('origin', '=', '%s,%s' % (self.__name__, self.id)),
                ('channel', '=', self.channel.id),
                ('is_resolved', '=', False)
            ])
        )

    @classmethod
    def __setup__(cls):
        super(Sale, cls).__setup__()

        cls._error_messages.update({
            'channel_missing': (
                'Go to user preferences and select a current_channel ("%s")'
            ),
            'channel_change_not_allowed': (
                'Cannot change channel'
            ),
            'not_create_channel': (
                'You cannot create order under this channel because you do not '
                'have required permissions'
            ),
        })

    @classmethod
    def default_channel(cls):
        User = Pool().get('res.user')

        user = User(Transaction().user)
        channel_id = Transaction().context.get('current_channel')

        if channel_id:
            return channel_id
        return user.current_channel and \
            user.current_channel.id  # pragma: nocover

    @staticmethod
    def default_company():
        Sale = Pool().get('sale.sale')
        Channel = Pool().get('sale.channel')

        channel_id = Sale.default_channel()
        if channel_id:
            return Channel(channel_id).company.id

        return Transaction().context.get('company')  # pragma: nocover

    @staticmethod
    def default_invoice_method():
        Sale = Pool().get('sale.sale')
        Channel = Pool().get('sale.channel')
        Config = Pool().get('sale.configuration')

        channel_id = Sale.default_channel()
        if not channel_id:  # pragma: nocover
            config = Config(1)
            return config.sale_invoice_method

        return Channel(channel_id).invoice_method

    @staticmethod
    def default_shipment_method():
        Sale = Pool().get('sale.sale')
        Channel = Pool().get('sale.channel')
        Config = Pool().get('sale.configuration')

        channel_id = Sale.default_channel()
        if not channel_id:  # pragma: nocover
            config = Config(1)
            return config.sale_invoice_method

        return Channel(channel_id).shipment_method

    @staticmethod
    def default_warehouse():
        Sale = Pool().get('sale.sale')
        Channel = Pool().get('sale.channel')
        Location = Pool().get('stock.location')

        channel_id = Sale.default_channel()
        if not channel_id:  # pragma: nocover
            return Location.search([('type', '=', 'warehouse')], limit=1)[0].id
        else:
            return Channel(channel_id).warehouse.id

    @staticmethod
    def default_price_list():
        Sale = Pool().get('sale.sale')
        Channel = Pool().get('sale.channel')

        channel_id = Sale.default_channel()
        if channel_id:
            return Channel(channel_id).price_list.id
        return None  # pragma: nocover

    @staticmethod
    def default_payment_term():
        Sale = Pool().get('sale.sale')
        Channel = Pool().get('sale.channel')

        channel_id = Sale.default_channel()
        if channel_id:
            return Channel(channel_id).payment_term.id
        return None  # pragma: nocover

    @fields.depends('channel', 'party')
    def on_change_channel(self):
        if not self.channel:
            return  # pragma: nocover
        for fname in ('company', 'warehouse', 'currency', 'payment_term'):
            fvalue = getattr(self.channel, fname)
            if fvalue:
                setattr(self, fname, fvalue.id)
        if (not self.party or not self.party.sale_price_list):
            self.price_list = self.channel.price_list.id  # pragma: nocover
        if self.channel.invoice_method:
            self.invoice_method = self.channel.invoice_method
        if self.channel.shipment_method:
            self.shipment_method = self.channel.shipment_method

    @fields.depends('channel', 'price_list', 'invoice_address', 'payment_term')
    def on_change_party(self):  # pragma: nocover
        super(Sale, self).on_change_party()
        channel = self.channel

        if channel:
            if not self.price_list and self.invoice_address:
                self.price_list = channel.price_list.id
                self.price_list.rec_name = channel.price_list.rec_name
            if not self.payment_term and self.invoice_address:
                self.payment_term = channel.payment_term.id
                self.payment_term.rec_name = self.channel.payment_term.rec_name

    @fields.depends('channel')
    def on_change_with_channel_type(self, name=None):
        """
        Returns the source of the channel
        """
        if self.channel:
            return self.channel.source

    def check_create_access(self, silent=False):
        """
            Check sale creation in channel
        """
        User = Pool().get('res.user')
        user = User(Transaction().user)

        if user.id == 0:
            return  # pragma: nocover

        if self.channel not in user.allowed_create_channels:
            if silent:
                return False
            self.raise_user_error('not_create_channel')
        return True

    @classmethod
    def write(cls, sales, values, *args):
        """
        Check if channel in sale is is user's create_channel
        """
        if 'channel' in values:
            # Channel cannot be changed at any cost.
            cls.raise_user_error('channel_change_not_allowed')

        super(Sale, cls).write(sales, values, *args)

    @classmethod
    def create(cls, vlist):
        """
        Check if user is allowed to create sale in channel
        """
        User = Pool().get('res.user')
        user = User(Transaction().user)

        for values in vlist:
            if 'channel' not in values and not cls.default_channel():
                cls.raise_user_error(
                    'channel_missing', (user.rec_name,)
                )  # pragma: nocover

        sales = super(Sale, cls).create(vlist)
        for sale in sales:
            sale.check_create_access()
        return sales

    @classmethod
    def copy(cls, sales, default=None):
        """
        Duplicating records
        """
        if default is None:
            default = {}

        for sale in sales:
            if not sale.check_create_access(True):
                default['channel'] = cls.default_channel()

        return super(Sale, cls).copy(sales, default=default)

    def process_to_channel_state(self, channel_state):
        """
        Process the sale in tryton based on the state of order
        when its imported from channel

        :param channel_state: State on external channel the order was imported
        """
        Sale = Pool().get('sale.sale')

        data = self.channel.get_tryton_action(channel_state)

        if data['action'] in ['process_manually', 'process_automatically']:
            Sale.quote([self])
            Sale.confirm([self])

        if data['action'] == 'process_automatically':
            Sale.process([self])

        if data['action'] == 'import_as_past':
            # XXX: mark past orders as completed
            self.state = 'done'
            self.save()
