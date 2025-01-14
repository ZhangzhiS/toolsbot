import json
import base64
from typing import Dict


def encode_info(info: Dict[str, str]):
    return base64.b64encode(json.dumps(info).encode()).decode()


def decode_info(code: str) -> Dict[str, str]:
    return json.loads(base64.b64decode(code).decode())


def get_code(callback_url: str, wxid: str) -> str:
    code = wxid + "|" + callback_url
    return base64.b64encode(code.encode()).decode()  # 进行base64编码


def parse_code(code):
    decoded_code = base64.b64decode(code).decode()  # 进行base64解码
    wxid, callback_url = decoded_code.split("|")
    return wxid, callback_url


if __name__ == "__main__":
    u = {
        "wxid": "wxid_lyxq7hnoy8d422",
        "callback_url": "http://192.168.68.111:8081/",
        "name": "",
    }
    code = get_code(u["callback_url"], u["wxid"])
    print(code)
    info = parse_code(code)
    print(info)
