{
	"name": "Data Mesin Produksi",
	"version": "2.0",
	"depends": [
				"hr","mrp"],
	"author": "hendri@gmail.com",
	"category": "Develope",
	'website': 'blog@gmail.com',
	"description": """\
	Devlope 
	""",
	"data": [ 
		'security/ir.model.access.csv',
		'security/security.xml',
		'views/menu.xml',
		'views/produksi.xml',
		'views/blok_mesin.xml',
		'views/deret_mesin.xml',
		#'view/kerusakan.xml',
		'views/divisi.xml',
		'views/no_beam.xml',
		"views/location.xml",
		#'views/shuttle.xml',
		#'views/rapier.xml',
		#'views/bs.xml',
		#'report/report_bs.xml',
		#'report/report_bs_total.xml',
		#"report/action_report_mesin.xml",
		#"report/report_mesin.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": True,
}