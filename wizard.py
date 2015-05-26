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
    Wizard, StateView, Button, StateTransition
)

__all__ = [
    'ImportDataWizard', 'ImportDataWizardStart', 'ImportDataWizardSuccess'
]


class ImportDataWizardStart(ModelView):
    "Import Sale Order Start View"
    __name__ = 'sale.channel.import_data.start'

    message = fields.Text("Message", readonly=True)

    import_orders = fields.Boolean("Import Orders")
    import_products = fields.Boolean("Import Products")


class ImportDataWizardSuccess(ModelView):
    "Import Sale Order Success View"
    __name__ = 'sale.channel.import_data.success'

    no_of_orders = fields.Integer("Number Of Orders Imported", readonly=True)
    no_of_products = fields.Integer(
        "Number Of Products Imported", readonly=True
    )


class ImportDataWizard(Wizard):
    "Wizard to import data from channel"
    __name__ = 'sale.channel.import_data'

    start = StateView(
        'sale.channel.import_data.start',
        'sale_channel.import_data_start_view_form',
        [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Continue', 'next', 'tryton-go-next'),
        ]
    )
    next = StateTransition()
    import_ = StateTransition()

    success = StateView(
        'sale.channel.import_data.success',
        'sale_channel.import_data_success_view_form',
        [
            Button('Ok', 'end', 'tryton-ok'),
        ]
    )

    def default_start(self, data):
        """
        Sets default data for wizard

        :param data: Wizard data
        """
        Channel = Pool().get('sale.channel')

        channel = Channel(Transaction().context.get('active_id'))
        return {
            'message':
                "This wizard will import all orders and products placed on "
                "%s channel(%s). Orders will be imported only which are "
                "placed after the Last Order Import "
                "Time. If Last Order Import Time is missing, then it will "
                "import all the orders from beginning of time. "
                "[This might be slow depending on number of orders]. "
                "Checking checkboxes below you may choose to import products "
                "or orders or both. "
                % (channel.name, channel.source)
        }

    def transition_next(self):
        return 'import_'

    def transition_import_(self):  # pragma: nocover
        """
        Downstream channel implementation can customize the wizard
        """
        Channel = Pool().get('sale.channel')

        channel = Channel(Transaction().context.get('active_id'))

        sales = []
        products = []

        if self.start.import_orders:
            sales = channel.import_orders()

        if self.start.import_products:
            products = channel.import_products()

        self.success.no_of_orders = len(sales)
        self.success.no_of_products = len(products)
        return 'success'

    def default_success(self, data):  # pragma: nocover
        return {
            'no_of_orders': self.success.no_of_orders,
            'no_of_products': self.success.no_of_products,
        }
