{
  'name': 'Snap QC Shuttle',
  'version': '14.0',
  'author': 'Steven Morison',
  'summary': 'Pengecekkan Mesin Shuttle Unggulrejo Wasono',
  'author': 'Steven Morison, stevenmorizon123@gmail.com',
  'category': 'Manufacture',
  'depends': ['base', 'web', 'mesin_unggul'],
  'data': [
 
    'security/ir.model.access.csv',
    'views/view_layout_shuttle.xml',
    'views/view_snap_qc.xml',
    'views/view_snap_qc_pop_up.xml',
    'views/css_loader.xml',
    'report/report_menu.xml',
    'report/report_qc_shuttle.xml',
  ],

  'auto_install': False,
  'installable': True,
  'application': True,
}
