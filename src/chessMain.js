"use strict";
//chessMain.ts
Object.defineProperty(exports, "__esModule", { value: true });
var restClient_1 = require("./restClient");
var fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
(0, restClient_1.get)(fen).then(function (result) {
    console.log(result);
});
