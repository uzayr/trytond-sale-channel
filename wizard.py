# -*- coding: utf-8 -*-
"""
    wizard.py

    :copyright: (c) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.model import ModelView, fields
from trytond.wizard import (
    Wizard, StateView, Button, StateTransition, StateAction
)

__all__ = [
    'OrderImportWizard', 'OrderImportWizardStart'
]


class OrderImportWizardStart(ModelView):
    "Import Sale Order Start View"
    __name__ = 'sale.channel.orders_import.start'

    message = fields.Text("Message", readonly=True)


class OrderImportWizard(Wizard):
    "Wizard to import sale order from channel"
    __name__ = 'sale.channel.orders_import'

    start = StateView(
        'sale.channel.orders_import.start',
        'sale_channel.import_order_start_view_form',
        [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Continue', 'next', 'tryton-go-next'),
        ]
    )
    next = StateTransition()
    import_ = StateAction('sale_channel.act_sale_form_all')

    def default_start(self, data):
        """
        Sets default data for wizard

        :param data: Wizard data
        """
        Channel = Pool().get('sale.channel')

        channel = Channel(Transaction().context.get('active_id'))
        return {
            'message':
                "This wizard will import all sale orders placed on "
                "%s channel(%s) on after the Last Order Import "
                "Time. If Last Order Import Time is missing, then it will "
                "import all the orders from beginning of time. [This might "
                "be slow depending on number of orders]." % (
                    channel.name, channel.source
                )
        }

    def transition_next(self):
        """
        Downstream channel implementation can customize the wizard
        """
        return "import_"

    def do_import_(self, action):
        """
        Import Orders from channel
        """
        Channel = Pool().get('sale.channel')

        channel = Channel(Transaction().context.get('active_id'))
        sales = channel.import_orders()
        data = {'res_id': [sale.id for sale in sales]}
        return action, data
