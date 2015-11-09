import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
 
class App(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui() 
 
    def init_ui(self):
        self.parent.title('Jusa - Stock Analyzer')

        self.init_filter_settings_ui(self)
        self.tabs.grid(row = 0, column = 0)
        self.parent.grid_columnconfigure(0, weight=1)


    def init_filter_settings_ui(self, parent):
        self.fs = tkinter.LabelFrame(self.parent, text='Filter Settings', \
            font = 'purisa 10', padx = 10, pady = 10) # fs for 'filter settings'
        self.fs.grid(row = 0, column = 0)

        # tab for 'stocks'
        self.tabs = ttk.Notebook(self.fs)
        f0 = ttk.Frame(self.tabs, padding = 10)
        f0.img = Image.open("res/target.png")
        f0.pimg = ImageTk.PhotoImage(f0.img)
        self.fs.stocks = f0
        self.init_single_or_specified_ui(f0, 'All', 'e.g. 1234,2345,3456')

        # tab for 'date'
        f1 = ttk.Frame(self.tabs, padding = 10);
        f1.img = Image.open("res/date.jpg")
        f1.pimg = ImageTk.PhotoImage(f1.img)
        self.fs.date = f1
        self.init_single_or_specified_ui(f1, 'Today', \
            'e.g. 2015/10/1 or 2015/10/1-2015/11/1')

        # tab for 'filters'
        f2 = ttk.Frame(self.tabs, padding = 10);
        f2.img = Image.open("res/filter.jpg")
        f2.pimg = ImageTk.PhotoImage(f2.img)
        self.fs.filters = f2
        self.init_filters_ui(f2)

        self.tabs.add(f0, image=f0.pimg)
        self.tabs.add(f1, image=f1.pimg)
        self.tabs.add(f2, image=f2.pimg)

        self.fs.grid_columnconfigure(0, pad = 10)

        self.run = tkinter.Button(self.fs, text = 'Run', \
            command = self.run_filters, font = 'purisa 10')
        self.run.grid(row = 0, column = 1, sticky = 'N')

    def run_filters(self):
        if self.fs.stocks.rvar.get() == 'All':
            stocks = 'all'
        else:
            stocks = self.fs.stocks.e1.get()

        if self.fs.date.rvar.get() == 'Today':
            date = 'today'
        else:
            date = self.fs.date.e1.get()

        print('stocks:', stocks)
        print('date:', date)

    def init_single_or_specified_ui(self, parent, single_name, \
            specified_hint):

        def select():
            s = rvar.get()
            if s == 'Specified':
                e1.configure(state = 'normal')
                e1.select_range(0, tkinter.END)
                e1.focus()
            else:
                e1.configure(state = 'disabled')

        # init radio buttons for 'all' and 'specified'
        rvar = tkinter.StringVar()
        r0 = tkinter.Radiobutton(parent, font='purisa 10', \
                variable = rvar, command = select, \
                value = single_name, text = single_name)
        r0.select()
        r1 = tkinter.Radiobutton(parent, font='purisa 10', \
                variable = rvar, command = select, \
                value = u'Specified', text = u'Specified')
        r0.grid(row = 0, column = 0, sticky = 'W')
        r1.grid(row = 1, column = 0, sticky = 'W')
        parent.grid_columnconfigure(0, pad = 10)

        # init entry for 'specified'
        evar = tkinter.StringVar()
        evar.set(specified_hint)
        e1 = tkinter.Entry(parent, state = tkinter.DISABLED, \
                textvariable = evar, width = 50, font = 'purisa 10')
        e1.grid(row = 1, column = 1)
        parent.e1 = e1
        parent.rvar = rvar

    def init_filters_ui(self, parent):

        def configure_interior(event):
            c.configure(scrollregion = c.bbox("all"))

        sb = tkinter.Scrollbar(parent, orient = "vertical")
        # sticky is used to expand scrollbar vertically
        sb.grid(row = 0, column = 1, sticky = 'ns') 

        c = tkinter.Canvas(parent, yscrollcommand = sb.set)
        c.grid(row = 0, column = 0)
        parent.grid_columnconfigure(0, weight=1)
        sb.config(command = c.yview)

        interior = tkinter.Frame(c)
        # anchor can reset scrollbar to top
        c.create_window(0, 0, window = interior, anchor = 'nw')
        interior.bind("<Configure>", configure_interior)


        filters = [
            ['c', '創', 'e', '日新高'], 
            ['c', '最近', 'e', '年, 毛利率不曾低於', 'e', '%'], 
            ['c', '毛利率連續', 'e', '年遞增'], 
            ['c', '毛利率創歷史新高'], 
            ['c', '連續', 'e', '年發放現金股利'], 
            ]
        i = 0
        for cond in filters:
            f = tkinter.Frame(interior)
            f.grid(sticky = 'w')
            col= 0
            for widget in cond:
                if widget == 'c':
                    cb = tkinter.Checkbutton(f)
                    cb.grid(row = 0, column = col)
                elif widget == 'e':
                    e = tkinter.Entry(f, width = 3)
                    e.grid(row = 0, column = col)
                else:
                    l = tkinter.Label(f, text = widget, font = 'purisa 10')
                    l.grid(row = 0, column = col)
                col += 1




APP_WIDTH = 700
APP_HEIGHT = 700
def main():
    root = tkinter.Tk()
    x = (root.winfo_screenwidth() - APP_WIDTH) // 2
    y = (root.winfo_screenheight() - APP_HEIGHT) // 2
    root.geometry('%dx%d+%d+%d' % (APP_WIDTH, APP_HEIGHT, x, y))
    app = App(root)
    app.mainloop()



if __name__ == '__main__':
    main()

