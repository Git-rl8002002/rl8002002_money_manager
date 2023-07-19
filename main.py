#!/usr/bin/python3

# Author   : JasonHung
# Date     : 20230220
# Update   : 20230220
# Function : money manager


import sys , pymysql , hashlib , time , os , platform

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QWidget , QApplication , QMainWindow , QMessageBox , QTreeWidgetItem
from PyQt6.QtCharts import *

from control.dao import *
from gui.ui_login import *
from gui.ui_main import *

########################################################################################################################
#
# main_content
#
########################################################################################################################
class main_content(QMainWindow):
    
    #########
    # init
    #########
    def __init__(self , parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.main_init()
    
    ##############
    # main_init
    ##############
    def main_init(self):
        

        ########
        # add
        ########
        self.ui.btn_add_del.setEnabled(False)
        self.ui.add_no.setEnabled(False)
        self.ui.add_kind_comboBox.setFixedWidth(300)
        self.ui.action_add.triggered.connect(self.add)
        self.ui.btn_add_new.clicked.connect(self.submit_add_new)
        self.ui.btn_add_cancel.clicked.connect(self.add_cancel)
        self.add_day_list()
        self.add_month_list()
        self.add_year_list()
        self.add_kind_list()

        ############
        # welcome
        ############
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_welcome)
    
    ###################
    # add_year_list
    ###################
    def add_year_list(self):
        
        ### clear
        self.ui.add_year_list.clear()
        
        try:
            self.conn = pymysql.connect(host=tinfar_VM['host'],port=tinfar_VM['port'],user=tinfar_VM['user'],passwd=tinfar_VM['pwd'],database=tinfar_VM['db'],charset=tinfar_VM['charset'])    
            self.curr = self.conn.cursor()
            self.sql = "select record_year , count(*) from money_record where account='{0}' group by record_year order by record_year desc".format(a_user)
            self.curr.execute(self.sql)
            self.res = self.curr.fetchall()

            self.ui.add_year_list.setHeaderLabels(['日期','總數量','總金額'])
            self.ui.add_year_list.setColumnWidth(0,150)
            self.ui.add_year_list.setColumnWidth(1,70)
            self.ui.add_year_list.setColumnWidth(2,150)

            for val in self.res:
                self.root = QTreeWidgetItem(self.ui.add_year_list)
                self.root.setText(0 , str(val[0]))
                self.root.setText(1 , str(val[1]))
                
                self.sql = "select sum(money) from money_record where account='{0}' and record_year='{1}'".format(a_user , val[0])
                self.curr.execute(self.sql)
                self.res = self.curr.fetchone()
                self.root.setText(2 , str(self.res[0]))

            ### double click show kind detail content  
            self.ui.add_year_list.doubleClicked.connect(self.show_add_year_list)

        except Exception as e:
            print('< Error > add_year_list : ' + str(e))
        finally:
            self.conn.commit()
            self.conn.close()

    ########################
    # show_add_year_list
    ########################
    def show_add_year_list(self):
        try:
            ### variables
            self.data = self.ui.add_year_list.currentItem()
            self.year = self.data.text(0)

            ### clear show_add_detail_list old data 
            self.ui.show_add_detail_list.clear()

            self.conn = pymysql.connect(host=tinfar_VM['host'],port=tinfar_VM['port'],user=tinfar_VM['user'],passwd=tinfar_VM['pwd'],database=tinfar_VM['db'],charset=tinfar_VM['charset'])    
            self.curr = self.conn.cursor()
            self.sql = "select record_time , money , content from money_record where account='{0}' and record_year='{1}' order by record_time desc".format(a_user , self.year)
            self.curr.execute(self.sql)
            self.res = self.curr.fetchall()

            self.ui.show_add_detail_list.setHeaderLabels(['日期','金額','內容'])
            self.ui.show_add_detail_list.setColumnWidth(0,150)
            self.ui.show_add_detail_list.setColumnWidth(1,70)
            self.ui.show_add_detail_list.setColumnWidth(2,300)

            for val in self.res:
                self.root = QTreeWidgetItem(self.ui.show_add_detail_list)
                self.root.setText(0 , str(val[0]))
                self.root.setText(1 , str(val[1]))  
                self.root.setText(2 , str(val[2]))

        except Exception as e:
            print('< Error > show_add_year_list : ' + str(e))
        finally:
            self.conn.commit()
            self.conn.close()

    ###################
    # add_month_list
    ###################
    def add_month_list(self):
        
        ### clear
        self.ui.add_month_list.clear()
        
        try:
            self.conn = pymysql.connect(host=tinfar_VM['host'],port=tinfar_VM['port'],user=tinfar_VM['user'],passwd=tinfar_VM['pwd'],database=tinfar_VM['db'],charset=tinfar_VM['charset'])    
            self.curr = self.conn.cursor()
            self.sql = "select record_month , count(*) from money_record where account='{0}' group by record_month order by record_month desc".format(a_user)
            self.curr.execute(self.sql)
            self.res = self.curr.fetchall()

            self.ui.add_month_list.setHeaderLabels(['日期','總數量','總金額'])
            self.ui.add_month_list.setColumnWidth(0,150)
            self.ui.add_month_list.setColumnWidth(1,70)
            self.ui.add_month_list.setColumnWidth(2,150)

            for val in self.res:
                self.root = QTreeWidgetItem(self.ui.add_month_list)
                self.root.setText(0 , str(val[0]))
                self.root.setText(1 , str(val[1]))
                
                self.sql = "select sum(money) from money_record where account='{0}' and record_month='{1}'".format(a_user , val[0])
                self.curr.execute(self.sql)
                self.res = self.curr.fetchone()
                self.root.setText(2 , str(self.res[0]))

            ### double click show kind detail content  
            self.ui.add_month_list.doubleClicked.connect(self.show_add_month_list)

        except Exception as e:
            print('< Error > add_month_list : ' + str(e))
        finally:
            self.conn.commit()
            self.conn.close()

    ########################
    # show_add_month_list
    ########################
    def show_add_month_list(self):
        try:
            ### variables
            self.data = self.ui.add_month_list.currentItem()
            self.month = self.data.text(0)

            ### clear show_add_detail_list old data 
            self.ui.show_add_detail_list.clear()

            self.conn = pymysql.connect(host=tinfar_VM['host'],port=tinfar_VM['port'],user=tinfar_VM['user'],passwd=tinfar_VM['pwd'],database=tinfar_VM['db'],charset=tinfar_VM['charset'])    
            self.curr = self.conn.cursor()
            self.sql = "select record_time , money , content from money_record where account='{0}' and record_month='{1}' order by record_time desc".format(a_user , self.month)
            self.curr.execute(self.sql)
            self.res = self.curr.fetchall()

            self.ui.show_add_detail_list.setHeaderLabels(['日期','金額','內容'])
            self.ui.show_add_detail_list.setColumnWidth(0,150)
            self.ui.show_add_detail_list.setColumnWidth(1,70)
            self.ui.show_add_detail_list.setColumnWidth(2,300)

            for val in self.res:
                self.root = QTreeWidgetItem(self.ui.show_add_detail_list)
                self.root.setText(0 , str(val[0]))
                self.root.setText(1 , str(val[1]))  
                self.root.setText(2 , str(val[2]))


        except Exception as e:
            print('< Error > show_add_month_list : ' + str(e))
        finally:
            self.conn.commit()
            self.conn.close()

    #################
    # add_kind_list
    #################
    def add_kind_list(self):
        try:
            self.conn = pymysql.connect(host=tinfar_VM['host'],port=tinfar_VM['port'],user=tinfar_VM['user'],passwd=tinfar_VM['pwd'],database=tinfar_VM['db'],charset=tinfar_VM['charset'])    
            self.curr = self.conn.cursor()
            self.sql = "select kind , count(*) from money_record where account='{0}' group by kind order by kind desc".format(a_user)
            self.curr.execute(self.sql)
            self.res = self.curr.fetchall()

            self.ui.add_kind_list.setHeaderLabels(['種類','總數量','總金額'])
            self.ui.add_kind_list.setColumnWidth(0,150)
            self.ui.add_kind_list.setColumnWidth(1,70)
            self.ui.add_kind_list.setColumnWidth(2,150)

            for val in self.res:
                self.root = QTreeWidgetItem(self.ui.add_kind_list)
                self.root.setText(0 , str(val[0]))
                self.root.setText(1 , str(val[1]))
                
                self.sql = "select sum(money) from money_record where account='{0}' and kind='{1}'".format(a_user , val[0])
                self.curr.execute(self.sql)
                self.res = self.curr.fetchone()
                self.root.setText(2 , str(self.res[0]))

            ### double click show kind detail content  
            self.ui.add_kind_list.doubleClicked.connect(self.show_add_kind_list)

        except Exception as e:
            print('< Error > add_kind_list : ' + str(e))
        finally:
            self.conn.commit()
            self.conn.close()
    
    #######################
    # show_add_kind_list
    #######################
    def show_add_kind_list(self):
        try:
            ### variables
            self.data = self.ui.add_kind_list.currentItem()
            self.kind = self.data.text(0)

            ### clear show_add_detail_list old data 
            self.ui.show_add_detail_list.clear()

            self.conn = pymysql.connect(host=tinfar_VM['host'],port=tinfar_VM['port'],user=tinfar_VM['user'],passwd=tinfar_VM['pwd'],database=tinfar_VM['db'],charset=tinfar_VM['charset'])    
            self.curr = self.conn.cursor()
            self.sql = "select record_time , money , content from money_record where account='{0}' and kind='{1}' order by record_time desc".format(a_user , self.kind)
            self.curr.execute(self.sql)
            self.res = self.curr.fetchall()

            self.ui.show_add_detail_list.setHeaderLabels(['日期','金額','內容'])
            self.ui.show_add_detail_list.setColumnWidth(0,150)
            self.ui.show_add_detail_list.setColumnWidth(1,70)
            self.ui.show_add_detail_list.setColumnWidth(2,300)

            for val in self.res:
                self.root = QTreeWidgetItem(self.ui.show_add_detail_list)
                self.root.setText(0 , str(val[0]))
                self.root.setText(1 , str(val[1]))  
                self.root.setText(2 , str(val[2]))


        except Exception as e:
            print('< Error > show_add_kind_list : ' + str(e))
        finally:
            self.conn.commit()
            self.conn.close()

    #################
    # add_day_list
    #################
    def add_day_list(self):
        
        ### clear 
        self.ui.add_day_list.clear()

        try:
            self.conn = pymysql.connect(host=tinfar_VM['host'],port=tinfar_VM['port'],user=tinfar_VM['user'],passwd=tinfar_VM['pwd'],database=tinfar_VM['db'],charset=tinfar_VM['charset'])    
            self.curr = self.conn.cursor()
            self.sql  = "select record_time , kind , content , money from money_record where account='{0}' order by record_time desc".format(a_user)
            self.curr.execute(self.sql)
            self.res = self.curr.fetchall()

            self.ui.add_day_list.setHeaderLabels(['日期','種類','金額','內容'])
            self.ui.add_day_list.setColumnWidth(0,150)
            self.ui.add_day_list.setColumnWidth(1,100)
            self.ui.add_day_list.setColumnWidth(2,100)
            self.ui.add_day_list.setColumnWidth(3,300)

            for val in self.res:
                self.root = QTreeWidgetItem(self.ui.add_day_list)
                self.root.setText(0 , str(val[0]))
                self.root.setText(1 , str(val[1]))
                self.root.setText(2 , str(val[3]))
                self.root.setText(3 , str(val[2]))

            ### add day new detail
            self.ui.add_day_list.doubleClicked.connect(self.show_add_new)
            
            self.conn.commit()
            self.conn.close()

        except Exception as e:
            print('< Error > add_day_list : ' + str(e))
        finally:
            pass
    
    ################
    # show_add_new
    ################
    def show_add_new(self):
        
        ### variable
        self.ui.btn_add_del.setEnabled(True)
        self.ui.btn_add_new.setEnabled(False)
        self.data = self.ui.add_day_list.currentItem()
        self.content = self.data.text(3)

        try:
            self.conn = pymysql.connect(host=tinfar_VM['host'],port=tinfar_VM['port'],user=tinfar_VM['user'],passwd=tinfar_VM['pwd'],database=tinfar_VM['db'],charset=tinfar_VM['charset'])    
            self.curr = self.conn.cursor()
            self.sql  = "select no , record_time , kind ,  money , content from money_record where account='{0}' and content='{1}'".format(a_user , self.content)
            self.curr.execute(self.sql)
            self.res = self.curr.fetchall()
            
            for val in self.res:
                self.ui.add_date.setText(str(val[1]))
                self.ui.add_kind.setText(str(val[2]))
                self.ui.add_no.setText(str(val[0]))
                self.ui.add_money.setText(str(val[3]))
                self.ui.add_content.setText(str(val[4]))
            
            ### del add day list
            self.ui.btn_add_del.clicked.connect(self.del_add_new)

            self.conn.commit()
            self.conn.close()

        except Exception as e:
            print('< Error > show_add_new : ' + str(e))
        finally:
            pass
    
    ################
    # del_add_new
    ################
    def del_add_new(self , del_no):
        
        ### variables
        self.d_no = self.ui.add_no.text()
        #self.d_no = del_no

        try:
            self.conn = pymysql.connect(host=tinfar_VM['host'],port=tinfar_VM['port'],user=tinfar_VM['user'],passwd=tinfar_VM['pwd'],database=tinfar_VM['db'],charset=tinfar_VM['charset'])    
            self.curr = self.conn.cursor()

            self.sql2  = "delete from money_record where account='{0}' and no='{1}'".format(a_user , self.d_no)
            self.curr.execute(self.sql2)

            self.conn.commit()
            self.conn.close()
            
            self.ui.btn_add_del.setEnabled(False)

            ### record time
            self.r_day   = time.strftime("%Y-%m-%d" , time.localtime()) 

            self.ui.add_date.setText(str(self.r_day))
            self.ui.add_no.clear()
            self.ui.add_kind.clear()
            self.ui.add_money.clear()
            self.ui.add_content.clear()

            ########################
            # reload add_day_list
            ########################
            self.add_day_list()

            QMessageBox.information(self , 'Msg' , str('刪除完成.'))

        except Exception as e:
            print('< Error > del_add_new : ' + str(e))
        finally:
            pass

    ########
    # add
    ########
    def add(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_add)
        
        ### variables
        self.ui.add_date.setFixedHeight(31)
        self.ui.add_kind.setFixedHeight(31)
        self.ui.add_kind_comboBox.setFixedHeight(31)
        self.ui.add_money.setFixedHeight(31)
        self.ui.add_content.setFixedHeight(31)

        ### record time
        self.r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        self.r_year  = time.strftime("%Y" , time.localtime())
        self.r_month = time.strftime("%Y-%m" , time.localtime())
        self.r_day   = time.strftime("%Y-%m-%d" , time.localtime()) 

        ### add_date
        self.ui.add_date.setText(str(self.r_day))

        ### select add form kind
        self.add_kind_selected()
    
    ######################
    # add_kind_selected
    ######################
    def add_kind_selected(self):
        try:
            ### clear
            self.ui.add_kind_comboBox.clear()
            
            self.conn = pymysql.connect(host=tinfar_VM['host'],port=tinfar_VM['port'],user=tinfar_VM['user'],passwd=tinfar_VM['pwd'],database=tinfar_VM['db'],charset=tinfar_VM['charset'])    
            self.curr = self.conn.cursor()
            self.sql = "select kind from money_record  where account='{0}' group by kind order by kind desc".format(a_user)
            self.curr.execute(self.sql)
            self.res = self.curr.fetchall()

            self.ui.add_kind_comboBox.addItem('')

            for val in self.res:
                self.ui.add_kind_comboBox.addItem(val[0])
            
            self.ui.add_kind_comboBox.currentIndexChanged.connect(self.add_kind_val)

            self.conn.commit()
            self.conn.close()

        except Exception as e:
            print('< Error > add kind comboBox : ' + str(e))
    
    #################
    # add_kind_val
    #################
    def add_kind_val(self):
        self.val = self.ui.add_kind_comboBox.currentText()
        self.ui.add_kind.setText(self.val)

    ###############
    # add_cancel
    ###############
    def add_cancel(self):
        
        ### variables
        self.ui.btn_add_new.setEnabled(True)
        self.ui.btn_add_del.setEnabled(False)

        ### record time
        self.r_day   = time.strftime("%Y-%m-%d" , time.localtime())     

        self.ui.add_date.setText(str(self.r_day))
        self.ui.add_no.clear()
        self.ui.add_kind.clear()
        self.ui.add_money.clear()
        self.ui.add_content.clear()

    ###################
    # submit_add_new
    ###################
    def submit_add_new(self):
        
        ### variable
        self.a_kind    = self.ui.add_kind.text()
        self.a_money   = self.ui.add_money.text()
        self.a_content = self.ui.add_content.text()

        if len(self.a_kind) == 0:
            QMessageBox.information(self , 'Msg' , '種類不能空白 !')
        elif len(self.a_money) == 0 :
            QMessageBox.information(self , 'Msg' , '金額不能空白 !')
        elif len(self.a_content) == 0:
            QMessageBox.information(self , 'Msg' , '內容不能空白 !')
        else:
            try:
                ### variables
                self.b_user    = a_user
                self.b_date    = self.ui.add_date.text()
                self.data      = self.b_date.split('-')
                self.r_year    = self.data[0]
                self.r_month   = self.data[1]
                self.r_day     = self.data[2]
                self.b_kind    = self.ui.add_kind.text()
                self.b_money   = self.ui.add_money.text()
                self.b_content = self.ui.add_content.text()
                self.os_path   = platform.system()

                self.conn = pymysql.connect(host=tinfar_VM['host'],port=tinfar_VM['port'],user=tinfar_VM['user'],passwd=tinfar_VM['pwd'],database=tinfar_VM['db'],charset=tinfar_VM['charset'])    
                self.curr = self.conn.cursor()
                self.sql = "insert into money_record(record_time , account , kind , content , money , record_year , record_month , record_day) value('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')".format(self.b_date , self.b_user , self.b_kind , self.b_content , self.b_money , self.r_year , self.r_month , self.r_day)
                self.curr.execute(self.sql)

                self.conn.commit()
                self.conn.close()

                ################
                # save to txt
                ################
                self.txt_content = self.b_date + ' , ' + self.b_user + ' , ' + self.b_kind + ' , ' + self.b_content + ' , ' + self.b_money + ' 元\n'
                if self.os_path == 'Darwin':
                    self.add = open(txt['mac_path'] + self.b_date + '.txt' ,'a')
                    self.add.write(self.txt_content)
                    self.add.close()
                elif self.os_path == 'Windows':    
                    self.add = open(txt['win_path'] + self.b_date + '.txt' ,'a')
                    self.add.write(self.txt_content)
                    self.add.close()

                ##########
                # clear 
                ##########
                self.ui.add_kind.clear()
                self.ui.add_money.clear()
                self.ui.add_content.clear()
                self.ui.add_kind_comboBox.clear()
                self.ui.add_day_list.clear()

                ########################
                # reload add day list
                ########################
                self.add_day_list()

                #############################
                # reload add kind comboBox
                #############################
                self.conn = pymysql.connect(host=tinfar_VM['host'],port=tinfar_VM['port'],user=tinfar_VM['user'],passwd=tinfar_VM['pwd'],database=tinfar_VM['db'],charset=tinfar_VM['charset'])    
                self.curr = self.conn.cursor()
                self.sql = "select kind from money_record group by kind order by kind desc"
                self.curr.execute(self.sql)
                self.res = self.curr.fetchall()

                self.ui.add_kind_comboBox.addItem('')

                for val in self.res:
                    self.ui.add_kind_comboBox.addItem(val[0])
                
                self.ui.add_kind_comboBox.currentIndexChanged.connect(self.add_kind_val)

                self.conn.commit()
                self.conn.close()

                QMessageBox.information(self , 'Msg' , '新增成功.')            
            
            except Exception as e:
                print('< Error > add_new : ' + str(e))
            finally:
                pass
            
        


        
        



