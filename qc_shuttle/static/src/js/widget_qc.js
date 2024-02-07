odoo.define('template_qc.widget_qc', function(require) {
    "use strict";
    // import object yang dibutuhkan untuk membuat sebuah widget
    var AbstractField = require('web.AbstractField');
    var FieldRegistry = require('web.field_registry');
    var field_utils = require('web.field_utils');
    var session = require('web.session');

    // import qweb untuk merender view
    var core = require('web.core');
    var qweb = core.qweb;

    // buat sebuah object dengan nama bebas
    // jangan lupa untuk extend ke object web.AbstractField atau object turunanya
    var WidgetQc = AbstractField.extend({
        step: 0, // nilai default, jika user tidak mengaturnya di file xml
        template: 'WidgetQcTemplate', // isi nama template yang telah dibuat untuk mengatur tampilan/view widget
        events: { // daftar event, mirip event di jquery
            'click .btn-minus': 'btn_minus_action',
            'click .btn-plus': 'btn_plus_action',
            'click .btn-dollar': 'btn_dollar_action', // tambahan di seri bagian 4
        },
        init: function() {
            // method 'init' dipanggil pertama kali saat widget digunakan
            this._super.apply(this, arguments);
            if (this.nodeOptions.step) {
                // jika user mengatur nilai step di file xml
                // ubah nilai step agar sesuai yang diinput user
                this.step = this.nodeOptions.step;
            }
        },
        btn_minus_action: function() {
            var new_value = this.value - this.step;
            this._setValue(new_value.toString());
        },
        btn_plus_action: function() {
            console.log(this);
            var new_value = this.value + this.step;
            this._setValue(new_value.toString());
        },
        btn_dollar_action: function() {
            var self = this;
            this._rpc({
                model: this.attrs.relatedModel,
                method: this.attrs.modifiers.relatedAction,
                args: [
                    [1, 2], 100, 200
                ],
                kwargs: { value_4: 4000 }
            }).then(function(result) {
                self._setValue(result.toString());
            });


            // session.rpc(
            //     '/tutorial/amount',
            //     {
            //         'oder': [1,2]
            //     }
            // ).then(function(result){
            //     self._setValue(result.toString());
            // });            
        },
        _render: function() {
            // render ulang jika nilai dari field berubah
            // format value agar tampilannya ada pemisah ribuan
            var self = this;
            var formated_value = field_utils.format[this.formatType](this.value);
            this.$el.html($(qweb.render(this.template, { 'widget': this, 'formated_value': formated_value })));
            this.$el.find('.btn-copy').click(function() {
                // kita juga bisa menggunakan kode
                // self.$el.find('input').val();
                // jika kita ingin mendapatkan value dari field one menggunakan jquery
                // dengan cara mengakses element widget
                var putus_pakan = self.value;
                var putus_lusi = self.value;
                var bendera_merah = self.value;
                var bendera_biru = self.value;
                var hb = self.value;
                var oh = self.value;
                var lain_lain = self.value
                var hasil = putus_pakan + putus_lusi + bendera_merah + bendera_biru + hb + oh + lain_lain;
                self.trigger_up('field_changed', {
                    dataPointID: self.dataPointID,
                    viewType: self.viewType,
                    changes: { 'hasil': hasil },
                });
            });
        },
    });

    // daftarkan widget yang telah kita buat ke web.field_registry
    // agar kita bisa menggunakan widget yang kita buat di file xml/view odoo 
    // dengan kode seperti di bawah ini
    // <field name="field_one" widget="widget_one" />
    // nama 'widget_one' ini bebas, asal selalu nyambung/tanpa spasi
    FieldRegistry.add('widget_qc', WidgetQc);

    // return object widget yang telah kita buat
    // agar bisa di-extend atau di-override oleh module lain
    return WidgetQc;

});