from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import tkinter as tk 
import threading

result = 0
course_ = 'course'
course0 = 'course_y0'
course1 = 'course_y1'
course2 = 'course_y2'
course3 = 'course_y3'
course4 = 'course_y4'
def searching(course_):
    global result
    for element in soup.find_all('tr', {'class':course_}):
        details = [ a.text for a in element.find_all('td', {'style':'text-align: center;'})]
        b = details[2:3]
        c = details[11:13]
        d = b+c
        if d[0] == str(var_serial.get()):
            print(d)
            if d[2] == '額滿':
                result = 0
                return result
            else:
                result += 1
                return result
        else:
            result += 1
            return result

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code  
def webcrawling():
    # 這兩行程式碼就是獲取使用者輸入的course和serial
    course = var_course.get()
    serial = var_serial.get()
    token = var_usr_token.get()
    # 修改為你要傳送的訊息內容
    message = ' %s %s 有餘額囉! \nhttps://course.ncku.edu.tw/course/signin.php' %(course, serial)
    message2 = ' QQ 額滿囉! '

    while 1:
        html = urlopen("http://course-query.acad.ncku.edu.tw/qry/qry001.php?dept_no=%s" %(course)).read().decode("utf-8")
        global soup 
        soup = BeautifulSoup(html, 'lxml')
        searching(course0)
        searching(course1)
        searching(course2)
        searching(course3)
        searching(course4)
        if result == 1 :
            lineNotifyMessage(token, message)
            quit()
            exit(0)
        else:
            lineNotifyMessage(token, message2)
def quit():
    window.destroy()
class Threader(threading.Thread):
    def __init__(self, func,func2):
        threading.Thread.__init__(self)
        self.func = func
        self.func2 = func2
        self.daemon = True
        self.start()
    def run(self):
        self.func()
        self.func2()
        


#main thread
if __name__ == '__main__':    
    # 第1步，例項化object，建立視窗window
    window = tk.Tk()

    # 第2步，給視窗的視覺化起名字
    window.title('NCKU Course Tracker')

    # 第3步，設定視窗的大小(長 * 寬)
    window.geometry('600x500')  # 這裡的乘是小x

    # 第4步，載入 wellcome image
    canvas = tk.Canvas(window, width=400, height=300)
    image_file = tk.PhotoImage(file='ncku.gif')
    image = canvas.create_image(200, 0, anchor='n', image=image_file)
    canvas.pack(side='top')
    tk.Label(window, text='Wellcome to NCKU Course tracker!',font=('Arial', 16)). place(x=130, y=200)

    # 第5步，使用者資訊
    tk.Label(window, text='Course Number:', font=('Arial', 14)).place(x=10, y=240)
    tk.Label(window, text='Serial Number:', font=('Arial', 14)).place(x=10, y=290)
    tk.Label(window, text='User Line Token:', font=('Arial', 14)).place(x=10, y=340)

    # 第6步，使用者登入輸入框entry
    # 使用者名稱
    var_course = tk.StringVar()
    entry_course = tk.Entry(window, textvariable=var_course, font=('Arial', 14))
    entry_course.place(x=200,y=240)
    # 使用者密碼
    var_serial = tk.StringVar()
    entry_serial = tk.Entry(window, textvariable=var_serial, font=('Arial', 14))
    entry_serial.place(x=200,y=290)

    var_usr_token = tk.StringVar()
    entry_usr_token = tk.Entry(window, textvariable= var_usr_token, font=('Arial', 14))
    entry_usr_token.place(x=200, y=340)

    # 修改為你的權杖內容
    # token = 'llfAsLGF07mCF4oRNc8XAE0ZXbhQc9gOQeKYBG3W6ge'
    

    # O = input("please input the department: ")
    # I = input('PLEASE input the course number: ')


    btn_login = tk.Button(window, text='Go', command= lambda: Threader(webcrawling, quit), font=('Arial, 25'), width=10)
    btn_login.place(x=200, y=400)

    

    window.mainloop()