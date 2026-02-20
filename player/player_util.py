

def print_room(area_service, writer, character):
    room = area_service.get_registry().room_registry[character.room_id]
    writer.write(f'[{room.name}]'.encode('utf-8'))
    area_service.print_description(writer, room)
    area_service.print_exits(writer, room)




