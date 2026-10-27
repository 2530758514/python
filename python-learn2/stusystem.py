import os

filename = 'student.txt'

def main():
    while True:
        menm()
        choice = int(input('请选择\n'))
        if choice in [0, 1, 2, 3, 4, 5, 6, 7]:
            if choice == 0:
                answer = input('确定退出吗?y/n\n')
                if answer == 'y' or answer == 'Y':
                    print('谢谢使用')
                    break
                else:
                    continue
            elif choice == 1:
                insert()
            elif choice == 2:
                search()
            elif choice == 3:
                delete()
            elif choice == 4:
                modify()
            elif choice == 5:
                sort()
            elif choice == 6:
                total()
            elif choice == 7:
                show() 

def menm(): 
    print('======菜单======')
    print('1. 录入信息')
    print('2. 查找信息')
    print('3. 删除信息')
    print('4. 修改信息')
    print('5. 排序')
    print('6. 统计学生总人数信息')
    print('7. 显示所有学生信息')
    print('0. 退出')

def insert():
    student_list = []
    while True:
        id = input('输入ID:')
        if not id:
            break
        name = input('输入姓名:')
        if not name:
            break

        try:
            english = int(input('英语:'))
            python = int(input('Python:'))
            java = int(input('Java:'))
        except ValueError:
            print('输入无效')
            continue

        student = {
            'id': id,
            'name': name,
            'english': english,
            'python': python,
            'java': java,
        }

        student_list.append(student)
        answer = input('是否继续添加?y/n\n')
        if answer == 'y':
            continue
        else:
            break

    save(student_list)
    print('学生信息录入完毕')

'''
def save1(lst):
    try:
        # stu_txt = open(filename, 'a', encoding='utf-8') # Use a context manager for opening files
        with open(filename, 'a', encoding='utf-8') as stu_txt:
            pass
    except ValueError:
        with open(filename, 'w', encoding='utf-8') as stu_txt:
                    pass
    for item in lst:
        stu_txt.writelines(str(item) + '\n')
    stu_txt.close()
'''
def save(lst):
    with open(filename, 'a', encoding='utf-8') as stu_txt:
        for item in lst:
            stu_txt.writelines(str(item) + '\n')

def search():
    pass

def delete():
    while True:
        student_id = input('删除ID')
        if student_id != '':
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as file:
                    student_old = file.readlines()
            else:
                student_old = []
            flag = False
            if student_old:
                with open(filename, 'w', encoding='utf-8') as wfile:
                    d = {}
                    for item in student_old:
                        d = dict(eval(item))
                        if d['id'] != student_id:
                            wfile.write(str(d) + '\n')
                        else:
                            flag = True
                    if flag:
                        print(f'已经删除了{student_id}的学生')
                    else:
                        print(f'没有找到{student_id}的学生')
            else:
                print('无学生信息')
                break
            show()
            answer = input('是否继续删除?y/n\n')
            if answer == 'y':
                continue
            else:
                break

def modify():
    show()
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as rfile:
            student_old = rfile.readlines()
    else:
        return
    student_id = input('修改学生ID')
    with open(filename, 'w', encoding='utf-8') as wfile:
        for item in student_old:
            d = dict(eval(item))
            if d['id'] == student_id:
                print('找到匹配学生，开始修改')
                while True:
                    try:
                        d['name'] = input('名字')
                        d['english'] = input('英语')
                        d['python'] = input('Python')
                        d['java'] = input('Java')
                    except:
                        print('输入有误')
                    else:
                        break
                wfile.write(str(d) + '\n')
                print('修改完成')
            else:
                wfile.write(str(d) + '\n')
        answer = input('继续修改?y/n\n')
        if answer == 'y':
            modify()

def sort():
    pass

def total():
    pass

def show():
    pass

main()   