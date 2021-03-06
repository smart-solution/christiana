#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
##############################################################################

from openerp.osv import osv, fields

class res_partner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
		'discount_ids': fields.one2many('res.partner.discount', 'partner_id', 'Kortingen'),
    }

res_partner()

#class sale_order_line(osv.osv):
#    _inherit = 'sale.order.line'
#
#    _columns = {
#    }
#
#    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
#            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
#            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, zichtzending=False, context=None):
#
#        if not partner_id:
#            return False
#    	if not product:
#	        return False
#
#        print 'ZICHTZENDING:',zichtzending
#        res = super(sale_order_line, self).product_id_change( cr, uid, ids, pricelist, product, qty, uom, qty_uos, uos, name, partner_id, lang, update_tax, date_order, packaging, fiscal_position, flag, zichtzending, context=context)
#
#        discount = 0.00
#
## partner and product
#        sql_stat = '''select discount_pct 
#from res_partner_discount d, product_product p
#where d.partner_id = %d 
#  and p.id = %d 
#  and ((d.awso_code = p.awso_code and %s = False)
#   or  (d.awso_code = 'Z' and %s = True))''' % (partner_id, product, zichtzending, zichtzending, )
#        print 'SQL_STAT:',sql_stat
#        cr.execute(sql_stat)
#        for sql_res in cr.dictfetchall():
#            discount = sql_res['discount_pct']
#
#        res['value']['discount'] = discount
#
#        print 'RES:',res
#        if 'warning' in res:
#            res['warning'] = {}
#
#        return res
#
#sale_order_line()

class res_partner_discount(osv.osv):
    _name = 'res.partner.discount'

    _columns = {
        'partner_id': fields.many2one('res.partner', 'Partner', select=True),
        'awso_code': fields.selection((('A','Algemeen'),('W','Wetenschappelijk'),('S','Studie'),('O','Overige'),('Z','Zichtzending')),'AWSO Code'),
        'discount_pct': fields.float('Korting', select=True),
    }

res_partner_discount()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

