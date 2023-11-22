# import tkinter as tk
# from tkVideoPlayer import TkinterVideo
# from tkinter import filedialog
# import datetime

# root = tk.Tk()
# root.title('Video Player')
# root.geometry('800x700+290+10')

# frame = tk.Frame(root)
# frame.pack()

# lower = tk.Frame(root, bg='#FFFFFF')
# lower.pack(fill="both", side='bottom')

# vid = TkinterVideo(root, scaled=True)
# vid.pack(expand=True, fill='both')

# def update(event):
#     duration = vid.video_info()["duration"]
#     end_time["text"] = str(datetime.timedelta(seconds=duration))
#     progress_slider["to"] = duration

# def update_sc(event):
#     progress_value.set(vid.current_duration())

# def video():
#     path = filedialog.askopenfilename()
#     if path:
#         vid.load(path)
#         progress_slider.config(to=0, from_=0)
#         play_btn['text'] = "Play"
#         progress_value.set(0)

# def seek(value):
#     vid.seek(int(value))

# def skip(value):
#     vid.seek(int(progress_slider.get()) + value)
#     progress_value.set(progress_slider.get() + value)

# def play_pause():
#     if vid.is_paused():
#         vid.play()
#         play_btn['text'] = "Pause"
#     else:
#         vid.pause()
#         play_btn['text'] = "Play"

# def video_end(event):
#     progress_slider.set(progress_slider['to'])
#     play_btn['text'] = 'Play'
#     progress_slider.set(0)

# start_time = tk.Label(root, text=str(datetime.timedelta(seconds=0)))
# start_time.pack(side='left')

# progress_value = tk.IntVar(root)

# progress_slider = tk.Scale(root, variable=progress_value, from_=0, to=0, orient="horizontal", command=seek)
# progress_slider.pack(side='left', fill='x', expand=True)

# end_time = tk.Label(root, text=str(datetime.timedelta(seconds=0)))
# end_time.pack(side="left")

# btn = tk.Button(root, text='Search', bg='#FFFFFF', font=('calibri', 12, 'bold'), command=video)
# btn.pack(ipadx=12, ipady=4, anchor=tk.NW)

# back = tk.PhotoImage(file="back.png")
# back_btn = tk.Button(lower, image=back, bd=0, height=50, width=50, command=lambda: skip(-5)).pack(side='left')
# play_btn = tk.Button(lower, text="Play", width=40, height=2, command=play_pause)
# play_btn.pack(expand=True, fill="both", side='left')
# front = tk.PhotoImage(file='back.png')
# front_btn = tk.Button(lower, image=front, bd=0, height=50, width=50, command=lambda: skip(5)).pack(side='left')
# image = tk.PhotoImage(file="icon.png")
# root.iconphoto(False, image)

# vid.bind("<<Duration>>", update)
# vid.bind("<<SecondChanged>>", update_sc)
# vid.bind("<<End>>", video_end)

# root.mainloop()
# # import tkinter as tk
# # from tkinter import filedialog  # Add this import for filedialog
# # import platform
# # import vlc

# # class VideoPlayer(tk.Label):
# #     def __init__(self, app, frame: tk.LabelFrame):
# #         super().__init__()
# #         self.master = frame
# #         # Create a bpip asic vlc instance
# #         self.instance = vlc.Instance()
# #         self.media = None
# #         # Create an empty vlc media player
# #         self.mediaplayer = self.instance.media_player_new()

# #     def open_file(self):
# #         """Open a media file in a MediaPlayer
# #         """
# #         file_name = filedialog.askopenfilename(title="Please choose a video file.")
# #         if file_name:
# #             self.media = self.instance.media_new(file_name)
# #             self.mediaplayer.set_media(self.media)

# #             # The media player has to be 'connected' to the Frame (otherwise the
# #             # video would be displayed in its own window). This is platform
# #             # specific, so we must give the ID of the Frame (or similar object) to
# #             # vlc. Different platforms have different functions for this
# #             if platform.system() == "Linux":  # for Linux using the X Server
# #                 self.mediaplayer.set_xwindow(int(self.master.winfo_id()))
# #             elif platform.system() == "Windows":  # for Windows
# #                 self.mediaplayer.set_hwnd(int(self.master.winfo_id()))
# #             elif platform.system() == "Darwin":  # for MacOS
# #                 self.mediaplayer.set_nsobject(int(self.master.winfo_id()))

# #             self.media.parse()
# #             self.mediaplayer.play()

# # # Example of how to use the VideoPlayer class:
# # root = tk.Tk()
# # frame = tk.LabelFrame(root)
# # frame.pack()

# # video_player = VideoPlayer(root, frame)
# # video_player.open_fil()

# # root.mainloop()
