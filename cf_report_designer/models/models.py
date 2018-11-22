# -*- coding: utf-8 -*-
# 康虎软件工作室
# http://www.khcloud.net
# QQ: 360026606
# wechat: 360026606
#--------------------------
#
import os
import sys
import logging
import string
try:
    import simplejson as json
except ImportError:
    import json

from lxml import etree
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from xml.dom import minidom

from odoo.exceptions import AccessError, UserError, ValidationError
from odoo import models, fields, api, _
from data_util import *

_logger = logging.getLogger(__name__)


#################################
##
##  接下来的思路：
##  1、在动态生成的模板中放一个t-esc标签
##  2、继承 _inherit = "report"，继承 def render(self, template, values=None) 方法，
##     在该方法中拼数据json，然后由渲染引擎渲染到html中
##
##################################

___1 = ('C') #此处16|24|32个字符
___2 = ('FS') #此处16|24|32个字符
___3 = ('O') #此处16|24|32个字符
___4 = ('F') #此处16|24|32个字符

REPORT_FILE_PERFIX = "rpt_"
REPORT_NAME_PERFIX = "rpt_"
REPORT_ID_PERFIX = "report_"
SHOW_MESSAHE_TEMPL = "<h4 style=\"margin-top: 3rem; text-align: center;\">%s</h4>"

TOKEN_CRYPT_KEY = ("CF","S","OFT","St","ud","io","72","01")


___5 = ('T') #此处16|24|32个字符
___6 = ('S') #此处16|24|32个字符
___7 = ('t') #此处16|24|32个字符
___8 = ('u') #此处16|24|32个字符


class IrModel(models.Model):
    _inherit = 'ir.model'

    def name_get(self):
        return [(model.id, '%s(%s)' % (model.name, model.model)) for model  in self]

