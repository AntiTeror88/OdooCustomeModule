from odoo import  api, models, fields, _
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import datetime, timedelta
from odoo.tools import float_compare, float_round, float_is_zero, format_datetime
from odoo.tools.misc import format_date

class SnapQc(models.Model):
    _name = 'snap.qc'
    _description = 'Snap Qc' 
    _date_name = 'date_planned_start'
    
    # Relasi ke model hr.employee
    operator = fields.Many2one('hr.employee', string='Operator')
    # Relasi ke model snap.qc.line (child class)
    snap_qc_line = fields.One2many('snap.qc.line', 'snap_qc_id') 
    tanggal_snap = fields.Datetime(string="Tanggal Snap", default=fields.Datetime.now)
    
    # Relasi ke model mesin.produksi dari modul mesin_unggul(mesin_produksi.py)
    # untuk menampilkan nomor_mesin menggunakan domain field deret.
    mesin_produksi_id = fields.Many2one('mesin.produksi', string='Mesin Produksi')
    deret = fields.Many2one('deret.mesin.produksi',
    string="Deret",domain="[('nama_deret', 'like', 'LINE SHUTTLE%')]")

    # field yang digunakan untuk menampilakn total dari masing masing kerusakkan
    # menggunakan compute
    total_snap=fields.Integer(string="Total Snap", compute='_compute_total_snap')  
    
    # Fungsi untuk menampilkan total snap dari masing masing kerusakkan
    @api.depends('snap_qc_line.putus_pakan', 'snap_qc_line.putus_lusi', 'snap_qc_line.ambrol', 'snap_qc_line.dedel', 'snap_qc_line.preventif', 'snap_qc_line.oh', 'snap_qc_line.naik_beam', 'snap_qc_line.hb', 'snap_qc_line.bendera_merah', 'snap_qc_line.lain_lain')
    def _compute_total_snap(self):
        for record in self:
            total_snap = 0
            for line in record.snap_qc_line:
                total_snap += 1 if line.putus_lusi else 0
                total_snap += 1 if line.putus_pakan else 0
                total_snap += 1 if line.bendera_merah else 0
                total_snap += 1 if line.ambrol else 0
                total_snap += 1 if line.dedel else 0
                total_snap += 1 if line.hb else 0
                total_snap += 1 if line.naik_beam else 0
                total_snap += 1 if line.oh else 0
                total_snap += 1 if line.preventif else 0
                total_snap += 1 if line.lain_lain else 0
            record.total_snap = total_snap   

    # field untuk menampilkan total mesin
    total_mesin = fields.Integer(string='Total Mesin', compute='_compute_total_mesin', store=True)

    # Query untuk menampilkan total mesin 
    # yang ada pada model mesin.produksi
    @api.depends('mesin_produksi_id')
    def _compute_total_mesin(self):
        for record in self:
            total_mesin = self.env['mesin.produksi'].sudo().search_count([])

            record.total_mesin = total_mesin       

    #field untuk menampilkan presentasi dari mesin yang mati
    presentasi_mesin_mati = fields.Float(string='Presentasi Mesin Mati', compute='_compute_presentasi_mesin_mati', store=True)

    # fungsi compute untuk menampilkan presentasi mesin mati
    @api.depends('total_snap', 'total_mesin')
    def _compute_presentasi_mesin_mati(self):
        for record in self:
            if record.total_mesin != 0:
                presentasi_mesin_mati = (record.total_snap / record.total_mesin) * 100
            else:
                presentasi_mesin_mati = 0

            record.presentasi_mesin_mati = presentasi_mesin_mati
 
    # field yang berfungsi untuk menampilkan mesin yang berjalan
    total_mesin_jalan = fields.Integer(string='Total Mesin Jalan', compute='_compute_total_mesin_jalan', store=True)

    # compute untuk menampilkan total mesin yang jalan
    @api.depends('total_mesin', 'total_snap')
    def _compute_total_mesin_jalan(self):
        for record in self:
            total_mesin_jalan = record.total_mesin - record.total_snap
            record.total_mesin_jalan = total_mesin_jalan

    # field yang berfungsi untuk menampilkan presentasi dari mesin jalan
    presentasi_mesin_jalan = fields.Float(string='Presentasi Mesin Jalan', compute='_compute_presentasi_mesin_jalan', store=True)

    # compute untuk menampilkan presentasi mesin jalan
    @api.depends('total_snap', 'total_mesin')
    def _compute_presentasi_mesin_jalan(self):
        for record in self:
            total_mesin = record.total_mesin
            total_snap = record.total_snap

            record.presentasi_mesin_jalan = (total_mesin - total_snap) / total_mesin * 100 if total_mesin != 0 else 0
    
    shift = fields.Selection([
        ('1', 'Shift A'),
        ('2', 'Shift B'),
        ('3', 'Shift C')
    ], string='Shift')
    
    putaran = fields.Selection([
            ('1', 'Putaran 1'),
            ('2', 'Putaran 2'),
            ('3', 'Putaran 3')
        ], string='Putaran')
    
    state    = fields.Selection([
            ('draft','Draft'),
            ('start','Confirmed'),
            ('progress','In Progress'),
            ('done', 'Done'),
            ('cancel', 'Cancelled')], 
            string="Status", readonly=True,copy=False, default="draft",track_visibility='onchange', widget='statusbar')            
    
    # Id Record Data
    def name_get(self):
        result = [] 
        for record in self:
            name = record.name 
            result.append((record.id, name))
        return result 
    
    name = fields.Char('Snap Reference', copy=False, readonly=True,default='New')
    
    # Kode Untuk Sequence QC/SHTL/0000
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('snap.qc.sequence') or 'New'
        return super(SnapQc, self).create(vals)
    
    date_planned_start = fields.Datetime(
        'Snap Date',
        copy=False,
        default=lambda self: fields.Datetime.now(),
        help="Date at which you plan to start the Snap.",
        index=True,
    )
    
    date_planned_finished = fields.Datetime(
        'Selesai Snap',
        default=lambda self: fields.Datetime.now() + timedelta(hours=8),
        compute='_compute_date_planned_finished',
        help="Date at which you plan to finish the Snap.",
        copy=False
    )
    
    date_deadline = fields.Datetime(
        'Deadline',
        copy=False ,
        store=True,
        compute='_compute_date_deadline',
        inverse='_set_date_deadline',
        help="Informative date allowing to define when the quality control should be processed at the latest to finish on time."
    )
    
    @api.depends('date_planned_start')
    def _compute_date_deadline(self):
        for record in self:
            if record.date_planned_start:
                record.date_deadline = record.date_planned_start + timedelta(hours=8)
    
    def _set_date_deadline(self):
        for record in self:
            if record.date_planned_start:
                record.date_deadline = record.date_planned_start + timedelta(hours=8)

    @api.model
    def _get_default_date_planned_finished(self):
        if self.env.context.get('default_date_planned_start'):
            return fields.Datetime.to_datetime(self.env.context.get('default_date_planned_start')) + timedelta(hours=8)
        return datetime.now() + timedelta(hours=8)
    
    @api.depends('date_planned_start')
    def _compute_date_planned_finished(self):
        for record in self:
            if record.date_planned_start:
                record.date_planned_finished = record.date_planned_start + timedelta(hours=8)  
    
    # Field untuk menghitung total dari masing masing kerusakkan dengan menggunakan compute
    total_putus_lusi = fields.Integer(string='Total Putus Lusi', compute='_compute_total_putus_lusi')
    total_putus_pakan = fields.Integer(string='Total Putus Pakan', compute='_compute_total_putus_pakan')
    total_bendera_merah = fields.Integer(string='Total Bendera Merah', compute='_compute_total_bendera_merah')
    total_ambrol = fields.Integer(string='Total Ambrol', compute='_compute_total_ambrol')
    total_dedel = fields.Integer(string='Total Dedel', compute='_compute_total_dedel')
    total_hb = fields.Integer(string='Total Habis Beam/Beam Baru', compute='_compute_total_hb')
    total_naik_beam = fields.Integer(string='Total Naik Beam', compute='_compute_total_naik_beam')
    total_oh = fields.Integer(string='Total Over Houle', compute='_compute_total_oh')
    total_preventif = fields.Integer(string='Total Preventif', compute='_compute_total_preventif')
    total_lain_lain = fields.Integer(string='Total Lain Lain', compute='_compute_total_lain_lain')
    
    @api.depends('snap_qc_line.putus_lusi')
    def _compute_total_putus_lusi(self):
        for record in self:
            record.total_putus_lusi = sum(record.snap_qc_line.mapped('putus_lusi'))

    @api.depends('snap_qc_line.putus_pakan')
    def _compute_total_putus_pakan(self):
        for record in self:
            record.total_putus_pakan = sum(record.snap_qc_line.mapped('putus_pakan'))

    @api.depends('snap_qc_line.bendera_merah')
    def _compute_total_bendera_merah(self):
        for record in self:
            record.total_bendera_merah = sum(record.snap_qc_line.mapped('bendera_merah'))

    @api.depends('snap_qc_line.ambrol')
    def _compute_total_ambrol(self):
        for record in self:
            record.total_ambrol = sum(record.snap_qc_line.mapped('ambrol'))

    @api.depends('snap_qc_line.dedel')
    def _compute_total_dedel(self):
        for record in self:
            record.total_dedel = sum(record.snap_qc_line.mapped('dedel'))

    @api.depends('snap_qc_line.hb')
    def _compute_total_hb(self):
        for record in self:
            record.total_hb = sum(record.snap_qc_line.mapped('hb'))

    @api.depends('snap_qc_line.naik_beam')
    def _compute_total_naik_beam(self):
        for record in self:
            record.total_naik_beam = sum(record.snap_qc_line.mapped('naik_beam'))

    @api.depends('snap_qc_line.oh')
    def _compute_total_oh(self):
        for record in self:
            record.total_oh = sum(record.snap_qc_line.mapped('oh'))

    @api.depends('snap_qc_line.preventif')
    def _compute_total_preventif(self):
        for record in self:
            record.total_preventif = sum(record.snap_qc_line.mapped('preventif'))

    @api.depends('snap_qc_line.lain_lain')
    def _compute_total_lain_lain(self):
        for record in self:
            record.total_lain_lain = sum(1 for line in record.snap_qc_line if line.lain_lain)
    
    #Field untuk menghitung rata-rata dari masing masing kerusakkan 
    rata_rata_putus_lusi = fields.Float(string='Rata-rata Putus Lusi', compute='_compute_rata_rata_putus_lusi', store=True)
    rata_rata_putus_pakan = fields.Float(string='Rata-rata Putus Pakan', compute='_compute_rata_rata_putus_pakan', store=True)
    rata_rata_bendera_merah = fields.Float(string='Rata-rata Bendera Merah', compute='_compute_rata_rata_bendera_merah', store=True)
    rata_rata_ambrol = fields.Float(string='Rata-rata Ambrol', compute='_compute_rata_rata_ambrol', store=True)
    rata_rata_dedel = fields.Float(string='Rata-rata Dedel', compute='_compute_rata_rata_dedel', store=True)
    rata_rata_hb = fields.Float(string='Rata-rata Habis Beam/Beam Baru', compute='_compute_rata_rata_hb', store=True)
    rata_rata_naik_beam = fields.Float(string='Rata-rata Naik Beam', compute='_compute_rata_rata_naik_beam', store=True)
    rata_rata_oh = fields.Float(string='Rata-rata Over Houle', compute='_compute_rata_rata_oh', store=True)
    rata_rata_preventif = fields.Float(string='Rata-rata Preventif', compute='_compute_rata_rata_preventif', store=True)
    rata_rata_lain_lain = fields.Float(string='Rata-rata Lain Lain', compute='_compute_rata_rata_lain_lain', store=True)
    
    @api.depends('total_putus_lusi', 'total_mesin')
    def _compute_rata_rata_putus_lusi(self):
        for record in self:
            record.rata_rata_putus_lusi = record.total_putus_lusi / record.total_mesin if record.total_mesin != 0 else 0

    @api.depends('total_putus_pakan', 'total_mesin')
    def _compute_rata_rata_putus_pakan(self):
        for record in self:
            record.rata_rata_putus_pakan = record.total_putus_pakan / record.total_mesin if record.total_mesin != 0 else 0

    @api.depends('total_bendera_merah', 'total_mesin')
    def _compute_rata_rata_bendera_merah(self):
        for record in self:
            record.rata_rata_bendera_merah = record.total_bendera_merah / record.total_mesin if record.total_mesin != 0 else 0

    @api.depends('total_ambrol', 'total_mesin')
    def _compute_rata_rata_ambrol(self):
        for record in self:
            record.rata_rata_ambrol = record.total_ambrol / record.total_mesin if record.total_mesin != 0 else 0

    @api.depends('total_dedel', 'total_mesin')
    def _compute_rata_rata_dedel(self):
        for record in self:
            record.rata_rata_dedel = record.total_dedel / record.total_mesin if record.total_mesin != 0 else 0

    @api.depends('total_hb', 'total_mesin')
    def _compute_rata_rata_hb(self):
        for record in self:
            record.rata_rata_hb = record.total_hb / record.total_mesin if record.total_mesin != 0 else 0

    @api.depends('total_naik_beam', 'total_mesin')
    def _compute_rata_rata_naik_beam(self):
        for record in self:
            record.rata_rata_naik_beam = record.total_naik_beam / record.total_mesin if record.total_mesin != 0 else 0

    @api.depends('total_oh', 'total_mesin')
    def _compute_rata_rata_oh(self):
        for record in self:
            record.rata_rata_oh = record.total_oh / record.total_mesin if record.total_mesin != 0 else 0

    @api.depends('total_preventif', 'total_mesin')
    def _compute_rata_rata_preventif(self):
        for record in self:
            record.rata_rata_preventif = record.total_preventif / record.total_mesin if record.total_mesin != 0 else 0

    @api.depends('total_lain_lain', 'total_mesin')
    def _compute_rata_rata_lain_lain(self):
        for record in self:
            record.rata_rata_lain_lain = record.total_lain_lain / record.total_mesin if record.total_mesin != 0 else 0

