import mysql.connector
from number import *
from add_edit_delete import *
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates


def view_most_users_done(db1):
    mydb = mysql.connector.connect(
    host="localhost",
    port = "3500",
    user="root",
    password="admin",
    database=db1
)
    mycursor = mydb.cursor()
    mycursor.execute(
        '''
        select count(tasks.taskId) as freq,users.email 
        from tasks 
        inner join users on users.Id = tasks.created_by
        group by email 
        order by 1 desc
        limit 5
        '''
        )
    myresult = mycursor.fetchall()
    plot_task_status(db1)
    print("******************")
    print("Top 5 Active Users") #อาจต้องเปลี่ยน wording อีกที
    for i,x in enumerate(myresult):
        print(i+1,x)
    log("top 5.txt", myresult)
    

def view_task_due(db1):
    mydb = mysql.connector.connect(
    host="localhost",
    port = "3500",
    user="root",
    password="admin",
    database=db1
)
    mycursor = mydb.cursor()
    mycursor.execute(
        '''
        select tasks_log.taskid
        -- ,DATEDIFF(tasks_log.taskLogUpdated,STR_TO_DATE(tasks.taskdue, '%d/%m/%Y')) as date_due
        ,concat(
        case 
        when DATEDIFF(tasks_log.taskLogUpdated,STR_TO_DATE(tasks.taskdue, '%d/%m/%Y')) >  0 then 'late'
        when DATEDIFF(tasks_log.taskLogUpdated,STR_TO_DATE(tasks.taskdue, '%d/%m/%Y')) <  0 then 'early'
        when DATEDIFF(tasks_log.taskLogUpdated,STR_TO_DATE(tasks.taskdue, '%d/%m/%Y')) =  0 then 'ontime'
        end , ' '
        ,abs(DATEDIFF(tasks_log.taskLogUpdated,STR_TO_DATE(tasks.taskdue, '%d/%m/%Y')) ),' ','day') as wording_datedue
        from tasks_log 
        inner join tasks on tasks.taskid = tasks_log.taskid
        where tasks_log.tasklogtype like 'approve'
        order by DATEDIFF(tasks_log.taskLogUpdated,STR_TO_DATE(tasks.taskdue, '%d/%m/%Y'))
        '''
        )
    myresult = mycursor.fetchall()
    plot_task_duedate(db1)
    plot_task_create(db1)
    print("*********************") 
    print("Task sort by date due") 
    for i,x in enumerate(myresult):
        print(i+1,x)
    view_task_avgdue(db1)
    log("task due log.txt", myresult)


def view_classify_tasks(db1):
    mydb = mysql.connector.connect(
    host="localhost",
    port = "3500",
    user="root",
    password="admin",
    database=db1
)
    mycursor = mydb.cursor()
    mycursor.execute(
        '''
        select 
        count(case 
        when taskTitle like '%ไฟ%' or taskTitle like '%เดินทาง%' or taskTitle like '%โทรศัพท์%' or taskTitle like '%เน็ต%' or taskTitle like '%น้ำ%'  then 'miscellaneous expenses' 
        when taskTitle like '%หุ้น%' or taskTitle like '%เพิ่มทุน%' then 'asset'
        when taskTitle like '%บริหาร%' or taskTitle like '%management%'  then 'management'
        when taskTitle like '%แมส%' or taskTitle like '%จ้าง%' then 'wage'
        when taskTitle like '%ผลิต%' then 'produce'
        when taskTitle like '%ผล%' then 'result lab'
        when taskTitle like '%ค่าสึกหรอ%' then 'depreciation'
        when taskTitle like '%ค่าเช่า%' then 'leasing'
        when taskTitle like '%ค่า%' or taskTitle like '%ซื้อ%' then 'expense'
        when taskTitle like '%เบิก%' or taskTitle like '%Adv%'  then 'Advance'
        when taskTitle like '%ยืม%' then 'loan'
        when taskTitle like '%ภาษี%' or taskTitle like '%ภงด%' then 'tax'
        when taskTitle like '%บรรจุ%' then 'Recruit'
        when taskTitle like '%ขาย%' then 'revenue'
        when taskTitle like '%ให้ความช่วยเหลือทางการเงิน%' then 'donate'
        when taskTitle like '%อนุมัติ%' or taskTitle like '%memo%' then 'acceptance'
        else 'other'
        end) as f,
        -- taskTitle,
        case 
        when taskTitle like '%ไฟ%' or taskTitle like '%เดินทาง%' or taskTitle like '%โทรศัพท์%' or taskTitle like '%เน็ต%' or taskTitle like '%น้ำ%'  then 'miscellaneous expenses' 
        when taskTitle like '%หุ้น%' or taskTitle like '%เพิ่มทุน%' then 'asset'
        when taskTitle like '%บริหาร%' or taskTitle like '%management%'  then 'management'
        when taskTitle like '%แมส%' or taskTitle like '%จ้าง%' then 'wage'
        when taskTitle like '%ผลิต%' then 'produce'
        when taskTitle like '%ผล%' then 'result lab'
        when taskTitle like '%ค่าสึกหรอ%' then 'depreciation'
        when taskTitle like '%ค่าเช่า%' then 'leasing'
        when taskTitle like '%ค่า%' or taskTitle like '%ซื้อ%' then 'expense'
        when taskTitle like '%เบิก%' or taskTitle like '%Adv%'  then 'Advance'
        when taskTitle like '%ยืม%' then 'loan'
        when taskTitle like '%ภาษี%' or taskTitle like '%ภงด%' then 'tax'
        when taskTitle like '%บรรจุ%' then 'Recruit'
        when taskTitle like '%ขาย%' then 'revenue'
        when taskTitle like '%ให้ความช่วยเหลือทางการเงิน%' then 'donate'
        when taskTitle like '%อนุมัติ%' or taskTitle like '%memo%' then 'acceptance'
        else 'other'
        end as group_task
        from tasks
        group by 2
        order by 1 desc
        '''
        )
    myresult = mycursor.fetchall()
    print("*************")
    print("Classify Task") #อาจต้องเปลี่ยน wording อีกที
    print("*************")
    for x in (myresult):
        print(x)
    log("classify tasks log.txt", myresult)