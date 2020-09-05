# -*- coding:UTF-8 -*-
import requests
import json
import csv
import os


def write_to_csv(filename, lesson_list):
    with open(filename,"w") as csvfile:
        writer = csv.writer(csvfile)

        # 判断是否有内容
        size = os.path.getsize(filename)
        if size == 0:
            writer.writerow([u'序号', u'名称', u'音频地址', u'课件地址', u'视频地址', u'视频时长'])

        #写入多行用writerows
        for item in lesson_list:
            index = item['index']
            name = item['name']
            audioUrl = item['audioUrl']
            lectureUrl = item['lectureUrl']
            videoUrl = item['videoUrl']
            totalTime = item['totalTime']
            
            writer.writerow([index, name, audioUrl, lectureUrl, videoUrl, totalTime])
        

def get_headers(cookie):
    headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
       'Accept': '*/*',
       'Accept-Encoding': 'gzip, deflate, br',
       'Accept-Language': 'zh-CN,zh;q=0.9',
       'Content-Type':'application/form-urlencode',
       'Cookie':cookie
    }
    return headers

# 获取所有课程列表
def get_lesson_list(csrf_token, goodsModuleId , url, headers):
    url='{}?csrf_token={}&goodsModuleId={}'.format(url,csrf_token,goodsModuleId)
    #print(url)
    
    lesson_list_string = []
    lesson_list_dict = []
    try:
        response = requests.get(url, data=None, headers=headers)
        if not response.status_code == 200:
            print('请求失败')
            return lesson_list_string,lesson_list_dict
            
        result_dict = json.loads(response.text)['data']
        
        result_errorCode = json.loads(response.text)['code']
        if result_errorCode != 0:
            print("======列表获取成功======")
            for i in range(len(result_dict['videoList'])):
                item = result_dict['videoList'][i]
                # 获取单个课程信息
                url_lesson_list = 'http://highso.cn/study/pc/video/download'
                videoId = item['id']
                totalTime = item['totalTime']
                m, s = divmod(int(totalTime), 60)
                totalTime = "%02d:%02d" % (m, s)
                lesson_dict = get_lesson_info(csrf_token, videoId, url_lesson_list, headers)
                
                i +=1
                print("      正在获取数据{}/{}      ".format(i, len(result_dict['videoList'])))
                
                list_dict = {}
                list_dict['index'] = i
                list_dict['name'] = item['name']
                list_dict['audioUrl'] = lesson_dict['audioUrl']
                list_dict['lectureUrl'] = lesson_dict['lectureUrl']
                list_dict['videoUrl'] = lesson_dict['videoUrl']
                list_dict['totalTime'] = totalTime
                print(list_dict)
                lesson_list_dict.append(list_dict)
                
                row_data = json.dumps(list_dict)
                #print(row_data)
                lesson_list_string.append(row_data)
        else:
            print("======列表获取失败======")
        return lesson_list_string,lesson_list_dict
    except Exception as e:
            print("======获取失败======{}".format(e))
            return lesson_list_string,lesson_list_dict

# 获取单个课程信息
def get_lesson_info(csrf_token, videoId, url, headers):
    url='{}?csrf_token={}&videoId={}'.format(url,csrf_token,videoId)
    #print(url)
    response = requests.get(url, data=None, headers=headers)
    result_dict = json.loads(response.text)['data']
    
    lesson_dict = {}
    lesson_dict['audioUrl'] = result_dict['audioUrl']
    lesson_dict['lectureUrl'] = result_dict['lectureUrl']
    videoUrl = result_dict['videoUrl'].split('?')[0]
    lesson_dict['videoUrl'] = videoUrl
    #print(lesson_dict)
    return lesson_dict


