import tkinter as tk
from tkinter import ttk
import DataCaptureClass

import ClassLeaderBoard


class MagicClassRoomData(tk.Toplevel):

    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.configure(background="gray20")
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('classroom.TLabelframe', background='gray20',borderwidth = 0)
        s.configure('classroom.TLabelframe.Label', font=('helvetica', 14, 'bold'))
        s.configure('classroom.TLabelframe.Label', background='gray20', foreground='snow')

        s.configure('classroom.Label', background='gray22', foreground='snow', font=('arial', 12, 'bold'))
        s.configure('doc.Label', background='gray22', foreground='white', font=('arial', 10, 'bold'))
        s.configure('classroom.TButton', background='steelblue', foreground='white')
        s.map('classroom.TButton', background=[('pressed', 'steelblue'),('active', '!disabled', 'dark turquoise')],
              foreground=[('pressed', 'white'), ('active', 'white')])

        self.thought_frame = ttk.LabelFrame(self,text="Quote/Announcement",style="classroom.TLabelframe")
        self.thought_text_label = ttk.Label(self.thought_frame,text="Add a quote or an Announcement",style="classroom.Label")
        self.thought_text = ttk.Entry(self.thought_frame,width=80)
        self.thought_button = ttk.Button(self.thought_frame, text="Submit", command=lambda: DataCaptureClass.save_thought(self.thought_text.get(),self), style="classroom.TButton")
        self.doc_frame = tk.Frame(self, background="gray20")
        self.doc_label = ttk.Label(self.doc_frame,
                                   text="Add your announcement or a quote which will be displayed at the beginning of all the lessons.\n\n"
                                        "Add participants name in each line to see them on the leaderboard.\n\nRemove individual participants by "
                                        "adding their names.\n\nTo remove all participants click on \"Remove Participants Button\" without "
                                        "filling in any names and confirm full deletion.", wraplength=200,style="doc.Label")

        self.display_thought_panel()

        self.leaderboard_frame = ttk.LabelFrame(self, text="Participating Students", style="classroom.TLabelframe")
        self.leaderboard = ClassLeaderBoard.MagicLeaderBoard(self.leaderboard_frame)
        self.badge_image_medala = tk.PhotoImage(file='../images/medala.png')
        self.badge_image_medalb = tk.PhotoImage(file='../images/medalb.png')
        self.levelone_threshold = ttk.Label(self.leaderboard_frame,text="Minimum points to reach level 1",image=self.badge_image_medala, style="classroom.Label")
        self.leveltwo_threshold = ttk.Label(self.leaderboard_frame, text="Minimum points to reach level 2",image=self.badge_image_medalb, style="classroom.Label")
        self.min_lev1_var = tk.IntVar()
        self.min_lev2_var = tk.IntVar()
        a_threshold, b_threshold = DataCaptureClass.get_threshold_values()
        self.min_lev1_var.set(a_threshold)
        self.min_lev2_var.set(b_threshold)
        self.levelonespinner = ttk.Spinbox(self.leaderboard_frame, background='gray20', foreground='royalblue4',
                                            font=('helvetica', 12),
                                            from_=0, to=100, textvariable = self.min_lev1_var, wrap=True,
                                            width=2)
        self.leveltwospinner = ttk.Spinbox(self.leaderboard_frame, background='gray20', foreground='royalblue4',
                                           font=('helvetica', 12),
                                           from_=0, to=100, textvariable=self.min_lev2_var, wrap=True,
                                           width=2)
        self.points_button = ttk.Button(self.leaderboard_frame, text="Set Points", command=lambda: DataCaptureClass.set_points(self.min_lev1_var.get(),self.min_lev2_var.get(),self),
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
        DataCaptureClass.add_participants(participant_text,self)
        self.add_delete_text.delete(1.0,tk.END)
        self.leaderboard_frame.grid_forget()
        self.leaderboard.destroy()
        self.leaderboard = ClassLeaderBoard.MagicLeaderBoard(self.leaderboard_frame)
        self.display_student_panel()
    def remove_participants(self,participant_text):
        DataCaptureClass.remove_participants(participant_text,self)
        self.leaderboard_frame.grid_forget()
        self.leaderboard.destroy()
        self.leaderboard = ClassLeaderBoard.MagicLeaderBoard(self.leaderboard_frame)
        self.display_student_panel()

    def display_thought_panel(self):
        #self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.thought_frame.grid(row=0,column=0,pady=15)
        self.thought_text_label.grid(row = 0, column = 0, padx = 10)
        self.thought_text.grid(row = 0, column = 1, padx = 10)
        self.thought_button.grid(row = 0, column = 2, padx = 10)
        self.doc_label.grid(row=0,column=0)
        self.doc_frame.grid(row=0,column=4,padx=10,rowspan = 8)

    def display_student_panel(self):
        self.leaderboard_frame.rowconfigure(0,weight=1)
        self.leaderboard_frame.columnconfigure(0,weight=1)
        self.levelone_threshold.grid(row=0,column=0,padx=30,pady=10)
        self.levelonespinner.grid(row=0, column=2, padx=30,pady=10)
        self.leveltwo_threshold.grid(row=0,column=3,padx=30,pady=10)
        self.leveltwospinner.grid(row=0, column=4, padx=30,pady=10)
        self.points_button.grid(row=0, column=5, padx=10,pady=10)


        self.leaderboard.grid(row=1,column=0,columnspan=3,rowspan=3,pady=15)
        self.add_delete_label.grid(row=1,column=3)
        self.add_delete_text.grid(row=1,column=4)
        self.add_button.grid(row=2,column=4,pady=10)
        self.remove_button.grid(row=2,column=5,pady=10)
        self.leaderboard_frame.grid(row=1,column=0,pady=20)





#
# if __name__ == "__main__":
#     classroom_app = tk.Tk()
#     classroom_app.title("Classroom Data")
#     classroom_app.geometry("1000x700")
#     frame = MagicClassRoomData(classroom_app)
#     frame.configure(background='gray20')
#     classroom_app.columnconfigure(0,weight=1)
#     classroom_app.configure(background='gray20')
#     frame.grid(row=0,column=0)
#     classroom_app.mainloop()