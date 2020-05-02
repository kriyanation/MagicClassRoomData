
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


def save_thought(thought_text):
    try:
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        sql = "update Magic_Quotes set Quote = ? where Theme_ID = 1"
        cur.execute(sql, (thought_text,))
        connection.commit()
        connection.close()

    except (sqlite3.OperationalError):
        traceback.print_exc()
        messagebox.showerror("Error Connecting to DB", "Saving the Information met with an error")

    else:
        messagebox.showinfo("Text Saved",
                            "All your sessions will play the text in the first screen of the Player")
def get_threshold_values():
    try:
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        sql = "select * from Magic_Class_Info"
        cur.execute(sql)
        rows = cur.fetchall()
        if not rows:
            return 80, 20
        sql = "select  Badge_A_Threshold, Badge_B_Threshold, Badge_C_Threshold from Magic_Class_Info limit 1"
        cur.execute(sql)
        rows=cur.fetchone()
        connection.commit()
        connection.close()
        return rows[0], rows[1]

    except (sqlite3.OperationalError):
        messagebox.showerror("Database Error","There was an error in saving your data, pleasecheck your logs")


def add_participants(participants_text):
    if participants_text is None or participants_text.rstrip() == "":
        messagebox.showinfo("Participants", "No Participants to add")
        return
    else:
        threshold_a, threshold_b = get_threshold_values()
        try:
            connection = sqlite3.connect(db)
            cur = connection.cursor()
            participant_list = participants_text.splitlines()
            list_index = 0
            while list_index < len(participant_list):
                if (participant_list[list_index].strip() == "") or (participant_list[list_index].rstrip() == ""):
                    break
                sql = "insert into Magic_Class_Info (Name, Badge, Points, Badge_A_Threshold, Badge_B_Threshold, Badge_C_Threshold)" \
                      " values(?, 'c', 0, ?, ?, 0)"
                cur.execute(sql, (participant_list[list_index],threshold_a,threshold_b))
                list_index += 1
            connection.commit()
            connection.close()
        except (sqlite3.OperationalError):
            traceback.print_exc()
            messagebox.showerror("Database Error", "There was an error in saving your data, pleasecheck your logs")
        else:
            messagebox.showinfo("Added Participants", "Specified Participants were added")


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







def set_points(a_threshold, b_threshold):
    try:
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        sql = "update Magic_Class_Info set Badge_A_Threshold = ?, Badge_B_Threshold=?, Badge_C_Threshold=0"
        cur.execute(sql,(a_threshold,b_threshold))
        connection.commit()
        connection.close()
    except (sqlite3.OperationalError):
        messagebox.showerror("Database Error", "There was an error in saving your data, pleasecheck your logs")

    else:
        messagebox.showinfo("Point Limits Saved",
                        "The point limits have been saved")

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


def remove_participants(participants_text):
    if participants_text is None or participants_text.rstrip() == "":
        msg = messagebox.askyesno("Delete Check", "Do you want to delete all the participants?")
        if msg == 'no':
            return
        else:
            try:
                connection = sqlite3.connect(db)
                cur = connection.cursor()
                sql = "delete from Magic_Class_Info"
                cur.execute(sql)
                connection.commit()
                connection.close()
            except (sqlite3.OperationalError):
                messagebox.showerror("Database Error", "There was an error in saving your data, pleasecheck your logs")
    else:
        try:
            connection = sqlite3.connect(db)
            cur = connection.cursor()
            participant_list = participants_text.splitlines()
            list_index = 0
            while list_index < len(participant_list):
                if (participant_list[list_index].strip() == "") or (participant_list[list_index].rstrip() == ""):
                    break
                sql = "delete from Magic_Class_Info where Name = ?"
                cur.execute(sql, (participant_list[list_index].strip(),))
                list_index += 1
            connection.commit()
            connection.close()
        except (sqlite3.OperationalError):
            traceback.print_exc()
            messagebox.showerror("Database Error", "There was an error in saving your data, please check your logs")
        else:
            messagebox.showinfo("Participants Removed", "Specified Participants were removed")