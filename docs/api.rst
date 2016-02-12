.. _api:

API Reference
=============

Following is the complete api reference for trytond-sale-channel.

Sale Channel
------------

.. currentmodule:: channel

*Fields*
````````

.. autoattribute:: SaleChannel.name
.. autoattribute:: SaleChannel.code
.. autoattribute:: SaleChannel.active
.. autoattribute:: SaleChannel.company
.. autoattribute:: SaleChannel.address
.. autoattribute:: SaleChannel.source
.. autoattribute:: SaleChannel.read_users
.. autoattribute:: SaleChannel.create_users
.. autoattribute:: SaleChannel.warehouse
.. autoattribute:: SaleChannel.invoice_method
.. autoattribute:: SaleChannel.shipment_method
.. autoattribute:: SaleChannel.currency
.. autoattribute:: SaleChannel.price_list
.. autoattribute:: SaleChannel.payment_term
.. autoattribute:: SaleChannel.order_states
.. autoattribute:: SaleChannel.last_order_import_time
.. autoattribute:: SaleChannel.last_order_export_time
.. autoattribute:: SaleChannel.last_shipment_export_time
.. autoattribute:: SaleChannel.last_product_price_export_time
.. autoattribute:: SaleChannel.last_product_export_time
.. autoattribute:: SaleChannel.last_inventory_export_time
.. autoattribute:: SaleChannel.timezone
.. autoattribute:: SaleChannel.sequence

*Methods*
`````````

.. automethod:: SaleChannel.get_order_states_to_import
.. automethod:: SaleChannel.export_product_prices
.. automethod:: SaleChannel.export_order_status
.. automethod:: SaleChannel.import_orders_using_cron
.. automethod:: SaleChannel.export_product_prices_using_cron
.. automethod:: SaleChannel.get_listings_to_export_inventory
.. automethod:: SaleChannel.export_inventory
.. automethod:: SaleChannel.export_inventory_from_cron
.. automethod:: SaleChannel.import_orders
.. automethod:: SaleChannel.import_order
.. automethod:: SaleChannel.import_products
.. automethod:: SaleChannel.import_product
.. automethod:: SaleChannel.get_product
.. automethod:: SaleChannel.import_order_states
.. automethod:: SaleChannel.get_tryton_action
.. automethod:: SaleChannel.create_order_state
.. automethod:: SaleChannel.get_availability_context
.. automethod:: SaleChannel.get_availability
.. automethod:: SaleChannel.update_order_status_using_cron
.. automethod:: SaleChannel.update_order_status

Sale
----

.. currentmodule:: sale

*Fields*
````````

.. autoattribute:: Sale.channel
.. autoattribute:: Sale.channel_type
.. autoattribute:: Sale.has_channel_exception
.. autoattribute:: Sale.exceptions

*Methods*
`````````

.. automethod:: Sale.process_to_channel_state

Product Channel Listing
-----------------------

.. currentmodule:: product

*Fields*
````````

.. autoattribute:: ProductSaleChannelListing.channel
.. autoattribute:: ProductSaleChannelListing.product
.. autoattribute:: ProductSaleChannelListing.product_identifier
.. autoattribute:: ProductSaleChannelListing.state
.. autoattribute:: ProductSaleChannelListing.quantity
.. autoattribute:: ProductSaleChannelListing.availability_type_used
.. autoattribute:: ProductSaleChannelListing.availability_used
.. autoattribute:: ProductSaleChannelListing.channel_source

*Methods*
`````````

.. automethod:: ProductSaleChannelListing.export_inventory
.. automethod:: ProductSaleChannelListing.export_bulk_inventory
.. automethod:: ProductSaleChannelListing.create_from
.. automethod:: ProductSaleChannelListing.get_availability_context
.. automethod:: ProductSaleChannelListing.get_availability