class SnapQcLine(models.Model):
    _name='snap.qc.line'
    _description='Hasil Snap'

    # Relasi balik ke model snap.qc (parent class)
    snap_qc_id = fields.Many2one('snap.qc', string='Snap QC', ondelete='cascade', index=True, copy=False)
    
    # Relasi ke model mesin.produksi dari modul mesin_unggul (mesin_produksi.py)
    # untuk menampilkan data mesin dari model mesin_produksi (Mesin Unggul).
    mesin_produksi_id = fields.Many2one('mesin.produksi', string='Mesin Produksi')
    deret = fields.Many2one('deret.mesin.produksi',string="Deret")
    
    #Field Tanggal 
    tanggal_snap = fields.Date(string="Tanggal Snap", default=fields.Date.context_today)
    
    #Kerusakkan Pada Mesin 
    putus_lusi = fields.Boolean(string="Putus Lusi")
    putus_pakan=fields.Boolean(string='Putus Pakan')
    bendera_merah = fields.Boolean(string=" Bendera Merah")
    ambrol = fields.Boolean(string="Ambrol")
    dedel=fields.Boolean(string="Dedel")  
    hb = fields.Boolean(string="Habis Beam/Beam Baru")
    naik_beam = fields.Boolean(string="Naik Beam")
    oh = fields.Boolean(string="Over Houle")
    preventif = fields.Boolean(string="Preventif")
    lain_lain  =  fields.Text(string="Lain Lain")
    keterangan = fields.Text(string="Keterangan") 
    
    line_mesin = fields.Char(string="Deret", onchange="_onchange_mesin_produksi_id")
    
    @api.onchange('mesin_produksi_id')
    def _onchange_mesin_produksi_id(self):
        if self.mesin_produksi_id:
            self.line_mesin = self.mesin_produksi_id.deret
        else:
            self.line_mesin = False


    