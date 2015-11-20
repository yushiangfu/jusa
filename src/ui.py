"""
ui layout
bypass parameters to filter
"""
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import stockfilter

# widgets@tkinter are highly configurable while ttk provides themed widgets
# so, use ttk if possible
class App():
    """ ui implementation """
    def __init__(self, parent):
        self.parent = parent
        self.stocks_tab = None
        self.date_tab = None
        self.filters_tab = None
        self.filters_descs = [
            [stockfilter.new_price_in_n_days, 'c', '股價創', 'e', '日新', 'e'],
            [stockfilter.new_revenue_in_n_months, 'c', '營收創', 'e', '月新', 'e'],
            ]
        self.filters_vars = None

        self.init_ui()


    def init_ui(self):
        """ init each sub ui """
        # set main ui's size/pos/title
        app_width = 800
        app_height = 800
        pos_x = (self.parent.winfo_screenwidth() - app_width) // 2
        pos_y = (self.parent.winfo_screenheight() - app_height) // 2
        self.parent.geometry('%dx%d+%d+%d' % (app_width, app_height, pos_x, pos_y))
        self.parent.title('Jusa - Stock Analyzer')

        filter_settings = self.init_filter_settings_ui()
        filter_settings.grid(row=0, column=0)

        self.parent.grid_columnconfigure(0, weight=1)

        # FIXME: add 'result' ui


    def init_filter_settings_ui(self):
        """
        the 'filter settings' ui, which is composed of stock/date/filter tabs
        """
        # 'filter settings' label frame
        filter_settings = \
            tkinter.LabelFrame(self.parent, text='Filter Settings',
                               font='purisa 10', padx=10, pady=10) # internal padding

        # 'setting' tabs
        tabs = self.init_tabs_ui(filter_settings)
        tabs.grid(row=0, column=0)

        # 'run' button
        run_button = \
            tkinter.Button(filter_settings, text='Run',
                           command=self.bypass_params, font='purisa 10')
        run_button.grid(row=0, column=1, sticky='N')

        return filter_settings


    def init_tabs_ui(self, parent):
        """ init each tab """
        tabs = ttk.Notebook(parent)
        tabs.grid()

        # tab for 'stocks'
        self.stocks_tab = ttk.Frame(tabs, padding=10)
        tmp_img = Image.open("res/target.png")
        self.stocks_tab.pimg = ImageTk.PhotoImage(tmp_img) # pimg must be referenced
        tabs.add(self.stocks_tab, image=self.stocks_tab.pimg)
        self.init_stocks_ui()

        # tab for 'date'
        self.date_tab = ttk.Frame(tabs, padding=10)
        tmp_img = Image.open("res/date.jpg")
        self.date_tab.pimg = ImageTk.PhotoImage(tmp_img)
        tabs.add(self.date_tab, image=self.date_tab.pimg)
        self.init_date_ui()

        # tab for 'filters'
        self.filters_tab = ttk.Frame(tabs, padding=10)
        tmp_img = Image.open("res/filter.jpg")
        self.filters_tab.pimg = ImageTk.PhotoImage(tmp_img)
        tabs.add(self.filters_tab, image=self.filters_tab.pimg)
        self.init_filters_ui()

        return tabs


    def init_stocks_ui(self):
        """ init stocks tab """
        def select():
            """ callback of radio button """
            sel = rb_var.get()
            if sel == 'Specified':
                ent_specified.configure(state='normal')
                ent_specified.select_range(0, tkinter.END)
                ent_specified.focus()
            else:
                ent_specified.configure(state='disabled')

        rb_var = tkinter.StringVar()
        self.stocks_tab.rb_var = rb_var

        # 'default' button
        rb_default = \
            tkinter.Radiobutton(self.stocks_tab, font='purisa 10',
                                variable=rb_var, command=select,
                                value='All', text='All')
        rb_default.grid(row=0, column=0, sticky='W')
        rb_default.select()

        # 'specified' button
        rb_specified = \
            tkinter.Radiobutton(self.stocks_tab, font='purisa 10',
                                variable=rb_var, command=select,
                                value='Specified', text='Specified')
        rb_specified.grid(row=1, column=0, sticky='W')

        # make space between ratio button and entry
        self.stocks_tab.grid_columnconfigure(0, pad=10)

        # 'specified' entry
        ent_var = tkinter.StringVar()
        ent_var.set('e.g. 1234,2345,3456')
        ent_specified = \
            tkinter.Entry(self.stocks_tab, state='disabled',
                          textvariable=ent_var, width=50, font='purisa 10')
        ent_specified.grid(row=1, column=1)
        self.stocks_tab.ent_specified = ent_specified


    def init_date_ui(self):
        """ init stocks tab """
        def select():
            """ callback of radio button """
            sel = rb_var.get()
            if sel == 'Specified':
                ent_specified.configure(state='normal')
                ent_specified.select_range(0, tkinter.END)
                ent_specified.focus()
            else:
                ent_specified.configure(state='disabled')

        rb_var = tkinter.StringVar()
        self.date_tab.rb_var = rb_var

        # 'default' button
        rb_default = \
            tkinter.Radiobutton(self.date_tab, font='purisa 10',
                                variable=rb_var, command=select,
                                value='Today', text='Today')
        rb_default.grid(row=0, column=0, sticky='W')
        rb_default.select()

        # 'specified' button
        rb_specified = \
            tkinter.Radiobutton(self.date_tab, font='purisa 10',
                                variable=rb_var, command=select,
                                value='Specified', text='Specified')
        rb_specified.grid(row=1, column=0, sticky='W')

        # make space between ratio button and entry
        self.date_tab.grid_columnconfigure(0, pad=10)

        # 'specified' entry
        ent_var = tkinter.StringVar()
        ent_var.set('e.g. 2015/10/1 or 2015/10/1-2015/11/1')
        ent_specified = \
            tkinter.Entry(self.date_tab, state='disabled',
                          textvariable=ent_var, width=50, font='purisa 10')
        ent_specified.grid(row=1, column=1)
        self.date_tab.ent_specified = ent_specified


    def init_filters_ui(self):
        """ according filters_descs to init widgets of each filter """
        # init scrollbar/text and bind them
        scrollbar = ttk.Scrollbar(self.filters_tab, orient='vertical')
        text = tkinter.Text(self.filters_tab, yscrollcommand=scrollbar.set, 
                            bg=self.parent.cget('bg'), takefocus=0)
        scrollbar.config(command=text.yview)
        scrollbar.pack(side='right', fill='y')
        text.pack()

        self.filters_vars = []
        for filt in self.filters_descs:
            frm = tkinter.Frame(text)
            text.window_create('end', window=frm)
            text.insert('end', '\n')
            filter_vars = []
            for desc in filt[1:]: # manually avoid filter function
                if desc == 'c':
                    var = tkinter.IntVar()
                    widget = tkinter.Checkbutton(frm, variable=var)
                    filter_vars.append(var)
                elif desc == 'e':
                    var = tkinter.StringVar()
                    widget = tkinter.Entry(frm, width=4, textvariable=var)
                    filter_vars.append(widget)
                else:
                    widget = tkinter.Label(frm, text=desc, font='purisa 10')
                widget.pack(side='left')
            self.filters_vars.append(filter_vars)


    def bypass_params(self):
        """ get params from widget and bypass to filters """
        if self.stocks_tab.rb_var.get() == 'All':
            stocks = 'all'
        else:
            stocks = self.stocks_tab.ent_specified.get()

        if self.date_tab.rb_var.get() == 'Today':
            date = 'today'
        else:
            date = self.date_tab.ent_specified.get()

        filters_params = []
        for i in range(len(self.filters_vars)):
            filter_vars = self.filters_vars[i]
            if int(filter_vars[0].get()): # [0] for checkbutton
                filt = self.filters_descs[i][0]
                filter_params = [var.get() for var in filter_vars[1:]]
                filters_params.append([filt] + filter_params)
        stockfilter.process_filters(stocks, date, filters_params)


def main():
    """
    application entry point
    """
    root = tkinter.Tk()
    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()

