from accord_client.model.AccordServer import (ActionType, ProtocolDataEncoding, ProtocolDataHeader, ServerData)


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