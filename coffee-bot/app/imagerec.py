import os
import math
from io import BytesIO

import requests
from PIL import Image

def resize_image(image, size=1024):
    image_bytesio = BytesIO(image)
    pilimage = Image.open(image_bytesio)
    pilimage.thumbnail((size,size))
    print(f"Image resized to {pilimage.size}")

    new_bytes = BytesIO()
    pilimage.save(new_bytes, format='png')

    return new_bytes.getvalue()

def FaceRecognition(image):
    ###############################################
    #### Update or verify the following values. ###
    ###############################################
    # Replace the subscription_key string value with your valid subscription key.
    subscription_key = os.environ['AZURE_CV_KEY']
    # You must use the same region in your REST API call as you used to obtain your subscription keys.
    # For example, if you obtained your subscription keys from the westus region, replace
    # "westcentralus" in the URI below with "westus".
    #
    # NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
    # a free trial subscription key, you should not need to change this region.
    uri_base = 'https://westus.api.cognitive.microsoft.com'
    
    # Request headers.
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
        }
    
    # Request parameters.
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
        }
    
    try:
        # Execute the REST API call and get the response.
        response = requests.post(uri_base + '/face/v1.0/detect', data=image, headers=headers, params=params)

        return response.json()
    
    except Exception as e:
        print(f'Error: {e}')
        return

def AngleScoreCalculation(angles):
    answer = {}
    #answer['roll'] = -6.538738250732422 
    #answer['pan']  = 11.67092514038086
    #answer['tilt'] =-11.563632011413574 

    #### for Google
    answer['roll'] = -27.5
    answer['pan']  =  -8.5
    answer['tilt'] =  0
    
    #### For CloudDays
    #answer['roll'] = -10.6
    #answer['pan']  =  13.8
    #answer['tilt'] =  0
    score = (1 - math.sqrt(
                              (
                                  ( (answer['roll'] - angles['roll']) / (45 + abs(answer['roll'])) ) ** 2 +
                                  ( (answer['pan']  - angles['pan'])  / (45 + abs(answer['pan'] )) ) ** 2 +
                                  ( (answer['tilt'] - angles['tilt']) / (45 + abs(answer['tilt'])) ) ** 2
                              )
                          ) / 3
            ) * 100
    #score = int(score * 100)/100
    return score ### returns 100 when same angle

def SmileScoreCalculation(asmile, aemotion):
    total_asmile = 0
    total_asmile -= asmile
    total_asmile -= aemotion['happiness']
    total_asmile += aemotion['anger']
    total_asmile += aemotion['contempt']
    total_asmile += aemotion['disgust']
    #total_asmile += aemotion['fear']
    total_asmile += aemotion['neutral']
    total_asmile += aemotion['sadness']
    #total_asmile += aemotion['surprise'])
    total_asmile = total_asmile / 7.0 * 100
    return total_asmile

def TotalScoreCalculation(angle_scores, emotion_scores):
    gtotal = 0.0
    gavg = 50.0
    print(f"angle Scores List: {angle_scores}")
    for angle_score in angle_scores:
        gtotal += angle_score
    if len(angle_scores) != 0:
        gavg = gtotal/len(angle_scores)

    atotal = 0.0
    aavg = 50
    print(f"emotion Scores List: {emotion_scores}")
    for score in emotion_scores:
        atotal += score
    if len(emotion_scores) != 0:
        aavg = atotal/len(emotion_scores)

    final_score = 0.8 * gavg + 0.5 * aavg
    return final_score

def get_fatique_score(image):
    # resize image
    resize_image(image)

    # Azure face recog (resized image)
    fr_res = FaceRecognition(image)
    print(f'Facial Recognition results: {fr_res}')

    aangles = {}
    ascore = []
    asmilescore = []
    for avision_result in fr_res:
        # angle
        aangles['roll'] = avision_result['faceAttributes']['headPose']['roll']
        aangles['pan'] = avision_result['faceAttributes']['headPose']['yaw']
        aangles['tilt'] = avision_result['faceAttributes']['headPose']['pitch']
        ascore_this_time = AngleScoreCalculation(aangles)
        
        print("Base Face Angle Score: %f" % ascore_this_time)

        # smile
        asmile = avision_result['faceAttributes']['smile']
        aemotion = avision_result['faceAttributes']['emotion']
        asmilescore_this_time = SmileScoreCalculation(asmile, aemotion)
        # if debug_mode:
        #     spark_message = "angles = {0}, smile = {1}, emotion = {2}, Your Azure emotion score is = {3}".format(str(aangles), str(asmile), str(aemotion), str(asmilescore_this_time))
        #     CiscoSparkPostMessage(spark_message, roomId)
        ascore.append(ascore_this_time)
        asmilescore.append(asmilescore_this_time)

    total_score = TotalScoreCalculation(ascore, asmilescore)

    return total_score