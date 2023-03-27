import number as n
import add_edit_delete as crud
from number import *
import analyze
import backup_txt
import mysql.connector


db_input = input("input you database : ")

mydb = mysql.connector.connect(
  host="localhost",
  port = "3500",
  user="root",
  password="admin",
  database=db_input
)

while True:
    try:
        user_email = input('Please input your email to login: ')
        if is_valid_email(user_email) and crud.check_email_in_database(user_email, mydb):
            print("This is a valid email address.")
            break
        else:
            raise
    except Exception as e :
        print(e)
        print("This is not a valid email address.")
        input("...")


def main():
    DFCMD = [False]*3
    cmd = [*DFCMD]
    while True:
        try:
            if cmd[0] == False:
                show_menu(cmd, title="Home Page", choices=["Analyze","Setting"])
                cmd[0] = cmd[0] if cmd[0] else int(input("Enter: "))
            if cmd[0] == 1:
                if cmd[1] == False:
                    show_menu(cmd, title="(Analyze)menu 1", choices=["Classify Tasks ","Top 5 user's performance ","Tasks Due", "back", "main menu"])
                    cmd[1] = cmd[1] if cmd[1] else int(input("Enter: "))
                if cmd[1] == 1:
                    analyze.view_classify_tasks(db_input)
                    pwd(cmd)
                    input("...")
                    cmd = cmd[:1] + DFCMD[1:]
                elif cmd[1] == 2:
                    analyze.view_most_users_done(db_input)
                    pwd(cmd)
                    input("...")
                    cmd = cmd[:1] + DFCMD[1:]
                elif cmd[1] == 3:
                    analyze.view_task_due(db_input)                    
                    pwd(cmd)
                    input("...")
                    cmd = cmd[:1] + DFCMD[1:]
                elif cmd[1] == 4:
                    print("\n[back] ", end="")
                    pwd(cmd)
                    input("...")
                    cmd = cmd[:0] + DFCMD[0:]
                elif cmd[1] == 5:
                    print("\n[main menu] ", end="")
                    pwd(cmd)
                    input("...")
                    cmd = [*DFCMD]
                else:
                    print("Not match any choices")
                    input("...")
                    cmd = cmd[:1] + DFCMD[1:]
            elif cmd[0] == 2:
                if cmd[1] == False:
                    show_menu(cmd, title="Setting", choices=["tasks","users", "back", "main menu"])
                    cmd[1] = cmd[1] if cmd[1] else int(input("Enter: "))
                if cmd[1] == 1:
                    if cmd[2] == False:
                        show_menu(cmd, title="tasks", choices=["View tasks Table","Insert tasks Table","Update tasks Table","Delete tasks Table", "back", "main menu"])
                        cmd[2] = cmd[2] if cmd[2] else int(input("Enter: "))
                    if cmd[2] == 1:
                        show_menu(cmd, title="View tasks Table")
                        crud.view_task_data(db_input)
                        print(f"{'View tasks Table':^20}")
                        input("...")
                        cmd = cmd[:2] + DFCMD[2:]
                    elif cmd[2] == 2:
                        show_menu(cmd, title="Insert tasks Table")
                        crud.create_task_data(user_email,db_input)
                        print(f"{'Insert tasks Table':^20}")
                        input("...")
                        cmd = cmd[:2] + DFCMD[2:]
                    elif cmd[2] == 3:
                        show_menu(cmd, title="Update tasks Table")
                        crud.update_task_data(user_email,db_input)
                        print(f"{'Update tasks Table':^20}")
                        input("...")
                        cmd = cmd[:2] + DFCMD[2:]
                    elif cmd[2] == 4:
                        show_menu(cmd, title="Delete tasks Table")
                        crud.delete_task_data(user_email,db_input)
                        print(f"{'Delete tasks Table':^20}")
                        input("...")
                        cmd = cmd[:2] + DFCMD[2:]
                    elif cmd[2] == 5:
                        show_menu(cmd, title="back")
                        pwd(cmd)
                        input("...")
                        cmd = cmd[:1] + DFCMD[1:]
                    elif cmd[2] == 6:
                        show_menu(cmd, title="main menu")
                        pwd(cmd)
                        input("...")
                        cmd = [*DFCMD]
                    else:
                        print("Not match any choices")
                        input("...")
                        cmd = cmd[:2] + DFCMD[2:]
                elif cmd[1] == 2:
                    if cmd[2] == False:
                        show_menu(cmd, title="users", choices=["View users Table","Insert users Table","Update users Table","Delete users Table", "back", "main menu"])
                        cmd[2] = cmd[2] if cmd[2] else int(input("Enter: "))
                    if cmd[2] == 1:
                        show_menu(cmd, title="View users Table")
                        crud.view_user_data(db_input)
                        print(f"{'View users Table':^20}")
                        input("...")
                        cmd = cmd[:2] + DFCMD[2:]
                    elif cmd[2] == 2:
                        show_menu(cmd, title="Insert users Table")
                        crud.create_user_data(db_input)
                        print(f"{'Insert users Table':^20}")
                        input("...")
                        cmd = cmd[:2] + DFCMD[2:]
                    elif cmd[2] == 3:
                        show_menu(cmd, title="Update users Table")
                        crud.update_user_data(db_input)
                        print(f"{'Update users Table':^20}")
                        input("...")
                        cmd = cmd[:2] + DFCMD[2:]
                    elif cmd[2] == 4:
                        show_menu(cmd, title="Delete users Table")
                        crud.delete_user_data(db_input)
                        print(f"{'Delete users Table':^20}")
                        input("...")
                        cmd = cmd[:2] + DFCMD[2:]
                    elif cmd[2] == 5:
                        show_menu(cmd, title="back")
                        pwd(cmd)
                        input("...")
                        cmd = cmd[:1] + DFCMD[1:]
                    elif cmd[2] == 6:
                        show_menu(cmd, title="main menu")
                        pwd(cmd)
                        input("...")
                        cmd = [*DFCMD]
                    else:
                        print("Not match any choices")
                        input("...")
                        cmd = cmd[:2] + DFCMD[2:]
                elif cmd[1] == 3:
                    print("\n[back] ", end="")
                    pwd(cmd)
                    input("...")
                    cmd = cmd[:0] + DFCMD[0:]
                elif cmd[1] == 4:
                    print("\n[main menu] ", end="")
                    pwd(cmd)
                    input("...")
                    cmd = [*DFCMD]
                else:
                    print("Not match any choices")
                    input("...")
                    cmd = cmd[:1] + DFCMD[1:]
            else:
                print("Not match any choices")
                input("...")
                cmd = [*DFCMD]
            
        except Exception as e:
            print(e)
            print("Ops! Unexcepted error!")
            input("...")
            pass

def pwd(cmd):
    print(f"~/{'/'.join([str(x) for x in cmd if x])}")

def show_menu(cmd, title="Untitled", choices=[]):
    print(f"\n[{title}] ", end="")
    pwd(cmd)
    if len(choices) > 0:
        print("Please select menu")
        print("\n".join([f"[{idx+1}] {txt}" for idx,txt in enumerate(choices)]))

main()
