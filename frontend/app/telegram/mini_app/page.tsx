"use client";

import { init, qrScanner, sendData, miniApp } from '@telegram-apps/sdk-react';

import { useEffect, useRef } from 'react';

export default function TelegramMiniApp() {
    const isScanned = useRef(false);

    useEffect(
        () => {
            init();
            debugger;

            if (qrScanner.open.isAvailable()) {
                qrScanner.open({
                    text: 'Scan the QR',
                    onCaptured(qr: string) {
                        isScanned.current = true;
                        sendData(qr);
                        qrScanner.close();
                        miniApp.close();
                    },
                });
            }
        },
        []
    );

    return (
        <div>
            {isScanned.current ? 'QR scanned' : 'Scanning QR...'}
        </div>
    );
}