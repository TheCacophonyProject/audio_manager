import tkinter as tk
from PIL import ImageTk,Image 

# https://books.google.co.nz/books?id=45lUDwAAQBAJ&pg=PA53&lpg=PA53&dq=yscrollcommand%3Dself.scroll_y.set&source=bl&ots=eXh5yGEdPg&sig=ACfU3U28iVZVP65ly0Q2AXBnIyYQLGkDyg&hl=en&sa=X&ved=2ahUKEwiim_H1oeToAhWhyDgGHTToC9oQ6AEwAHoECAsQKQ#v=onepage&q=yscrollcommand%3Dself.scroll_y.set&f=false

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
#         self.scroll_x = tk.Scrollbar(self, orient=tk.HORIZONTAL)
#         self.scroll_y = tk.Scrollbar(self, orient=tk.VERTICAL)
#         
#         self.canvas = tk.Canvas(self, width=300, height=100, xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)    
#         
#         self.scroll_x.config(command=self.canvas.xview())
#         self.scroll_y.config(command=self.canvas.yview())
#         
#         self.frame = tk.Frame(self.canvas)
#         self.btn = tk.Button(self.frame, text="Load image", command=self.load_image)
#         self.btn.pack()     
#         
#               
#         self.canvas.create_window((0,0), window=self.frame, anchor=tk.NW)
#         
#         self.canvas.grid(row=0, column=0, sticky="nswe")
#         self.scroll_x.grid(row=1, column=0, sticky="we")
#         self.scroll_y.grid(row=0, column=1, sticky="ns")
#         
#         self.rowconfigure(0, weight=1)
#         self.columnconfigure(0, weight=1)
#         self.bind("<Configure>", self.resize)
#         self.update_idletasks()
#         self.minsize(self.winfo_width(),self.winfo_height())



        self.setup_image_canvas()
        self.btn = tk.Button(self.frame, text="Load image", command=self.load_image)
        self.btn.grid(row=0, column=2, sticky="nswe")
        
    def setup_image_canvas(self):
        
        self.scroll_x = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.scroll_y = tk.Scrollbar(self, orient=tk.VERTICAL)
        
        self.canvas = tk.Canvas(self, width=300, height=100, xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)    
        
        self.scroll_x.config(command=self.canvas.xview())
        self.scroll_y.config(command=self.canvas.yview())
        
        self.frame = tk.Frame(self.canvas)
#         self.btn = tk.Button(self.frame, text="Load image", command=self.load_image)
#         self.btn.pack()     
        
              
        self.canvas.create_window((0,0), window=self.frame, anchor=tk.NW)
        
        self.canvas.grid(row=0, column=0, sticky="nswe")
        self.scroll_x.grid(row=1, column=0, sticky="we")
        self.scroll_y.grid(row=0, column=1, sticky="ns")
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.bind("<Configure>", self.resize)
        self.update_idletasks()
        self.minsize(self.winfo_width(),self.winfo_height())
        
    def resize(self, event):
        region = self.canvas.bbox(tk.ALL)
        self.canvas.configure(scrollregion=region)
        
    def load_image(self):
        self.btn.destroy()
        image = Image.open("temp_waveform.jpg")
        self.spectrogram_image = ImageTk.PhotoImage(image)
#         self.image = tk.PhotoImage()
        tk.Label(self.frame, image=self.spectrogram_image).pack()
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
        