def get_save_all_lesson(file_name, csrf_token, goodsModuleId, url_lesson_list, headers):
    url_lesson_list_string, lesson_list_dict = get_lesson_list(csrf_token, goodsModuleId, url_lesson_list, headers)
    #print(lesson_list)
    
    print("======正在写入文件======")
    write_to_csv('{}.csv'.format(file_name), lesson_list_dict)
    print("======写入文件完成======")
    
    lesson_list_all_string = ''
    for i in range(len(url_lesson_list_string)):
        item = url_lesson_list_string[i]
        if (i != len(url_lesson_list_string)-1):
            lesson_list_all_string += item+';'
        else:
            lesson_list_all_string += item
    #print(lesson_list_all_string)
        
    # 将结果输出并存储
    with open('{}.txt'.format(file_name),"w") as file:
        file.write(lesson_list_all_string+'\n')
                
    # http://highso.cn/study/pc/video/download?csrf_token=be2R5k&videoId=98181
    # http://highso.cn/study/pc/goodsmodule/findbyid?csrf_token=be2R5k&goodsModuleId=18385
    
if __name__ == '__main__':
    
    input_type = input('首先请保重csrf_token、cookie正确(根据调试具有这两个参数实时性)，请输入goodsModuleId：\n1-实务教材精讲:18385\n2-综合教材精讲:18387\n3-案例教材精讲:18389\n：')
    # 必须 *
    csrf_token = 'KIMCIM'
    
    # 必须 *
    cookie='__jsluid_h=6bf1eb16beb6abe31ebd64c264e63bb8; gr_user_id=cbf469e0-8b64-4865-bab4-7c909501708f; grwng_uid=c522ecc4-e18a-4b91-b7d1-1245d3c547e2; deviceType=NORMAL; pageNum=0; 88da63a710494189_gr_last_sent_cs1=28770711; haixue_playback_bj=1599235513178; H_U_C=28770711%2C18520156468_6598%40haixue.com%2C%E5%AD%A6%E5%91%9828770711; U_N_C=18520156468; pass_sec=8df95c2dcd4b492a8885890f4114a1a3.28770711.1599265124674.web.bd24c901af498381232d01107699a102; csrf_token=KIMCIM; security_refresh=8df95c2dcd4b492a8885890f4114a1a3.28770711.1599265124674.web.bd24c901af498381232d01107699a102; 88da63a710494189_gr_session_id=970eedde-5b31-4399-ac27-e22bc0751462; 88da63a710494189_gr_last_sent_sid_with_cs1=970eedde-5b31-4399-ac27-e22bc0751462; security=d0d93f53-a58e-4dd8-a2aa-56df30f92876.1599274564647.28770711.web.53654bf197e425221479becf8f212e3d; 88da63a710494189_gr_session_id_970eedde-5b31-4399-ac27-e22bc0751462=true; security_access=eyJhbGciOiJSUzUxMiJ9.eyJ1aWQiOjI4NzcwNzExLCJzdWIiOiJ3ZWIiLCJpc3MiOiJwYXNzcG9ydCIsImV4cCI6MTU5OTI3NTU3NCwiaWF0IjoxNTk5Mjc1Mjc0LCJqdGkiOiIyNmUxNjgwMi0zMGZlLTRkZGEtYWFiYy1jNThmNGM0MGM0MjIifQ.fWBRQFbqECet67sg2DDENYoNOZTniZv0BAwoVwnBbJkiwwOPxnjK7rkhGQL2cLhUvi3KaLOl9PETNUWLAf0yc9hnZ3MaE20OXGKa5GGI962id1BHhI5OsqAsgwu3znf5_cu0mKQOrXL3xp3nJRzhD8fpT6p9MxIuYbvNOdvhKEc; 88da63a710494189_gr_cs1=28770711; JSESSIONID=72C17CA7EED4367A7F57C72512A788B3'
    headers = get_headers(cookie)
    
    filename = ''
    # 必须 *
    goodsModuleId = ''
    if int(input_type) == 1:
        filename = '1、实务教材精讲'
        goodsModuleId = 18385
    elif int(input_type) == 2:
        filename = '2、综合教材精讲'
        goodsModuleId = 18387
    elif int(input_type) == 3:
        filename = '3、案例教材精讲'
        goodsModuleId = 18389
    else:
        filename = input_type
        goodsModuleId = input_type
    print(filename)
    print(goodsModuleId)
    
    #print(filename)
    
    # 获取并保存所有课程列表
    url_lesson_list = 'http://highso.cn/study/pc/goodsmodule/findbyid'
    get_save_all_lesson(filename, csrf_token, goodsModuleId, url_lesson_list, headers)
    print("======脚本执行完成======")
