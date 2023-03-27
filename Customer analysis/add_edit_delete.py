import mysql.connector
import number
from number import *
import datetime
from backup_txt import *

# USER (P'Ging)
# function ดูข้อมูล View function -- Choose Users(data clean)
def view_user_data(db1):
  mydb = mysql.connector.connect(
  host="localhost",
  port = "3500",
  user="root",
  password="admin",
  database=db1
)
  mycursor = mydb.cursor()
  email = input('Please enter your email to filter :')
  while True:
    try:
        status = int(float(input('Please select status\n0 : Inactive\n1 : active\nselect : ')))
        if status == 1:
            status = '1'
            break
        else:
            break
    except:
        print('Invalid option')
  mycursor.execute(
      f'''
      SELECT 
      u.Id , u.email ,c.companyName
      ,(CASE
	    WHEN status = 1 THEN "Active"
	    ELSE "Inactive"
      END) AS status
      FROM users AS u
      INNER JOIN companies AS c on c.Id = u.companyId
      WHERE u.email like '%{email}%' and u.status like '%{status}%'
      '''
      )
  myresult = mycursor.fetchall()
  for i,x in enumerate (myresult):
    print(f"{i+1} {x}")

# function เพิ่มข้อมูล Create function -- Users (Must data) Generate UID
def create_user_data(db1):
  mydb = mysql.connector.connect(
  host="localhost",
  port = "3500",
  user="root",
  password="admin",
  database=db1
)
  mycursor = mydb.cursor()
  sql = "INSERT INTO users (Id, email,status, companyId) VALUES (%s, %s, %s, %s)"
  val = (generate_uid(), email_input(),'1','C211110000002') # ใส่ตัวแปรตรงแถวนี้
  mycursor.execute(sql, val)
  mydb.commit()
  log('user log.txt', val)
  print(mycursor.rowcount, "record inserted.")
    
# function เเก้ไขข้อมูล Updated -- Users (Filter, rename data) -- 
def update_user_data(db1):
  mydb = mysql.connector.connect(
  host="localhost",
  port = "3500",
  user="root",
  password="admin",
  database=db1
)
  while True:
    try:
        email_in = email_check_in()
        if is_valid_email(email_in) and check_email_in_database(email_in, mydb):
            pass
        else:
            raise
        email_new = email_check_new()
        if is_valid_email(email_in):
            pass
        else:
            raise
        mycursor = mydb.cursor()
        sql = "UPDATE users SET email = %s WHERE email = %s"   # ใส่ตัวแปรตรงแถวนี้
        val = (email_new,email_in)
        mycursor.execute(sql,val)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")
        if mycursor.rowcount == 0:
            raise ValueError('')
    
    except ValueError:
      print("The email is existing, please try another email.\n")
    break

def delete_user_data(db1):
    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        port="3500",
        user="root",
        password="admin",
        database=db1
    )

    try:
        email_in = input('Please enter your email to delete :')
        if is_valid_email(email_in) and check_email_in_database(email_in, mydb):
            pass
        else:
            raise
        mycursor = mydb.cursor()
        sql = "UPDATE users As u SET u.status = '0' WHERE u.Id = %s"
        print(email_in)
        val = (get_user_id(email_in),)
        print(val)
        mycursor.execute(sql, val)
        mydb.commit()

        print(mycursor.rowcount, "record(s) deleted")
        if mycursor.rowcount == 0:
            print("The email is not exist.\n")

    except:
        print("An error occurred while deleting the user data.\n")

# Tasks (P'Pip)
# function ดูข้อมูล View function -- Choose Users and Tasks Log (data clean)
def view_task_data(db1):
  mydb = mysql.connector.connect(
  host="localhost",
  port = "3500",
  user="root",
  password="admin",
  database=db1
)
  while True:
    try:
      mycursor = mydb.cursor()
      tasktitle = input('Please enter your Tasktiltle to filter : ')
      email_view = input('Please enter your email to filter : ')
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
          WHERE taskTitle like "%{tasktitle}%" AND email like "%{email_view}%"
          '''
          )
      myresult = mycursor.fetchall()
      for i,x in enumerate (myresult):
        print(f"{i+1} {x}")
      return tasktitle,email_view
    except:
      print("Don't find any Taks")
  
# function เพิ่มข้อมูล Create function -- Tasks (Must data) Generate TaskID tasklog
def create_task_data(user_email,db1):
  mydb = mysql.connector.connect(
  host="localhost",
  port = "3500",
  user="root",
  password="admin",
  database=db1
  )
  a = generate_tasksid()
  mycursor = mydb.cursor()
  sql = "INSERT INTO tasks (taskId,email,taskTitle,taskDue,taskType,created_by,updated_by,created_at,updated_at,taskStatus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
  val = (a,email_input(),freetext(),taskdue_input(),'1',get_user_id(user_email),get_user_id(user_email),create_at(),create_at(),'1') # ใส่ตัวแปรตรงแถวนี้
  mycursor.execute(sql, val)
  mydb.commit()
  print(mycursor.rowcount, "record inserted.")
  log('tasks log.txt', val)
  create_createtask_log(a, user_email)

# function เเก้ไขข้อมูล Updated -- Task (Filter, rename data)
def update_task_data(user_email,db1):
  mydb = mysql.connector.connect(
  host="localhost",
  port = "3500",
  user="root",
  password="admin",
  database=db1
)
  while True:
    try:
      tasks_id = input("Please input your task ID to Update: ")
      if not tasks_id:
        raise ValueError("Task ID cannot be empty")
      mycursor = mydb.cursor()
      mycursor.execute(f"SELECT * FROM tasks WHERE taskId = '{tasks_id}'")
      result = mycursor.fetchone()
      if not result:
        raise ValueError("Task ID does not exist in the database")
      tasktitle = input("Please input your tasktitle to Update: ")
      taskstatus = input('''1 = "In-Process"\n2 = "Approved"\n3 = "Declined"\n4 = "Expired"\n5 = "Deleted"\nPlease input your taskstatus to Update: ''')
      if taskstatus not in ['1', '2', '3', '4', '5']:
        raise ValueError("Task status is not true")
      mycursor = mydb.cursor()
      sql = "UPDATE tasks SET taskTitle = %s,updated_by = %s, updated_at = %s ,taskStatus = %s WHERE taskId = %s"
      val = (tasktitle,get_user_id(user_email),create_at_datetime(),taskstatus,tasks_id)
      mycursor.execute(sql, val)
      mydb.commit()
      print(mycursor.rowcount, "record(s) affected")
      create_updatetask_log_(tasks_id,user_email,taskstatus)
      break
    except ValueError as e:
       print(e)

def delete_task_data(user_email,db1):
  mydb = mysql.connector.connect(
  host="localhost",
  port = "3500",
  user="root",
  password="admin",
  database=db1
)
  view_task_data(db1)
  while True:
    try:
        tasks_id = input("Please input your task ID to delete: ")
        if not tasks_id:
            raise ValueError("Task ID cannot be empty")
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM tasks WHERE taskId = '{tasks_id}'")
        result = mycursor.fetchone()
        if not result:
            raise ValueError("Task ID does not exist in the database")
        sql = "DELETE FROM tasks WHERE taskId = %s"
        adr = (tasks_id,)
        mycursor.execute(sql, adr)
        mydb.commit()
        print(f"{mycursor.rowcount} record(s) deleted")
        create_task_log(tasks_id,user_email)
        break
    except ValueError as e:
        print(e)