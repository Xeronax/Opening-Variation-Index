//chessMain.ts

import { get } from "./restClient"


const fen: string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

get(fen).then(function (result) {
    console.log(result)
});