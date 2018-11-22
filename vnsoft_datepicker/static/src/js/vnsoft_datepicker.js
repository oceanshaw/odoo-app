odoo.define('vnsoft.datepicker', function (require) {
"use strict";

var DatePicker = require('web.datepicker');

DatePicker.DateWidget.include({
        init: function (parent, options) {
            var self = this;
            this._super.apply(this, arguments);
            this.minDate = parent.node.attrs.mindate;
            this.maxDate = parent.node.attrs.maxdate;
            this.pobj = parent;
        },
        year:function(){
          return 2017
        },
        month:function () {
            return 9
        },

        set_datetime_default: function () {
            if (this.minDate == undefined){
                this.picker.options.minDate = moment().add(-36500,'day');
            }
            else if( !isNaN(this.minDate)) {
                this.picker.options.minDate = moment().add(parseInt(this.minDate),'day');
            } else {
                var d = this.pobj.field_manager.fields[this.minDate].get('value');
                if (d!=undefined) {
                    this.picker.options.minDate = moment().add(this.DateMinus(d),'day');
                } else {
                    this.picker.options.minDate = moment().add(-36500,'day');
                }
            }
            if (this.maxDate == undefined){
                this.picker.options.maxDate = moment().add(3650,'day');
            }
            else if(!isNaN(this.maxDate)) {
                this.picker.options.maxDate = moment().add(parseInt(this.maxDate),'day');
            } else {
                var d = this.pobj.field_manager.fields[this.maxDate].get('value');
                if (d!=undefined) {
                    this.picker.options.maxDate = moment().add(this.DateMinus(d),'day');
                } else {
                    this.picker.options.maxDate = moment().add(3650,'day');
                }
            }

            return this._super.apply(this, arguments);
        },
        is_valid: function () {
            var res = this._super.apply(this, arguments);
            var value_ = this.$input.val();
            debugger;
            if (this.minDate != undefined) {
                if (!isNaN(this.minDate)) {
                    if (this.DateMinus(value_) < parseInt(this.minDate)) {
                        return false;
                    }
                } else {
                    var d = this.pobj.field_manager.fields[this.minDate].get('value');
                    if (d && this.DateMinus(value_) < this.DateMinus(d)) {
                        return false;
                    }
                }
            }
            if (this.maxDate != undefined) {
                if (!isNaN(this.maxDate)) {
                    if (this.DateMinus(value_) > parseInt(this.maxDate)) {
                        return false;
                    }
                } else {
                    var d = this.pobj.field_manager.fields[this.maxDate].get('value');
                    if (d && this.DateMinus(value_) > this.DateMinus(d)) {
                        return false;
                    }
                }
            }
            return res
        },
        DateMinus: function (sDate) {
            var sdate = new Date(moment(sDate,this.options.format).format("YYYY/MM/DD"));
            var now = new Date();
            now = new Date(now.getFullYear() + "/" + (now.getMonth() + 1) + "/" + now.getDate());
            var days = sdate.getTime() - now.getTime();
            var day = parseInt(days / (1000 * 60 * 60 * 24));
            return day;
        }
    });
return DatePicker;
})
