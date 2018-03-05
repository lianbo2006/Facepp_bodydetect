#pic_detect.py

import requests
import json
from pprint import pprint
import time
import cv2
import key_secret


def body_detector(response):
    req_con = response.content.decode('utf-8')
    req_dict = json.loads(req_con)
    pprint(req_dict)
    pic_ori = cv2.imread(pic_path)
    img_rectangle = pic_ori
    for humanbody in req_dict['humanbodies']:
        confidence = humanbody.get('confidence')
        if confidence < 85:
            continue
        else:
            lower_body_cloth_color_rgb_1 = humanbody.get('attributes').get('upper_body_cloth').get(
                'upper_body_cloth_color_rgb')
            humanbody_rectangle = humanbody.get('humanbody_rectangle')
            img_rectangle = cv2.rectangle(img_rectangle,
                                          (humanbody_rectangle.get('left'), humanbody_rectangle.get('top')),
                                          (humanbody_rectangle.get('left') + humanbody_rectangle.get('width'),
                                           humanbody_rectangle.get('top') + humanbody_rectangle.get('height')),
                                          (lower_body_cloth_color_rgb_1.get('b'),
                                           lower_body_cloth_color_rgb_1.get('g'),
                                           lower_body_cloth_color_rgb_1.get('r')), 2)
            if humanbody.get('attributes').get("gender").get("male") >= humanbody.get('attributes').get(
                    "gender").get("female"):
                gender_value = "male"
                gender_confidence = humanbody.get('attributes').get("gender").get("male")
            else:
                gender_value = "female"
                gender_confidence = humanbody.get('attributes').get("gender").get("female")
            gender_info = gender_value + " " + str(gender_confidence)
            img_rectangle = cv2.putText(img_rectangle,
                                        gender_info,
                                        (humanbody_rectangle.get('left'), humanbody_rectangle.get('top') - 5),
                                        cv2.FONT_HERSHEY_PLAIN, 1,
                                        (lower_body_cloth_color_rgb_1.get('b'),
                                         lower_body_cloth_color_rgb_1.get('g'),
                                         lower_body_cloth_color_rgb_1.get('r')),
                                        2, False)
    cv2.imwrite(result_pic_path, img_rectangle)
    print("写入新文件:{}".format(result_pic_path))
    time_end = time.time()  # 计时结束标签
    print("总计用时:{:.2f}s".format(time_end - time_start))
    win = cv2.namedWindow("img_rectangle")
    cv2.imshow("img_rectangle", img_rectangle)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def file_name_creater():
    path_list = pic_path.split("\\")
    pic_full_name = path_list[-1]
    pic_full_name_list = pic_full_name.split(".")
    pic_name, pic_ext = pic_full_name_list[0], pic_full_name_list[1]
    result_pic_name = pic_name + "_result"
    result_pic_full_name =  result_pic_name + "." + pic_ext
    result_pic_path = pic_path.replace(pic_full_name,result_pic_full_name)
    return result_pic_path


def main():
    global time_start, pic_path, result_pic_path
    time_start = time.time()  # 计时起始标签
    pic_path = r"body_detect/1.jpg"
    result_pic_path = file_name_creater()
    http_url = "https://api-cn.faceplusplus.com/humanbodypp/v1/detect"
    key = key_secret.key
    secret = key_secret.secret
    print("文件目录为:{:}".format(pic_path))
    file = open(pic_path, "rb")
    data = {"api_key": key,
            "api_secret": secret,
            "return_attributes": "gender,upper_body_cloth,lower_body_cloth"}
    file_post = {"image_file": file}
    response = requests.post(http_url, data=data, files=file_post)
    file.close()
    body_detector(response)

if __name__ == '__main__':
    main()