class CFPrintLicense(models.Model):
    _name = 'cf.cfprint.license'
    _description = u'许可证信息'

    mcode = fields.Char(string=u'机器码', default=lambda x: get_machine_code(), help=u'服务器机器码')
    license = fields.Binary(string=u'许可证', help=u'授权许可证文件，下载后改名为cfprint.lic放到客户端cfprint目录下。')
    note = fields.Char(string=u'备注')

    @api.model
    def create(self, vals):
        vals['mcode'] = machine_code = get_machine_code() or ''  #Get machine code
        return super(CFPrintLicense, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['mcode'] = machine_code = get_machine_code() or ''  #Get machine code
        return super(CFPrintLicense, self).write(vals)


___9 = ('d') #此处16|24|32个字符
___10 = ('i') #此处16|24|32个字符
___11 = ('o72') #此处16|24|32个字符
___12 = ('0') #此处16|24|32个字符
___13 = ('1') #此处16|24|32个字符


def get__():
    return ''.join(___1+___2+___3+___4+___5+___6+___7+___8+___9+___10+___11+___12+___13)

class CFReportDefine(models.Model):
    _name = 'cf.report.define'
    _description = u'报表定义'

    name = fields.Char(string=u'报表ID', copy=True, help=u"用一确定报表的唯一ID，只允许英文、数字和下划线。")
    comment = fields.Char(string=u'报表中文名称', copy=True)
    model_id = fields.Many2one('ir.model', string=u'数据表(model)', required=True, copy=True, help=u"报表对应的数据表(model)")
    template_id = fields.Many2one('cf.template', string=u'报表模板', copy=True, help=u"该报表使用的打印模板。\n模板如果尚未设计，可以先创建一个模板定义，待生成数据并设计报表模板后再上传到模板库。")
    company_id = fields.Many2one('res.company', string=u'所属公司', default=lambda self: self.env['res.company']._company_default_get(''))
    open_print = fields.Boolean(string=u"是否弹出打印", default=False)
    use_client_templ = fields.Boolean(string=u"使用客户端模板",  default=False, help=u"")
    client_templ_name = fields.Char(string=u"客户端模板文件名", help=u"如果设置了使用客户端模板，则在此录入客户端模板路径和文件名")
    field_ids = fields.One2many("cf.report.define.field", "report_id", string=u"字段", help=u"要在报表模板中使用的字段信息")
    state = fields.Selection([('draft', u'草稿'),('defined', u'完成报表定义')], string=u"状态", default="draft")
    note = fields.Text(string=u"备注")

    _sql_constraints = [
        ('uniq_name', 'unique(name)', u'报表名称必须唯一!'),
    ]

    @api.model
    def create(self, vals):
        if not vals.get("template_id", False):
            _name = vals.get("name", False)
            _comment = vals.get("comment", False)
            if not _name:
                raise ValidationError(_(u"请先指定报表ID！"))
            cf_templ_id = "cf_templ_%s" % (REPORT_NAME_PERFIX, _name.replace('.', '_'))
            cf_templ = self.env["cf.template"].search([('templ_id', '=', cf_templ_id)], limit=1)
            if not cf_templ:
                cf_templ = self.env["cf.template"].create({
                    "templ_id": cf_templ_id,
                    "name": (_comment or cf_templ_id) + "打印模板",
                    "description": (_comment or cf_templ_id) + "打印模板",
                })
            vals["template_id"] = cf_templ.id

        return super(CFReportDefine, self).create(vals)

    # def _upgrade_module(self):
    #     modules = self.env['ir.module.module'].sudo().search([('name', '=', "cf_report_designer")])
    #     if modules:
    #         modules.button_immediate_upgrade()

    @api.multi
    def unlink(self):
        for rpt in self:
            rpt._remove_report()
        return super(CFReportDefine, self).unlink()


    def _get_report_id(self):
        self.ensure_one()
        return "%s%s" % (REPORT_ID_PERFIX, self.name)

    def _get_report_name(self, with_module=True):
        self.ensure_one()
        if with_module:
            return "cf_report_designer.%s%s" % (REPORT_NAME_PERFIX, self.name.replace('.', '_'))
        else:
            return "%s%s" % (REPORT_NAME_PERFIX, self.name.replace('.', '_'))

    def _get_report_file(self, with_module=True):
        self.ensure_one()
        if with_module:
            return "cf_report_designer.%s%s" % (REPORT_FILE_PERFIX, self.name.replace('.', '_'))
        else:
            return "%s%s" % (REPORT_FILE_PERFIX, self.name.replace('.', '_'))

    @api.one
    def _remove_report(self):
        report_id = self._get_report_id()
        report_name = self._get_report_name()
        report_file = self._get_report_file()

        # 删除报表定义
        self.env["ir.model.data"].sudo().search([('name', '=', report_id)]).unlink()
        self.env['ir.values'].sudo().search([('name', '=', report_id)]).unlink()
        reports = self.env['ir.actions.report.xml'].sudo().search([('report_name', '=', report_name)])
        for rpt in reports:
            rpt.unlink_action()
            rpt.unlink()

        # 删除模板
        self.env['ir.ui.view'].search([('key', '=', report_name)]).unlink()

    def action_retrieve_fields(self):
        """生成报表字段"""
        # 先删除旧字段记录
        self.env["cf.report.define.field"].search([('report_id', '=', self.id)]).unlink()

        # 增加字段
        for line in self.model_id.field_id:
            field = self.env['cf.report.define.field'].create({
                "report_id": self.id,
                "model_id": line.model_id.id,
                "field_id": line.id,
           })


    def _make_report_defind(self):
        # # 生成报表定义
        # report_id = "%s%s"%(REPORT_ID_PERFIX, self.name)
        # 生成报表定义
        report_id = self._get_report_id()
        report_name = self._get_report_name()
        report_file = self._get_report_file()

        # 再创建新记录
        report_obj = self.env['ir.actions.report.xml']
        report = report_obj.create({
            "name": self.comment or self.name,
            "type": "ir.actions.report.xml",
            # "binding_type": "report",     //12才有的字段
            "model": self.model_id.model,
            "report_type": "qweb-html",
            "report_name": report_name,
            "report_file": report_file,  # 自定义的报表取数逻辑python类，如果有，则根据该文件执行结果渲染报表
            "multi": False,
            "print_report_name": self.comment or self.name,  # TODO：这个打印名称可改成其他值
            "attachment_use": False,
            # "cf_report_define_id": self.id,
        })
        if report:
            self.env["ir.model.data"].create({
                "name": report_id,
                "model": "ir.actions.report.xml",
                "module": "cf_report_designer",
                "noupdate": False,
                "res_id": report.id,
                "date_init": fields.Datetime.now(),
                "date_update": fields.Datetime.now(),
            })

            report.create_action()

    def _make_templ(self):
        """生成QWeb模板定义"""

        templ_id = "%s%s" % (REPORT_NAME_PERFIX, self.name.replace('.', '_'))
        report_id = self._get_report_id()
        report_name = self._get_report_name()
        report_file = self._get_report_file()

        _short_report_name = self._get_report_name(False)

        arch_db = """<?xml version="1.0"?>
<t t-name="%s">
    <t t-call="cfprint.html_container">
        <t t-raw="show_message"/>
    </t>
    <script type="text/javascript">
        <t t-raw="cfprint_json"/>
    </script>
</t>
""" % (_short_report_name)

        view_obj = self.env['ir.ui.view']

        try:
            view = view_obj.create({
                "name": _short_report_name,
                "key": report_name,
                "priority": 16,
                "type": "qweb",
                "arch_db": arch_db,
                "mode": "primary",
                "active": True,
                # "cf_report_define_id": self.id,
            })
            if view:
                self.env["ir.model.data"].create({
                    "name": _short_report_name,
                    "model": "ir.ui.view",
                    "module": "cf_report_designer",
                    "noupdate": False,
                    "res_id": view.id,
                    "date_init": fields.Datetime.now(),
                    "date_update": fields.Datetime.now(),
                })

        except Exception as e:
            _logger.error("Create report template[%s] failed." % (report_name))
            raise e



    def action_generate(self):
        """生成报表定义和模板定义"""

        # 先删除旧的记录
        self._remove_report()

        # 创建odoo原生的报表定义
        self._make_report_defind()

        # 创建Qweb模板定义
        self._make_templ()

        self.write({"state": "defined"})

    def action_design(self):
        """启动模板设计"""

        #查询5条记录用记于设计模板
        docs = self.env[self.model_id.model].search([], limit=5)
        docids = [x.id for x in docs]

        # report_id = "%s%s" % (REPORT_ID_PERFIX, self.name)
        report_id = "cf_report_designer.%s%s" % (REPORT_ID_PERFIX, self.name)
        # report_id = "%s.%s%s" % (self.model_id.model, REPORT_ID_PERFIX, self.name)
        report_name = "cf_report_designer.%s%s" % (REPORT_NAME_PERFIX, self.name)
        datas = {"is_design": True,
                 # "docs": docs,
                 "docids": docids,
                 "is_design": True
                 }
        return self.env['report'].with_context(is_design=True).get_action(docids, report_name, data=datas)

class CFReportDefineFields(models.Model):
    _name = 'cf.report.define.field'
    _description = u'报表字段'
    _order = 'report_id, id'

    report_id = fields.Many2one("cf.report.define", string=u"报表定义", required=True, ondelete='cascade', help=u"字段所在的报表定义")
    model_id = fields.Many2one('ir.model', string=u"数据表(模型)", required=True, ondelete='cascade', help=u"字段所在的model")
    model_name = fields.Char(related="model_id.name", string=u"模型名称")
    field_id = fields.Many2one("ir.model.fields", string=u"字段", required=True, ondelete='cascade')
    name = fields.Char(related="field_id.name", string=u'字段名称', required=True)
    field_description = fields.Char(related="field_id.field_description", string=u'字段说明')
    ttype = fields.Selection(related="field_id.ttype", string=u'字段类型')
    parent_field_id = fields.Many2one("cf.report.define.field", string=u"关联上级字段")
    sub_field_ids = fields.One2many("cf.report.define.field", "parent_field_id", string=u"下级字段")
    note = fields.Text(string=u"备注")

    _sql_constraints = [
        ('uniq_repoer_model_field', 'unique(report_id, model_id, field_id)', u'报表+表+字段必须唯一!'),
    ]

    def action_retrieve_fields(self):
        if self.field_id and (self.field_id.ttype == 'one2many' or self.field_id.ttype == 'many2many'):
            if self.env.get(self.field_id.relation, "NO") == "NO":
                raise AccessError(_(u"未找到关联字段对应的表（%s），无法获取子表字段！" % (self.field_id.relation)))

            rel_model = self.env["ir.model"].search([('model', '=', self.field_id.relation)], limit=1)

            # 先删除旧字段记录
            self.env["cf.report.define.field"].search([('report_id', '=', self.id), ('model_id', '=', rel_model.id)]).unlink()
            # 增加字段
            for line in rel_model.field_id:
                field = self.env['cf.report.define.field'].create({
                    "parent_field_id": self.id,
                    "report_id": self.report_id.id,
                    "model_id": line.model_id.id,
                    "field_id": line.id,
               })

    def action_view_sub_fields(self):
        self.ensure_one()
        form_id = self.env.ref('cf_report_designer.cf_report_define_field_form').id
        return {'type': 'ir.actions.act_window',
                'res_model': 'cf.report.define.field',
                'view_mode': 'form',
                'views': [(form_id, 'form')],
                'res_id': self.id,
                'target': 'new',
                'limit': 1000,
                'name':u'从表字段',
                'flags': {'form': {'action_buttons': False}}
                }


class Report(models.Model):
    """
    继承Report基类，增加自定义函数输出到QWeb模板中，方便在模板中便捷取康虎云报表模板
    """
    _inherit = "report"
    _description = "Report"

    # cf_report_define_id = fields.Many2one("cf.report.define", string=u"报表定义", help=u"如果是康虎云报表，则保存对应的报表定义。")

    def _make_cfprint_json(self, values):
        """根据报表定义生成报表数据"""

        def _make_data_obj(report_define, model, fields, docs, datas):
            """生成数据对象"""

            def _remove_duplicated(lst):
                seen = set()
                new_l = []
                for d in lst:
                    t = tuple(d.items())
                    if t not in seen:
                        seen.add(t)
                        new_l.append(d)
                return new_l

            field_len = {}  #记录字段长度，生成数据结构时用作字段长度

            model_name_dash = model.model.replace(".", "_")

            _logger.debug("Processing docs...")
            # 生成报表数据
            for doc in docs:
                _logger.debug("Retrieve data...")
                obj = {}
                # # 只处理本级model的字段
                for field in [d for d in fields if d.model_id.model == model.model]:
                    try:
                        if field.ttype in ["one2many", "many2many"] and len(field.sub_field_ids)>0:
                            _docs = doc[field.name]
                            _fields = field.sub_field_ids
                            _model = self.env['ir.model'].search([('model', '=', field.field_id.relation)], limit=1)
                            if _docs and len(_docs)>0 and _fields and len(_fields)>0 and _model:
                                _make_data_obj(report_define, _model, _fields, _docs, datas)

                        elif field.ttype in ['boolean', 'char', 'datetime', 'integer', 'float', 'binary']:
                            obj[field.name] = doc[field.name] or ""
                            #记录字符型字段长度
                            if field.ttype ==  'char' and doc[field.name] and len(doc[field.name]) > field_len.get(field.name, 0):
                                field_len[field.name] = len(doc[field.name])

                        elif field.ttype in ['many2one']:
                            obj[field.name] = doc[field.name].id or ""
                            obj[field.name + "_name"] = doc[field.name].name or ""

                            # 记录字符型字段长度
                            if doc[field.name].name and len(doc[field.name].name) > field_len.get(field.name, 0):
                                field_len[field.name] = len(doc[field.name])
                            if doc[field.name + "_name"].name and len(doc[field.name + "_name"].name) > field_len.get(field.name + "_name", 0):
                                field_len[field.name + "_name"] = len(doc[field.name + "_name"])

                    except Exception as ex:
                        _logger.error(_(u"生成康虎云报表打印数据出错。model: %s, field: %s")%(model.model, field.name))

                if obj:
                    if not datas.get(model_name_dash, False):
                        datas[model_name_dash] = {"cols":[],  "rows":[] }
                    datas[model_name_dash]["rows"].append(obj)

            _logger.debug("Retrieve fields...")
            # 生成报表字段定义，只处理本级model的字段
            for field in [d for d in fields if d.model_id.model == model.model]:
                _type = "str"
                if field.ttype in ["integer"]:
                    _type = "int"
                elif field.ttype in ["float"]:
                    _type = "float"
                elif field.ttype in ["datetime"]:
                    _type = "date"
                elif field.ttype in ["boolean"]:
                    _type = "boolean"
                elif field.ttype in ["many2one"]:
                    _type = "str"

                _len = 0
                if _type == "str":
                    _len = field_len.get(field.name, 20)

                if not datas.get(model_name_dash, False):
                    datas[model_name_dash] = {"cols":[],  "rows":[] }
                datas[model_name_dash]["cols"].append(  { "type": _type, "size": _len, "name": field.name, "required": False, "comment": field.field_description } )
                if field.ttype in ["many2one"]:
                    datas[model_name_dash]["cols"].append( {"type": _type, "size": field_len.get(field.name + "_name", 20), "name": field.name+ "_name", "required": False, "comment": field.field_description})

            _logger.debug("Remove duplicated fields...")
            datas[model_name_dash]["cols"] = _remove_duplicated(datas[model_name_dash]["cols"])  #去除重复添加的字段
            return datas

            ## 以上内部函数

        report_define = values.get("report_define")
        _logger.debug("Get machine code...")
        machine_code = get_machine_code() or ''  #Get machine code
        print_obj = {
            "template": "",
            "ver": 4,
            "Copies": 1,
            "Duplex": 0,
            "mcode": machine_code,
            "Tables": []
        }

        _logger.debug("Check is design")
        _is_design = self._context.get("is_design", False)
        if _is_design:
            print_obj["design"] = True
            show_message = SHOW_MESSAHE_TEMPL % (_(u"""请在康虎云报表设计器设计报表。<br/>
            如果报表设计器未打开，请检查康虎云报表是否已启动！<br/><br/><br/>
            模板设计完成后，请在odoo菜单“康虎云报表”--&gt;“模板”菜单中，打开模板记录上传或更新模板！<br/><br/>
            <a href=\"cfprint://open\">启动康虎云报表</a>
            """))
            values.update(
                show_message=show_message
            )

        _logger.debug("Get template...")
        if report_define.use_client_templ and report_define.client_templ_name:
            print_obj["template"] = report_define.client_templ_name
        else:
            if not report_define.template_id or not report_define.template_id.templ_id:
                values.update(  show_message = SHOW_MESSAHE_TEMPL%(_(u"未指定要打印的报表模板，请先指定报表模板。") ))
            templ_data = self.env['cf.template'].search([('templ_id', '=', report_define.template_id.templ_id)], limit=1).template
            if not templ_data or templ_data=="":
                if not _is_design:
                    values.update( show_message = SHOW_MESSAHE_TEMPL%(_(u"指定的报表模板未定义或模板无内容，请先设计模板并更新到模板记录表。</h3>")) )
                else:
                    print_obj["template"] = "cf_templ_%s" % (report_define.name.replace('.', '_'))
            else:
                print_obj["template"] = "base64:" + templ_data.strip().replace("\n", "")

        _logger.debug("Get docs...")
        datas = {}
        docs = values.get("docs")
        if not docs or len(docs)<1:
            active_ids = self._context.get("active_ids", [])
            docs = self.env[report_define.model_id.model].browse(active_ids)

        _logger.debug("Convert docs to data object...")
        _make_data_obj(report_define, report_define.model_id, report_define.field_ids, docs, datas)

        _logger.debug("Merge data object...")
        # 数据合并到总的数据对象
        for i, (model_name, v) in enumerate(datas.items()):
            tableName = string.capwords(model_name).replace(".","_")
            cols = v["cols"]
            rows = v["rows"]
            print_obj["Tables"].append({
                "Name": tableName,
                "Cols": cols,
                "Data": rows,
            })

        return print_obj

    def set_report_data(self, values, report_data):
        """把生成的报表数据渲染到qweb模板形成HTML格式报表"""

        # 把数据转成json对象
        json_scripts = [
            "var cfprint_addr = \"127.0.0.1\"",
            "var _delay_close = -1"
        ]
        _logger.debug('Dump report data to json...')
        _report_data_plain = json.dumps(report_data)

        # 加密数据
        _logger.debug('Encrypt report data...')
        key = AESCoder.rand_aes_key(16, False)
        _logger.debug("AES Key: %s"%(key))
        aes = AESCoder(key, AES.MODE_CBC)
        _report_data_encrypted = aes.encrypt(_report_data_plain);

        # 加密密码
        _logger.debug('Encrypt key...')
        # FIXME: 这里的密码加密最后要改成不对称加密，由于Delphi和Python之间的互解密问题难以解决，暂时先只对密码进行Base64处理
        # rsa = RSACipher()
        # _key_encrypted = rsa.encrypt_str(key)
        # aes = AESCoder(''.join(TOKEN_CRYPT_KEY), AES.MODE_CBC)
        aes = AESCoder(get__(), AES.MODE_CBC)
        _key_encrypted = aes.encrypt(key);

        final_data = {
            "token": _key_encrypted,
            "dea": "aes",        #数据加密方法, Data Encrypt Algorithm
            "tea": "aes",        #Token加密方法, Token Encrypt Algorithm
            "data": _report_data_encrypted
        }

        _logger.debug('Dump final_data...')
        # json_scripts.append("var _data = %s"%(json.dumps(report_data)))
        json_scripts.append("var _data = %s" % (json.dumps(final_data)))

        json_scripts.append("""_reportData = JSON.stringify(_data);\nconsole.log(_reportData);""")
        json_data = ";\n".join(json_scripts)
        _logger.debug('json_data: %s'%(json_data[0: 300]))

        values.update(
            cfprint_json=json_data,
        )

    @api.multi
    def render(self, template, values=None):
        """
        继承report对象的渲染方法，在上下文中增加模板对象ORM
        :param template:
        :param values:
        :return:
        """
        if values is None:
            values = {}

        _logger.debug("Render report...")
        report = self._get_report_from_name(template)
        if not report:
            raise AccessError(_(u"未找到报表（%s）定义，可能是报表未定义或定义未生效，如果使用康虎云报表，请在报表定义中重新生成一下报表定义！" % (template)))

        show_message = SHOW_MESSAHE_TEMPL%(_(u"正在打印，请稍候...<br/><br/>如果打印机未输出报表，请检查康虎云报表是否已启动！<br/><br/><a href=\"cfprint://open\">启动康虎云报表</a>"))

        _logger.debug("Prepare docs...")
        docs = values.get("docs", False)
        if not docs or len(docs)<1:
            active_ids = self._context.get("active_ids", [])
            docs = self.env[report.model].browse(active_ids)
            values.update( docs = docs )
        if not docs or len(docs)<1:
            show_message = SHOW_MESSAHE_TEMPL%(_(u"没有可以打印数据。"))

        _logger.debug("Retrieve report define...")
        #解析报表定义ID
        rpt_defind_name = report.xml_id.split(".")
        if len(rpt_defind_name)>1:
            rpt_defind_name = rpt_defind_name[1].replace(REPORT_ID_PERFIX, "")
        else:
            rpt_defind_name = rpt_defind_name[0].replace(REPORT_ID_PERFIX, "")

        values.update(
            show_message=show_message
        )

        # 根据报表定义ID查询报表定义
        rpt_define = self.env["cf.report.define"].search([('name', '=', rpt_defind_name)], limit=1)
        _logger.debug("Prepare to make json...[%s]"%(rpt_defind_name))
        if rpt_define:
            _logger.debug("Set report_define to values...")
            values.update(  report_define=rpt_define, )
            _logger.debug("Begin to make report data ...")
            report_data = self._make_cfprint_json(values)
            _logger.debug("Begin to convert report data to json...")
            self.set_report_data(values, report_data)
            _logger.debug("Converted!!!")

        obj = super(Report, self).render(template, values)
        return obj


    def action_upload_templ_win(self):
        res_id = self._context.get("templ_id", False)
        return {
            'name': _(u'上传康虎云报表模板'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'res_model': 'cf.template',
            'res_id': res_id,
            # 'view_id': False,
            'context': self._context,
            'target': 'current',
            'nodestroy': True
        }



# class IrUIView(models.Model):
#     _inherit = 'ir.ui.view'
#
#     cf_report_define_id = fields.Many2one("cf.report.define", string=u"报表定义", help=u"如果是康虎云报表，则保存对应的报表定义。")