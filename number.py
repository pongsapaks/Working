import datetime
import mysql.connector
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

mydb = mysql.connector.connect(
    host="localhost",
    port="3500",
    user="root",
    password="admin",
    database="db1"
)

def generate_uid():
    x = datetime.datetime.now()
    a = 'U'+(x.strftime("%y%m%d%H%M%S"))
    return a


def receive_input():
    while True:
        try:
            question = abs(int(input('select option: ')))
            print(question)
            break
        except:
            print("That's not a valid option!")
    return question


def generate_tasksid():
    x = datetime.datetime.now()
    a = 'T'+(x.strftime("%y%m%d%H%M%S"))
    print(a)
    return a


def email_input():
    while True:
        try:
            mail = input("Please enter your email :")
            for i in range(len(mail)):
                if mail[i] == '@':
                    return mail
            else:
                raise
        except:
            print("That's not a valid option!")


def email_update():
    while True:
        try:
            m = input("Please enter NEW email :")
            if m != "":
                print(m)
                break
        except:
            print("That's not a valid option!")
    return m


def status_input():
    while True:
        try:
            status = input('Please select status\n0 : Inactive\n1 : active\n')
            if status == '1' or status == '0':
                break
            else:
                raise
        except:
            print('Invalid option')
    return status


def where_userId():
    while True:
        try:
            mycursor = mydb.cursor()
            email = input('Please enter your email: ')
            mycursor.execute(
                f'SELECT u.Id FROM users AS u WHERE u.email like "{email}"')
            myresult = mycursor.fetchall()
            myresult = myresult[0]
            if myresult == '':
                raise
            else:
                for x in myresult:
                    x = str(x)
                return x
        except:
            print("Don't have userId, please enter it again")


def taskdue_input():  # Note : เหมือนต้อง check input ที่รับเข้ามาเก็บใน database
    while True:
        try:
            taskdue = input(
                'Please enter you Due date Example DD/MM/YYYY (15/5/2022): ').split('/')
            case = datetime.datetime(
                int(taskdue[2]), int(taskdue[1]), int(taskdue[0]),)
            a = (case.strftime("%x"))
            if a < datetime.date.today().strftime("%x"):
                raise
            else:
                return a
        except:
            print("Please choose due date today or after")


def create_at():
    x = datetime.datetime.now()
    return x.strftime("%Y-%m-%d %X")


def freetext():
    x = input('Please enter Tasktile: ')
    return x


def create_task_log(tasks_id, user_email):
    user_id = get_user_id(user_email)
    mycursor = mydb.cursor()
    sql = '''
        INSERT INTO tasks_log (
            taskId,
            tasklogid,
            tasklogtype,
            userid,
            taskLogCreated,
            taskLogUpdated
        ) VALUES (%s, %s, %s, %s, %s, %s)
    '''
    val = (tasks_id, '2', 'delete', user_id, create_at(), create_at())
    mycursor.execute(sql, val)
    mydb.commit()
    print(f"{mycursor.rowcount} record inserted.")


def email_check_in():
    while True:
        try:
            email_in = email_input()
            mycursor = mydb.cursor()
            mycursor.execute(
                f'SELECT u.email FROM users AS u WHERE u.email like "%{email_in}%"')
            myresult = mycursor.fetchall()
            if len(myresult) != 0:
                print(f'{email_in}')
                return email_in
            else:
                raise
        except:
            print("Invalid email, try again.\n")


def email_check_new():
    while True:
        try:
            email_new = email_update()
            mycursor = mydb.cursor()
            mycursor.execute(
                f'SELECT u.email FROM users AS u WHERE u.email like "%{email_new}%"')
            myresult = mycursor.fetchall()
            if len(myresult) == 0:
                return email_new
            else:
                raise
        except:
            print(f"Duplicated email, try another one.\n")


def is_valid_email(email: str) -> bool:
    import re
    pattern = re.compile(r"^[\w\.\+-]+@[\w\.-]+\.[a-zA-Z]{2,}$")
    if not pattern.match(email):
        return False
    parts = email.split("@")
    if len(parts) != 2:
        return False
    domain = parts[1]
    if len(domain) < 4:
        return False
    return True


def check_email_in_database(email: str, mydb) -> bool:
    cursor = mydb.cursor()
    cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
    results = cursor.fetchall()
    for result in results:
        if result[0] == email:
            return True
    return False


def get_user_id(email):
    mydb = mysql.connector.connect(
        host="localhost",
        port="3500",
        user="root",
        password="admin",
        database="db1"
    )
    mycursor = mydb.cursor()
    mycursor.execute(
        f'SELECT u.Id FROM users AS u WHERE u.email like "{email}"')
    myresult = mycursor.fetchall()
    if myresult:
        return myresult[0][0]
    return None


def create_at_datetime():
    x = datetime.datetime.now()
    return x.strftime('%Y-%m-%d %H:%M:%S')


