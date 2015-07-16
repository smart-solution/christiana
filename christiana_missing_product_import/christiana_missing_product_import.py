# -*- coding: utf-8 -*-
##############################################################################
#
#    Smart Solution bvba
#    Copyright (C) 2010-Today Smart Solution BVBA (<http://www.smartsolution.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################## 

#. module: web
#. openerp-web
#: code:addons/web/static/src/js/view_form.js:4981
#, python-format
#msgid "The selected file exceed the maximum file size of %s."
#msgstr ""
#
# Aanpassing nodig voor max file size
#        this.max_upload_size = 25 * 1024 * 1024; // 25Mo

from osv import osv, fields
from datetime import datetime
import csv
import base64
from openerp.tools.translate import _

class missing_product_import_wizard(osv.TransientModel):
    _name = "missing.product.import.wizard"

    _columns = {
        'product_file': fields.binary('Bestand Ontbrekende Boeken', required=True),
    }

    def product_import(self, cr, uid, ids, context=None):
        """Import products from a file"""

        obj = self.browse(cr, uid, ids)[0]

        fname = '/tmp/csv_temp_' + datetime.today().strftime('%Y%m%d%H%M%S') + '.csv'
        fp = open(fname,'w+')
        fp.write(base64.decodestring(obj.product_file))

        # Find the company
        company = self.pool.get('res.users').browse(cr, uid, uid).company_id.id             

        # Find boekenbank.be
#        supplier_found = False
#        supplier_search = self.pool.get('res.partner').search(cr, uid, [('name','=','Boekenbank vzw')])
#        for supplier_rec in self.pool.get('res.partner').browse(cr, uid, supplier_search):  
#            supplier_id = supplier_rec.id
#            supplier_found = True

        nbr_lines = 0
        nbr_lines_1000 = 0

        nbr_product_categs = 0
        nbr_product_template_a = 0
        nbr_product_product_a = 0
        nbr_product_template_c = 0
        nbr_product_product_c = 0

        print 'Check supplier'
        fp.close()
        fp = open(fname,'rU')
        reader = csv.reader(fp, delimiter=";", quotechar='"')
        for row in reader:
            if reader.line_num <= 1:
                continue
            isbn = row[0]
            supplier = row[6]
            print supplier
            supplier_found = False
            if supplier != "":
                supplier_search = self.pool.get('res.partner').search(cr, uid, [('name','=',supplier)])
                for supplier_rec in self.pool.get('res.partner').browse(cr, uid, supplier_search):
                    supplier_found = True
            if not supplier_found:
                raise osv.except_osv(('Fout !'),_(('Boek met ISBN barcode %s heeft niet gekende leverancier') % (isbn, )))
                return

        print 'Check distributor'
        fp.close()
        fp = open(fname,'rU')
        reader = csv.reader(fp, delimiter=";", quotechar='"')
        for row in reader:
            if reader.line_num <= 1:
                continue
            isbn = row[0]
            distributor = row[5]
            print distributor
            distributor_found = False
            if distributor != "":
                distributor_search = self.pool.get('res.distributor').search(cr, uid, [('name','=',distributor)])
                for distributor_rec in self.pool.get('res.distributor').browse(cr, uid, distributor_search):
                    distributor_found = True
            if not distributor_found:
                raise osv.except_osv(('Fout !'),_(('Boek met ISBN barcode %s heeft niet gekende distributeur') % (isbn, )))
                return

        print 'Check AWSO'
        fp.close()
        fp = open(fname,'rU')
        reader = csv.reader(fp, delimiter=";", quotechar='"')
        for row in reader:
            if reader.line_num <= 1:
                continue
            isbn = row[0]
            awso_code = row[3]
            if awso_code not in ('A', 'W', 'S', 'O'):
                raise osv.except_osv(('Fout !'),_(('Boek met ISBN barcode %s heeft niet gekende AWSO code') % (isbn, )))
                return

        print 'Import products started'
        fp.close()
        fp = open(fname,'rU')
        reader = csv.reader(fp, delimiter=";", quotechar='"')
        for row in reader:
            nbr_lines = nbr_lines + 1
            nbr_lines_1000 = nbr_lines_1000 + 1
            if nbr_lines_1000 == 1000:
                print "Number of lines processed: ", nbr_lines
                nbr_lines_1000 = 0

            if reader.line_num <= 1:
                continue

            if row[0] == '':
                continue

            isbn_nummer = row[0]
            print isbn_nummer
            titel = row[1]
            auteur = row[2].upper()
            awso_code = row[3]
            if awso_code not in ('A', 'W', 'S', 'O'):
                raise osv.except_osv(('Fout !'),_(('Boek met ISBN barcode %s heeft niet gekende AWSO code') % (isbn_nummer, )))
                return
            if row[4] == '':
                verkoopprijs = 0
            else:
                verkoopprijs = row[4].replace(",",".")
            distributor = row[5]
            supplier = row[6]

            categ_id = 2
            supplier_btw_code_id = 20
            cust_btw_code_id = 6

