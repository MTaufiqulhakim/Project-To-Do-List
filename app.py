import eel
import time
import pywhatkit
import threading
import datetime
import pyautogui as pg
import random

class App:
    def __init__(self):
        eel.init('web')

    def start(self):
        print('Starting...')
        thread = threading.Thread(target=self.check_task)
        thread.start()
        eel.start('signin.html')
                    
    @eel.expose
    def signup_process(name, wa, password):
        res = dict()
        otp = random.randint(100000, 999999)
        wa_correct = '+62' + wa[1:]
        pywhatkit.sendwhatmsg(wa_correct, f"*Don't give this code to anyone, this is your OTP code :* {otp}", datetime.datetime.now().hour, datetime.datetime.now().minute + 1, 35)
        pg.press('enter')

        res = {
            'name': name,
            'wa': wa,
            'password': password,
            'otp': otp,
            'response_status': 'success'
        }
        eel.signup_response(res)
        
    @eel.expose
    def signin_process(wa, password):
        try:
            with open('user_data.txt', 'r') as file:
                data = file.read()
                response = dict()

                data = data.split('\n')
                for i in data:
                    user = i.split(',')

                    if wa == user[2] and password == user[3]:
                        response = {
                            'response_status': 'success',
                            'id': user[0], 
                            'name': user[1], 
                            'wa': user[2], 
                        }
                        break
                
                if len(response) == 0:
                    eel.signin_response({'response_status': 'error'})
                    response = {}
                    return
                else:
                    eel.signin_response(response)
                    response = {}
                    return
        except Exception as e:
            print(e)
            
    @eel.expose
    def add_task(list):
        try:
            with open('task_list.txt', 'r') as file:
                data = file.read()
                tasks = 0

                data = data.split('\n')

                if data[0] == '':
                    with open('task_list.txt', 'a') as file:
                        file.write(f"1,{list['id']},{list['wa']},{list['task']},{list['date']},{list['time']},{list['priority']},ToDo")
                        eel.add_task_response('success')
                        return
                else:
                    tasks = int(data[-1].split(',')[0])
                    with open('task_list.txt', 'a') as file:
                        file.write(f"\n{tasks + 1},{list['id']},{list['wa']},{list['task']},{list['date']},{list['time']},{list['priority']},ToDo")
                        eel.add_task_response('success')
                        return
        except Exception as e:
            print(e)
                
    @eel.expose
    def list_task(id, status):
        try:
            with open('task_list.txt', 'r') as file:
                data = file.read()
                tasks = []

                data = data.split('\n')
                for i in data:
                    task = i.split(',')

                    if id == task[1] and status == task[7]:
                        tasks.append({
                            'id': task[0],
                            'task': task[3],
                            'date': task[4],
                            'time': task[5],
                            'priority': task[6],
                            'status': task[7]
                        })
                
                if len(tasks) == 0:
                    eel.list_task_response({'response_status': 'error'})
                    return
                else:
                    eel.list_task_response(tasks)
                    return
        except Exception as e:
            print(e)
            
    @eel.expose
    def delete_task(id_list):
        try:
            with open('task_list.txt', 'r') as file:
                data = file.read()
                tasks = []
                id_list = str(id_list)

                data = data.split('\n')
                for i in data:
                    task = i.split(',')
                    if id_list == task[0]:
                        continue
                    else:
                        tasks.append(f"{task[0]},{task[1]},{task[2]},{task[3]},{task[4]},{task[5]},{task[6]},{task[7]}")

            with open('task_list.txt', 'w') as file:
                for i in tasks:
                    if i == tasks[-1]:
                        file.write(f"{i}")
                    else:
                        file.write(f"{i}\n")

                eel.delete_task_response('success')
                return
        except Exception as e:
            print(e)
        
    @eel.expose
    def done_task(id_list):
        try:
            with open('task_list.txt', 'r') as file:
                data = file.read()
                tasks = []
                id_list = str(id_list)

                data = data.split('\n')
                for i in data:
                    task = i.split(',')
                    if id_list == task[0]:
                        tasks.append(f"{task[0]},{task[1]},{task[2]},{task[3]},{task[4]},{task[5]},{task[6]},Done")
                    else:
                        tasks.append(f"{task[0]},{task[1]},{task[2]},{task[3]},{task[4]},{task[5]},{task[6]},{task[7]}")

            with open('task_list.txt', 'w') as file:
                for i in tasks:
                    if i == tasks[-1]:
                        file.write(f"{i}")
                    else:
                        file.write(f"{i}\n")

                eel.done_task_response('success')
                return
        except Exception as e:
            print(e)
            
    @eel.expose
    def cancel_task(id_list):
        try:
            with open('task_list.txt', 'r') as file:
                data = file.read()
                tasks = []
                id_list = str(id_list)

                data = data.split('\n')
                for i in data:
                    task = i.split(',')
                    if id_list == task[0]:
                        tasks.append(f"{task[0]},{task[1]},{task[2]},{task[3]},{task[4]},{task[5]},{task[6]},Cancel")
                    else:
                        tasks.append(f"{task[0]},{task[1]},{task[2]},{task[3]},{task[4]},{task[5]},{task[6]},{task[7]}")

            with open('task_list.txt', 'w') as file:
                for i in tasks:
                    if i == tasks[-1]:
                        file.write(f"{i}")
                    else:
                        file.write(f"{i}\n")

                eel.cancel_task_response('success')
                return
            
        except Exception as e:
            print(e)

    @eel.expose
    def otp_process(name, wa, password):
        try:
            with open('user_data.txt', 'r') as file:
                data = file.read()
                users = 0

                data = data.split('\n')
                for i in data:
                    users += 1
                    user = i.split(',')
                    if wa == user[2]:
                        eel.otp_response('error') 
                        return  # Add return statement to exit the function

                if data[0] == '':
                    with open('user_data.txt', 'a') as file:
                        file.write(f"1,{name},{wa},{password}")
                        eel.otp_response('success')
                        return
                else:
                    users = int(data[-1].split(',')[0])
                    with open('user_data.txt', 'a') as file:
                        file.write(f"\n{users + 1},{name},{wa},{password}")
                        eel.otp_response('success')
                        return
        except Exception as e:
            print(e)
        
    def check_task(self):
        while True:
            print('Checking for tasks...')
            time.sleep(10)
            with open('task_list.txt', 'r') as file:
                data = file.read()
                data = data.split('\n')
                for i in data:
                    task = i.split(',')
                    wa_correct = '+62' + task[2][1:] 

                    if task[7] == 'ToDo':
                        if task[4] == datetime.datetime.now().strftime("%Y-%m-%d"):
                            waktu = task[5].split(':')
                            jam = int(waktu[0])
                            menit = int(waktu[1])

                            if task[6] == 'High':
                                if menit >= 5:
                                    menit -= 5
                                else:
                                    menit += 55
                                    if jam > 0:
                                        jam -= 1
                                    else:
                                        jam = 23

                                waktu_now = str(jam) + ':' + str(menit)
                            
                                if  waktu_now == datetime.datetime.now().strftime("%H:%M"):
                                    pywhatkit.sendwhatmsg(wa_correct, f"*Hello, I'm Your Reminder*\n\nTask : {task[3]}\nDate : {task[4]}\nTime : {task[5]}\nPriority : {task[6]}", jam, menit + 1, 35)
                                    pg.press('enter')
                                else:
                                    continue
                            elif task[6] == 'Medium':
                                if menit >= 3:
                                    menit -= 3
                                else:
                                    menit += 57
                                    if jam > 0:
                                        jam -= 1
                                    else:
                                        jam = 23

                                waktu_now = str(jam) + ':' + str(menit)
                            
                                if  waktu_now == datetime.datetime.now().strftime("%H:%M"):
                                    pywhatkit.sendwhatmsg(wa_correct, f"*Hello, I'm Your Reminder*\n\nTask : {task[3]}\nDate : {task[4]}\nTime : {task[5]}\nPriority : {task[6]}", jam, menit + 1, 35)
                                    pg.press('enter')
                                else:
                                    continue
                            elif task[6] == 'Low':
                                if menit >= 1:
                                    menit -= 1
                                else:
                                    menit += 59
                                    if jam > 0:
                                        jam -= 1
                                    else:
                                        jam = 23
                                
                                waktu_now = str(jam) + ':' + str(menit)
                            
                                if  waktu_now == datetime.datetime.now().strftime("%H:%M"):
                                    pywhatkit.sendwhatmsg(wa_correct, f"*Hello, I'm Your Reminder*\n\nTask : {task[3]}\nDate : {task[4]}\nTime : {task[5]}\nPriority : {task[6]}", jam, menit + 1, 35)
                                    pg.press('enter')
                                else:
                                    continue
                        else:
                            continue
                    else:
                        continue
        
app = App()
app.start()
