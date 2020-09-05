#-*-coding:utf-8-*-
import os
import json

# 获取指定文件夹下所有文件名
def get_file_names(file_dir):
    for root, dirs, files in os.walk(file_dir):
        #print(root) #当前目录路径
        #print(dirs) #当前路径下所有子目录
        #print(files) #当前路径下所有非目录子文件
        return files

# 读全部内容
def get_lesson_name_list(file_path):
    txt_content_string = ''
    with open(file_path, "r") as f:  # 打开文件
        txt_content_string = f.read()  # 读取文件
    
    #print(txt_content_string)
    lesson_list = txt_content_string.split(';')

    # index:{}-name:{}-audioUrl:{}-lectureUrl:{}-videoUrl:{}-totalTime:
    lesson_list_dict = []
    for i in range(len(lesson_list)):
        item = lesson_list[i]
        # JSON字符串转换字典
        item_dict = json.loads(item)
        
        lesson_dict = {}
        lesson_dict['index'] = item_dict['index']
        lesson_dict['name'] = item_dict['name']
        
        videoUrl = item_dict['videoUrl']
        # 只分割最后一个
        videoUrl = videoUrl.rsplit("/",1)[1]
        
        lesson_dict['videoUrl'] = videoUrl
        lesson_list_dict.append(lesson_dict)
    return lesson_list_dict
    
def rename_video_file(file_dir_path, save_file_dir_path, lesson_list_dict):
    for item in lesson_list_dict:
        item_index = item['index']
        item_name = item['name']
        item_ideoUrl = item['videoUrl']
        
        old_Path = file_dir_path+'/'+item_ideoUrl
        #print(old_Path)
        new_Path = save_file_dir_path+'/'+'{}、'.format(item_index)+item_name+'.mp4'
        #print(new_Path)
        os.rename(old_Path, new_Path)

    print('重命名 成功')

if __name__ == '__main__':
    input_type = input('请输入类型：\n1-实务教材精讲\n2-综合教材精讲\n3-案例教材精讲\n：')
    
    video_file_name = 'videos'
    dirt_path = os.getcwd()
    file_dir_path = dirt_path+'/'+video_file_name
    print(file_dir_path)
    
    # 获取指定文件夹下所有文件名
    #files_list = get_file_names(file_dir_path)
    #print(files_list)
    
    txt_file_name = "1、实务教材精讲"
    # 必须 *
    if int(input_type) == 1:
        txt_file_name = '1、实务教材精讲'
    elif int(input_type) == 2:
        txt_file_name = '2、综合教材精讲'
    else:
        txt_file_name = '3、案例教材精讲'
    file_path = dirt_path+'/'+'脚本数据'+'/'+txt_file_name+'.txt'
    print(file_path)
    
    # 获取课程信息列表（字典数组）
    lesson_list_dict = get_lesson_name_list(file_path)
    print(lesson_list_dict)
    
    save_file_dir_path = dirt_path+'/'+txt_file_name
    # 判断目标是否存在
    if (os.path.exists(save_file_dir_path) == False):
        # 创建目录
        os.mkdir(save_file_dir_path)
    rename_video_file(file_dir_path, save_file_dir_path, lesson_list_dict)
    
