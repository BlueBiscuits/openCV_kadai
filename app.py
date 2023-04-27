from flask import Flask, render_template, Response, request, jsonify
import cv2
import time

app = Flask(__name__)

# カメラを開く
camera = cv2.VideoCapture(0)

# ルートディレクトリへのアクセスを処理し、index.htmlを表示
@app.route('/')
def index():
    return render_template('index.html')

# カメラの設定を更新するためのエンドポイント
@app.route('/update_camera', methods=['POST'])
def update_camera():
    # フォームからbrightness、exposureとimageSizeを取得
    brightness = int(request.form.get('brightness', 0))
    exposure = int(request.form.get('exposure', 0))
    imageSize = int(request.form.get('imageSize', 1))

    # カメラのbrightness、exposureとimageSizeを設定
    camera.set(cv2.CAP_PROP_BRIGHTNESS, (brightness + 100) / 100)
    camera.set(cv2.CAP_PROP_EXPOSURE, exposure)
    width = int(640 * imageSize)
    height = int(480 * imageSize)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    return jsonify({'success': True})

# ビデオフレームを生成する関数
def generate_frames():
    while True:
        # カメラからフレームを読み取る
        ret, frame = camera.read()
        if not ret:
            break

        # フレームをJPEGに変換し、バイト列に変換
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # ジェネレータがmultipart/x-mixed-replace形式でフレームを返す
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.1)  

# ビデオフィードのエンドポイント
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# アプリケーションを実行する
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
