from odoo import models

class TaskSummaryReport(models.AbstractModel):
    _name = 'report.task_tracker.report_task_summary_template'
    _description = 'Task Summary Report'

    def _get_report_values(self, docids, data=None):
        tasks = self.env['task.tracker'].search([])

        return {
            'docs': tasks,
        }