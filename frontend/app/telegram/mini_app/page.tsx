"use client";

import sendQRCodeDataToBackend from '@/api/sendQrCodeData';

import { useEffect } from 'react';

interface Telegram {
    WebApp: {
        ready: () => void;
        initData: string;
        init: () => void;
        showScanQrPopup: (options: { text: string }, callback: (qr: string) => void) => void;
        showPopup: (options: { message: string }) => void;
        closeScanQrPopup: () => void;
        close: () => void;
    };
}

declare global {
    interface Window {
        Telegram: Telegram;
    }
}


function checkUUIDv4(data: string) {
    return data.match(/^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$/i);
}

function parseParams(data: string) {
    return data.split('&').reduce(function (params: { [key: string]: string }, param) {
        const paramSplit = param.split('=').map(function (value) {
            return decodeURIComponent(value.replace(/\+/g, ' '));
        });
        params[paramSplit[0]] = paramSplit[1];
        return params;
    }, {} as { [key: string]: string });
}

function getUser(data: string) {
    const initDataObject = parseParams(data);

    if (initDataObject.user === undefined) {
        throw new Error("User data is missing");
    }

    return JSON.parse(initDataObject.user);
}


export default function TelegramMiniApp() {
    useEffect(
        () => {
            window.Telegram.WebApp.ready();

            const initData = window.Telegram.WebApp.initData;
            // Verify initData integrity by checking hash
            const user = getUser(initData);

            window.Telegram.WebApp.showScanQrPopup(
                {
                    text: "Scan the QR",
                },
                (qr) => {
                    if (!checkUUIDv4(qr)) {
                        window.Telegram.WebApp.showPopup(
                            {
                                message: 'Invalid QR code. Try again.',
                            }
                        );

                        return;
                    }

                    sendQRCodeDataToBackend(
                        {
                            payload: qr,
                            chat_id: user.id,
                        }
                    )

                    window.Telegram.WebApp.closeScanQrPopup();
                    window.Telegram.WebApp.close();
                },
            );
        },
        []
    );

    return (
        <div>
            <h1>Please close the Mini-App if it was not closed automatically</h1>
        </div>
    );
}