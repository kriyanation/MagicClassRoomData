import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import configparser

import FlashLeaderBoard, DataCapture

config = configparser.RawConfigParser()
two_up = Path(__file__).absolute().parents[2]
print(str(two_up) + '/magic.cfg')

class MagicClassRoomData(tk.Frame):

    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('classroom.TLabelframe', background='beige',borderwidth = 0)
        s.configure('classroom.TLabelframe.Label', font=('courier', 14, 'bold', 'italic'))
        s.configure('classroom.TLabelframe.Label', background='beige', foreground='brown')

        s.configure('classroom.Label', background='beige', foreground='firebrick', font=('arial', 12, 'bold'))
        s.configure('classroom.TButton', background='firebrick', foreground='snow')
        s.map('classroom.TButton', background=[('pressed', 'snow'),('active', '!disabled', 'maroon')],
              foreground=[('pressed', 'firebrick'), ('active', 'snow')])
        try:
            config.read(str(two_up) + '/magic.cfg')
            self.db = config.get("section1", "file_root") + os.path.sep + "MagicRoom.db"
        except configparser.NoSectionError():
            messagebox.showerror("Read Error", "Could not read the config file or the configuration script is incorrect")
            sys.exit()
        self.thought_frame = ttk.LabelFrame(self,text="Quote/Announcement",style="classroom.TLabelframe")
        self.thought_text_label = ttk.Label(self.thought_frame,text="Add a quote or an Announcement",style="classroom.Label")
        self.thought_text = ttk.Entry(self.thought_frame,width=80)
        self.thought_button = ttk.Button(self.thought_frame, text="Submit", command=lambda: DataCapture.save_thought(self.thought_text.get()), style="classroom.TButton")
        self.display_thought_panel()

        self.leaderboard_frame = ttk.LabelFrame(self, text="Participating Students", style="classroom.TLabelframe")
        self.leaderboard = FlashLeaderBoard.MagicLeaderBoard(self.leaderboard_frame)
        self.badge_image_medala = tk.PhotoImage(file='../images/medala.png')
        self.badge_image_medalb = tk.PhotoImage(file='../images/medalb.png')
        self.levelone_threshold = ttk.Label(self.leaderboard_frame,text="Minimum points to reach level 1",image=self.badge_image_medala, style="classroom.Label")
        self.leveltwo_threshold = ttk.Label(self.leaderboard_frame, text="Minimum points to reach level 2",image=self.badge_image_medalb, style="classroom.Label")
        self.min_lev1_var = tk.IntVar()
        self.min_lev2_var = tk.IntVar()
        a_threshold, b_threshold = DataCapture.get_threshold_values()
        self.min_lev1_var.set(a_threshold)
        self.min_lev2_var.set(b_threshold)
        self.levelonespinner = ttk.Spinbox(self.leaderboard_frame, background='beige', foreground='brown',
                                            font=('TkDefaultFont', 12),
                                            from_=0, to=100, textvariable = self.min_lev1_var, wrap=True,
                                            width=2)
        self.leveltwospinner = ttk.Spinbox(self.leaderboard_frame, background='beige', foreground='brown',
                                           font=('TkDefaultFont', 12),
                                           from_=0, to=100, textvariable=self.min_lev2_var, wrap=True,
                                           width=2)
        self.points_button = ttk.Button(self.leaderboard_frame, text="Set Points", command=lambda: DataCapture.set_points(self.min_lev1_var.get(),self.min_lev2_var.get()),
                                         style="classroom.TButton")

        self.add_delete_label = ttk.Label(self.leaderboard_frame, text="Enter Participants",
                                             style="classroom.Label")
        self.add_delete_text = tk.Text(self.leaderboard_frame,width = 20, height=20)
        self.add_button = ttk.Button(self.leaderboard_frame, text="Add Participants", command=lambda: self.add_participants(self.add_delete_text.get("1.0",tk.END)),
                                         style="classroom.TButton")
        self.remove_button = ttk.Button(self.leaderboard_frame, text="Remove Participants", command=lambda: self.remove_participants(self.add_delete_text.get("1.0",tk.END)),
                                         style="classroom.TButton")

        self.display_student_panel()

    def add_participants(self,participant_text):
        DataCapture.add_participants(participant_text)
        self.leaderboard_frame.grid_forget()
        self.leaderboard.destroy()
        self.leaderboard = FlashLeaderBoard.MagicLeaderBoard(self.leaderboard_frame)
        self.display_student_panel()
    def remove_participants(self,participant_text):
        DataCapture.remove_participants(participant_text)
        self.leaderboard_frame.grid_forget()
        self.leaderboard.destroy()
        self.leaderboard = FlashLeaderBoard.MagicLeaderBoard(self.leaderboard_frame)
        self.display_student_panel()

    def display_thought_panel(self):
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.thought_frame.grid(row=0,column=0,pady=40)
        self.thought_text_label.grid(row = 0, column = 0, padx = 10)
        self.thought_text.grid(row = 0, column = 1, padx = 10)
        self.thought_button.grid(row = 0, column = 2, padx = 10)

    def display_student_panel(self):
        self.leaderboard_frame.rowconfigure(0,weight=1)
        self.leaderboard_frame.columnconfigure(0,weight=1)
        self.levelone_threshold.grid(row=0,column=0,padx=30)
        self.levelonespinner.grid(row=0, column=2, padx=30)
        self.leveltwo_threshold.grid(row=0,column=3,padx=30)
        self.leveltwospinner.grid(row=0, column=4, padx=30)
        self.points_button.grid(row=0, column=5, padx=10)


        self.leaderboard.grid(row=1,column=0,columnspan=3,rowspan=3)
        self.add_delete_label.grid(row=1,column=3)
        self.add_delete_text.grid(row=1,column=4)
        self.add_button.grid(row=2,column=4)
        self.remove_button.grid(row=2,column=5)
        self.leaderboard_frame.grid(row=1,column=0)





if __name__ == "__main__":
    classroom_app = tk.Tk()
    classroom_app.title("Classroom Data")
    classroom_app.geometry("800x500")
    frame = MagicClassRoomData(classroom_app)
    frame.configure(background='beige')
    classroom_app.columnconfigure(0,weight=1)
    classroom_app.configure(background='beige')
    frame.grid(row=0,column=0)
    classroom_app.mainloop()