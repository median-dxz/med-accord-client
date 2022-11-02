import accord_client.model.data as AccordData


def server(data: dict):
    return AccordData.ServerData(
        hash=str(data["hash"]),
        actualName=str(data["actualName"]),
        icon=str(data["icon"]),
        showName=str(data["showName"]),
    )


def update_members_list(data: dict):
    return AccordData.MemberData(name=str(data["name"]), avatar=str(data["avatar"]))
