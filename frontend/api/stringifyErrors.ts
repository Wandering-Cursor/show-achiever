interface ErrorDetail {
    msg: string;
    type: string;
}

interface Response {
    detail: Array<ErrorDetail>;
}


export default function stringifyErrors(
    response: Response
) {
    // Returns a string representation of the error details
    // shows a type of error, it's message for all the errors

    return response.detail.map(
        (error) => {
            return `${error.type}: ${error.msg}`;
        }
    ).join('\n');
}