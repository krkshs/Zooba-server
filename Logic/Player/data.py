import time

from Protocol.Pitaya.pb import mk
from Server.Theme.cfg import cfg, opt


def plr(row):
    score = opt['trophies']
    league = max(idx for idx, val in enumerate(cfg.configLeagues) if val.trophiesMin <= score)
    return mk('DataPlayer', id=row['id'], name=row['name'], locale=row['loc'],
              trophies=score, maxTrophies=score, seasonMaxTrophies=score,
              league=league, gold=opt['gold'], gems=opt['gems'], tutorial=255,
              trophyRoadClaimed=score, nameSanitized=True,
              eventEnergy={'amount': 100, 'lastAutoRefillTimestamp': int(time.time())},
              createdAt={'seconds': row['born']},
              seasonalMasteryRoad={})


def inv(row):
    chars = [mk('DataCharacter', id=name, level=1,
                trophies=opt['trophies'] if name == 'buffalo' else 0,
                maxTrophies=opt['trophies'] if name == 'buffalo' else 0,
                isUnlocked=True, skins=[0], loadoutSize=1)
             for name in ('buffalo', 'gorilla')]
    upgrades = []
    for name in ('buffalo', 'gorilla'):
        wpns = cfg.configCharUpgrade.charWeapons[name].ConfigCharUpgradeWeapon
        if len(wpns) != 3:
            raise ValueError('missing character weapon config: ' + name)
        vals = {'id': name, 'upgrades': {'levelsReached': ['1.0'], 'levelsUnlocked': ['1.1']},
                'achievedPrimalInstincts': {}}
        for num, wpn in enumerate(wpns, 1):
            vals['weapon'+str(num)] = {'weaponId': wpn.weaponId,
                                      'skills': {attr.attributeId: 0 for attr in wpn.attributes}}
        upgrades.append(mk('CharacterUpgrade', **vals))
    return mk('DataInventory', selectedCharId=row['chr'], characters=chars, characterUpgrades=upgrades)


def loadouts():
    return mk('DataLoadouts', loadouts=[{'charId': name, 'loadoutId': '0', 'loadoutSize': 1}
                                      for name in ('buffalo', 'gorilla')])
