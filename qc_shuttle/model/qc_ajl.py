from odoo import  api, models, fields, _
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

class SnapQcAjl(models.Model):
    _name = 'snap.qc.ajl'
    _description = 'Snap Qc Ajl'
    
    
    putus_lusi = fields.Integer('Putus Lusi')
    putus_pakan = fields.Integer('Putus Pakan')
    naik_beam = fields.Integer(string="Naik Beam Baru")
    hb = fields.Integer('Habis Beam')
    troble_kualitas = fields.Integer(string="Troble Kualitas")
    troble_mekanik = fields.Integer(string="Troble Mekanaik")
    tunggu_beam_cucuk = fields.Integer(string="Tunggu Beam/Cucuk")
    lain_lain = fields.Integer('Lain-lain')
    shift = fields.Selection([
        ('A',_('A')),
        ('B',_('B')),
        ('C',_('C')),
    ],string="Shift")
    tgl = fields.Datetime(string="Tanggal Snap",default=fields.Datetime.now,readonly=True)
    total_mesin = fields.Integer(string="Total Mesin",default=14,readonly=True)
    total_snap = fields.Integer(string="Hasil Snap",compute='tambah',readonly=True,store=True)
    mesin_stop = fields.Float(string='Mesin Stop',compute="resume",readonly=True,store=True)
    total_mesin_jalan = fields.Float(string="Mesin Jalan", compute="total",readonly=True,store=True)
    
    @api.depends('total_mesin','shift')         
    def tambah(self):
        for tam in self:
            if tam.total_mesin:
                tam.total_snap = tam.putus_pakan + tam.putus_lusi  + tam.naik_beam + tam.hb + tam.troble_mekanik + tam.troble_kualitas + tam.tunggu_beam_cucuk + tam.lain_lain
            else:
                tam.total_snap = 0
    
    
    @api.depends('total_mesin','shift')
    def resume(self):
        for res in self:
            if res.total_mesin:
                res.mesin_stop = res.total_snap / res.total_mesin
            else:
                res.mesin_stop = 0
                

    @api.depends('total_mesin','shift')
    def total(self):
        for tot in self:
            if tot.total_mesin:
                # mesin = tot.total_snap/tot.total
                tot.total_mesin_jalan = (tot.total_mesin - tot.total_snap)/ tot.total_mesin
            else:
                tot.total_mesin_jalan = 0
    