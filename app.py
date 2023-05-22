from flask import Flask, render_template, Response, request, jsonify, url_for
import cv2
import time
from datetime import datetime

# Flask アプリケーションを作成
app = Flask(__name__)

process_flag = False

# カメラオブジェクトを初期化（None）
camera = None

# ルートエンドポイント（"/"）を定義
@app.route('/')
def index():
    # index.html をレンダリングして表示
    return render_template('index.html')

# カメラを開始するエンドポイントを定義
@app.route('/start_camera', methods=['POST'])
def start_camera():
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        return jsonify(error='Failed to open camera'), 400
    return jsonify(success=True)

# カメラを停止するエンドポイントを定義
@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    global camera
    if camera is not None and camera.isOpened():
        camera.release()
    camera = None
    return jsonify(success=True)

# カメラの設定を更新するためのエンドポイント
@app.route('/update_camera', methods=['POST'])
def update_camera():
    if not camera.isOpened():
        return jsonify(error='Camera is closed'), 400
    # フォームからbrightness、exposureとimageSizeを取得
    brightness = int(request.form.get('brightness', 0))
    exposure = int(request.form.get('exposure', 1))
    imageSize = int(request.form.get('imageSize', 2))

    # カメラのbrightness、exposureとimageSizeを設定
    camera.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
    camera.set(cv2.CAP_PROP_EXPOSURE, exposure)
    width = int(640 * imageSize)
    height = int(360 * imageSize)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    print("CAP_PROP_FRAME_WIDTH: ", int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print("CAP_PROP_FRAME_HEIGHT: ", int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    #print("CAP_PROP_BRIGHTNESS: ", int(camera.get(cv2.CAP_PROP_BRIGHTNESS)))

    return jsonify({'success': True})

@app.route('/process_image', methods=['POST'])
def process_image():
    global process_flag

    # Toggle the process_flag
    process_flag = not process_flag

    return {'success': True}

# ビデオフレームを生成する関数
def generate_frames():
    while camera is None or not camera.isOpened():
        yield (b'--frame\r\n'
               b'Content-Type: image/\r\n\r\n' + b'\r\n')
        time.sleep(0.1)

    while True:
        if camera is None or not camera.isOpened():
            break
        # カメラからフレームを読み込む
        ret, frame = camera.read()
        if not ret:
            break
        # フレームを JPEG 形式に変換し、バイト列に変換
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # フレームを multipart/x-mixed-replace 形式で出力
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.1)


# ビデオフィードのエンドポイント
@app.route('/video_feed')
def video_feed():
    if camera is None or not camera.isOpened():
        return jsonify(error='Camera is closed'), 400
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# キャプチャーのエンドポイント
@app.route('/capture', methods=['POST'])
def capture():
    global camera
    if camera is None or not camera.isOpened():
        return jsonify(error='Camera is closed'), 400

    ret, frame = camera.read()
    if ret:
        if process_flag:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f'capture_{timestamp}.jpg'
        cv2.imwrite('static/' + filename, frame)
        return jsonify(url=url_for('static', filename=filename, _external=True))
    
    return jsonify(error='Failed to read a frame'), 400

# アプリケーションを実行する
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
