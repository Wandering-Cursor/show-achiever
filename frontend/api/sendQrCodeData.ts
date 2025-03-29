interface QRCodeData {
    payload: string;
    chat_id: number;
}

export default function sendQRCodeDataToBackend(
    {
        payload,
        chat_id
    }: QRCodeData
) {
    const encodedPayload = encodeURIComponent(payload);

    return fetch(
        `/api/task/${encodedPayload}`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(
                {
                    attendee_id: chat_id,
                }
            ),
        }
    );
}