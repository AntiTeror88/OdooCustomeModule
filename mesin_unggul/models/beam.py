from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class beam(models.Model):
    _name = "nomor.beam"
    _description = 'Nomor Beam'
    _rec_name = "no_beam"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    no_beam = fields.Char(string="No Beam", tracking=True)
    divis_id = fields.Many2one(string="DIVISI", comodel_name="divisi.divisi", ondelete="set null")
    state = fields.Selection([('plan','Open'),
                            ('stock','Stock'),
                            ('cancel','Cancel'),
                            ('tying','Tying'),
                            ('cucuk', "Cucuk "),
                            ('done', 'Naik Mesin'),
                            ('close', 'Turun Beam')], string="Status", readonly=True, copy=False, )
	
	