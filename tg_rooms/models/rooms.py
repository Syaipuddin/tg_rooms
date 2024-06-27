from odoo import models, fields, api, exceptions, _


class TGRooms(models.Model):
    _name = "tg.rooms"

    name = fields.Char("Nama Ruangan", store=True)
    location = fields.Selection([
        ('1a', '1A'),
        ('1b', '1B'),
        ('1c', '1C'),
        ('2a', '2A'),
        ('2b', '2B'),
        ('2c', '2C'),
    ], string='Lokasi Ruangan', default='1a', store=True)
    photo = fields.Binary(string='Foto Ruangan', store=True)
    type = fields.Selection([
        ('big', 'Besar'),
        ('small', 'Kecil')
    ], string="Tipe Ruangan", default='small', store=True)
    capacity = fields.Char("Kapasitas Ruangan", store=True)
    note = fields.Char("Keterangan", store=True)
    detail = fields.One2many("tg.room.orders", "room", domain=[('status', '=', 'done')], store=True)