// HTML要素を取得する
const stream = document.getElementById('stream');
const captureCanvas = document.getElementById('captureCanvas');
const startBtn = document.getElementById('start');
const stopBtn = document.getElementById('stop');
const captureBtn = document.getElementById('capture');
const brightnessValue = document.getElementById('brightnessValue');
const brightnessSlider = document.getElementById('brightnessSlider');
const exposureValue = document.getElementById('exposureValue');
const exposureSlider = document.getElementById('exposureSlider');
const imageSizeValue = document.getElementById('imageSizeValue');
const imageSizeSlider = document.getElementById('imageSizeSlider');
const timestamp = document.getElementById('timestamp');

let streaming = false;
let mediaStream = null;

// Streamを開始する関数
const startStream = async () => {
    try {
        mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
        stream.srcObject = mediaStream;
        streaming = true;
    } catch (err) {
        console.error("Error starting stream:", err);
    }
};

// Streamを停止する関数
const stopStream = () => {
    if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
        stream.srcObject = null;
        streaming = false;
    }
};

// Streamを開始するボタンのイベントリスナー
startBtn.onclick = () => {
    if (!streaming) {
        startStream();
    }
};

// Streamを停止するボタンのイベントリスナー
stopBtn.onclick = () => {
    if (streaming) {
        stopStream();
    }
};

// カメラパラメータを更新する
const updateCameraSettings = async () => {
    const brightness = brightnessSlider.value;
    const exposure = exposureSlider.value;
    const imageSize = imageSizeSlider.value;

    const formData = new FormData();
    formData.append('brightness', brightness);
    formData.append('exposure', exposure);
    formData.append('imageSize', imageSize);

    try {
        const response = await fetch('/update_camera', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (!data.success) {
            console.error('Error updating camera settings.');
        }
    } catch (err) {
        console.error('Error updating camera settings:', err);
    }
};

// Brightnessスライダーのイベントリスナー
brightnessSlider.oninput = () => {
    const brightness = brightnessSlider.value;
    brightnessValue.innerText = brightness;
    updateCameraSettings();
};

// Exposureスライダーのイベントリスナー
exposureSlider.oninput = async () => {
    const exposure = exposureSlider.value;
    exposureValue.innerText = exposure;
    updateCameraSettings();
};

// Image Sizeスライダーのイベントリスナー
imageSizeSlider.oninput = () => {
    const imageSize = imageSizeSlider.value;
    imageSizeValue.innerText = imageSize;
    updateCameraSettings();
};

// タイムスタンプを更新する
setInterval(() => {
    if (streaming) {
        const date = new Date();
        timestamp.innerText = date.toLocaleTimeString();
    }
}, 1000);

// Captureボタンのイベントリスナー
captureBtn.onclick = () => {
    if (streaming) {
        const imageSize = imageSizeSlider.value;
        const width = 640 * imageSize;
        const height = 480 * imageSize;
        captureCanvas.width = width;
        captureCanvas.height = height;
        const ctx = captureCanvas.getContext('2d');

        // 明るさを設定する
        const brightness = parseInt(brightnessSlider.value);
        ctx.filter = `brightness(${100 + brightness}%)`;

        ctx.drawImage(stream, 0, 0, width, height);
        const capturedImage = new Image();
        capturedImage.src = captureCanvas.toDataURL("image/png");
        capturedImage.width = width / 4;
        capturedImage.height = height / 4;

        // 画像とタイムスタンプを含むdivを作成する
        const imageDiv = document.createElement('div');
        imageDiv.style.margin = '10px';

        // タイムスタンプを追加する
        const imageTimestamp = document.createElement('p');
        imageTimestamp.innerText = timestamp.innerText;
        imageDiv.appendChild(imageTimestamp);

        imageDiv.appendChild(capturedImage);

        // ダウンロードリンクを追加する
        const downloadLink = document.createElement('a');
        downloadLink.href = capturedImage.src;
        downloadLink.download = `capture-${Date.now()}.png`;
        downloadLink.innerText = 'Download';
        imageDiv.appendChild(downloadLink);

        // 画像とタイムスタンプを含むdivをcapturedImagesに追加する
        document.getElementById('capturedImages').appendChild(imageDiv);

        // フィルタをリセットする
        ctx.filter = 'none';
    }
};


const clearBtn = document.getElementById('clear');

// Clearボタンのイベントリスナー
clearBtn.onclick = () => {
    const capturedImages = document.getElementById('capturedImages');
    capturedImages.innerHTML = '';
};

