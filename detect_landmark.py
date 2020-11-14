# from google.cloud.vision import types
from google.cloud.vision_v1 import ImageAnnotatorClient
from google.oauth2 import service_account
# from google.cloud.vision import types

from google.cloud import vision
def detect_landmarks(path):
    """Detects landmarks in the file."""
    from google.cloud import vision
    import io
    import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./thi.json"
    # credentials = service_account.Credentials.from_service_account_file('hack.json')
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    # print('Landmarks:')

    for landmark in landmarks:
        print(landmark.description)

        for location in landmark.locations:
            lat_lng = location.lat_lng
            x = lat_lng.latitude
            y = lat_lng.longitude
        # lat_lng = location.lat_lng
        # print('Latitude {}'.format(lat_lng.latitude))
        # print('Longitude {}'.format(lat_lng.longitude))
    return landmark.description,x,y
# path= "test.jpeg"
# detect_landmarks(path)
