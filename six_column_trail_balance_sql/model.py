#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################
from openerp import models, fields, api
from datetime import timedelta,datetime,date
from dateutil.relativedelta import relativedelta
import time
import re

class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.six_column_trail_balance_sql.customer_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('six_column_trail_balance_sql.customer_report')
        active_wizard = self.env['six.trailbalancesql'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['six.trailbalancesql'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['six.trailbalancesql'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()


        date_from = record_wizard.date_from
        date_to = record_wizard.date_to


        records = []
        rec = self.env['account.account'].search([('user_type_id.name','!=','View_Type')])
        for x in rec:
            records.append(x)


        def open_debit(attr):
            pre_field = "debit"
            table_name = "account_move_line"
            line_id = attr
            datefrom_id = record_wizard.date_from
            self.env.cr.execute("select SUM("+pre_field+") FROM "+table_name+" WHERE account_id = "+str(line_id)+" AND date < '"+datefrom_id+"' ")
            result = self._cr.fetchall()[0]
            if re.findall(r"[-+]?\d*\.\d+|\d+", str(result)):
                n = float(re.findall("[-+]?\d*\.\d+|\d+", str(result))[0])
                return n
            else:
                return 0.0


        def open_cre(attr):
            pre_field = "credit"
            table_name = "account_move_line"
            line_id = attr
            datefrom_id = record_wizard.date_from
            self.env.cr.execute("select SUM("+pre_field+") FROM "+table_name+" WHERE account_id = "+str(line_id)+" AND date < '"+datefrom_id+"' ")
            result = self._cr.fetchall()[0]
            if re.findall(r"[-+]?\d*\.\d+|\d+", str(result)):
                n = float(re.findall("[-+]?\d*\.\d+|\d+", str(result))[0])
                return n
            else:
                return 0.0


        def get_debit(attr):
            pre_field = "debit"
            table_name = "account_move_line"
            line_id = attr
            form = record_wizard.date_from
            to = record_wizard.date_to
            self.env.cr.execute("select SUM("+pre_field+") FROM "+table_name+" WHERE account_id = "+str(line_id)+" AND date >= '"+form+"' AND date <= '"+to+"' ")
            result = self._cr.fetchall()[0]
            if re.findall(r"[-+]?\d*\.\d+|\d+", str(result)):
                n = float(re.findall("[-+]?\d*\.\d+|\d+", str(result))[0])
                return n
            else:
                return 0.0

        def get_cre(attr):
            pre_field = "credit"
            table_name = "account_move_line"
            line_id = attr
            form = record_wizard.date_from
            to = record_wizard.date_to
            self.env.cr.execute("select SUM("+pre_field+") FROM "+table_name+" WHERE account_id = "+str(line_id)+" AND date >= '"+form+"' AND date <= '"+to+"' ")
            result = self._cr.fetchall()[0]
            if re.findall(r"[-+]?\d*\.\d+|\d+", str(result)):
                n = float(re.findall("[-+]?\d*\.\d+|\d+", str(result))[0])
                return n
            else:
                return 0.0



        docargs = {
        
            'doc_ids': docids,
            'doc_model': 'account.move',
            'date_from': date_from,
            'date_to': date_to,
            'records': records,
            'open_debit': open_debit,
            'open_cre': open_cre,
            'get_cre': get_cre,
            'get_debit': get_debit,
    
            }

        return report_obj.render('six_column_trail_balance_sql.customer_report', docargs)