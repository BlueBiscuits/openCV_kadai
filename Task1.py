import cv2

def main():
    # デフォルトのWebカメラ（通常は内蔵カメラ）からビデオをキャプチャする
    cap = cv2.VideoCapture(0)

    while True:
        # 1フレーム読み込む
        ret, frame = cap.read()

        # 読み取りに成功した場合、フレームを表示する
        if ret:
            cv2.imshow('Webcam Stream', frame)

            # 'q'キーを押してループを終了する
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Failed to capture frame. Check if your webcam is connected.")
            break

    # カメラを解放し、すべての開いているウィンドウを閉じる
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()