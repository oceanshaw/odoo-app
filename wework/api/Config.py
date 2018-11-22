#!/usr/bin/python
# -*- coding:utf-8 -*-
##
 # Copyright (C) 2018 All rights reserved.
 #   
 # @File conf.py
 # @Brief 
 # @Author abelzhu, abelzhu@tencent.com
 # @Version 1.0
 # @Date 2018-02-23
 #
 #
 
## 设置为true会打印一些调试信息
DEBUG = True 


WXConfig = {

    "SuiteID"               : "ww94b9a94bd7ce2f42",
    "Secret"                : "zpS2YRh8eJkZLNo6pvl-kkmNyTXZCP0zcoq5ooqTf2E",
    "Token"                 : "3tIW4rToO45TE4zp4D",
    "EncodingAESKey"        : "Dpfvz5YxaNEXieF3RzhuoJeMO59a9Yt71oKRQaCTh6B",


    # "通讯录同步"应用的secret, 开启api接口同步后，可以在管理端->"通讯录同步"看到
    #"CONTACT_SYNC_SECRET"   : "	zpS2YRh8eJkZLNo6pvl-kkmNyTXZCP0zcoq5ooqTf2E",

    # 某个自建应用的id及secret, 在管理端 -> 企业应用 -> 自建应用, 点进相应应用可以看到
    #"APP_ID"                : 1000002,
    #"APP_SECRET"            : "v1Z2KSw2WqPFECAwn2R0a1dFsanVF5sE4IE6X5ogveQ",

    # 打卡应用的 id 及secrete， 在管理端 -> 企业应用 -> 基础应用 -> 打卡，
    # 点进去，有个"api"按钮，点开后，会看到
    #"CHECKIN_APP_ID"        : 3010011,
    #"CHECKIN_APP_SECRET"    : "3Qz2OGPvE1Eb6WKpEDfczvyQjL5Lr1CjrDTKn0RHdLE",

    # 审批应用的 id 及secrete， 在管理端 -> 企业应用 -> 基础应用 -> 审批，
    # 点进去，有个"api"按钮，点开后，会看到
    #"APPROVAL_APP_ID"       : 3010040,
    #"APPROVAL_APP_SECRET"   : "1vrlwItWpz_5Qkud55aImQPCvpzi51H3F2j-1OQzhYE",
}
