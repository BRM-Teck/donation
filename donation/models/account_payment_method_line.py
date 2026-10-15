# Copyright 2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AccountPaymentMethodLine(models.Model):
    _inherit = "account.payment.method.line"

    donation = fields.Boolean(
        help="If enabled, this payment method will be available on donations",
    )

    @api.constrains("donation")
    def _check_donation(self):
        for mode in self:
            if mode.donation and mode.payment_type != "inbound":
                raise ValidationError(
                    self.env._(
                        "Donation payment method '%s' is not an inbound payment "
                        "method.",
                        mode.display_name,
                    )
                )

    @api.onchange("journal_id")
    def _onchange_journal_id_payment_method(self):
        # The methods on offer depend on the journal: a method chosen for
        # another journal would be refused on save.
        for line in self:
            if line.payment_method_id not in line.available_payment_method_ids:
                line.payment_method_id = False
