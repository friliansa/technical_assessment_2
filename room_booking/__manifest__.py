{
    'name': 'Room Booking',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Module to manage room booking',
    'author': 'Nopri Wiratama Friliansa',
    'depends': ['base'],
    'data': [
        'views/room_booking_order_views.xml',
        'views/master_room_views.xml',
        'views/menu_views.xml',
        'security/res_groups.xml',
        'security/res_groups_button.xml'
    ],
    'installable': True,
    'application': True,
}
