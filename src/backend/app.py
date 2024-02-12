import logging
from ovi_db import get
from flask import Flask, jsonify, request


logger = logging.getLogger("ovi")

logging.basicConfig(level=logging.INFO, filename="../../data/log.log", filemode="w",
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


app = Flask("ovi")


def main() -> None:
    app.run(debug=True)


if __name__ == "__main__":
    main()


@app.route('/query', methods=['GET'])
def query():
    if request.method == 'GET':
        params: str = request.args.get('fen')
        if not params:
            return jsonify({"error": "FEN parameter is required."}), 400
        fen_strings: tuple = tuple(params.split(','))
        logger.info(f"received strings: {fen_strings}")
        result: list = json_fen(get(fen_strings))
        return jsonify(result), 200


def json_fen(queries: list[tuple]) -> list:
    result = [{"fen": fen, "evaluation": evaluation} for fen, evaluation in queries]  # List comprehension
    return result

