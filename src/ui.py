"""
ui layout
bypass parameters to filter
"""
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import stockfilter

class App(tkinter.Frame):
    """
    ui implementation
    """
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.filesetting = None
        self.run = None
        self.tabs = None
        self.filters_table = None
        self.filters_params = None
        self.init_ui()

    def init_ui(self):
        """
        init each sub ui
        """
        self.parent.title('Jusa - Stock Analyzer')

        self.init_filter_settings_ui()
        self.tabs.grid(row=0, column=0)
        self.parent.grid_columnconfigure(0, weight=1)

    def init_filters_ui(self, parent):
        """
        according filters_table to init widgets of each filter
        """
        def configure_interior(event):
            """
            callback for scrollbar
            """
            _ = event
            cnvs.configure(scrollregion=cnvs.bbox("all"))

        tmp = tkinter.Scrollbar(parent, orient="vertical")
        # sticky is used to expand scrollbar vertically
        tmp.grid(row=0, column=1, sticky='ns')

        cnvs = tkinter.Canvas(parent, yscrollcommand=tmp.set)
        cnvs.grid(row=0, column=0)
        parent.grid_columnconfigure(0, weight=1)
        tmp.config(command=cnvs.yview)

        interior = tkinter.Frame(cnvs)
        # anchor can reset scrollbar to top
        cnvs.create_window(0, 0, window=interior, anchor='nw')
        interior.bind("<Configure>", configure_interior)


        self.filters_table = [
            [stockfilter.new_price_in_n_days, 'c', '創', 'e', '日新', 'e'],
            [None, 'c', '最近', 'e', '年, 毛利率不曾低於', 'e', '%'],
            [None, 'c', '毛利率連續', 'e', '年遞增'],
            [None, 'c', '毛利率創歷史新高'],
            [None, 'c', '連續', 'e', '年發放現金股利'],
            ]
#parent.filters_table = filters_table
        self.filters_params = []
        for cond in self.filters_table:
            frm = tkinter.Frame(interior)
            frm.grid(sticky='w')
            col = 0
            widget_set = []
            for widget in cond[1:]:
                if widget == 'c':
                    var = tkinter.IntVar()
                    tmp = tkinter.Checkbutton(frm, variable=var)
                    tmp.grid(row=0, column=col)
                    widget_set.append(var)
                elif widget == 'e':
                    var = tkinter.StringVar()
                    tmp = tkinter.Entry(frm, width=3, textvariable=var)
                    tmp.grid(row=0, column=col)
                    widget_set.append(tmp)
                else:
                    lbl = tkinter.Label(frm, text=widget, font='purisa 10')
                    lbl.grid(row=0, column=col)
                col += 1
            self.filters_params.append(widget_set)


    def init_single_or_specified_ui(self, parent, single_name, \
            specified_hint):
        """
        used to init stock/filter tab
        which contains 'default'/'specified' options
        """

        def select():
            """ callback of radio button """
            sel = rvar.get()
            if sel == 'Specified':
                ent1.configure(state='normal')
                ent1.select_range(0, tkinter.END)
                ent1.focus()
            else:
                ent1.configure(state='disabled')

        # init radio buttons for 'all' and 'specified'
        rvar = tkinter.StringVar()
        rb0 = tkinter.Radiobutton(parent, font='purisa 10', \
                variable=rvar, command=select, \
                value=single_name, text=single_name)
        rb0.select()
        rb1 = tkinter.Radiobutton(parent, font='purisa 10', \
                variable=rvar, command=select, \
                value=u'Specified', text='Specified')
        rb0.grid(row=0, column=0, sticky='W')
        rb1.grid(row=1, column=0, sticky='W')
        parent.grid_columnconfigure(0, pad=10)

        # init entry for 'specified'
        evar = tkinter.StringVar()
        evar.set(specified_hint)
        ent1 = tkinter.Entry(parent, state=tkinter.DISABLED, \
                textvariable=evar, width=50, font='purisa 10')
        ent1.grid(row=1, column=1)
        parent.e1 = ent1
        parent.rvar = rvar






    def init_filter_settings_ui(self):
        """
        the main ui, which is composed of stock/date/filter tabs
        """
        self.filesetting = \
            tkinter.LabelFrame(self.parent, text='Filter Settings', \
            font='purisa 10', padx=10, pady=10)
        self.filesetting.grid(row=0, column=0)

        # tab for 'stocks'
        self.tabs = ttk.Notebook(self.filesetting)
        fr0 = ttk.Frame(self.tabs, padding=10)
        fr0.img = Image.open("res/target.png")
        fr0.pimg = ImageTk.PhotoImage(fr0.img)
        self.filesetting.stocks_tab = fr0
        self.init_single_or_specified_ui(fr0, 'All', 'e.g. 1234,2345,3456')

        # tab for 'date'
        fr1 = ttk.Frame(self.tabs, padding=10)
        fr1.img = Image.open("res/date.jpg")
        fr1.pimg = ImageTk.PhotoImage(fr1.img)
        self.filesetting.date_tab = fr1
        self.init_single_or_specified_ui(fr1, 'Today', \
            'e.g. 2015/10/1 or 2015/10/1-2015/11/1')

        # tab for 'filters'
        fr2 = ttk.Frame(self.tabs, padding=10)
        fr2.img = Image.open("res/filter.jpg")
        fr2.pimg = ImageTk.PhotoImage(fr2.img)
        self.filesetting.filters_tab = fr2
        fr1.pimg = ImageTk.PhotoImage(fr1.img)
        self.init_filters_ui(fr2)

        self.tabs.add(fr0, image=fr0.pimg)
        self.tabs.add(fr1, image=fr1.pimg)
        self.tabs.add(fr2, image=fr2.pimg)

        self.filesetting.grid_columnconfigure(0, pad=10)

        self.run = tkinter.Button(self.filesetting, text='Run', \
            command=self.run_filters, font='purisa 10')
        self.run.grid(row=0, column=1, sticky='N')

    def run_filters(self):
        """
        get params from widget and bypass to filters
        """
        if self.filesetting.stocks_tab.rvar.get() == 'All':
            stocks = 'all'
        else:
            stocks = self.filesetting.stocks_tab.e1.get()

        if self.filesetting.date_tab.rvar.get() == 'Today':
            date = 'today'
        else:
            date = self.filesetting.date_tab.e1.get()

        #print('stocks:', stocks)
        #print('date:', date)
        i = 0
        for cond in self.filters_params:
            if int(cond[0].get()): # [1] for checkbutton
                #filt = self.filesetting.filters_tab.filters_table[i][0]
                filt = self.filters_table[i][0]
                ft_params = [widget.get() for widget in cond[1:]]
                stockfilter.process_filter(filt, stocks, date, ft_params)
            i += 1
            #for widget in cond:
                #print(widget.get())






APP_WIDTH = 700
APP_HEIGHT = 700
def main():
    """
    application entry point
    """
    root = tkinter.Tk()
    pos_x = (root.winfo_screenwidth() - APP_WIDTH) // 2
    pos_y = (root.winfo_screenheight() - APP_HEIGHT) // 2
    root.geometry('%dx%d+%d+%d' % (APP_WIDTH, APP_HEIGHT, pos_x, pos_y))
    app = App(root)
    app.mainloop()



if __name__ == '__main__':
    main()

