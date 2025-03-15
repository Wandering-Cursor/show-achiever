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
    return fetch(
        `/api/task/${payload}`,
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