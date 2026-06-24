from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ExpenseRecord(models.Model):
    _name = 'expense.record'
    _description = 'Tracking the Expense'

    name = fields.Char(string='Expense Name', required=True)
    date = fields.Date(string='Date', default=fields.Date.today)
    amount = fields.Float(string='Amount', required=True)
    tax = fields.Float(string='Tax')

    total = fields.Float(
        string='Total Amount',
        compute='_compute_total',
        store=True
    )

    category = fields.Selection(
        [
            ('food', 'Food'),
            ('travel', 'Travel'),
            ('bills', 'Bills'),
            ('other', 'Other')
        ],
        string='Category',
        required=True
    )

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('submitted', 'Submitted'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected')
        ],
        string='State',
        default='draft'
    )

    # UI Context evaluation field
    is_manager = fields.Boolean(compute="_compute_is_manager")

     
    is_approved_by_manager = fields.Boolean(string="Approved By Manager", default=False)

    
    is_amount_credited = fields.Boolean(string="Amount Credited Status", default=False)

    @api.depends('amount', 'tax')
    def _compute_total(self):
        for record in self:
            record.total = record.amount + record.tax

    # --- YOUR ORIGINAL VALIDATION CODE UNCHANGED ---
    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if any(char.isdigit() for char in record.name):
                raise ValidationError(
                    "Expense Name should not contain numbers."
                )
    # -----------------------------------------------

    @api.depends_context('uid')
    def _compute_is_manager(self):
        for rec in self:
            rec.is_manager = self.env.user.has_group(
                'expense_manager.group_expense_manager' 
            )


    def action_toggle_credited(self):
        for record in self:
            record.is_amount_credited = not record.is_amount_credited