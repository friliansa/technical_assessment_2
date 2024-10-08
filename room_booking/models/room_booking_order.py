from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import imghdr

class RoomBookingOrder(models.Model):
    _name = 'room.booking.order'
    _description = 'Room Booking Order berisi pemesanan ruangan'

    name = fields.Char(string='Nomor Pemesanan', default="/", required=True, readonly=True)
    type = fields.Selection([
        ('Normal', 'Normal'),
        ('Promo', 'Promo')
    ], string='Tipe Pemesanan', required=True)
    room_id = fields.Many2one('master.room', 'Ruangan', ondelete='restrict', required=True)
    booking_name = fields.Char(string='Nama Pemesanan', required=True)
    date = fields.Date(string='Tanggal Pemesanan', required=True)
    state = fields.Selection([
        ('Draft', 'Draft'),
        ('On Going', 'On Going'),
        ('Done', 'Done')
    ], default='Draft', string='Status Pemesanan', required=True)
    note = fields.Char(string='Keterangan')

    # Untuk memastikan tidak ada nama pemesanan yang sama
    @api.constrains('booking_name')
    def _check_booking_name(self):
        for record in self:
            existing_book = self.env['room.booking.order'].search([('booking_name', '=', record.booking_name), ('id', '!=', record.id)])
            if existing_book:
                raise ValidationError(f"Pemesanan dengan nama '{record.booking_name}' sudah ditambahkan. Silakan gunakan nama pemesanan yang berbeda.")

    # Untuk memastikan tidak memesan ruangan dan tanggal pemesanan yang sama
    @api.constrains('room_id', 'date')
    def _check_avail(self):
        for record in self:
            existing_book = self.env['room.booking.order'].search([('room_id', '=', record.room_id.id), ('date', '=', record.date), ('id', '!=', record.id)])
            if existing_book:
                raise ValidationError(f"Ruangan '{record.room_id.name}' sudah dipesan pada tanggal '{str(record.date)}'. Silakan pesan ruangan/waktu yang berbeda.")

    # Method ketika pemesanan diproses
    def action_process(self):
        self.write({
            'state': 'On Going',
        })
    
    # Method ketika pemesanan diselesaikan
    def action_finish(self):
        self.write({
            'state': 'Done',
        })

    @api.model
    def create(self, vals):
        # Proses mendapatkan nomor pemesanan
        room_type = self.env['master.room'].search([('id', '=', vals['room_id'])], limit=1).type
        last_word_room_type = room_type.split()[-1]
        prefix = vals['type'] + '/' + last_word_room_type + '/'  + str(vals['date']) + '/'
        name = 'room_booking_order'
        code = 'RBO'

        # Apabila sequence belum terbentuk maka dibentuk terlebih dahulu
        ids = self.env['ir.sequence'].search(
            [('name', '=', name), ('code', '=', code)], limit=1)
        if not ids:
            ids = self.env['ir.sequence'].create({
                'name': name,
                'implementation': 'standard',
                'padding': 6,
                'code': code
            })

        # Mendapatkan nomor selanjutnya
        vals['name'] = prefix + self.env['ir.sequence'].next_by_code(code)
        return super(RoomBookingOrder, self).create(vals)

    def write(self, vals):
        # Merubah nomor pemesanan jika terdapat perubahan pada tipe pemesanan, tipe ruangan, dan tanggal pemesanan
        if 'room_id' in vals:
            room_type = self.env['master.room'].search([('id', '=', vals['room_id'])], limit=1).type
        else:
            room_type = self.room_id.type
        last_word_room_type = room_type.split()[-1]

        if 'type' in vals:
            book_type = vals['type']
        else:
            book_type = self.type

        if 'date' in vals:
            book_date = vals['date']
        else:
            book_date = self.date.strftime("%Y-%m-%d")

        prefix = book_type + '/' + last_word_room_type + '/'  + book_date + '/'
        vals['name'] = prefix + self.name.split('/')[-1]
        return super(RoomBookingOrder, self).write(vals)

    