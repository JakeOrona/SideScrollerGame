import json

def load_high_score():
    try:
        with open("C:\\Users\\Jake\\sideScrollerGame\\gameData\\myGameHighScore.json", "r") as file:
            high_score_data = json.load(file)
            score = int(high_score_data["score"])
            enemies_avoided = int(high_score_data["enemies_avoided"])
            timer = float(high_score_data["timer"])
    except FileNotFoundError:
        high_score_data = {"score": 0, "enemies_avoided": 0, "timer": 0}
        with open("C:\\Users\\Jake\\sideScrollerGame\\gameData\\myGameHighScore.json", "w") as file:
            json.dump(high_score_data, file)
        score = 0
        enemies_avoided = 0
        timer = 0
    return score, enemies_avoided, timer

def save_high_score(score, enemies_avoided, timer):
    high_score, high_enemies_avoided, high_timer = load_high_score()
    if score > high_score:
        high_score = score
    if enemies_avoided > high_enemies_avoided:
        high_enemies_avoided = enemies_avoided
    if timer > high_timer:
        high_timer = timer
    high_score_data = {"score": high_score, "enemies_avoided": high_enemies_avoided, "timer": int(high_timer)}
    with open("C:\\Users\\Jake\\sideScrollerGame\\gameData\\myGameHighScore.json", "w") as file:
        json.dump(high_score_data, file)