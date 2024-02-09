
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class Location(models.Model):
    _name = "loc.tem"
    _description = 'Loc Tem'
    _rec_name = 'tempat'

    name = fields.Integer(string="Id Location")
    tempat = fields.Char(string="Nama Lokasi")