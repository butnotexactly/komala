from common import *

async def register_user(ctx, uid):
    await send_message(ctx, 'Register user')
        # jacobStartAmount = 62000

    # htgMedal = InventoryMedal()
    # htgMedal.n = 85
    # htgMedal.lv = 100
    # htgMedal.strength = 7143
    # htgMedal.defense = 7235
    # htgMedal.id = 0
    # inventory = [htgMedal]
    # inventoryData = gzip.compress(json.dumps([inventoryMedal.__dict__ for inventoryMedal in inventory]).encode('utf-8'))

    # c.execute('insert or ignore into user(discord_id, server_id, season, jacobs, medal_count, inventory_data, id_incrementor, inventory_update) values(?, ?, ?, ?, ?, ?, ?, ?)', [uid, client.context.groupId, season, jacobStartAmount, 1, inventoryData, 1, 1])

    # album_update(uid, inventory)

    # # c.execute('insert or ignore into user_keyblade (discord_id, kb, level) values(?, 0, 11)', [uid])
    # # c.execute('insert or ignore into user_keyblade (discord_id, kb, level) values(?, 1, 11)', [uid])
    # # c.execute('insert or ignore into user_keyblade (discord_id, kb, level) values(?, 2, 11)', [uid])
    # # c.execute('insert or ignore into user_keyblade (discord_id, kb, level) values(?, 3, 11)', [uid])
    # dbGame.commit()

    # if c.rowcount == 1:
    #     serverName = client.NetworkInfo.GetGroupInfo(id=client.context.groupId).name
    #     print('New account registered with {} jacobs! <:blobaww:360940687287648256> Welcome to the game. Be sure to do the `.tutorial` for 10000 extra jacobs and to read `.khuxhelp`.\n\nIf you'd like to support the project / costs, jacob's paypal is `jacob@rgby.xyz`. Donors get various benefits including:\n\n- **2x** daily amounts!\n- inventory images!\n- the ability to change your season at will!\n- the pristine satisfaction of knowing I love them'.format(jacobStartAmount))
        
    #     t = ((int(uid) >> 22) + 1420070400000) / 1000
    #     d = datetime.fromtimestamp(t)
    #     client.Messaging.MessageUser(id=jacobId, format='raw', content='New account <@{}> made on server {} ({})\nAccount Age: {}'.format(uid, serverName, client.context.groupId, d))
    #     return True

    # print('Unknown error, couldn''t create an account. :(')
    # return False
    return True


class Trainer(object):
    pass