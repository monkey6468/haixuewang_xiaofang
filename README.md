# 嗨学网_2020一级消防工程师

[嗨学网地址](http://highso.cn/v5/my/course)
基于python3，自学爬虫获取嗨学网2020一级消防工程师的视频

## 效果图
![](image/100.jpg)


## 一、使用
#### 1、需要通过网页获取csrf_token、cookie参数。
    
#### 2、进入`get_all_lesson_list_by_type.py`所在的文件路径，运行如下命令：
    ```
    python3 get_all_lesson_list_by_type.py 
    ```
    
    若参数设置正确，则可获取 相对数据的 `.csv`和 `.txt`文档数据。
    
    - csv：用于批量下载视频使用
    - txt：用于批量重命名视频使用
#### 3、批量下载视频功能，测试机器为MAC，提供软件`Motrix`
    下载地址：https://xclient.info/s/motrix.html
    
    视频地址必须放在`rename_file.py`同级目录的 `videos`下面。
    
#### 4、进入`rename_file.py`所在的文件路径，运行如下命令：
    ```
    python3 rename_file.py 
    ```
    通过选择类型，进入批量重命名视频操作。
    
    
#### 5、总结
    python3 的文件仅供参考，技术点包含了如下操作：
    
    - 文件的创建
    - 文件的写入（csv、txt）、读取(txt)，
    - 网络的数据请求（Get方式）
    - json数据的处理
    - 文件目录下的文件重命名
