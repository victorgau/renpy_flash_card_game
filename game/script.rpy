# 您可以在此編寫遊戲的腳本。

# image命令可用於定義一個圖像。
# eg. image eileen happy = "eileen_happy.png"

# define命令可定義遊戲中出現的角色名稱與對應文本顏色。
define e = Character('Eileen', color="#c8ffc8")


# 遊戲從這裡開始。
label start:
    play music "Darktown_Strutters_Ball.mp3"
    show eileen happy
    e "準備好要挑戰了嗎？"
    hide eileen

    label new_game:
        
        menu:
            "請選擇一個難度喔？"

            "入門":            
                window hide
                call flash_card_game pass (game_time=50.0)

            "中級":
                window hide
                call flash_card_game pass (game_time=30.0)

            "超難":
                window hide
                call flash_card_game pass (game_time=15.0)

    
    show eileen happy
    if _return:
        e "好不好玩？要不要再玩一次？"
    else:
        e "沒關係啦！要不要再玩一次？"
    hide eileen
    
    menu:
        "要":
            jump new_game
        "不要":
            show eileen happy
            e "好吧！歡迎下次再來玩喔！Bye-bye！"

    return
