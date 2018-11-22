# -*- coding: utf-8 -*-
####################################################
#  康虎云报表模板存储
#  该表中以Base64格式存储康虎云报表，可以方便地取
#  出来嵌入到康虎云报表打印数据(json)中
#
#
####################################################

import logging
import base64
from odoo import fields, models, api, http, _
from odoo.http import request
from cStringIO import StringIO
from werkzeug.utils import redirect
import warnings
from decimal import Decimal
from datetime import datetime

_logger = logging.getLogger(__name__)

def _get_cfprint_template(env, templ_id):
    """
    根据模板ID查询康虎云报表模板，用法如下：
    <t t-esc="cf_template(user.env, '12345')" />
    如果不使用这种方法，也可以在QWeb模板中按下面的方法取得模板内容：
    <t t-esc="user.env['cf.template'].search([('templ_id', '=', '12345')], limit=1).template" />
    取得模板
    :param env:         Env对象，在qweb模板中可以通过user.env或res_company.env取到
    :param templ_id:    模板唯一编号
    :return:
    """
    if (env is not None) and (templ_id is not None):
        templ = env['cf.template'].search([('templ_id', '=', templ_id)], limit=1)
        if len(templ)>0 :
            return templ.template.replace('\n','').strip(' ')   #去掉Base64中的换行符然后返回

    #条件无效或无相符记录，则返回空字符串
    return ''


