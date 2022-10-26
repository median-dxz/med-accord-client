from accord_client.model.AccordServer import ServerData


def server(data: dict):
    return ServerData(
        hash=str(data.get('hash')),
        actualName=str(data.get('actualName')),
        icon=str(data.get('icon')),
        showName=str(data.get('showName')),
    )
