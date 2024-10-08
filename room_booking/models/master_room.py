from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import imghdr

class MasterRoom(models.Model):
    _name = 'master.room'
    _description = 'Master ruangan berisi ruangan yang tersedia'

    name = fields.Char(string='Nama Ruangan', required=True)
    type = fields.Selection([
        ('Meeting Room Kecil', 'Meeting Room Kecil'),
        ('Meeting Room Besar', 'Meeting Room Besar'),
        ('Aula', 'Aula')
    ], string='Tipe Ruangan', required=True)
    location = fields.Selection([
        ('1A', '1A'),
        ('1B', '1B'),
        ('1C', '1C'),
        ('2A', '2A'),
        ('2B', '2B'),
        ('2C1A', '2C')
    ], string='Lokasi Ruangan', required=True)
    file = fields.Binary(string='Foto Ruangan', store=True, attachment=True, required=True)
    filename = fields.Char(string='Filename')
    image_preview = fields.Image(string='Preview Foto', compute='_compute_image_preview')
    capacity = fields.Integer(string='Kapasitas Ruangan', required=True)
    note = fields.Char(string='Keterangan')

    # Untuk memastikan tidak ada nama yang sama
    @api.constrains('name')
    def _check_name(self):
        for record in self:
            existing_room = self.env['master.room'].search([('name', '=', record.name), ('id', '!=', record.id)])
            if existing_room:
                raise ValidationError(f"Ruangan dengan nama '{record.name}' sudah ditambahkan. Silakan gunakan nama ruangan yang berbeda.")
            
    # Memastikan kapasitas ruangan minimal 1
    @api.constrains('capacity')
    def _check_capacity(self):
        for record in self:
            if record.capacity < 1:
                raise ValidationError("Kapasitas Ruangan Minimal 1.")

    # Memastikan hanya foto bertipe (JPEG, JPG, PNG) yang diupload user
    @api.constrains('file')
    def _check_file_is_image(self):
        for record in self:
            if record.file:
                file_data = base64.b64decode(record.file)
                image_type = imghdr.what(None, file_data)
                if image_type not in ['jpeg', 'jpg', 'png']:
                    raise ValidationError("Hanya file gambar (JPEG, JPG, PNG) yang diperbolehkan untuk diunggah.")

    # Menampilkan photo yang telah diinput user
    @api.depends('file')
    def _compute_image_preview(self):
        for record in self:
            record.image_preview = record.file if record.file else False