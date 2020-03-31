# encoding:utf-8
import requests
import base64
import json


def Get_API():  #To obtain API

    #Register Baidu intelligent cloud face comparison interface to obtain API Key and Secret Key.
    client_id = 'API Key'    
    client_secret = 'Secret Key'    #Please replace when using
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'%(client_id,client_secret)

    #Construct a function,request the value of the Access_token from the server and generate the face comparison API.
    response=requests.get(host)  #Construct a url object from requests.get(url) that requests a resource from the server
    access_token=eval(response.text)['access_token']  #Returns the value of the requested str and takes out the "access_token"
    request_url='https://aip.baidubce.com/rest/2.0/face/v3/match'
    API = request_url + "?access_token=" + access_token      #Stitching API
    #API = "https://aip.baidubce.com/rest/2.0/face/v3/match"+"?access_token="+access_token    

    return API 


def Image_coding(img1,img2):   #Base64 encoding of the images

    f=open(r'%s' % img1,'rb')     
    pic1=base64.b64encode(f.read())     #Image1 Base64 encoding
    f.close()    
    f=open(r'%s' % img2,'rb')     
    pic2=base64.b64encode(f.read())    #Image2 Base64 encoding
    f.close()
    params=json.dumps([
        {"image":str(pic1,"utf-8"),"image_type":'BASE64',"face_type":"LIVE"},
        {"image":str(pic2,"utf-8"),"image_type":'BASE64',"face_type":"IDCARD"}])

    #Add a "liveness_control" option to identify if the person in the picture is a real person
    '''params=json.dumps([
        {"image":str(pic1,"utf-8"),"image_type":'BASE64',"face_type":"LIVE","liveness_control": "HIGH"},
        {"image":str(pic2,"utf-8"),"image_type":'BASE64',"face_type":"IDCARD","liveness_control": "HIGH"}])'''
    
    return params  #Return image parameters


def Image_contrast(img1,img2):   #Analyze images and compare them

    API=Get_API()    #obtain API
    params=Image_coding(img1,img2)   #Base64 encoding of the images
    content=requests.post(API,params).text   #Requests for posts are sent as form forms
    score=eval(content)['result']['score']   #Calculate the score
    if score>=60:     #Set the threshold
        print('二人相似度得分为 %s, 是同一人的可能性极大'%str(score))
    else:
        print('二人相似度得分为 %s, 不是同一人的可能性极大'%str(score))

Image_contrast("1.png","4.jpg")     #To run the program
