#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from sqlalchemy import Column, Integer, String, SmallInteger

from . import Base


class CallbackMsgType(Enum):
    TEXT_MSG = 1
    IMG_MSG = 3
    VOICE_MSG = 34
    FRIEND_VER = 37
    USER_CARD = 42
    VIDEO_MSG = 43
    GIF_MSG = 47
    LOCALTION_MSG = 48
    SHARE_LINK_MSG = 49
    TRANSFER_ACCOUNTS = 2000
    RED_PACK = 2001
    MINI_PROGRAM = 2002
    GROUP_INVITATION = 2003
    FILE_MSG = 2004
    WITHDRAW_MSG = 2005
    SYSTEM_MSG = 10000
    SERVICE_MSG = 10002


class WechatRobot(Base):
    """微信机器人"""
    token = Column(String(64), comment="httpAPI配置的token")
    api_host = Column(String(255), comment="微信httpAPI地址")
    account_wxid = Column(String(64), comment="账号的微信id")
    nickname = Column(String(64), comment="机器人微信昵称")
    status = Column(SmallInteger, comment="机器人的状态")


class BotPlugins(Base):
    """机器人的插件权限"""
    pluigin_id = Column(String(64), comment="插件id")
    account_wxid = Column(String(64), comment="bot的微信id")
    status = Column(SmallInteger, comment="插件的状态")
