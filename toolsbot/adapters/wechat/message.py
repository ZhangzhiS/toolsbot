from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Dict,
    Iterable,
    List,
    Optional,
    Type,
    TypedDict,
    Union,
)

from nonebot.adapters import (
    Message as BaseMessage,
)
from nonebot.adapters import (
    MessageSegment as BaseMessageSegment,
)
from typing_extensions import override
from .api import SendImageMessageAPI, SendTextMessageAPI, WechatHookApi


class MessageSegment(BaseMessageSegment["Message"]):
    @classmethod
    @override
    def get_message_class(cls) -> Type["Message"]:
        return Message

    @override
    def is_text(self) -> bool:
        return self.type == "text"

    @override
    def __str__(self) -> str:
        if self.is_text():
            return self.data.get("text", "")

        return ""

    @override
    def __add__(
        self, other: Union[str, "MessageSegment", Iterable["MessageSegment"]]
    ) -> "Message":
        return Message(self) + (
            MessageSegment.text(other) if isinstance(other, str) else other
        )

    @override
    def __radd__(
        self, other: Union[str, "MessageSegment", Iterable["MessageSegment"]]
    ) -> "Message":
        return (
            MessageSegment.text(other) if isinstance(other, str) else Message(other)
        ) + self

    @staticmethod
    def text(text: str) -> "Text":
        return Text("text", {"text": str(text)})

    @staticmethod
    def image(path: str) -> "Image":
        return Image("image", {"path": path})

    @staticmethod
    def at(wxid: str = ""):
        return At("at", {"wxid": wxid})

    @staticmethod
    def api(api: WechatHookApi):
        return WeCahtApi("api", {"api": api})

    @staticmethod
    def receiver(receiver: str):
        return Receiver("receiver", {"receiver": receiver})

    @staticmethod
    def hongbao(text: str) -> "Hongbao":
        return Hongbao("hongbao", {"text": text})

    @staticmethod
    def share_chat(chat_id: str) -> "MessageSegment":
        return ShareChat("share_chat", {"chat_id": chat_id})

    @staticmethod
    def share_user(user_id: str) -> "MessageSegment":
        return ShareUser("share_user", {"user_id": user_id})


class _WeChatApi(TypedDict):
    api: WechatHookApi


@dataclass
class WeCahtApi(MessageSegment):
    if TYPE_CHECKING:
        data: _WeChatApi

    @override
    def __str__(self) -> str:
        return self.data["api"].__class__.__name__


class _Receiver(TypedDict):
    receiver: str


@dataclass
class Receiver(MessageSegment):
    if TYPE_CHECKING:
        data: _Receiver

    @override
    def __str__(self) -> str:
        return self.data["receiver"]


class _TextData(TypedDict):
    text: str


@dataclass
class Text(MessageSegment):
    if TYPE_CHECKING:
        data: _TextData

    @override
    def __str__(self) -> str:
        return self.data["text"]


class _AtData(TypedDict):
    wxid: str


@dataclass
class At(MessageSegment):
    if TYPE_CHECKING:
        data: _AtData

    @override
    def __str__(self) -> str:
        return f"@{self.data['wxid']}"


class _ImageData(TypedDict):
    path: str


@dataclass
class Image(MessageSegment):
    if TYPE_CHECKING:
        data: _ImageData

    @override
    def __str__(self) -> str:
        return self.data["path"]


class _ShareChatData(TypedDict):
    chat_id: str


@dataclass
class ShareChat(MessageSegment):
    if TYPE_CHECKING:
        data: _ShareChatData

    @override
    def __str__(self) -> str:
        return f"[share_chat:{self.data['chat_id']!r}]"


class _ShareUserData(TypedDict):
    user_id: str


@dataclass
class ShareUser(MessageSegment):
    if TYPE_CHECKING:
        data: _ShareUserData

    @override
    def __str__(self) -> str:
        return f"[share_user:{self.data['user_id']!r}]"


class _HongbaoData(TypedDict):
    text: str


@dataclass
class Hongbao(MessageSegment):
    if TYPE_CHECKING:
        data: _HongbaoData

    @override
    def __str__(self) -> str:
        return f"[hongbao:{self.data['text']!r}]"


class Message(BaseMessage[MessageSegment]):
    req: WechatHookApi = WechatHookApi()

    @classmethod
    @override
    def get_segment_class(cls) -> Type[MessageSegment]:
        return MessageSegment

    @staticmethod
    @override
    def _construct(msg: str) -> Iterable[MessageSegment]:
        yield Text("text", {"text": msg})

    def validate(self) -> bool:
        if len(self.get("text")) < 1:
            raise Exception
        return True

    def serialize(self, receiver) -> Dict[str, str]: ...


class SendTextMessage(Message):
    req: WechatHookApi = SendTextMessageAPI()
    msg: str

    def validate(self) -> bool:
        if len(self.get("text")) < 1:
            raise Exception
        return True

    def serialize(self, receiver: str) -> Dict[str, str]:
        aters = ",".join([str(i) for i in self.get("at")])
        message = " ".join([str(i) for i in self.get("text")])
        return dict(aters=aters, msg=message, receiver=receiver)

    @classmethod
    @override
    def get_segment_class(cls) -> Type[MessageSegment]:
        return MessageSegment

    @staticmethod
    @override
    def _construct(msg: str) -> Iterable[MessageSegment]:
        yield Text("text", {"text": msg})

    @override
    def extract_plain_text(self) -> str:
        text_list: List[str] = []
        for seg in self:
            if seg.is_text():
                text_list.append(str(seg))

        return "".join(text_list)


class SendImageMessage(Message):
    req: WechatHookApi = SendImageMessageAPI()
    path: str

    def serialize(self, receiver) -> Dict[str, str]:
        path = self.get("image")[0]
        return dict(receiver=receiver, path=str(path))

    def validate(self) -> bool:
        if len(self.get("image")) != 1:
            raise Exception
        return True

    @staticmethod
    @override
    def _construct(path: str) -> Iterable[MessageSegment]:
        yield Image("image", {"path": path})
