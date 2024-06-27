from datetime import date

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError


class TGRoomsOrder(models.Model):
    _name = "tg.room.orders"

    name = fields.Char("Nama Pemesan", store=True)
    order_id = fields.Char(string='Order ID', required=True, copy=False,
                                 readonly=True, default=lambda self:_('New'))
    room = fields.Many2one("tg.rooms", string="Ruangan", store=True)
    date = fields.Date("Tanggal Pemesanan", store=True)
    status = fields.Selection([
        ('draft', "Draft"),
        ('done', "Selesai")
    ], string="Status Pemesanan", default='draft', store=True)
    note = fields.Char("Keterangan", store=True)

    @api.model
    def create(self, vals_list):
        if vals_list.get('order_id','New') =='New':
            vals_list['order_id'] = self.env['ir.sequence'].next_by_code('tg_orders_seq') or 'New'
            result = super(TGRoomsOrder,self).create(vals_list)

            return result

    @api.constrains('date')
    def _check_past_date(self):
        today = date.today()
        for record in self:

            if record.date and record.date < today:
                raise ValidationError("Tanggal tidak boleh lebih kecil dari hari ini")

        booked_room = self.env['tg.room.orders'].search(
            ['&', '&', ('date', '=', self.date), ('room', '=', self.room.id), ('status', '=', 'done')])
        print(booked_room.name)
        if booked_room:
            raise ValidationError(f"Ruangan Yang anda pilih telah dipesan pada tanggal {self.date}")

    def book(self):
        self.status = 'done'

    def save_draft(self):
        return True
