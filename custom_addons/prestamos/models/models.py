# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
import numpy as np
class Prestamos(models.Model):
    _name = 'prestamos.prestamos'
    _description = 'Prestamos'
    _rec_name='name'

    name = fields.Char("Nombre")
    partner_id = fields.Many2one(string="Cliente",comodel_name="res.partner")
    date = fields.Date(string="Fecha",default=fields.datetime.now())
    fees = fields.Integer(string="Numero de cuotas")
    amount_total = fields.Float(string='Monto total')
    line_ids = fields.One2many('lineas.lineas', 'prestamos_id', string='lineas')

    def action_calcular_cuota(self):
        cantidad = self.amount_total / self.fees
        cuotas = []
        self.line_ids = [(6, 0, [])]
        # import pdb;pdb.set_trace()
        for rec in range(1,self.fees+1):
            new_date = self.date + relativedelta(months=rec)
            cuotas.append((0, 0, {'payment_date': new_date, 'amount': cantidad}))
        self.write({'line_ids':cuotas})
    
    @api.onchange('partner_id','date')
    def _onchange_name(self):
        name_list = []
        for rec in self:
            if rec.partner_id:
                name_list.append('Prestamo de %s' %rec.partner_id.name)
            if rec.date:
                name_list.append(' en la fecha %s' %rec.date.strftime('%d/%m/%Y'))
        self.name = ''.join(name_list)



class lineas(models.Model):
    _name = 'lineas.lineas'
    _description = 'Lineas'

    payment_date = fields.Date(string='Fecha')
    amount = fields.Float(string='Monto total')
    prestamos_id = fields.Many2one('prestamos.prestamos', string='Prestamos')

