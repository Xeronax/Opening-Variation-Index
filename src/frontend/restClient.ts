//restclient.ts

import axios from "axios";

const endpoint: string = "http://127.0.0.1:5000"

export async function get(fenStrings: string | Array<string>): Promise<any> {
    let fen: string
    if(Array.isArray(fenStrings)) {
        fen = fenStrings.join(',')
    } else {
        fen = fenStrings
    }
    try {
        axios({
            method: 'get',
            url: `${endpoint}/query`,
            params: { fen }
        }).then(function (response) {
            console.log(response)
            return response.data
        });
    } catch (e) {
        console.log(e)
        return null
    }

}
