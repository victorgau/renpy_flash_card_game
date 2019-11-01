##### The game screen
screen flash_card_screen:  
    ##### Timer
    # timer 使用法參考：https://www.renpy.cn/doc-tw/screens.html 裡面的 timer 語句
    # If 跟 SetVariable 語句的參考連結在：https://www.renpy.cn/doc/screen_actions.html
    timer 1.0 action If (memo_timer > 1, SetVariable("memo_timer", memo_timer - 1), Jump("game_lose") ) repeat True
    
    # 在螢幕上方，顯示剩餘的時間
    text "剩餘時間：" + str(memo_timer) xalign 0.5 yalign 0.02
    
    ##### Cards
    grid 4 3:
        xalign 0.5 yalign 0.5
        for card in cards_list:
            button:
                background None

                if card["c_chosen"]:       # 
                    add card["c_value"]    # 顯示對應值的圖形
                else:                      # 
                    add "G"                # 顯示 image G (定義在下面)

                # action 有點像是 event handler
                # SetDict 的參考連結：https://www.renpy.cn/doc/screen_actions.html
                action If ( (card["c_chosen"] or not can_click), None, [SetDict(cards_list[card["c_number"]], "c_chosen", True), Return(card["c_number"]) ] )
 

init:
    python:
        # 洗牌用的函式
        def cards_shuffle(x):
            renpy.random.shuffle(x)
            return x

    # 設定遊戲的圖形
    image A = "1.png"
    image B = "2.png"
    image C = "3.png"          
    image D = "4.png"
    image E = "5.png" 
    image F = "6.png"
    image G = "9.png"


# 遊戲的進入點
label flash_card_game (game_time=50.0):
    #####
    #
    # 設定牌面的值
    $ values_list = ["A", "A", "B", "B", "C", "C", "D",  "D", "E", "E", "F", "F"]
    
    # 洗牌
    $ values_list = cards_shuffle(values_list)
    
    # cards_list 用來記錄第幾張牌的內容是甚麼
    $ cards_list = []
    python:
        for i in range (0, len(values_list) ):
            cards_list.append ( {"c_number":i, "c_value": values_list[i], "c_chosen":False} )   

    # 設定遊戲時間
    $ memo_timer = game_time
    
    # 顯示遊戲畫面
    # 所有的圖形在這裡會重畫
    show screen flash_card_screen
    
    # 遊戲的主迴圈
    label game_loop:
        $ can_click = True
        $ turned_cards_numbers = []
        $ turned_cards_values = []
        
        # 每一輪可以翻幾張牌 (全部要一樣才可以消掉喔！)
        $ turns_left = 2
        
        # 翻牌的迴圈
        label turns_loop:
            if turns_left > 0:
                $ result = ui.interact() # ui.interact() 的使用參考 https://www.renpy.cn/doc-tw/screen_python.html
                $ memo_timer = memo_timer
                $ turned_cards_numbers.append (cards_list[result]["c_number"])
                $ turned_cards_values.append (cards_list[result]["c_value"])
                $ turns_left -= 1
                jump turns_loop
        
        # 避免處理圖形的過程中，蓋著的牌面又被點擊
        $ can_click = False
        # 如果牌面不 Match，Pause 完之後，牌面會被蓋起來。
        if turned_cards_values.count(turned_cards_values[0]) != len(turned_cards_values):
            $ renpy.pause (0.5, hard = True)
            python:
                for i in range (0, len(turned_cards_numbers) ):
                    cards_list[turned_cards_numbers[i]]["c_chosen"] = False
        # 如果牌面是一樣的，最後要檢查是不是所有的牌都 match 了。
        else:
            $ renpy.pause (0.5, hard = True)
            python: 
                # 把一樣的牌移除掉
                # 如果沒有要移除掉，把下面兩行 comment out 掉
                for i in range (0, len(turned_cards_numbers) ):
                    cards_list[turned_cards_numbers[i]]["c_value"] = Null()

                # 如果有任一張牌還沒有被選，就跳回去 game_loop
                # 如果全部都被選了，就跳到 game_win
                for j in cards_list:
                    if j["c_chosen"] == False:
                        renpy.jump ("game_loop")
                renpy.jump ("game_win")
                
        jump game_loop


# 遊戲輸掉，跳來這裡處理
label game_lose:
    hide screen flash_card_screen
    show eileen concerned
    e "哇！輸掉了！"
    $ renpy.pause (0.1, hard = True)
    $ renpy.pause (1.0, hard = True)
    return (0)

# 遊戲贏了，跳來這裡處理
label game_win:
    hide screen flash_card_screen
    show eileen vhappy
    $ renpy.pause (0.1, hard = True)
    $ renpy.pause (0.1, hard = True)
    e "好棒喔！你贏了！"
    return (1)