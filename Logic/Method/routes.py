import time

from Logic.Method.auth import lgn
from Logic.Player.data import loadouts
from Protocol.Pitaya.pb import dec, mk


def run(ctx, route, data):
    if route == 'metagame.playerHandler.authenticate':
        return lgn(ctx, data)
    if ctx.row is None:
        raise PermissionError('BAT-400')
    if route in ('metagame.playerHandler.timestamp', 'metagame.playerHandler.healthCheck'):
        return mk('TimestampUTCAnswer', TimestampUtc=int(time.time()), Code='BAT-200')
    if route == 'metagame.pendingPurchasesHandler.getPendingPurchase':
        return mk('GetPendingPurchaseAnswer')
    if route == 'metagame.pendingPurchasesHandler.getPendingWildTokens':
        return mk('GetPendingWildTokensAnswer')
    if route == 'metagame.dailyRewardsHandler.getPendingDailyRewards':
        return mk('GetPendingDailyRewardsAnswer', code='BAT-200')
    if route == 'metagame.matchmakingHandler.getRoomsForPing':
        return mk('GetRoomsForPingAnswer')
    if route == 'metagame.subscriptionHandler.getPlayerSubscription':
        return mk('Subscription', freeTrialRejectedForever=True)
    if route == 'metagame.membershipHandler.getPlayerMembership':
        return mk('PlayerMembership')
    if route == 'metagame.playerHandler.getLoadouts':
        return mk('GetLoadoutsAnswer', code='BAT-200', dataLoadouts=loadouts())
    if route == 'metagame.playerHandler.changeChar':
        req = dec('DefaultArgs', data)
        if req.parameter not in ('buffalo', 'gorilla'):
            return mk('DefaultAnswer', code='BAT-404')
        ctx.db.set(ctx.row['id'], 'chr', req.parameter)
        ctx.row['chr'] = req.parameter
        return mk('DefaultAnswer', code='BAT-200')
    if route in ('metagame.playerHandler.setPlayerOnline',
                 'metagame.playerHandler.updateLocale',
                 'metagame.clientDependencyHandler.clientDependencyLoaded',
                 'metagame.dailyRewardsHandler.clearPendingDailyRewards',
                 'metagame.pendingPurchasesHandler.ackPendingWildTokens'):
        return mk('DefaultAnswer', code='BAT-200')
    raise LookupError(route)