# AUTEUR
            auteur_id = None
            auteur_found = False
            if auteur != "":
                auteur_search = self.pool.get('res.author').search(cr, uid, [('name','=',auteur)])
                for auteur_rec in self.pool.get('res.author').browse(cr, uid, auteur_search):
                    auteur_id = auteur_rec.id
                    auteur_found = True
            if not auteur_found:
                vals = {
                    'name': auteur,
                }
                auteur_id = self.pool.get('res.author').create(cr, uid, vals) 

# SUPPLIER
            supplier_id = None
            supplier_found = False
            if supplier != "":
                supplier_search = self.pool.get('res.partner').search(cr, uid, [('name','=',supplier)])
                for supplier_rec in self.pool.get('res.partner').browse(cr, uid, supplier_search):
                    supplier_id = supplier_rec.id
                    supplier_found = True

# PRODUCT TEMPLATE   
            product_template_id = None
            if isbn_nummer != "":
                product_template_found = False
                product_template_search = self.pool.get('product.template').search(cr, uid, [('unique_name','=',isbn_nummer)])
                for product_template_rec in self.pool.get('product.template').browse(cr, uid, product_template_search):
                    product_template_id = product_template_rec.id
                    product_template_found = True
                    continue
                product_product_found = False
                product_product_search = self.pool.get('product.product').search(cr, uid, [('default_code','=',isbn_nummer)])
                for product_product_rec in self.pool.get('product.product').browse(cr, uid, product_product_search):
                    product_product_id = product_product_rec.id
                    product_product_found = True
                    continue
                if not product_template_found:
                    vals = {
                        'uos_id': 1,
                        'mes_type': 'fixed',
                        'uom_id': 1,
                        'cost_method': 'standard',
                        'uos_coeff': 1.00,
                        'volume': 0,
                        'sale_ok': True,
                        'company_id': 1,
                        'produce_delay': 0.00,
                        'uom_po_id': 1,
                        'rental': False,
                        'type': 'product',
                        'sale_delay': 0.00,
                        'supply_method': 'buy',
                        'procure_method': 'make_to_order',
                        'purchase_ok': True,
                        'unique_name': isbn_nummer,
                        'list_price': verkoopprijs,
                        'description': titel,
                        'standard_price': verkoopprijs,
                        'categ_id': categ_id,
                        'name': titel[:128],
                    }
                    product_template_id = self.pool.get('product.template').create(cr, uid, vals)   
                    nbr_product_template_a = nbr_product_template_a + 1  

# PRODUCT PRODUCT   
            product_product_id = None
            if isbn_nummer != "":
                product_product_found = False
                product_product_search = self.pool.get('product.product').search(cr, uid, [('default_code','=',isbn_nummer)])
                for product_product_rec in self.pool.get('product.product').browse(cr, uid, product_product_search):
                    product_product_id = product_product_rec.id
                    product_product_found = True
                    continue
                if not product_product_found:
                    vals = {
                        'active': True,
                        'product_tmpl_id': product_template_id,
                        'track_outgoing': False,
                        'track_incoming': False,
                        'valuation': 'manual_periodic',
                        'track_production': False,
                        'sale_line_warn': 'no-message',
                        'purchase_line_warn': 'no-message',
                        'default_code': isbn_nummer,
                        'name_template': titel[:128],
                        'awso_code': awso_code,
                        'distributeur': distributor,
                        'author_id': auteur_id,
                        'author_temp': auteur,
                        'btw_code_file': 1,
                    }
                    product_product_id = self.pool.get('product.product').create(cr, uid, vals)   
                    nbr_product_product_a = nbr_product_product_a + 1  

                    if supplier_found:
                        vals = {
                            'name': supplier_id,
                            'sequence': 1,
                            'company_id': 1,
                            'qty': 1.00,
                            'delay': 1,
                            'min_qty': 1.00,
                            'product_id': product_template_id,
                        }
                        product_supplier_id = self.pool.get('product.supplierinfo').create(cr, uid, vals)

                    sql_stat = 'insert into product_taxes_rel (prod_id, tax_id) values(%d, 6)' % (product_template_id, )
                    cr.execute(sql_stat)
                    sql_stat = 'insert into product_supplier_taxes_rel (prod_id, tax_id) values(%d, 20)' % (product_template_id, )
                    cr.execute(sql_stat)

            cr.commit()
              
        print "End of Import Job - Number of lines processed: ", nbr_lines
        print "Nbr of product templates added: ", nbr_product_template_a
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
