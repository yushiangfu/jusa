import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import stockfilter
 
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
        self.fs.stocks_tab = f0
        self.init_single_or_specified_ui(f0, 'All', 'e.g. 1234,2345,3456')

        # tab for 'date'
        f1 = ttk.Frame(self.tabs, padding = 10);
        f1.img = Image.open("res/date.jpg")
        f1.pimg = ImageTk.PhotoImage(f1.img)
        self.fs.date_tab = f1
        self.init_single_or_specified_ui(f1, 'Today', \
            'e.g. 2015/10/1 or 2015/10/1-2015/11/1')

        # tab for 'filters'
        f2 = ttk.Frame(self.tabs, padding = 10);
        f2.img = Image.open("res/filter.jpg")
        f2.pimg = ImageTk.PhotoImage(f2.img)
        self.fs.filters_tab = f2
        f1.pimg = ImageTk.PhotoImage(f1.img)
        self.init_filters_ui(f2)

        self.tabs.add(f0, image=f0.pimg)
        self.tabs.add(f1, image=f1.pimg)
        self.tabs.add(f2, image=f2.pimg)

        self.fs.grid_columnconfigure(0, pad = 10)

        self.run = tkinter.Button(self.fs, text = 'Run', \
            command = self.run_filters, font = 'purisa 10')
        self.run.grid(row = 0, column = 1, sticky = 'N')

    def run_filters(self):
        if self.fs.stocks_tab.rvar.get() == 'All':
            stocks = 'all'
        else:
            stocks = self.fs.stocks_tab.e1.get()

        if self.fs.date_tab.rvar.get() == 'Today':
            date = 'today'
        else:
            date = self.fs.date_tab.e1.get()

        #print('stocks:', stocks)
        #print('date:', date)
        i = 0
        for cond in self.fs.filters_tab.filters_param:
            if int(cond[0].get()): # [1] for checkbutton
                ft = self.fs.filters_tab.filters_table[i][0]
                ft_params = [widget.get() for widget in cond[1:]]
                stockfilter.process_filter(ft, stocks, date, ft_params) 
            i += 1
            #for widget in cond:
                #print(widget.get())

        


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


        filters_table = [
            [stockfilter.new_price_in_n_days, 'c', '創', 'e', '日新', 'e'], 
            [None, 'c', '最近', 'e', '年, 毛利率不曾低於', 'e', '%'], 
            [None, 'c', '毛利率連續', 'e', '年遞增'], 
            [None, 'c', '毛利率創歷史新高'], 
            [None, 'c', '連續', 'e', '年發放現金股利'], 
            ]
        i = 0
        parent.filters_table = filters_table
        parent.filters_param = []
        for cond in filters_table:
            f = tkinter.Frame(interior)
            f.grid(sticky = 'w')
            col= 0
            widget_set = []
            for widget in cond[1:]:
                if widget == 'c':
                    var = tkinter.IntVar()
                    cb = tkinter.Checkbutton(f, variable = var)
                    cb.grid(row = 0, column = col)
                    widget_set.append(var)
                elif widget == 'e':
                    var = tkinter.StringVar()
                    e = tkinter.Entry(f, width = 3, textvariable = var)
                    e.grid(row = 0, column = col)
                    widget_set.append(e)
                else:
                    l = tkinter.Label(f, text = widget, font = 'purisa 10')
                    l.grid(row = 0, column = col)
                col += 1
            parent.filters_param.append(widget_set)
            i += 1




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

