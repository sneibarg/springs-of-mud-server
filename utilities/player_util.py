

def print_room(area_service, writer, character):
    room = area_service.get_registry().room_registry[character.room_id]
    writer.write(f'[{room.name}]'.encode('utf-8'))
    area_service.print_description(writer, room)
    area_service.print_exits(writer, room)


def visible_players(player_service, interested_player) -> list:
    visible = []
    current_character = interested_player.current_character
    role = current_character.role
    for name in player_service.get_connected_players():
        if name == current_character.name:
            continue
        connected = player_service.get_connected_player(name)
        if connected.cloaked and role == "player":
            continue
        else:
            visible.append(connected)
    return visible


def to_room(player_service, character, message, pattern):
    loiterers = player_service.get_in_room(character)
    cloaked_name = "Someone"
    cloaked = character.cloaked
    character_name = character.name
    if pattern is not None:
        pattern = pattern.replace('%p', cloaked_name if cloaked else character_name)
        pattern = pattern.replace('%m', message)
        message = pattern + "\r\n"
    else:
        message = message + "\r\n"
    for in_room in loiterers:
        in_room.get_writer().write(message.encode('utf-8'))

