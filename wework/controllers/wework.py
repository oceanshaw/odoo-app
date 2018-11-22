# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from werkzeug.utils import redirect
import logging,time,json
from WXBizMsgCrypt import WXBizMsgCrypt
import xml.etree.cElementTree as ET
from Config import *
import sys

_logger = logging.getLogger(__name__)

class Wework(http.Controller):

	@http.route('/wework/callback_data', auth='public',csrf=False)
	def callback_data(self, **kw):
		wxcpt = WXBizMsgCrypt(WXConfig["Token"], WXConfig["EncodingAESKey"], WXConfig["SuiteID"])

		sVerifyMsgSig = kw.get("msg_signature")
		sVerifyTimeStamp = kw.get("timestamp")
		sVerifyNonce = kw.get("nonce")
		sVerifyEchoStr = kw.get("echostr")

		sVerifyMsgSig = "16340441fee1b3d55f6676d2fdc54a15d038cf89"
		sVerifyTimeStamp = "1522647527"
		sVerifyNonce = "384487989"
		sVerifyEchoStr = "3oBOMUsvtUK0XOPIBvEjSkHFgqEZjJF/f4+KSj8G9ZmElZSV2BhWEpYlhTSQl0zlcTh2lAFTr87jcK+JXuNPpQ=="
		_logger.info(sVerifyEchoStr)
		ret, sEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)
		if (ret != 0):
			return "ERR: VerifyURL ret: " + str(ret)
		else:
			return sEchoStr

	@http.route('/wework/callback_command', auth='public',csrf=False)
	def callback_command(self, **kw):
		wxcpt = WXBizMsgCrypt(WXConfig["Token"], WXConfig["EncodingAESKey"], WXConfig["SuiteID"])

		sVerifyMsgSig = kw.get("msg_signature")

		sVerifyTimeStamp = kw.get("timestamp")
		sVerifyNonce = kw.get("nonce")
		sVerifyEchoStr = kw.get("echostr")
		_logger.info(sVerifyEchoStr)
		ret, sEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)
		if (ret != 0):
			return "ERR: VerifyURL ret: " + str(ret)
		else:
			return sEchoStr





