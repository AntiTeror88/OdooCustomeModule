from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class Produksi(models.Model):
	_name = 'mesin.produksi'
	_description = 'Mesin Produksi'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Char("No Mesin",tracking=True)
	mesin = fields.Char(string="Nama Mesin",tracking=True)
	divisi_id = fields.Many2one(string="DIVISI", comodel_name="divisi.divisi", ondelete="set null")
	block = fields.Char(string="Blok Mesin")
	deret = fields.Char(string="Deret")
	rpm = fields.Integer(string='RPM')
	reference = fields.Char(compute='_name_mesin', string='Reference', store=True)
	# plan_id = fields.Many2one('plan.mes', 'Plan', required=False,)
	state = fields.Selection([('open','Kosong'),
							('progres','Proses Naik Beam'),
                            ('done', 'Mesin Jalan'),
                            ('close', 'Turun Beam')], string="Status", readonly=True, copy=False, )
	blok_mesin_id= fields.Many2one('blok.mesin.produksi', string="Blok Mesin")
	deret_mesin_id = fields.Many2one('deret.mesin.produksi',string="Deret")

	 # Tombol Kosong  
	def action_open(self):
		self.write({'state': 'open'}) 
	# Tombol Mesin Jalan
	def action_progress(self):
		self.write({'state': 'progress'})
	# Tombol Turun Beam
	def action_done(self): 
		self.write({'state': 'done'})
	# Tombol Cancel
	def action_close(self):
		self.write({'state': 'close'})   
	
	def _name_mesin(self):
    		for mesin in self:
      			mesin.reference = mesin.name