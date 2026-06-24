from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessError, UserError
from datetime import date

class TaskTracker(models.Model):
    _name = 'task.tracker'
    _description = 'Task Tracker'

    task_code = fields.Char(string='Task Code')
    name = fields.Char(string='Task Name', required=True)
    description = fields.Text(string='Description')

    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string='Priority')

    deadline = fields.Date(string='Deadline')
    is_done = fields.Boolean(string='Completed', default=False)
    status = fields.Char(string='Status', compute='_compute_status', store=True)
    
    # RENAMED and kept non-stored so it updates dynamically on every page refresh
    deadline_live_status = fields.Char(string='Deadline Status', compute='_compute_deadline_live_status')
    
    is_manager = fields.Boolean(compute='_compute_is_manager')

    # ---------------- USER PERMISSION CHECK ----------------
    @api.depends_context('uid')
    def _compute_is_manager(self):
        for rec in self:
            user = self.env.user
            is_admin_or_manager = user.has_group('base.group_system') or user.name == 'Manager' or user.login == 'manager'
            rec.is_manager = is_admin_or_manager

    # ---------------- STATUS ----------------
    @api.depends('is_done')
    def _compute_status(self):
        for rec in self:
            rec.status = 'Completed' if rec.is_done else 'Pending'

    # ---------------- DEADLINE COMPUTE ----------------
    @api.depends('deadline')
    def _compute_deadline_live_status(self):
        today = date.today()
        for rec in self:
            if rec.deadline:
                days = (rec.deadline - today).days
                if days > 0:
                    rec.deadline_live_status = f"{days} days left"
                elif days < 0:
                    rec.deadline_live_status = f"{abs(days)} days overdue"
                else:
                    rec.deadline_live_status = "Today"
            else:
                rec.deadline_live_status = "No Deadline"

    # ---------------- VALIDATION ----------------
    @api.constrains('task_code')
    def _check_task_code(self):
        for rec in self:
            if rec.task_code and not rec.task_code.isdigit():
                raise ValidationError("Task Code must contain only numbers.")

    # ---------------- BACKEND SECURITY RULE ----------------
    def write(self, vals):
        if 'is_done' in vals:
            user = self.env.user
            is_allowed = user.has_group('base.group_system') or user.name == 'Manager' or user.login == 'manager'
            if not is_allowed:
                raise AccessError("Only an Administrator or Manager can change the task status.")
        return super(TaskTracker, self).write(vals)

    # ---------------- BUTTON METHOD ----------------
    def action_request_deadline_extension(self):
        """ Opens a wizard modal window to collect extension details """
        self.ensure_one()
        
        # Guard clause against triggering requests on completed tasks
        if self.is_done:
            raise UserError("This task is already completed. Deadline extensions cannot be requested.")
            
        return {
            'name': 'Request Deadline Extension',
            'type': 'ir.actions.act_window',
            'res_model': 'task.deadline.extension.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_task_id': self.id}
        }


class TaskDeadlineExtensionWizard(models.TransientModel):
    _name = 'task.deadline.extension.wizard'
    _description = 'Deadline Extension Wizard'

    task_id = fields.Many2one('task.tracker', string="Task", required=True)
    new_deadline = fields.Date(string="Proposed New Deadline", required=True)
    reason = fields.Text(string="Reason for Extension", required=True)

    def action_submit_request(self):
        self.ensure_one()
        if self.new_deadline <= date.today():
            raise ValidationError("The proposed deadline must be a future date.")
        
        note = f"**Deadline Extension Requested**\n" \
               f"Proposed Date: {self.new_deadline}\n" \
               f"Reason: {self.reason}"
               
        existing_desc = self.task_id.description or ""
        self.task_id.write({
            'description': f"{existing_desc}\n\n{note}"
        })
        return {'type': 'ir.actions.act_window_close'}