########################################################################################################################
#
# login
#
########################################################################################################################
class login(QWidget):
    
    #########
    # init
    #########
    def __init__(self, parent=None):
            super().__init__(parent)
            self.ui = Ui_login()
            self.ui.setupUi(self)
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            self.login_init()

    ###############
    # login_init
    ###############
    def login_init(self):
        try:
            ### cancel 
            self.ui.btn_cancel.clicked.connect(self.login_cancel)

            ### login
            self.ui.btn_login.clicked.connect(self.login_submit)

        except Exception as e:
            print('< Error > login_init : ' + str(e))

    #################
    # login_submit
    #################
    def login_submit(self):
        try:
            ### variables
            self.user = self.ui.login_user.text()
            self.pwd = self.ui.login_pwd.text()

            ### pwd encode MD5
            self.pwd_str = hashlib.md5()
            self.pwd_str.update(self.pwd.encode(encoding='utf8'))
            self.pwd_md5 = self.pwd_str.hexdigest()

            try:
                self.conn = pymysql.connect(host=tinfar_VM['host'],port=tinfar_VM['port'],user=tinfar_VM['user'],passwd=tinfar_VM['pwd'],database=tinfar_VM['db'],charset=tinfar_VM['charset'])    
                self.curr = self.conn.cursor()
                self.sql = "select a_user from m_m_a where a_user='{0}' and a_pwd='{1}' and a_status='on'".format(self.user , self.pwd_md5)
                self.curr.execute(self.sql)
                self.res = self.curr.fetchone()

                if len(self.res[0]) != 0:
                    
                    ### global a_user
                    global a_user 
                    a_user = self.res[0]
                    
                    ### close login form
                    self.close()

                    ### main form
                    self.main = main_content()
                    self.main.show()
                    self.ui.label_3.setText(str(self.res[0]))
                
            except Exception as e:
                self.ui.label_3.clear()
                self.ui.label_3.setStyleSheet('color:red')
                self.ui.label_3.setText(str('無此帳號 !'))
            finally:
                self.conn.commit()
                self.conn.close()

        except Exception as e:
            print('< Error > login_submit : ' + str(e))
    
    #################
    # login_cancel
    #################
    def login_cancel(self):
        try:
            QApplication.closeAllWindows()
        except Exception as e:
            print('< Error > login_cancel : ' + str(e))

########################################################################################################################
#
# main 
#
########################################################################################################################
def main(): 
    app = QApplication(sys.argv)
    main = login()
    main.show()
    app.exit(app.exec())

if __name__ == '__main__':
    main()


    