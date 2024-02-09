from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class DeretMesin(models.Model):
    _name ='deret.mesin.produksi'
    _description='Deret Mesin Produksi'


    nama_deret = fields.Char(string="Deret")
    total_mesin = fields.Char(string="Total Mesin")


     # Id Record Data
    def name_get(self):
        result = [] 
        for record in self:
            nama_deret = record.nama_deret 
            result.append((record.id, nama_deret))
        return result 