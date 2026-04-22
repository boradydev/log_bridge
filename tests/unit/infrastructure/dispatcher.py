from src.infrastructure.dispatcher import Dispatcher


async def test_dispatch(
    mock_log_file,
    mock_logger,
    mock_first_route,
    mock_second_route,
) -> None:
    first_route_line = "first_route line"
    second_route_line = "second_route line"
    another_line = "another line"

    async def async_gen():
        for line in [
            "\n",
            first_route_line,
            "\r\n",
            second_route_line,
            "      ",
            another_line,
            "",
            "\r",
            "\n\r",
        ]:
            yield line

    file_path = "/banned.log"
    mock_log_file.get_line.side_effect = async_gen
    mock_log_file.file_path = file_path
    dispatcher = Dispatcher(
        logs=mock_log_file,
        logger=mock_logger,
    )

    first_route_data = {"value1": "first_route", "value2": "line"}
    second_route_data = {"value1": "second_route", "value2": "line"}

    def side_effect_first(line: str) -> dict[str, str] | None:
        return first_route_data if line == first_route_line else None

    mock_first_route.extract.side_effect = side_effect_first
    dispatcher.add_route(mock_first_route)

    def side_effect_second(line: str) -> dict[str, str] | None:
        return second_route_data if line == second_route_line else None

    mock_second_route.extract.side_effect = side_effect_second
    dispatcher.add_route(mock_second_route)

    await dispatcher.run()

    mock_first_route.run.assert_called_with(first_route_data)
    mock_second_route.run.assert_called_with(second_route_data)
    mock_logger.info.assert_called_once_with(
        dispatcher._START_MSG.format(line=another_line, file_path=file_path)
    )
    mock_logger.warning.assert_called_once_with(
        dispatcher._NO_ROUTE_MSG.format(line=another_line, file_path=file_path)
    )
