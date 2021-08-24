import json
import base64
import io
from PIL import Image
import yaml
import cv2

from tool.utils import *
from tool.torch_utils import *
from tool.darknet2pytorch import Darknet
import argparse

CONFIG_FILE = './cfg/yolov4.cfg'
WEIGHT_FILE = './yolov4.weights'


def get_args():
    parser = argparse.ArgumentParser('Test your image or video by trained model.')
    parser.add_argument('-cfgfile', type=str, default=CONFIG_FILE,
                        help='path of cfg file', dest='cfgfile')
    
    
    args = parser.parse_args()

    return args




def init_context(context):
    cfg = get_args()
    predictor = Darknet(cfg.cfgfile)
    predictor.load_weights(WEIGHT_FILE)

    setattr(context.user_data, 'model_handler', predictor)
    functionconfig = yaml.safe_load(open("/opt/nuclio/function.yaml"))
    labels_spec = functionconfig['metadata']['annotations']['spec']
    labels = {item['id']: item['name'] for item in json.loads(labels_spec)}
    setattr(context.user_data, 'labels', labels)

def handler(context, event):
    data = event.body
    buf = io.BytesIO(base64.b64decode(data['image'].encode('utf-8')))
    threshold = float(data.get('threshold',0.5))
    image = cv2.imread(buf)
    sized = cv2.resize(image, (context.user_data.model_handler.width, context.user_data.model_handler.height))
    sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)
    boxes = do_detect(context.user_data.model_handler,sized, threshold, 0.6, 0)[0]
    results = []
    for i in range(len(boxes)):
        box = boxes[i][0:4]
        score = boxes[i][4]
        label = boxes[i][-1]
        label = context.user_data.labels[int(label)]
        results.append({
            'confidence': str(float(score)),
            'label': label,
            'points': box.tolist(),
            'type': 'rectangle'
        })
    return context.Response(body=json.dumps(results), headers={},content_type='application/json',status_code=200)






