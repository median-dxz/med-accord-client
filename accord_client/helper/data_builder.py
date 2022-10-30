import json

from accord_client.model.AccordServer import *
from accord_client.model.AccordAction import *


def server(data: dict):
    return ServerData(
        hash=str(data['hash']),
        actualName=str(data['actualName']),
        icon=str(data['icon']),
        showName=str(data['showName']),
    )


def protocol_data_header(data: dict):
    return ProtocolDataHeader(
        Action=ActionType(data['Action']),
        ContentEncoding=ProtocolDataEncoding(data['ContentEncoding']),
        ContentLength=int(data['ContentLength']),
        ContentMime=str(data['ContentMime']),
    )


def update_members_list(datas: list[dict]):
    ret = []
    for data in datas:
        ret.append(MemberData(name=str(data['name']), avatar=str(data['avatar'])))
    return ret


class ProtocolDataHeaderEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, ProtocolDataHeader):
            return {
                "Action": obj.Action.value,
                "ContentEncoding": obj.ContentEncoding.value,
                "ContentLength": obj.ContentLength,
                "ContentMime": obj.ContentMime
            }
        return json.JSONEncoder.default(self, obj)