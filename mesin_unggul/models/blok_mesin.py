from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class BlokMesin(models.Model):
    _name ='blok.mesin.produksi'
    _description='Blok Mesin Produksi'


    nama_blok = fields.Char(string="Blok")
    total_mesin = fields.Char(string="Total Mesin")

     # Id Record Data
    def name_get(self):
        result = [] 
        for record in self:
            nama_blok = record.nama_blok
            result.append((record.id, nama_blok))
        return result 