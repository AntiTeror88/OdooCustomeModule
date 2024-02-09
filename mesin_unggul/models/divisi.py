from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class divisi(models.Model):
	_name = "divisi.divisi"
	_description = 'Divisi Divisi'
	_rec_name = 'name'

	name = fields.Many2one(comodel_name='hr.department', string="DIVISI")


#class divisi(models.Model):
#	_name = "divisi.divisi"
#	_rec_name = "name"
#
#	name = fields.Selection([
#        ('SECURITY',_('SECURITY')),
#        ('HRD',_('HRD')),
		# ('GUDANG',_('GUDANG')),
		# ('PERSIAPAN WARPING',_('PERSIAPAN WARPING')),
		# ('PERSIAPAN SIZING',_('PERSIAPAN SIZING')),
		# ('PERSIAPAN CUCUK',_('PERSIAPAN CUCUK')),
		# ('PERSIAPAN PALET',_('PERSIAPAN PALET')),
		# ("WEAVING SHUTTLE",_("WEAVING SHUTTLE")),
		# ("WEAVING RAPIER",_("WEAVING RAPIER")),
		# ("INSPECTING",_("INSPECTING")),
		# ("DLB",_("DLB")),
		# ("UTILITY",_("UTILITY")),
		# ], string="DIVISI", required=True,)