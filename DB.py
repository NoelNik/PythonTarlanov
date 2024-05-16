import sqlite3
import datetime
from random import randint

con = sqlite3.connect("baza.db", check_same_thread=False)
cur = con.cursor()


def newUser(telegramID, username):
    if not cur.execute(f"""SELECT TelegramID FROM interns WHERE TelegramID = '{telegramID}'""").fetchone():
        cur.execute(f"""INSERT INTO interns (comingData, TelegramID, username) VALUES 
            ('{datetime.date.today()}', '{telegramID}', '{username}')""")
        con.commit()


def newAdmin(telegramID):
    if not cur.execute(f"""SELECT TelegramID FROM Admins WHERE TelegramID = '{telegramID}'""").fetchone():
        cur.execute(f"""INSERT INTO Admins (Name, TelegramID) VALUES 
            ('{telegramID}', '{telegramID}')""")
        con.commit()


def deleteUser(telegramID):
    cur.execute(f"""DELETE FROM interns WHERE TelegramID = '{telegramID}'""")
    con.commit()


def getExp(telegramID):
    return cur.execute(f"""SELECT exp FROM interns WHERE TelegramID = '{telegramID}'""").fetchone()[0]


def check_for_win(telegramID):
    stage = cur.execute(f"""SELECT stage FROM interns WHERE TelegramID = '{telegramID}'""").fetchone()[0]
    # список может дополняться
    prize_list = {"first": ["стикер", "ручку"], "second": ["худи", "мышку"], "third": ["яхту", "машину"]}
    quantity_for_first = 15
    quantity_for_second = 30
    quantity_for_third = 45
    if (getExp(telegramID) > quantity_for_first) and (stage == 0):
        cur.execute(f"""UPDATE interns set stage = '{stage + 1}' WHERE TelegramID = '{telegramID}'""")
        ind = randint(0, len(prize_list["first"]) - 1)
        prize = prize_list["first"][ind]
        prize_list["first"].pop(ind)
        return f"Вы выйграли {prize}"

    elif getExp(telegramID) > quantity_for_second and (stage == 1):
        cur.execute(f"""UPDATE interns set stage = '{stage + 1}' WHERE TelegramID = '{telegramID}'""")
        ind = randint(0, len(prize_list["second"]) - 1)
        prize = prize_list["second"][ind]
        prize_list["second"].pop(ind)
        return f"Вы выйграли {prize}"

    elif getExp(telegramID) > quantity_for_third and (stage == 2):
        cur.execute(f"""UPDATE interns set stage = '{stage + 1}' WHERE TelegramID = '{telegramID}'""")
        ind = randint(0, len(prize_list["third"]) - 1)
        prize = prize_list["third"][ind]
        prize_list["third"].pop(ind)
        return f"Вы выйграли {prize}"

    else:
        exp = getExp(telegramID)
        if exp < quantity_for_first:
            return f"У вас нет призов. Кол-во баллов до следующей награды: {quantity_for_first - exp}"
        elif exp < quantity_for_second:
            return f"У вас нет призов. Кол-во баллов до следующей награды: {quantity_for_second - exp}"
        elif exp < quantity_for_third:
            return f"У вас нет призов. Кол-во баллов до следующей награды: {quantity_for_third - exp}"

    con.commit()


def get_info_of_workers():
    return cur.execute(f"""SELECT * FROM interns""")


def getCurrentDate():
    return datetime.datetime.now().date()


def check_for_data(telegramID):
    data = datetime.datetime.strptime(getData(telegramID), "%Y-%m-%d")
    current_date = datetime.datetime.today()
    # 180 – это кол-во дней в полугоде
    dif = 180 - (current_date - data).days
    return dif


def check_for_notifications(telegramID):
    dif = check_for_data(telegramID)
    if dif >= 7:
        cur.execute(f"""UPDATE interns set readyToMeeteng = '{1}' WHERE TelegramID = '{telegramID}'""")
    elif dif >= 14:
        cur.execute(f"""UPDATE interns set readyToMeeteng = '{1}' WHERE TelegramID = '{telegramID}'""")
    con.commit()


def getData(telegramID):
    data = cur.execute(f"""SELECT comingData FROM interns WHERE TelegramID = '{telegramID}'""").fetchone()
    if data:
        return data[0]


def if_user_exist(telegramID):
    return bool(cur.execute(f"""SELECT TelegramID FROM interns WHERE TelegramID = '{telegramID}'""").fetchone())


def if_user_admin(telegramID):
    admin_list = [x[0] for x in cur.execute(f"""SELECT TelegramID FROM admins""").fetchall()]
    return str(telegramID) in admin_list


def getAdminList():
    return [x[0] for x in cur.execute(f"""SELECT TelegramID FROM admins""").fetchall()]


def appendQueue(telegramID):
    cur.execute(f"""INSERT INTO queue (TelegramID) VALUES ('{telegramID}')""")
    con.commit()


def appendChatActive(intern, Admin):
    cur.execute(f"""INSERT INTO activeChat (idIntern, idAdmin) VALUES ('{intern}', '{Admin}')""")
    con.commit()


def deleteChatActive(TelegramID):
    cur.execute(f"""DELETE FROM activeChat WHERE idIntern = {TelegramID} OR idAdmin = {TelegramID}""")
    con.commit()


def isChatActive(TelegramID):
    data = cur.execute(f"""SELECT idIntern, idAdmin FROM activeChat""").fetchall()
    for s in data:
        if s[0] == str(TelegramID) or s[1] == str(TelegramID):
            return True
    return False


def getIDinterlocutor(telegramID):
    chat = cur.execute(
        f"""SELECT idIntern, idAdmin FROM activeCHAT WHERE idIntern = '{telegramID}' or idAdmin ='{telegramID}'""").fetchone()
    if chat:
        if str(telegramID) == chat[0]:
            return int(chat[1])
        else:
            return int(chat[0])
    return telegramID


def deleteQueue(telegramID):
    cur.execute(f"""DELETE FROM queue WHERE TelegramID = '{telegramID}'""")
    con.commit()


def getQueue():
    return cur.execute(f"""SELECT TelegramID FROM queue""").fetchall()


def getTasks(telegramID):
    return cur.execute(f"""SELECT * FROM tasks WHERE id = {telegramID}""").fetchall()


def addTask(telegramID, newTask):
    cur.execute(f"""UPDATE interns set task = '{newTask}' WHERE TelegramID = '{telegramID}'""")
    con.commit()
    return "Задание обновлено"

def addPoints(telegramID, quantity):
    cur.execute(f"""UPDATE interns set exp = '{getExp(telegramID) + quantity}' WHERE TelegramID = '{telegramID}'""")
