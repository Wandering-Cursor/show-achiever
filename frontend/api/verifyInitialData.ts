export default function verifyInitialData(
    initialData: string
) {
    return fetch(
        `/api/telegram/initial_data`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(
                {
                    data: initialData,
                }
            ),
        }
    );
}