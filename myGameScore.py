# high score manager

def load_high_score():
    try:
        with open("C:\\Users\\Jake\\myGameHighScore.txt", "r") as file:
            high_score_data = file.read().split(",")
            score = int(high_score_data[0])
            enemies_avoided = int(high_score_data[1])
            timer = float(high_score_data[2])
    except FileNotFoundError:
        with open("C:\\Users\\Jake\\myGameHighScore.txt", "w") as file:
            file.write("0,0,0")
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
    with open("C:\\Users\\Jake\\myGameHighScore.txt", "w") as file:
        file.write(f"{high_score},{high_enemies_avoided},{high_timer}")

