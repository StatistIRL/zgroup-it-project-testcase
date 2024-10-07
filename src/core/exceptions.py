"""
Исключения уровня проекта в целом, могут пригодиться в любом месте и для разных объектов.
"""


class ObjectNotFoundError(Exception):
    """
    Исключение для случаев, когда объект не найден в БД.
    """

    def __init__(self, id_: str, entity_name: str, trace_id: str | None = None) -> None:
        """Параметры для передачи в HTTPError класс.

        Args:
            id_ (str): идентификатор ненайденного объекта.
            entity_name (str): название ненайденной сущности.
            trace_id (str | None, optional): идентификатор. Defaults to None.
        """
        self.id = id_
        self.entity_name = entity_name
        self.trace_id = trace_id
