odoo.define('qc_shuttle.qc_widget', function (require) { 
    "use strict";
  
    var AbstractField = require('web.AbstractField');
    var FieldRegistry = require('web.field_registry');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var qweb = core.qweb;
    
    var QcWidget = AbstractField.extend({
        template: 'WidgetQcTemplate',
  
        events: {
            'click .button_tambah_snap': '_onClickButton',
        },
        
        _onClickButton: function () {
            var self = this;
            var deret_value = this.$('input[name="deret_value"]:checked').val();
                if(deret_value){
                    console.log("Deret Sudah Di Pilih 😉");
                }else{
                    console.log("Deret Belum Di Pilih ⛔");
                }
            var mesin_produksi_id = this.$('input[name="mesin_produksi_id"]:checked').val();
                if(mesin_produksi_id){
                    console.log("Nomor Mesin Sudah Di Pilih 😉");
                }else{
                    console.log("Nomor Mesin Belum Di Pilih ⛔");
                }
            var putus_lusi = this.$('#putusLusi').is(":checked");
                if (putus_lusi) {
                    console.log("putus_lusi sudah di centang! 😉");
                } else {
                    console.log("putus_lusi tidak di centang ⛔");
                }
            var putus_pakan =this.$('input[data-field="putus_pakan"]').is(":checked");
                if (putus_pakan) {
                    console.log("putus_pakan sudah di centang! 😉");
                } else {
                    console.log("putus_pakan tidak di centang ⛔");
                }
            var bendera_merah =this.$('input[data-field="bendera_merah"]').is(":checked");
                if (bendera_merah){
                    console.log("bendera_merah sudah di centang !😉");
                }else{
                    console.log("bendera_merah tidak di centang ⛔");
                }
            var ambrol =this.$('input[data-field="ambrol"]').is(":checked"); 
                if (ambrol){
                    console.log("ambrol sudah di centang ! ");
                }else{
                    console.log("ambrol tidak di centang ⛔");
                }
            var dedel =this.$('input[data-field="dedel"]').is(":checked");
                if (dedel){
                    console.log("dedel sudah di centang ! 😉");
                }else{
                    console.log("dedel tidak di centang ⛔");
                }
            var hb =this.$('input[data-field="hb"]').is(":checked");
                if (hb){
                    console.log("habis beam sudah di centang ! 😉");
                }else{
                    console.log("habis beam tidak di centang ⛔");
                }
            var naik_beam =this.$('input[data-field="naik_beam"]').is(":checked");
                if (naik_beam){
                    console.log("naik_beam sudah di centang ! 😉");
                }else{
                    console.log("naik_beam tidak di centang ⛔");
                }
            var oh =this.$('input[data-field="oh"]').is(":checked");
                if (oh){
                    console.log("oh sudah di centang ! 😉");
                }else{  
                    console.log("oh tidak di centang ⛔");
                }
            var preventif =this.$('input[data-field="preventif"]').is(":checked");
                if (preventif){
                    console.log("preventif sudah di centang ! 😉");
                }else{
                    console.log("preventif tidak di centang ⛔");
                }
            var lain_lain =this.$('textarea[data-field="lain_lain"]').val();
                if(lain_lain){
                    console.log("Keterangan Sudah Di isi 😉");
                }else{
                    console.log("Keterangan Belum Di Isi ⛔");
                }

            console.log(this);   
                
            this.saveDataSnap({
                deret_value: deret_value,
                mesin_produksi_id: mesin_produksi_id,
                putus_lusi: putus_lusi,
                putus_pakan: putus_pakan,
                bendera_merah: bendera_merah,
                ambrol: ambrol,
                dedel: dedel,
                hb: hb,
                naik_beam: naik_beam,
                oh: oh,
                preventif: preventif,
                lain_lain: lain_lain,
            });
        },
        
        saveDataSnap: function (data) {
            var self = this;
            rpc.query({
                model: 'snap.qc.line',
                method: 'create',
                args: [data],
            }).then(function (result) {
                console.log('Berhasil Simpan Data 😀 :', result);
            }).catch(function (error) {
                console.error('Gagal Menyimpan Data ⛔ :', error);
            });
         },
  
        _render: function() {
            var self = this;
            if (!this.get('effective_readonly')) {
                this.$el.html(qweb.render('WidgetQcTemplate', {widget: self}));
            }
        },
    });
  
    FieldRegistry.add('qc_widget', QcWidget);
    
    return QcWidget;
 });
 