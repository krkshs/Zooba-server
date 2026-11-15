import time

from Logic.Player.data import plr, inv, loadouts
from Protocol.Pitaya.pb import mk
from Server.Theme.cfg import cfg


def home(row, tok):
    now = int(time.time())
    return mk('AuthenticatePlayerAnswer', code='BAT-200', token=tok, timestampUtc=now,
              dataPlayer=plr(row), dataInventory=inv(row), dataPlayerChests={},
              dataMatchInfo={}, dataItems={}, dataLoadouts=loadouts(), configHash=cfg.hash,
              dataMissions={'cycleEndsAt': now + 86400}, dataClan={}, piggyBank={},
              team={}, subscription={'freeTrialRejectedForever': True}, featureStatus={},
              dataSeason={'currentSeasonId': 1, 'lastAcknowledgedSeason': 1,
                          'currentSeasonEndsAt': now + 31536000},
              dataEvents={}, dataStickers={}, remoteActionsConfig='{}',
              dataBattlePassRoad={'playerBattlePass': {'battlePassId': 'local',
                                 'battlePassType': 'free', 'endsAt': now + 31536000}},
              appAccountMigration={}, dataMeta={'serverBuildVersion': '7.6.0',
              'gameServerBuildVersion': '7.6.0', 'serverStack': 'local'})
