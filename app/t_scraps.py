a = 100
d = 82

ATK_BUFFS = (1, 1.18, 1.33, 1.47, 1.57, 1.67, 1.77, 1.87)
DEF_DEBUFFS = (1, 0.8, 0.65, 0.5, 0.4, 0.3, 0.2, 0.1)
TYPE_ATK_BUFFS = (0, 0.25, 0.55, 0.9, 1.1, 1.3, 1.5, 1.7)
TYPE_DEF_BUFFS = (1, 0.88, 0.76, 0.64, 0.52, 0.4, 0.35, 0.3)

#print(a/d)
#print((a * 1.1) / d)
#print(a / (d * 0.9))

#
# for i in range(len(ATK_BUFFS)):
#     print(f'atk[{i}] = {(a * ATK_BUFFS[i]) / d}')
#     print(f'def[{i}] = {a / (d * DEF_DEBUFFS[i])}')
#     print('')

#
# for i in range(1, 101):
#     print((2 * i) / 5 + 2)


ivy = 80, 100
nidorina = 62, 67

xAbility = 1
xSlot = 1.5
xZ = 1
atkBuff = 0
defDebuff = 0
typeBonus = 0

attack = ivy[0]
defense = ivy[1]
enemyDef = nidorina[1] * 2
pierceFactor = 1

enemyTypeDefBuff = 0

typeBuff = 3#tb.atkBuffs[p.type] - tb.atkDebuffs[p.type]
typeDebuff = 0

xSkill = 1.2


def scale_stat(lv, base, iv, ev, nature):
    return int(int((2 * base + iv + ev) * lv / 100 + 5) * nature)

def scale_hp(lv, base, iv, ev):
    return int(int((2 * base + iv + ev) * lv / 100 + lv + 10))


def khux_damage_formula(attack, xSlot, atkBuff, defDebuff, enemyDef, pierceFactor,
    typeBuff, typeDebuff, enemyTypeDefBuff, typeBonus, xAbility, xZ, xSkill):

    atkCalc = attack * xSlot * ATK_BUFFS[atkBuff]
    defCalc = enemyDef * DEF_DEBUFFS[defDebuff] * pierceFactor
    xType = (1 + TYPE_ATK_BUFFS[typeBuff] + TYPE_ATK_BUFFS[typeDebuff] + typeBonus)

    damage = round(atkCalc - defCalc) * xType * xAbility * xZ * TYPE_DEF_BUFFS[enemyTypeDefBuff] * xSkill


    return damage



dmg = khux_damage_formula(attack, xSlot, atkBuff, defDebuff, enemyDef, 1,
                          typeBuff, typeDebuff, enemyTypeDefBuff, typeBonus,                                  xAbility, xZ, xSkill)

#print(dmg)

br = False
# for i in range(40, 121):
#     dmg = round(khux_damage_formula(i, xSlot, atkBuff, defDebuff, enemyDef, 1,
#                               typeBuff, typeDebuff, enemyTypeDefBuff, typeBonus,                                    xAbility, xZ, xSkill))
#     if dmg > 0 and not br:
#         print("\nBreak")
#         br = True
#     print(f'{i} vs {enemyDef}: {dmg} dmg')

baseAtk = ivy[0]
baseDef = ivy[1]

iv = 0
ev = 0
nature = 1

for lv in range(5, 101):
    print(f'\nLv {lv}')
    print(f'Atk: {scale_stat(lv, baseAtk, iv, ev, nature)}')
    print(f'Def: {scale_stat(lv, baseDef, iv, ev, nature)}')
    print(f'Hp: {scale_hp(lv, baseDef, iv, ev)}')
