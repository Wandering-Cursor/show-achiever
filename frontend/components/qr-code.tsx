import { CameraDevice, Html5Qrcode } from 'html5-qrcode';
import { useEffect, useRef } from 'react';

interface Html5QrcodePluginProps {
    elementId: string;

    fps: number;
    qrAreaSize: number;

    scanResultCallback?: (qrCodeMessage: string) => void;
    errorCallback?: (errorMessage: string) => void;
}

function initializeCamera(html5Qrcode: Html5Qrcode, cameraId: string, props: Html5QrcodePluginProps) {
    html5Qrcode.start(
        cameraId,
        {
            fps: props.fps,
            qrbox: props.qrAreaSize,
        },
        (qrCodeMessage) => {
            console.debug("QR code detected: ", qrCodeMessage);
            if (props.scanResultCallback) {
                props.scanResultCallback(qrCodeMessage);
            }
        },
        (errorMessage) => {
            if (props.errorCallback) {
                props.errorCallback(errorMessage);
            }
        }
    );
}

const Html5QrcodePlugin = (props: Html5QrcodePluginProps) => {

    const html5Qrcode = useRef<Html5Qrcode | null>(null);
    const availableCameras = useRef<CameraDevice[]>([]);
    const currentCameraIndex = useRef<number>(0);

    useEffect(() => {
        html5Qrcode.current = new Html5Qrcode(props.elementId);

        Html5Qrcode.getCameras().then((cameras) => {
            availableCameras.current = cameras;

            if (cameras.length === 0) {
                console.error("No cameras found.");
                return;
            }

            const lastCamera = availableCameras.current[availableCameras.current.length - 1];
            currentCameraIndex.current = availableCameras.current.length - 1;

            if (html5Qrcode.current === null) {
                console.error("html5Qrcode is null.");
                return;
            }

            initializeCamera(
                html5Qrcode.current,
                lastCamera.id,
                props
            );
        });


    }
    );


    function changeCamera() {
        if (html5Qrcode.current === null) {
            console.error("html5Qrcode is null.");
            return;
        }

        if (availableCameras.current.length < 2) {
            console.warn("Only one camera available.");
            return;
        }

        currentCameraIndex.current = (currentCameraIndex.current + 1) % availableCameras.current.length;
        const camera = availableCameras.current[currentCameraIndex.current];

        html5Qrcode.current.stop().then(() => {
            console.debug("Stopped camera.");

            if (html5Qrcode.current === null) {
                console.error("html5Qrcode is null.");
                return;
            }

            html5Qrcode.current.clear();

            initializeCamera(
                html5Qrcode.current,
                camera.id,
                props
            );
        });

    }

    return (
        <div>
            <p>Camera Controls</p>
            <div id={props.elementId} />
            <button onClick={changeCamera}>Flip camera</button>
        </div>
    );
};

export default Html5QrcodePlugin;