def _convert_cn_currency(value, capital=True, prefix=False, classical=None):
    '''
    把金额转成中文大写
    用法：
    print (cncurrency(i))

    参数:
    capital:    True   大写汉字金额
                False  一般汉字金额
    classical:  True   元
                False  圆
    prefix:     True   以'人民币'开头
                False, 无开头
    '''
    # if not isinstance(value, (Decimal, str, int)):
    #     msg = u'由于浮点数精度问题，请考虑使用字符串，或者 decimal.Decimal 类。\
    #     因使用浮点数造成误差而带来的可能风险和损失作者概不负责。'
    #     warnings.warn(msg, UserWarning)
    # 默认大写金额用圆，一般汉字金额用元
    if classical is None:
        classical = True if capital else False

    # 汉字金额前缀
    if prefix is True:
        prefix = u'人民币'
    else:
        prefix = ''

    # 汉字金额字符定义
    dunit = (u'角', u'分')
    if capital:
        num = (u'零', u'壹', u'贰', u'叁', u'肆', u'伍', u'陆', u'柒', u'捌', u'玖')
        iunit = [None, u'拾', u'佰', u'仟', u'万', u'拾', u'佰', u'仟', u'亿', u'拾', u'佰', u'仟', u'万', u'拾', u'佰', u'仟']
    else:
        num = (u'○', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九')
        iunit = [None, u'十', u'百', u'千', u'万', u'十', u'百', u'千', u'亿', u'十', u'百', u'千', u'万', u'十', u'百', u'千']
    if classical:
        iunit[0] = u'元' if classical else u'圆'
    # 转换为Decimal，并截断多余小数

    if not isinstance(value, Decimal):
        value = Decimal(value).quantize(Decimal('0.01'))

    # 处理负数
    if value < 0:
        prefix += u'负'  # 输出前缀，加负
        value = - value  # 取正数部分，无须过多考虑正负数舍入
        # assert - value + value == 0
    # 转化为字符串
    s = str(value)
    if len(s) > 19:
        raise ValueError(u'金额太大了，不知道该怎么表达。')
    istr, dstr = s.split('.')  # 小数部分和整数部分分别处理
    istr = istr[::-1]  # 翻转整数部分字符串
    so = []  # 用于记录转换结果

    # 零
    if value == 0:
        return prefix + num[0] + iunit[0]
    haszero = False  # 用于标记零的使用
    if dstr == '00':
        haszero = True  # 如果无小数部分，则标记加过零，避免出现“圆零整”

    # 处理小数部分
    # 分
    if dstr[1] != '0':
        so.append(dunit[1])
        so.append(num[int(dstr[1])])
    else:
        so.append(u'整')  # 无分，则加“整”
    # 角
    if dstr[0] != '0':
        so.append(dunit[0])
        so.append(num[int(dstr[0])])
    elif dstr[1] != '0':
        so.append(num[0])  # 无角有分，添加“零”
        haszero = True  # 标记加过零了

    # 无整数部分
    if istr == '0':
        if haszero:  # 既然无整数部分，那么去掉角位置上的零
            so.pop()
        so.append(prefix)  # 加前缀
        so.reverse()  # 翻转
        return ''.join(so)

    # 处理整数部分
    for i, n in enumerate(istr):
        n = int(n)
        if i % 4 == 0:  # 在圆、万、亿等位上，即使是零，也必须有单位
            if i == 8 and so[-1] == iunit[4]:  # 亿和万之间全部为零的情况
                so.pop()  # 去掉万
            so.append(iunit[i])
            if n == 0:  # 处理这些位上为零的情况
                if not haszero:  # 如果以前没有加过零
                    so.insert(-1, num[0])  # 则在单位后面加零
                    haszero = True  # 标记加过零了
            else:  # 处理不为零的情况
                so.append(num[n])
                haszero = False  # 重新开始标记加零的情况
        else:  # 在其他位置上
            if n != 0:  # 不为零的情况
                so.append(iunit[i])
                so.append(num[n])
                haszero = False  # 重新开始标记加零的情况
            else:  # 处理为零的情况
                if not haszero:  # 如果以前没有加过零
                    so.append(num[0])
                    haszero = True

    # 最终结果
    so.append(prefix)
    so.reverse()
    return u''.join(so)


class Report(models.Model):
    """
    继承Report基类，增加自定义函数输出到QWeb模板中，方便在模板中便捷取康虎云报表模板
    """
    _inherit = "report"
    _description = "Report"

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

        # cf_template = self.env['cf.template'].browse()

        ####################################
        # 暴露给模板使用的工具函数
        values.update(
            cf_template=_get_cfprint_template,          # 把获取模板函数传入模板，*******不建议使用*******
            get_cf_template=_get_cfprint_template,       #把获取模板函数传入模板
            get_cn_currency = _convert_cn_currency,     #把金额转成中文大写
        )

        obj = super(Report, self).render(template, values)
        return obj

class CFTemplateCategory(models.Model):
    """
    康虎云报表模板分类
    """
    _name = 'cf.template.category'
    _description = _(u"Report templates category of CFPrint")

    name = fields.Char(string=u"Category Name", required=True)
    lines = fields.One2many("cf.template", "category_id", string=u"Templates")
    # templ_histories = fields.One2many("cf.template.history", "category_id", string=u"Templates History")

    _sql_constraints = [
        ('cons_cf_templ_category', 'unique(name)', u'Template category name already exists!')
    ]

class CFTemplate(models.Model):
    """
    康虎云报表模板模型类，通过该模型把康虎云报表保存在服务器数据库中，便于统一管理模板
    """
    _name = 'cf.template'
    _description = _(u"Report templates of CFPrint")

    category_id = fields.Many2one("cf.template.category", string=u"Category", default=lambda self: self.env.ref('cfprint.cf_templ_category_common'))
    templ_id = fields.Char(u'Template ID', required=True, help=u'Unique ID of template')
    name = fields.Char(u'Name', required=True)
    description = fields.Text(u'Description', required=False)
    preview_img = fields.Binary(u'Preview image', required=False, help=u'Picture used to preview a report')
    template = fields.Binary(u'Template', help=u'Content of template')
    template_filename = fields.Char(string=u'Template Filename', compute="_compute_template_filename")
    templ_histories = fields.One2many('cf.template.history', 'origin', string=u'History', help=u"History of template")

    _sql_constraints = [
        ('cons_cf_templ_id', 'unique(templ_id)', u'Template ID already exists!')
    ]

    @api.multi
    def write(self, vals):
        # 保存模板历史


        # if not vals.get("templ_id", False) and \
        #         ( vals.get("template", False) or vals.get("category_id", False) or vals.get("name", False) or vals.get("description", False) ):
        if vals.get("template", False) and self.template:
            # 模板ID未更新时，表示是模板更新,需要保存历史记录，否则是新建模板
            ver = ""
            if isinstance(self.write_date, str):
                ver = self.write_date.replace('-', '').replace(':', '').replace(' ', '')
            else:
                ver = datetime.strftime(self.write_date, "%Y%m%d%H%M%S")

            self.env['cf.template.history'].create({
                "category_id": self.category_id.id,
                'origin': self.id,
                "version": ver,
                "templ_id":self.templ_id,
                "name":self.name,
                "description":self.description,
                "preview_img":self.preview_img,
                "template":self.template,
            })

        return super(CFTemplate, self).write(vals)

    @api.multi
    def _compute_template_filename(self):
        for templ in self:
            templ.template_filename = templ.templ_id + ".fr3";


class CFTemplateHistory(models.Model):
    """
    康虎云报表模板历史版本，通过该模型把康虎云报表保存在服务器数据库中，便于统一管理模板
    """
    _name = 'cf.template.history'
    _description = _(u"History of report templates of CFPrint")

    category_id = fields.Many2one("cf.template.category", string=u"Category")
    origin = fields.Many2one('cf.template', string=u'Origin Template')
    version = fields.Char(string=u"Version", help=u"Version of template")
    templ_id = fields.Char(u'Template ID', required=True, help=u'Unique ID of template')
    name = fields.Char(u'Name', required=True)
    description = fields.Text(u'Description', required=False)
    preview_img = fields.Binary(u'Preview image', required=False, help=u'Picture used to preview a report')
    template = fields.Binary(u'Template', help=u'Content of template')

    _sql_constraints = [
        ('cons_cf_templ_id_ver', 'unique(templ_id, version)', u'Same version and template ID already exists!')
    ]