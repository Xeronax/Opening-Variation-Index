from dotenv import load_dotenv
from position import Position
from typing import List, Optional, Union
from contextlib import closing
import mysql.connector
import os
import logging

load_dotenv()
host: str = os.getenv('HOST')
username: str = os.getenv('USER')
password: str = os.getenv('PASSWORD')
database: str = os.getenv('DB_NAME')


logger = logging.getLogger("mySQL")


def execute(
        operation: Union[str, list[str]],
        values: Optional[Union[tuple, list[tuple]]] = None) -> Optional[Union[int, list[tuple]]]:
    result = None
    with closing(mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=database
    )) as connection:
        with closing(connection.cursor()) as cursor:
            try:
                if isinstance(operation, list):  # Multi-line command
                    select = False
                    for command, value in zip(operation, values or ()):
                        if command.strip().upper().startswith("SELECT"):
                            select = True
                        try:
                            cursor.execute(command, value or ())
                        except mysql.connector.Error as err:
                            logger.error(f"Caught SQL Batch operation error\nInciting Syntax: {operation}\nError:\n{err}")
                            continue
                    if select:
                        result = cursor.fetchall()
                    else:
                        result = cursor.rowcount
                    connection.commit()
                else:
                    cursor.execute(operation, values or ())
                    if operation.strip().upper().startswith("SELECT"):
                        result = cursor.fetchall()
                    else:
                        connection.commit()
                        result = cursor.rowcount

            except mysql.connector.Error as err:
                logger.error(f"Caught SQL Operation Error\nInciting Syntax: {operation}\nError: \n{err}")

            if isinstance(result, int | None):
                return result

            return result if len(result) > 0 else None


def insert(position: Union[Position, List[Position]]) -> int:
    if isinstance(position, List):
        sql: list[str] = []
        vals: list[tuple] = []
        for pos in position:
            sql.append("INSERT INTO Positions (FEN, Evaluation) VALUES (%s, %s)")
            vals.append((pos.fen, pos.eval))
            logger.debug(f"Batch-adding: {pos.line}")
        return execute(sql, vals)
    else:
        sql: str = "INSERT INTO Positions (FEN, Evaluation) VALUES (%s, %s)"
        val: tuple = (position.fen, position.eval)
        result = execute(sql, val)
        logger.debug(f"Inserting {val} at row {result}")
        return result


def get(fen: Union[str, tuple]) -> list[tuple]:
    sql: str = "SELECT * FROM Positions WHERE FEN = %s"
    if isinstance(fen, tuple):
        unpack_placeholders: str = ", ".join(["%s" for _ in fen])  # Concatenate %s statements together for each query
        sql = f"SELECT * FROM Positions WHERE FEN IN ({unpack_placeholders})"
        params = fen  # Pass tuple itself
    else:
        params = (fen,)
    result = execute(sql, params)
    logger.info(f"Searched for {params} and found {result}")
    if result is None or len(result) < len(params):
        positions_to_insert: list[Position] = []
        for fenstr in params:
            positions_to_insert.append(Position(fenstr))
        insert(positions_to_insert)

    return execute(sql, params)


def print_db() -> None:
    print("Printing DB")
    try:
        for result in execute("SELECT * FROM Positions"):
            print(result)
    except IndexError:
        print("Encountered Index Error, DB possibly empty?")


def custom_command(command: Union[str, list[str]]) -> Optional:
    return execute(command)
