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

def save(lst):
    try:
        stu_txt = open(filename, 'a', encoding='utf-8')
    except ValueError:
        stu_txt = open(filename, 'w', encoding='utf-8')

    for item in lst:
        stu_txt.writelines(str(item) + '\n')
    stu_txt.close()

def search():
    pass

def delete():
    pass

def modify():
    pass

def sort():
    pass

def total():
    pass

def show():
    pass

main()   