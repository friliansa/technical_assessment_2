# Technical Assessment 2
Repository ini merupakan jawaban dari Technical Assessment 2

## Requirements used
1. Python 3.10.11
2. pip 23.0.1
3. Postgresql 15
4. Odoo version 14

## Installation
1. Move to the directory where you would like to perform the installation
2. run command: "git clone https://www.github.com/odoo/odoo --depth 1 --branch 14.0 --single-branch odoo14" (clone base odoo 14)
3. run command: "git clone https://github.com/friliansa/technical_assessment_2 custom_addons" (clone this repo for custom_addons directory name)
4. run command: "python -m venv odoo14_venv" (create virtual env)
5. run command: On Windows: "odoo14_venv/Scripts/activate" | On Linux/macOS: "source odoo14_venv/bin/activate" (activate virtual env)
6. run command: "python -m pip install --upgrade pip" (install latest pip)
7. run command: "pip install -r odoo14/requirements.txt" (install requirement odoo 14 from odoo repo, Please check the manually installed requirements against the requirements listed in odoo14\requirements.txt)
8. run command: "python odoo14/odoo-bin -c custom_addons/odoo14.conf -u all" (init running odoo)
9. Open "http://127.0.0.1:8070/" in browser and Login with default credential, email: admin & password: admin
10. open Apps menu in odoo and search 'room_booking' and click "install"
   ![Install Module](assets/install_module_room_booking.png)
11. The module is installed successfully
12. Setup access user
   ![Setup access Module](assets/setup_access.png)
13. Now, You can add record

## Features
1. Admin can add access for users to add/edit/delete in the Room Master and Room Booking modules.
2. Admin can add access for users to the process/finish button in the Room Booking module.
3. Room names in the Room Master cannot be duplicated.
   ![Room names](assets/validation_add_master_ruangan.png)
4. Booking names in the Room Booking cannot be duplicated.
   ![Booking names](assets/validation_nama_pemesanan.png)
5. A room that is booked cannot be booked by another customer.
   ![Room booked](assets/validation_pemesanan_ruangan.png)

## Result
1. Master Ruangan
   ![List Ruangan](assets/list_ruangan.png)
   ![Grid Ruangan](assets/grid_ruangan.png)
   ![Form Ruangan](assets/form_ruangan.png)

2. Pemesanan
   ![List Pemesanan](assets/list_pemesanan.png)
   ![Form Pemesanan](assets/form_pemesanan.png)

