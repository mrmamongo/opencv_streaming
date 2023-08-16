import cv2


def nothing(x):
    pass


cv2.namedWindow('options', cv2.WINDOW_NORMAL)
cv2.createTrackbar('Treshold', 'options', 55, 100, nothing)
cv2.createTrackbar('NMS_thresh', 'options', 45, 100, nothing)

cap = cv2.VideoCapture(link)

classnames = []
classfile = 'stream/classnames.txt'
with open(classfile, 'rt', encoding='UTF-8') as f:
    classnames = f.read().rstrip('\n').split('\n')

configpath = 'stream/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightspath = 'stream/frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightspath, configpath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

count = 0

while True:
    success, img = cap.read()
    thres = cv2.getTrackbarPos('Treshold', 'options') / 100
    nms_thres = cv2.getTrackbarPos('NMS_thresh', 'options') / 100
    classids, confs, bbox = net.detect(img, confThreshold=thres)
    bbox = list(bbox)
    confs = list(np.array(confs).reshape(1, -1)[0])
    confs = list(map(float, confs))
    indices = cv2.dnn.NMSBoxes(bbox, confs, thres, nms_thres)

    objs = []
    for i in indices:
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        cv2.rectangle(img, (x, y), (x + w, h + y), color=(0, 255, 0), thickness=2)
        cv2.putText(img, classnames[classids[i] - 1].upper(), (box[0] + 5, box[1] - 5),
                    cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 2)

        # вывод объектов в кадре
        objs.append(f"{classnames[classids[i] - 1]} - {round(confs[i] * 100)}%")
        # sys.stdout.write("\r{0}".format(classNames[classIds[i]-1]))
        sys.stdout.write("\r{0}".format(', '.join(objs)))
        sys.stdout.flush()
        # time.sleep(0)
        # print(f"{classNames[classIds[i]]} - {round(confs[i] *100)}%", sep='\r')

    name = 'stream/screen/frame' + str(count) + '.jpg'
    cv2.imshow('Output', img)
    key = cv2.waitKey(1)
    if key == ord('s') or key == ord('S'):
        cv2.imwrite(name, img)

        entry = max((e for e in os.scandir('stream/screen') if e.is_file(follow_symlinks=False)),
                    key=lambda e: getattr(e.stat(), 'st_birthtime', None) or e.stat().st_ctime)
        last_file = entry.path
        print('Frame saved:' + last_file)
        count += 1
    elif key == ord('Q') or key == ord('q') or key == 27:
        break

cap.release()
cv2.destroyAllWindows()