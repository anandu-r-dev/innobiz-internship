from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Library Book"

    book_title = fields.Char(string="Book Title", required=True)
    author = fields.Char(string="Author", required=True)
    isbn = fields.Char(string="ISBN", required=True)
    book_loc = fields.Char(string="Book Location")
    status = fields.Selection(
        [('return', 'Return'),
         ('borrow', 'Borrow')],
        string="Status",
        default='return'
    )
    

    available = fields.Boolean(string="Available", default=True)
    total_copies = fields.Integer(string="Total Copies")
    borrowed_copies = fields.Integer(string="Borrowed Copies")
    available_copies = fields.Integer(
        string="Available Copies",
        compute="_compute_available_copies",
        store=True
    )

    @api.depends('total_copies', 'borrowed_copies')
    def _compute_available_copies(self):
        for rec in self:
            rec.available_copies = rec.total_copies - rec.borrowed_copies

    late_days = fields.Integer(string="Late Days")
    fine = fields.Float(
        string="Fine",
        compute="_compute_fine",
        store=True
    )


    @api.depends('late_days')
    def _compute_fine(self):
        for rec in self:
            rec.fine = rec.late_days * 10
    
    fine_paid = fields.Boolean(
        string="Fine Paid",
        default=False
    )

    def action_fine_paid(self):
        for rec in self:
            rec.fine_paid = not rec.fine_paid
   

    @api.constrains('isbn')
    def _check_isbn(self):
        for rec in self:
            if rec.isbn and not rec.isbn.isdigit():
                raise ValidationError("ISBN must contain only numbers.")