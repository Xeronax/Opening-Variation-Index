//restclient.ts

import axios from "axios";

const endpoint: string = "http://127.0.0.1:5000"

export async function get(fen: string): Promise<any> {
    axios({
        method: 'get',
        url: `${endpoint}/query`,
        params: { fen }
    }).then(function (response) {
        console.log(response)
        return response.data
    });
}
