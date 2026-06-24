from odoo import models

class ExpenseReport(models.AbstractModel):
    _name = 'report.expense_manager.expense_report_template'
    _description = 'Expense Summary Report'

    def _get_report_values(self, docids, data=None):
        expenses = self.env['expense.record'].search([])
        grand_total = sum(expenses.mapped('total'))

        return {
            'docs': expenses,
            'grand_total': grand_total,
        }