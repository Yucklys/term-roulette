from GunMechanics import Gun, GunType
from player import Agent, decide_action, calculate_reward, Action

def test_against(gun, agent, num_games=1000, step=100, verbose=False):
    hp = {}
    hp["player"] = 5
    hp["agent"] = 5
    # if True, player's turn, else agent's turn
    player_turn = True
    player_win_count = 0

    # test agent vs. agent
    for i in range(num_games):
        game_decision = []
        game_probs = []
        chamber = gun.chamber
        winner = None
        
        while len(gun.chamber) > 0:
            decisions, probs = proceed_turn(agent, hp, gun, player_turn)
            player_turn = not player_turn
            if player_turn:
                game_decision.extend(decisions)
                game_probs.extend(probs)
            else:
                game_decision.extend(decisions)
                game_probs.extend(probs)

            if hp["agent"] <= 0:
                winner = "player"
                hp = {"player": 5, "agent": 5}
                player_win_count += 1
                break
            elif hp["player"] <= 0:
                winner = "agent"
                hp = {"player": 5, "agent": 5}
                break

            # reload bullet if game is not finished
            if winner is None:
                gun.reload()

        gun.reload()
        if i % step == step - 1 and verbose:
            print(f"Game {i + 1} finished. Winner: {winner}")
            print_statistic(chamber, game_decision, game_probs)
            
    return player_win_count

def proceed_turn(agent, hp, gun, turn):
    decision, prob = test_decision(agent, hp, gun)
    bullet = gun.shoot()
    decisions = []
    probs = []

    if turn:
        decisions = [decision["player"]]
        probs = [prob["player"]]
        target, hp_change = shoot_result(bullet, decision["player"])
        if target == "self":
            hp["player"] += hp_change
        else:
            hp["agent"] += hp_change
    else:
        decisions = [decision["agent"]]
        probs = [prob["agent"]]
        target, hp_change = shoot_result(bullet, decision["agent"])
        if target == "self":
            hp["agent"] += hp_change
        else:
            hp["player"] += hp_change
            
    if hp_change == 0 and target == "self":
        next_decision, next_prob = proceed_turn(agent, hp, gun, turn)
        decisions.extend(next_decision)
        probs.extend(next_prob)

    # prefix the decision with the turn name
    for i in range(len(decisions)):
        turn_name = "player" if turn else "agent"
        decisions[i] = f"{turn_name}_{decisions[i]}"

    return decisions, probs


def test_decision(agent, hp, gun):
    decision = {}
    probs = {}
    match agent:
        case Agent.BERSERKER:
            decision['player'] = decide_action(hp['player'], gun=gun).value
            probs['player'] = calculate_reward(hp['player'], gun=gun)
            decision['agent'] = decide_action(hp['agent'], gun=gun).value
            probs['agent'] = calculate_reward(hp['agent'], gun=gun)
    return decision, probs

def shoot_result(bullet, decision):
    hp_change = 0
    match bullet:
        case 1:
            hp_change = -1
        case 2:
            hp_change = 0
        case 3:
            hp_change = -2
        case 4:
            hp_change = 1
    match decision:
        case "shoot_self":
            return "self", hp_change
        case "shoot_opponent":
            return "agent", hp_change

def print_statistic(dist, decisions, probs):
    print("Bullet distribution: ", dist)
    print("Decisions: ", decisions)
    formated_probs = []
    for i in probs:
        formated_probs.append(f"({i[0]:.2f}, {i[1]:.2f})")
    print("Rewards: ", formated_probs)

def test():
    gun = Gun(GunType.REVOLVER)
    total_games = 1000
    player_win_count = test_against(gun, Agent.BERSERKER, num_games=total_games, step=100, verbose=False)
    print(f"Player win rate: {player_win_count / total_games:.2f}")

if __name__ == "__main__":
    test()
