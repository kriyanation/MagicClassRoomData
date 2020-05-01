
import sqlite3
from pathlib import Path
import configparser, os
from tkinter import StringVar,messagebox
import traceback

TEST_ROW = 16

config = configparser.RawConfigParser()
two_up = Path(__file__).absolute().parents[2]
print(str(two_up)+'/magic.cfg')
config.read(str(two_up)+'/magic.cfg')
file_root = config.get("section1",'file_root')
db = file_root+os.path.sep+"MagicRoom.db"


def save_thought(self):
    try:
        connection = sqlite3.connect(self.db)
        cur = connection.cursor()
        sql = "update Magic_Quotes set Quote = ? where Theme_ID = 1"
        cur.execute(sql, (self.thought_text.get(),))
        connection.commit()

    except (sqlite3.OperationalError):
        traceback.print_exc()
        messagebox.showerror("Error Connecting to DB", "Saving the Information met with an error")

    else:
        messagebox.showinfo("Text Saved",
                            "All your sessions will play the text in the first screen of the Player")

def class_info():
    list_names = []
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "select * from Magic_Class_Info"
    cur.execute(sql)
    rows = cur.fetchall()
    for element in rows:
        list_names.append(element)

    connection.commit()
    connection.close()
    return list_names



def save_leader_board_data(list_points):
    connection = sqlite3.connect(db)
    cur = connection.cursor()

    for element in list_points:
        sql = "select Badge_A_Threshold, Badge_B_Threshold, Badge_C_Threshold from Magic_Class_Info where Name=?"
        badge_info_c = cur.execute(sql, (element[0],))
        badge_info = badge_info_c.fetchone()
        badge_a = badge_info[0]
        badge_b = badge_info[1]
        badge_c= badge_info[2]
        var = StringVar()
        var = element[1]
        value = var.get()
        badge = ''
        if int(value) > badge_a:
            badge = 'a'
        elif int(value) > badge_b:
            badge ='b'
        elif int(value) > badge_c:
            badge = 'c'
        sql='update Magic_Class_Info set Points = ? , Badge = ? where Name=?'
        print(value,element[0])
        cur.execute(sql,(int(value), badge, element[0]))

    connection.commit()
    connection.close()