def view_task_avgdue(db1):
    mydb = mysql.connector.connect(
        host="localhost",
        port="3500",
        user="root",
        password="admin",
        database=db1
    )
    count = 0
    mycursor = mydb.cursor()
    mycursor.execute(
        '''
        select tasks_log.taskid
        -- ,DATEDIFF(tasks_log.taskLogUpdated,STR_TO_DATE(tasks.taskdue, '%d/%m/%Y')) as date_due
        ,concat(DATEDIFF(tasks_log.taskLogUpdated,STR_TO_DATE(tasks.taskdue, '%d/%m/%Y'))) as wording_datedue
        from tasks_log 
        inner join tasks on tasks.taskid = tasks_log.taskid
        where tasks_log.tasklogtype like 'approve'
        order by DATEDIFF(tasks_log.taskLogUpdated,STR_TO_DATE(tasks.taskdue, '%d/%m/%Y'))
        '''
    )
    myresult = mycursor.fetchall()
    for i in range(len(myresult)):
        count += int(myresult[i][1])
    if int(-(count/len(myresult))) >= 0:
        print(f'Reduce Time {int(-(count/len(myresult)))} task per Days')
    elif int(-(count/len(myresult))) < 0:
        print(f'late Time {int(-(count/len(myresult)))} task per Days')
    else:
        print(
            f"Can't reduce any tasks {int(-(count/len(myresult)))} task per Days")


def get_task_data(db1):
    mydb = mysql.connector.connect(
        host="localhost",
        port="3500",
        user="root",
        password="admin",
        database=db1
    )
    data = []
    mycursor = mydb.cursor()
    mycursor.execute(
        f'''
        SELECT 
        taskId,taskTitle,email,taskDue 
        ,DATE_FORMAT(created_at, "%d/%m/%Y")
        ,DATE_FORMAT(updated_at, "%d/%m/%Y")
        ,(CASE
        WHEN taskStatus = 1 THEN "In-Process"
        WHEN taskStatus = 2 THEN "Approved"
        WHEN taskStatus = 3 THEN "Declined"
        WHEN taskStatus = 4 THEN "Expired"
        WHEN taskStatus = 5 THEN "Deleted"
        ELSE "-"
        END) AS status
        FROM tasks 
        '''
    )
    myresult = mycursor.fetchall()
    for row in myresult:
        data.append(row)
    df = pd.DataFrame(data, columns=[
                      'taskId', 'taskTitle', 'email', 'taskDue', 'created_at', 'updated_at', 'status'])
    return df


def plot_task_status(db1):
    df = get_task_data(db1)
    plt.figure(figsize=(10, 5))
    sns.countplot(x='status', data=df)
    plt.title('Task Status Counts')
    plt.xlabel('Status')
    plt.ylabel('Count')
    plt.show()


def plot_task_create(db1):
    df = get_task_data(db1)
    plt.figure(figsize=(10, 5))
    df['created_at'] = pd.to_datetime(df['created_at'])
    df.groupby(df['created_at'].dt.date).count()['taskId'].plot(kind='bar')
    plt.title('Task Creation Dates')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.show()


def plot_task_duedate(db1):
    df = get_task_data(db1)
    plt.figure(figsize=(10, 5))
    df['taskDue'] = pd.to_datetime(df['taskDue'])
    plt.scatter(x=df['created_at'], y=df['taskDue'])
    plt.title('Task Due Dates vs. Creation Dates')
    plt.xlabel('Creation Date')
    plt.ylabel('Due Date')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    plt.show()

def create_createtask_log(tasks_id, user_email):
    user_id = get_user_id(user_email)
    mycursor = mydb.cursor()
    sql = '''
        INSERT INTO tasks_log (
            taskId,
            tasklogid,
            tasklogtype,
            userid,
            taskLogCreated,
            taskLogUpdated
        ) VALUES (%s, %s, %s, %s, %s, %s)
    '''
    val = (tasks_id, '1', 'create', user_id, create_at(), create_at())
    mycursor.execute(sql, val)
    mydb.commit()
    print(f"{mycursor.rowcount} record inserted Task Log.")

def create_updatetask_log_(tasks_id, user_email,taskstatus):
    user_id = get_user_id(user_email)
    if taskstatus == 1:
       taskstaus_name = 'In-Process'
    elif taskstatus == 2:
       taskstaus_name = 'approve'
    elif taskstatus == 3:
       taskstaus_name = 'Declined'
    elif taskstatus == 4:
       taskstaus_name = 'Expired'
    elif taskstatus == 5:
       taskstaus_name = 'Deleted'
    mycursor = mydb.cursor()
    sql = '''
        INSERT INTO tasks_log (
            taskId,
            tasklogid,
            tasklogtype,
            userid,
            taskLogCreated,
            taskLogUpdated
        ) VALUES (%s, %s, %s, %s, %s, %s)
    '''
    val = (tasks_id, taskstatus, 'delete', user_id, create_at(), create_at())
    mycursor.execute(sql, val)
    mydb.commit()
    print(f"{mycursor.rowcount} record inserted.")
