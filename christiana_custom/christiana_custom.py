# -*- encoding: utf-8 -*-

from mx import DateTime
import time

from openerp.osv import fields, osv
from openerp.tools.translate import _

ARTIKEL_STATUS_SELECTION = [
    ('1', 'In Productie'),
    ('2', 'Verschenen'),
    ('3', 'In Bijdruk/Herdruk'),
    ('4', 'Uitverkocht'),
    ('5', 'Ongekend'),
    ('6', 'Te Bestellen bij Uitgever'),
    ('7', 'In Prijs Opgeheven'),
    ('8', 'Herdruk in Overweging'),
    ('9', 'Printing on Demand')
]

WARNING_MESSAGE = [
                   ('no-message','No Message'),
                   ('warning','Warning'),
                   ('block','Blocking Message')
                   ]

WARNING_HELP = _('Selecting the "Warning" option will notify user with the message, Selecting "Blocking Message" will throw an exception with the message and block the flow. The Message has to be written in the next field.')

class product_product(osv.osv):
    _inherit = "product.product"
    
    def _reservation_count(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            sql_stat = '''select sum(qty_to_deliver - qty_retour) as reservatie from stock_reservation_line
 inner join stock_reservation on stock_reservation.id = stock_reservation_line.reservation_id
 where stock_reservation_line.product_id = %d
 and stock_reservation.state = 'draft' group by stock_reservation_line.product_id ''' % (id, )
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res:
                res[id] = sql_res['reservatie']
            else:
                res[id] = 0
                
        return res

    _columns = {
        'print_number': fields.integer('Druknummer'),
        'release_date': fields.date('Verschijningsdatum'),
        'author_id': fields.many2one('res.author', 'Auteur', select=True),
        'co_author_id': fields.many2one('res.co.author', 'Co-Auteur', select=True),
        'awso_code': fields.selection((('A','Algemeen'),('W','Wetenschappelijk'),('S','Studie'),('O','Overige')),'AWSO Code'),
        'artikel_status': fields.selection((('1','In Productie'),('2','Verschenen'),('3','In Bijdruk/Herdruk'),('4','Uitverkocht'),('5','Ongekend'),('6','Te Bestellen bij Uitgever'),('7','In Prijs Opgeheven'),('8','Herdruk in Overweging'),('9','Printing on Demand')),'Artikel Status'),
        'uitgave_soort': fields.selection((('B','Boek'),('K','Kaart'),('D','Diverse'),('C','CD-Rom'),('V','Video'),('A','Audiocassette'),('Z','DVD'),('P','CDI'),('S','Software'),('I','Internetpublicatie'),('E','CD (Audio)'),('X','Display/Promotiemateriaal'),('DG','E-Boek')),'Uitgave Soort'),
        'uitvoering': fields.selection((('GB','Gebonden'),('PB','Paperback'),('PK','Pocket'),('LB','Losbladig'),('GL','Garenloos'),('SP','Spiraalband'),('AA','Andere'),('EDB','EDB'),('BUB','BUB'),('PZ','PZ'),('AK','AK'),('EZD','EZD'),('HT','HT'),('EAD','EAD'),('PA','PA'),('PD','PD'),('EAB','EAB'),('EZB','EZB')),'Uitvoering'),
        'voorraadcode': fields.selection((('V','Leverbaar uit Voorraad'),('S','Speciale Bestelling'),('I','Informatieve Titel'),('P','Printing on Demand'),('N','Niet Leverbaar'),('O','Nog niet Leverbaar'),('T','Tijdelijk niet Leverbaar')),'Voorraadcode'),
        'netwerkcode': fields.selection((('J','Bestellen via Boekenbank'),('N','Niet bestellen via Boekenbank')),'Netwerkcode'),
        'nbr_paginas': fields.integer('Aantal Paginas'),
        'illustraties': fields.boolean('Illustraties'),
        'co_editie': fields.char('Co-Editie', size=13),
        'substituut_isbn': fields.char('Substituut ISBN', size=13),
        'set_isbn': fields.char('Set ISBN', size=13),
        'sectietitel': fields.selection((('WB','Werkboek'),('HB','Handboek'),('HL','Handleiding'),('DO','Docenthandleiding')),'Sectietitel'),
        'jaar_release1': fields.integer('Jaar 1ste Verschijning'),
        'hoofdtitel': fields.text('Hoofdtitel'),
        'ondertitel': fields.text('Ondertitel'),
        'deeltitel': fields.text('Deeltitel'),
        'oorsprtitel': fields.text('Oorspronkelijke Titel'),
        'imprint': fields.text('Imprint'),
        'reeksnaam': fields.text('Reeksnaam'),
        'reeksnummer': fields.char('Nr. binnen Reeks', size=10),
        'taalcode': fields.char('Taalcode', size=32),
        'oorsprtaal': fields.char('Oorspronkelijke Taal', size=32),
        'bijlage': fields.selection((('CD','CD-Rom'),('DVD','DVD'),('DI','Diskette'),('P','Printing on Demand')),'Bijlage'),
        'uitgevernummer': fields.char('Uitgevernummer', size=32),
        'distributeur': fields.char('Distributeur', size=32),
        'fondscode': fields.char('Fondscode', size=32),
        'formaat': fields.char('Formaat', size=10),
        'depotnummer': fields.char('Wettelijk Depotnummer', size=32),
        'avi_niveau': fields.char('Avi-Niveau', size=10),
        'btw21': fields.float('Percentage 21% BTW'),
        'author_temp': fields.char('Auteur (Temp)', size=128),
        'co_author_temp': fields.char('Co-Auteur (Temp)', size=128),
        'combined_vat': fields.boolean('Samengestelde BTW'),
        'btw_code_file': fields.integer('BTW Code Bestand'),
        'reservation_count': fields.function(_reservation_count, string="Op reservaties", type='integer'),
     }

product_product()

class product_template(osv.osv):
    _inherit = "product.template"
    
    _columns = {
        'unique_name': fields.char('Unique Name', size=128, select=True, searchable=True, translate=True),
    }

product_template()

class res_author(osv.osv):
    _name = 'res.author'
    _description = 'Author'

    _columns = { 
        'name': fields.char('Name', size=128, required=True, select=True, searchable=True),
        'product_ids': fields.one2many('product.product', 'author_id', 'Products'),
    }

res_author()

class res_co_author(osv.osv):
    _name = 'res.co.author'
    _description = 'Co-Author'

    _columns = { 
        'name': fields.char('Name', size=128, required=True, select=True, searchable=True),
        'product_ids': fields.one2many('product.product', 'co_author_id', 'Products'),
    }

res_co_author()

class res_distributor(osv.osv):
    _name = 'res.distributor'
    _description = 'Distributor'

    _columns = { 
        'name': fields.char('Name', size=32, required=True, select=True, searchable=True),
        'supplier_id': fields.many2one('res.partner', 'Supplier', select=True),
    }

res_distributor()

class sale_order(osv.osv):
    _inherit = 'sale.order'

    _columns = { 
        'zichtzending': fields.boolean('Zichtzending'),
        'order_line_product': fields.one2many('sale.order.line', 'order_id', 'Order Lines', readonly=True, domain=[('product_id','=',False)]),
        'order_line_titel': fields.one2many('sale.order.line', 'order_id', 'Order Lines', readonly=True, domain=[('boolean_name_excel','=',False)]),
        'order_line_qoh': fields.one2many('sale.order.line', 'order_id', 'Order Lines', readonly=True, domain=[('qoh_boolean','!=',False)]),
        'order_line_nosupp': fields.one2many('sale.order.line', 'order_id', 'Order Lines', readonly=True, domain=[('product_supplierinfo_id','=',False)]),
        'order_line_qoh_code': fields.one2many('sale.order.line', 'order_id', 'Order Lines', readonly=True, domain=['&',('voorraadcode','!=','V'),('voorraadcode','!=','O')]),
	'invoice_text': fields.char('Factuurreferentie klant'),
    }

    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        res = super(sale_order, self).onchange_partner_id( cr, uid, ids, partner_id, context=context)
 
        if partner_id:
            sql_stat = '''select invoice_text from res_partner where id = %d''' % (partner_id, )
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res:
                res['value']['invoice_text'] = sql_res['invoice_text']

        return res

sale_order()

class res_partner_budget(osv.osv):
    _name = 'res.partner.budget'
    _description = 'Partner budget'

    def _to_deliver(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids):
            if line.partner_id.type == 'delivery':
                sql_stat = '''select sum(product_qty) as totaal
 from stock_move
 where 
  partner_id = %d
  and
  state in ('assigned','confirmed')
  and
  not(sale_line_id is null)
''' % (line.partner_id)
            else:
                sql_stat = '''select sum(product_qty) as totaal
 from stock_move
 where 
 (
  partner_id in (select id from res_partner where parent_id = %d)
  or
  partner_id = %d
 )
  and
  state in ('assigned','confirmed')
  and
  not(sale_line_id is null)
''' % (line.partner_id, line.partner_id)
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res:
                res[line.id] = sql_res['totaal']
            else:
                res[line.id] = 0
                
        return res

    def _gefactureerd(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids):
            sql_stat = '''select sum(case when type = 'out_invoice' 
 then amount_total else (0 - amount_total) end) as totaal
 from account_invoice
 inner join account_period on account_invoice.period_id = account_period.id
 inner join account_fiscalyear on account_period.fiscalyear_id = account_fiscalyear.id
 where 
  (
    ('%s' = 'delivery' and del_addr_id = %d)
    or
    (not('%s' = 'delivery') and partner_id = %d)
  )
 and account_fiscalyear.code = '%s'
 and not(account_invoice.state = 'cancel')
''' % (line.partner_id.type, line.partner_id, line.partner_id.type, line.partner_id, line.year )
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res:
                res[line.id] = sql_res['totaal']
            else:
                res[line.id] = 0
                
        return res
        
    _columns = { 
        'year': fields.char('Year', size=4, required=True),
        'budget': fields.float('Budget', digits=(12,2)),
        'partner_id': fields.many2one('res.partner', 'Partner', required=True, select=True),
        'invoiced': fields.function(_gefactureerd, string="Gefactureerd", type='float', digits=(12,2)),
        'to_deliver': fields.function(_to_deliver, string="Aantal nog te leveren", type='float', digits=(12,2)),
    }

res_partner_budget()

class res_partner(osv.osv):
    _inherit = "res.partner"
    
    _columns = {
        'sale_qty_warn' : fields.selection(WARNING_MESSAGE, 'Sales Order', help=WARNING_HELP, required=True),
        'sale_qty_warn_msg' : fields.text('Message for Sales Order exceeding the Max Qty per Book'),
        'min_order_amount': fields.float('Min Order Amount', digits=(12,2)),
        'max_qty_per_book': fields.integer('Max Book Qty'),
        'partner_budget_ids': fields.one2many('res.partner.budget', 'partner_id', 'Budgets'),
        'for_attn_of': fields.char('Ter attentie van'),
        'zichtzending': fields.boolean('Zichtzending'),
        'total_invoice': fields.boolean('Enkel factuurtotalen'),
        'invoice_text': fields.char('Tekst factuur'),
    }
    
    _defaults = {
         'sale_qty_warn' : 'no-message',
    }

res_partner()

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'

    def _function_qoh(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids):
            if line.product_id:
                res[line.id] = line.product_id.qty_available - line.product_id.reservation_count
            else:
                res[line.id] = 0
        return res
   
    def _function_qoh_boolean(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids):
            res[line.id] = False
            if line.product_id.qty_available and (line.product_id.qty_available - line.product_id.reservation_count) > 0.00:
                res[line.id] = True
        return res
   
    def _function_date_ordered(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids):
            res[line.id] = line.order_id.date_order
        return res

    def _product_supplierinfo(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for po in self.browse(cr, uid, ids):
            res[po.id] = 0
            if po.id and po.order_id.id and po.product_id.id:
                product_id = po.product_id.product_tmpl_id.id
                sql_stat = '''select id from product_supplierinfo where product_id = %d''' % (product_id, )
                cr.execute(sql_stat)
                sql_res = cr.dictfetchone()
                if sql_res:
                    res[po.id] = sql_res['id']
        return res
 
    _columns = {
        'author_id': fields.many2one('res.author', 'Auteur', select=True),
        'isbn_number': fields.char('ISBN', size=13),
        'voorraadcode': fields.selection((('V','Leverbaar uit Voorraad'),('S','Speciale Bestelling'),('I','Informatieve Titel'),('P','Printing on Demand'),('N','Niet Leverbaar'),('O','Nog niet Leverbaar'),('T','Tijdelijk niet Leverbaar')),'Voorraadcode'),
        'price_excel': fields.float('Prijs Excel'),
        'name_excel': fields.char('Titel Excel'),
        'boolean_name_excel': fields.boolean('Titel Excel'),
        'qoh': fields.function(_function_qoh, string='Voorraad', type='float'),
        'qoh_boolean': fields.function(_function_qoh_boolean, string='Voorraad', type='boolean', store=True),
        'date_order': fields.function(_function_date_ordered, string='Besteldatum', type='date'),
        'zichtzending': fields.related('order_id', 'zichtzending', type='boolean', string='Zichtzending'),
        'product_supplierinfo_id': fields.function(_product_supplierinfo, string='Supplierinfo', type='many2one', relation='product.supplierinfo', select=True, store=True),
        'distributeur': fields.related('product_id', 'distributeur', type='char', string='Distributeur'),
        }

    def isbn_change(self, cr, uid, ids, isbn_number, context=None):
        res = {}
        res['value'] = {}
        sql_stat = "select id as product_id from product_product where default_code = '%s'" % (isbn_number, )
#         print 'SQL_STAT:',sql_stat
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            res['value']['product_id'] = sql_res['product_id']

        return res

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0, uom=False, qty_uos=0, uos=False, name='', partner_id=False, lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, zichtzending=False, context=None):

        res = super(sale_order_line, self).product_id_change( cr, uid, ids, pricelist, product, qty, uom, qty_uos, uos, name, partner_id, lang, update_tax, date_order, packaging, fiscal_position, flag, context=context)
 
        if not product:
            return False

        discount = 0.00

#         print 'ZICHTZENDING:',zichtzending
# partner and product
        sql_stat = '''select discount_pct 
from res_partner_discount d, product_product p
where d.partner_id = %d 
  and p.id = %d 
  and ((d.awso_code = p.awso_code and %s = False)
   or  (d.awso_code = 'Z' and %s = True))''' % (partner_id, product, zichtzending, zichtzending, )
#         print 'SQL_STAT:',sql_stat
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            discount = sql_res['discount_pct']

        res['value']['discount'] = discount

#         print 'RES:',res
        if 'warning' in res:
            res['warning'] = {}

        if product:
            product_obj = self.pool.get('product.product')
            product_info = product_obj.browse(cr, uid, product)
            if product_info.author_id:
                res['value']['author_id'] = product_info.author_id.id
            if product_info.default_code:
                res['value']['isbn_number'] = product_info.default_code
            if product_info.voorraadcode:
                res['value']['voorraadcode'] = product_info.voorraadcode

        warning = False
        title = ''
        message = ''
        
        if partner_id:
            partner_obj = self.pool.get('res.partner')
            partner_info = partner_obj.browse(cr, uid, partner_id)
            if partner_info.max_qty_per_book and partner_info.max_qty_per_book < qty:
                if partner_info.sale_qty_warn != 'no-message':
                    if partner_info.sale_qty_warn == 'block':
                        raise osv.except_osv(_('Alert for %s !') % (partner_info.name), partner_info.sale_qty_warn_msg)
                title = _('Warning for %s') % partner_info.name
                if partner_info.sale_qty_warn_msg:
                    message = partner_info.sale_qty_warn_msg
                else:
                    message = "Maximum aantal boeken overschreden"
#                 print 'MESSAGE:',message
                if not warning:
                    warning = True
                    res['warning'] = {}
                res['warning']['title'] = title
                res['warning']['message'] = message

        return res

sale_order_line()

class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    _columns = { 
        'combined_vat': fields.char('Gecombineerde BTW', size=256),
        'combined_vat_flag': fields.char('BTW-Comb.'),
        'del_addr_id': fields.many2one('res.partner', 'Leveringsadres'),
        }

    _defaults={
       'combined_vat_flag': False,
    }

    def create(self, cr, uid, vals, context=None):
        res = super(account_invoice, self).create(cr, uid, vals, context=context)
        inv = self.browse(cr, uid, res)

        warning = False
        message = 'Product(en) met gecombineerd BTW-tarief:'

        for invl in inv.invoice_line:
            if invl.product_id:
                product_obj = self.pool.get('product.product')
                product_info = product_obj.browse(cr, uid, invl.product_id.id)
#                 print product_info.default_code
#                 print product_info.combined_vat
                if product_info.combined_vat:
                    message = message + ' ' + invl.product_id.default_code
#                     print message
                    if not warning:
                        warning = True
#		        res['warning'] = {}

        if warning:
            sql_stat = "update account_invoice set combined_vat_flag = %s, combined_vat = '%s' where id = %d" % (warning, message, inv.id, )
#             print 'SQL:',sql_stat
            cr.execute(sql_stat)

        return res

    def write(self, cr, uid, ids, vals, context=None):
#	if 'active_id' in context:
#            inv = self.browse(cr, uid, context['active_id'])

#            warning = False
#            message = 'Product(en) met gecombineerd BTW-tarief:'

#   	    for invl in inv.invoice_line:
#	        if invl.product_id:
#                    product_obj = self.pool.get('product.product')
#                    product_info = product_obj.browse(cr, uid, invl.product_id.id)
#		    print product_info.default_code
#		    print product_info.combined_vat
#                    if product_info.combined_vat:
#                        message = message + ' ' + invl.product_id.default_code
#		        print message
#		        if not warning:
#		            warning = True

#	    if warning:
#                vals['combined_vat_flag'] = True
#	        vals['combined_vat'] = message

        return super(account_invoice, self).write(cr, uid, ids, vals, context=context)

account_invoice()

class account_invoice_line(osv.osv):
    _inherit = 'account.invoice.line'

    _columns = {
        'combined_vat': fields.boolean('Gecombineerde BTW'),
        'vat06': fields.float('Bedrag BTW 6%'),
        'vat21': fields.float('Bedrag BTW 21%'),
        }

    def product_id_change(self, cr, uid, ids, product, uom_id, qty=0, name='', type='out_invoice', partner_id=False, fposition_id=False, price_unit=False, currency_id=False, context=None, company_id=None):
        res_final = super(account_invoice_line, self).product_id_change(cr, uid, ids, product, uom_id, qty, name, type, partner_id, fposition_id, price_unit, currency_id, context, company_id)
        if context is None:
            context = {}
        if not partner_id:
            raise osv.except_osv(_('No Partner Defined!'),_("You must first select a partner!") )
        if not product:
            return res_final
        discount = 0.00
        sql_stat = '''select discount_pct 
from res_partner_discount d, product_product p
where d.partner_id = %d 
  and p.id = %d 
  and d.awso_code = p.awso_code''' % (partner_id, product)
#         print 'SQL_STAT:',sql_stat
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            discount = sql_res['discount_pct']
        res_final['value']['discount'] = discount
        return res_final
    
account_invoice_line()

class purchase_order(osv.osv):
    _inherit = 'purchase.order'

    def _function_distributeur(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for po in self.browse(cr, uid, ids):
#             print 'PO-ID:',po.id
            if po.id:
                distributeur = ''
                sql_stat = '''select distinct product_product.distributeur from purchase_order_line, product_product where product_id = product_product.id and order_id =  %d''' % (po.id, )
                cr.execute(sql_stat)
            for sql_res in cr.dictfetchall():
#                 print 'DISTR:',sql_res['distributeur']
                if distributeur == '':
                    distributeur = sql_res['distributeur']
                else:
                    distributeur = 'Meerdere'
            res[po.id] = distributeur
        return res

    def _function_titel(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for po in self.browse(cr, uid, ids):
            if po.id:
                titel = ''
                sql_stat = '''select distinct name from purchase_order_line where order_id =  %d''' % (po.id, )
                cr.execute(sql_stat)
                for sql_res in cr.dictfetchall():
                    if titel == '':
                        titel = sql_res['name']
                    else:
                        titel = 'Meerdere'
                res[po.id] = titel
        return res

    _columns = {
        'distributeur': fields.function(_function_distributeur, string='Distributeur', type='char', store=True, select=True),
        'titel': fields.function(_function_titel, string='Titel', type='char'),
        'zichtzending': fields.boolean('Zichtzending'),
        }

purchase_order()

class purchase_order_line(osv.osv):
    _inherit = 'purchase.order.line'

    def _function_distributeur(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for po in self.browse(cr, uid, ids):
#             print 'PO-ID:',po.id
            if po.id:
                distributeur = ''
                sql_stat = '''select distinct distributeur from product_product where id = %d''' % (po.product_id, )
                cr.execute(sql_stat)
                for sql_res in cr.dictfetchall():
                    distributeur = sql_res['distributeur']
                res[po.id] = distributeur
        return res

    _columns = {
        'isbn_number': fields.char('ISBN', size=13),
        'author_id': fields.many2one('res.author', 'Auteur', select=True),
        'distributeur': fields.function(_function_distributeur, string='Distributeur', type='char', store=True, select=True),
        'order_state': fields.related('order_id', 'state', type='char', relation='purchase.order', string='Order State', readonly=True),
    }

    def isbn_change(self, cr, uid, ids, isbn_number, context=None):
        res = {}
        res['value'] = {}
        sql_stat = "select id as product_id from product_product where default_code = '%s'" % (isbn_number, )
#         print 'SQL_STAT:',sql_stat
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            res['value']['product_id'] = sql_res['product_id']

        return res

purchase_order_line()

class stock_picking(osv.osv):
    _inherit = 'stock.picking'

    def _function_invoice_amount(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for po in self.browse(cr, uid, ids):
            if po.id:
                amount = 0.00
                sql_stat = '''select round(cast((product_qty * (so_price * (100 - so_discount) / 100)) as numeric),2) as amount
from stock_move, stock_reservation_line
where stock_move.id = stock_reservation_line.move_id
  and stock_move.picking_id =  %d''' % (po.id, )
                cr.execute(sql_stat)
                for sql_res in cr.dictfetchall():
                    amount = amount + sql_res['amount']
                res[po.id] = amount
        return res

    def _function_zichtzending(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for po in self.browse(cr, uid, ids):
            if po.id:
                zichtzending = False
                sql_stat = '''select sale_order.zichtzending
from stock_move, stock_reservation_line, sale_order
where stock_move.id = stock_reservation_line.move_id
  and stock_reservation_line.so_id = sale_order.id
  and stock_move.picking_id =  %d''' % (po.id, )
                cr.execute(sql_stat)
                for sql_res in cr.dictfetchall():
                    zichtzending = sql_res['zichtzending']
                res[po.id] = zichtzending
        return res

    def _function_reservation(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for po in self.browse(cr, uid, ids):
            res[po.id] = 0
            if po.id:
                sql_stat = '''select min(stock_reservation.id) as res_id from stock_reservation, stock_reservation_line, stock_move 
where stock_move.picking_id = %d
  and stock_reservation_line.move_id = stock_move.id
  and stock_reservation.id = stock_reservation_line.reservation_id''' % (po.id, )
                cr.execute(sql_stat)
                sql_res = cr.dictfetchone()
                if sql_res:
                    res[po.id] = sql_res['res_id']
        return res

    _columns = {
        'invoice_amount': fields.function(_function_invoice_amount, string='Bedrag', type='float'),
        'zichtzending': fields.function(_function_zichtzending, string='Zichtzending', type='boolean', store=True),
        'zichtz_inv_allowed': fields.boolean('Te factureren zichtzending'),
        'reservation_id': fields.function(_function_reservation, string='Reservatie', type='many2one', relation='stock.reservation', select=True, store=True),
    }

    def _get_combined_vat_invoice(self, cr, uid, move_line):
        '''Return the combined vat for the move line'''
        combined_vat = False
        if move_line.id:
            sql_stat = "select combined_vat from stock_reservation_line where move_id = %d" % (move_line.id, )
            cr.execute(sql_stat)
            for sql_res in cr.dictfetchall():
	        combined_vat = sql_res['combined_vat']
        return combined_vat

    def _get_vat06_invoice(self, cr, uid, move_line):
        '''Return the vat for the move line'''
        vat06 = 0.0
        if move_line.id:
            sql_stat = "select vat06 from stock_reservation_line where move_id = %d" % (move_line.id, )
            cr.execute(sql_stat)
            for sql_res in cr.dictfetchall():
                vat06 = sql_res['vat06']
        return vat06

    def _get_vat21_invoice(self, cr, uid, move_line):
        '''Return the vat for the move line'''
        vat21 = 0.0
        if move_line.id:
            sql_stat = "select vat21 from stock_reservation_line where move_id = %d" % (move_line.id, )
            cr.execute(sql_stat)
            for sql_res in cr.dictfetchall():
                vat21 = sql_res['vat21']
        return vat21

    def write(self, cr, uid, ids, vals, context=None):
        if 'zichtz_inv_allowed' in vals and vals['zichtz_inv_allowed']:
            vals['invoice_state'] = '2binvoiced'
        if 'zichtz_inv_allowed' in vals and not vals['zichtz_inv_allowed']:
            vals['invoice_state'] = 'none'

        return super(stock_picking, self).write(cr, uid, ids, vals, context=context)

    def _prepare_invoice_line(self, cr, uid, group, picking, move_line, invoice_id,
        invoice_vals, context=None):
        """ Builds the dict containing the values for the invoice line
            @param group: True or False
            @param picking: picking object
            @param: move_line: move_line object
            @param: invoice_id: ID of the related invoice
            @param: invoice_vals: dict used to created the invoice
            @return: dict that will be used to create the invoice line
        """
        if group:
            name = (picking.name or '') + '-' + move_line.name
        else:
            name = move_line.name
        origin = move_line.picking_id.name or ''
        if move_line.picking_id.origin:
            origin += ':' + move_line.picking_id.origin

        if invoice_vals['type'] in ('out_invoice', 'out_refund'):
            account_id = move_line.product_id.property_account_income.id
            if not account_id:
                account_id = move_line.product_id.categ_id.\
                        property_account_income_categ.id
        else:
            account_id = move_line.product_id.property_account_expense.id
            if not account_id:
                account_id = move_line.product_id.categ_id.\
                        property_account_expense_categ.id
        if invoice_vals['fiscal_position']:
            fp_obj = self.pool.get('account.fiscal.position')
            fiscal_position = fp_obj.browse(cr, uid, invoice_vals['fiscal_position'], context=context)
            account_id = fp_obj.map_account(cr, uid, fiscal_position, account_id)
        # set UoS if it's a sale and the picking doesn't have one
        uos_id = move_line.product_uos and move_line.product_uos.id or False
        if not uos_id and invoice_vals['type'] in ('out_invoice', 'out_refund'):
            uos_id = move_line.product_uom.id

        return {
            'name': name,
            'origin': origin,
            'invoice_id': invoice_id,
            'uos_id': uos_id,
            'product_id': move_line.product_id.id,
            'account_id': account_id,
            'price_unit': self._get_price_unit_invoice(cr, uid, move_line, invoice_vals['type']),
            'combined_vat': self._get_combined_vat_invoice(cr, uid, move_line),
            'vat06': self._get_vat06_invoice(cr, uid, move_line),
            'vat21': self._get_vat21_invoice(cr, uid, move_line),
            'discount': self._get_discount_invoice(cr, uid, move_line),
            'quantity': move_line.product_uos_qty or move_line.product_qty,
            'invoice_line_tax_id': [(6, 0, self._get_taxes_invoice(cr, uid, move_line, invoice_vals['type']))],
            'account_analytic_id': self._get_account_analytic_invoice(cr, uid, picking, move_line),
        }

stock_picking()

class stock_picking_out(osv.osv):
    _inherit = 'stock.picking.out'

    def _function_invoice_amount(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for po in self.browse(cr, uid, ids):
            if po.id:
                amount = 0.00
                sql_stat = '''select (product_qty * (so_price - (so_price * so_discount / 100))) as amount
from stock_move, stock_reservation_line
where stock_move.id = stock_reservation_line.move_id
  and stock_move.picking_id =  %d''' % (po.id, )
                cr.execute(sql_stat)
	        for sql_res in cr.dictfetchall():
		    amount = amount + sql_res['amount']
                res[po.id] = amount
        return res

    def _function_zichtzending(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for po in self.browse(cr, uid, ids):
            if po.id:
                zichtzending = False
                sql_stat = '''select zichtzending
from stock_move, stock_reservation_line, sale_order
where stock_move.id = stock_reservation_line.move_id
  and stock_reservation_line.so_id = sale_order.id
  and stock_move.picking_id =  %d''' % (po.id, )
                cr.execute(sql_stat)
	        for sql_res in cr.dictfetchall():
		    zichtzending = sql_res['zichtzending']
                res[po.id] = zichtzending
        return res

    def _function_reservation(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for po in self.browse(cr, uid, ids):
            res[po.id] = 0
            if po.id:
                sql_stat = '''select max(stock_reservation.id) as res_id from stock_reservation, stock_reservation_line, stock_move 
where stock_move.picking_id = %d
  and stock_reservation_line.move_id = stock_move.id
  and stock_reservation.id = stock_reservation_line.reservation_id''' % (po.id, )
                cr.execute(sql_stat)
                sql_res = cr.dictfetchone()
                if sql_res:
                    res[po.id] = sql_res['res_id']
        return res

    def write(self, cr, uid, ids, vals, context=None):
        if 'zichtz_inv_allowed' in vals and vals['zichtz_inv_allowed']:
            vals['invoice_state'] = '2binvoiced'
        if 'zichtz_inv_allowed' in vals and not vals['zichtz_inv_allowed']:
            vals['invoice_state'] = 'none'

        return super(stock_picking_out, self).write(cr, uid, ids, vals, context=context)

    _columns = {
        'invoice_amount': fields.function(_function_invoice_amount, string='Bedrag', type='float'),
        'zichtzending': fields.function(_function_zichtzending, string='Zichtzending', type='boolean', store=True),
        'zichtz_inv_allowed': fields.boolean('Te factureren zichtzending'),
        'reservation_id': fields.function(_function_reservation, string='Reservatie', type='many2one', relation='stock.reservation', select=True, store=True),
    }

stock_picking_out()

class stock_move(osv.osv):
    _inherit = 'stock.move'

    def _function_distributeur(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for po in self.browse(cr, uid, ids):
            if po.id:
                distributeur = ''
                sql_stat = '''select distinct product_product.distributeur from stock_move, product_product where product_id = product_product.id and stock_move.id =  %d''' % (po.id, )
                cr.execute(sql_stat)
                for sql_res in cr.dictfetchall():
                    distributeur = sql_res['distributeur']
                res[po.id] = distributeur
        return res

    def create(self, cr, uid, vals, context=None):
#         print 'Stock Move aanmaken met', vals
        if 'purchase_line_id' in vals:
            sql_stat = '''select zichtzending from purchase_order, purchase_order_line where purchase_order.id = purchase_order_line.order_id and purchase_order_line.id = %d''' % vals['purchase_line_id']
            cr.execute(sql_stat)
            for sql_res in cr.dictfetchall():
                vals['zichtzending'] = sql_res['zichtzending']
        if 'sale_line_id' in vals:
            sql_stat = '''select zichtzending from sale_order, sale_order_line where sale_order.id = sale_order_line.order_id and sale_order_line.id = %d''' % vals['sale_line_id']
            cr.execute(sql_stat)
            for sql_res in cr.dictfetchall():
                vals['zichtzending'] = sql_res['zichtzending']
        return super(stock_move, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
#         print 'Stock Move wijzigen met', ids, vals
#         if 'sale_line_id' in vals:
#             sql_stat = '''select zichtzending from sale_order, sale_order_line where sale_order.id = sale_order_line.order_id and sale_order_line.id = %d''' % vals['sale_line_id']
#             cr.execute(sql_stat)
#             for sql_res in cr.dictfetchall():
#                 vals['zichtzending'] = sql_res['zichtzending']
        return super(stock_move, self).write(cr, uid, ids, vals, context=context)
    
    _columns = {
        'distributeur_search': fields.function(_function_distributeur, string='Distributeur', type='char', store=True),
        'zichtzending': fields.boolean('Zichtzending'),
        'order_state': fields.related('order_id', 'state', type='char', relation='purchase.order', string='Order State', readonly=True),
        'artikel_status': fields.related('product_id', 'artikel_status', type='selection', relation='product.product', string='Artikel Status', selection=ARTIKEL_STATUS_SELECTION, readonly=True),
    }

    _defaults={
        'zichtzending': False,
    }

stock_move()

class res_users(osv.osv):
    _inherit = 'res.users'

    _columns = {
    'portal_customer_id': fields.many2one('res.partner','Customer for Portal',domain=[('is_company','=',True),('customer','=',True)]),
    }

res_users()

class port_scan(osv.osv_memory):
    _name = "port.scan"
    _description = "Scannen ontvangst"

    _columns = {
        'pakbon': fields.char('Pakbon', size=8),
        'boek': fields.char('ISBN', size=13),
        }
    
    def boek_change(self, cr, uid, ids, pakbon, boek, context=None):
        res = {}
        if boek == False or boek == None:
            return res
        boek_found = False
        pakbon_found = False
        line_found = False
        
        sql_stat = """
select id
from product_product
where default_code = '%s';
""" % (boek, )
        cr.execute (sql_stat)
        for sql_res in cr.dictfetchall():
            boek_found = True
            product_id = sql_res['id']

        if boek_found:        
            sql_stat = """
select id
from stock_reservation
where name = '%s';
""" % (pakbon, )
        cr.execute (sql_stat)
        for sql_res in cr.dictfetchall():
            pakbon_found = True
            pakbon_id = sql_res['id']

        if pakbon_found: 
            print "select 1"       
            sql_stat = """
select id, qty_to_deliver, qty_retour, qty_confirmed
from stock_reservation_line
where product_id = %d and reservation_id = %d;
""" % (product_id, pakbon_id)
            cr.execute (sql_stat)
            for sql_res in cr.dictfetchall():
                line_found = True
                line_id = sql_res['id']
                qty_to_deliver = sql_res['qty_to_deliver']
                qty_retour = sql_res['qty_retour']
                qty_confirmed = sql_res['qty_confirmed']
                
        if line_found and qty_confirmed < qty_to_deliver - qty_retour:        
            sql_stat = """
update stock_reservation_line set qty_confirmed = qty_confirmed + 1
where id = %d;
""" % (line_id, )
            cr.execute (sql_stat)
            cr.commit()
            res['boek'] = None
        else:
            print "2° select"
            sql_stat = """
select id, qty_to_deliver, qty_retour, qty_confirmed
from stock_reservation_line
where product_id = %d and reservation_id = %d and qty_confirmed < qty_to_deliver - qty_retour;
""" % (product_id, pakbon_id)
            cr.execute (sql_stat)
            for sql_res in cr.dictfetchall():
                line_found = True
                line_id = sql_res['id']
                qty_to_deliver = sql_res['qty_to_deliver']
                qty_retour = sql_res['qty_retour']
                qty_confirmed = sql_res['qty_confirmed']
                
            if line_found and qty_confirmed < qty_to_deliver - qty_retour:        
                sql_stat = """
update stock_reservation_line set qty_confirmed = qty_confirmed + 1
where id = %d;
""" % (line_id, )
                cr.execute (sql_stat)
                cr.commit()
                res['boek'] = None
        
        if not boek_found:
            raise osv.except_osv(('Waarschuwing !'),_(('Boek met ISBN barcode %s bestaat niet in de data base') % (boek, )))
        if not pakbon_found:
            raise osv.except_osv(('Waarschuwing !'),_(('Pakbon %s bestaat niet') % (pakbon, )))
        if boek_found and pakbon_found and not line_found:
            raise osv.except_osv(('Waarschuwing !'),_(('Boek %s komt niet voor in pakbon %s') % (boek, pakbon, )))
        if line_found and not(qty_confirmed < qty_to_deliver - qty_retour):
            raise osv.except_osv(('Waarschuwing !'),_(('U zou meer ontvangen dan op de pakbon voorzien, zie na en contacteer eventueel Christiana')))
        
        return {'value':res}
    
port_scan()

class stock_reservation(osv.osv):
    _inherit = 'stock.reservation' 
    
    def action_port_scan(self, cr, uid, ids, context=None):

        view_id = self.pool.get('ir.ui.view').search(cr, uid, [('model','=','port.scan'),
                                                            ('name','=','view.portal.scan.form')])

        pakbon = self.browse(cr, uid, ids)[0]
        context['default_pakbon'] = pakbon.name
        context['default_boek'] = None

        return {
            'type': 'ir.actions.act_window',
            'name': 'Scan ontvangst pakbon',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': view_id[0],
            'res_model': 'port.scan',
            'target': 'new',
            'context': context,
            }
