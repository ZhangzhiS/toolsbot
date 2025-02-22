import datetime
import hashlib

from nonebot import logger, on_keyword, require, on_command
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me

from models.discount import JdRebate, PositionIdMap
from toolsbot.adapters.wechat.event import Event
from toolsbot.adapters.wechat.message import SendTextMessage
from toolsbot.utils.dtk import dtk_cli

require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler  # noqa: E402

__plugin_meta__ = PluginMetadata(
    name="返利插件",
    description="购物返利",
    usage="",
)


jd_discount = on_keyword({"https://u.jd.com", "https://3.cn"}, block=True)


@jd_discount.handle()
async def _(event: Event):
    if event.roomid == "22374012632@chatroom" and event.sender == "wxid_hdo76qijifvz22":
        res = await dtk_cli.get_jd_url_content(event.content)
        if res:
            msg = SendTextMessage(res)
            return await jd_discount.finish(msg, receiver="34407719097@chatroom")
    if event.is_group:
        logger.info("不处理其他群消息中的优惠信息")
        return
    position_obj = await PositionIdMap.get_or_none(wxid=event.sender)
    if not position_obj:
        position_id = (
            int(hashlib.sha256(event.sender.encode()).hexdigest(), 16) % 1000000
        )
        await PositionIdMap.create(wxid=event.sender, position_id=position_id)
    else:
        position_id = position_obj.position_id
    res = await dtk_cli.get_jd_url_content(event.content, position_id=position_id)
    if not res:
        return await jd_discount.finish("""未找到优惠信息
暂时只支持京东
""")
    res += "\n通过链接下单，订单完成后即可返利"
    msg = SendTextMessage(res)
    await jd_discount.finish(msg, receiver=event.sender)


withdrawal = on_command("提现", rule=to_me())


@withdrawal.handle()
async def _(event: Event):
    if event.is_group:
        logger.info("不处理其他群消息中的优惠信息")
        return

    position_obj = await PositionIdMap.get_or_none(wxid=event.sender)
    if not position_obj:
        position_id = (
            int(hashlib.sha256(event.sender.encode()).hexdigest(), 16) % 1000000
        )
        await PositionIdMap.create(wxid=event.sender, position_id=position_id)
    else:
        position_id = position_obj.position_id
    orders = list(
        await JdRebate.filter(
            position_id=position_id, withdrawal_status=False, order_status=True
        ).limit(10)
    )
    if len(orders) == 0:
        return await withdrawal.finish(
            "暂无可提现订单\n通过我获取商品链接，下单获取返利！"
        )
    msg = ""
    for order in orders:
        msg += f"{order.sku_name[:6]} "


@scheduler.scheduled_job("cron", minute="*/10", id="checkJdOrder")
async def check_jd_order():
    end = datetime.datetime.now()
    start = end - datetime.timedelta(minutes=15)
    data = await dtk_cli.get_jd_order(
        start.strftime("%Y-%m-%d %H:%M:%S"),
        end.strftime("%Y-%m-%d %H:%M:%S"),
    )
    order_list = data.get("data", [])
    if not order_list:
        return
    order_info = {}
    for order in order_list:
        tmp = {
            "order_id": order["orderId"],
            "order_time": order["orderTime"],
            "modify_time": order["modifyTime"],
            "finish_time": order["finishTime"],
            "price": order["price"],
            "sub_union_id": order["subUnionId"],
            "position_id": order["positionId"],
            "sku_name": order["skuName"],
            "balance_ext": order["balanceExt"],
            "actual_fee": order["actualFee"],
            "actual_cos_price": order["actualCosPrice"],
            "estimate_cos_price": order["estimateCosPrice"],
            "estimate_fee": order["estimateFee"],
            "data": order,
        }
        order_id = str(tmp["order_id"])
        order_info[order_id] = tmp
    order_ids = [order for order in order_info]
    order_objs = list(await JdRebate.filter(order_id__in=order_ids))
    in_db_order_ids = [order.order_id for order in order_objs]
    # 更新数据库中的数据
    for update_order in order_objs:
        new_data = order_info.get(str(update_order.order_id))
        if not new_data:
            continue
        update_order.actual_cos_price = new_data.get("actual_cos_price")
        update_order.actual_fee = new_data.get("actual_fee")
        update_order.modify_time = new_data.get("modify_time")
        update_order.finish_time = new_data.get("finish_time")
        if update_order.finish_time:
            update_order.order_status = True
        update_order.data = new_data.get("data")
    if order_objs:
        await JdRebate.bulk_update(
            order_objs,
            fields=[
                "actual_cos_price",
                "actual_fee",
                "modify_time",
                "finish_time",
                "data",
            ],
        )
    # 创建新订单数据
    new_orders = []
    for new_order in order_info:
        if new_order not in in_db_order_ids:
            new_orders.append(JdRebate(**order_info[new_order]))
    if new_orders:
        await JdRebate.bulk_create(new_orders)
