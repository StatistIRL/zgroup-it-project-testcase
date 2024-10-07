from typing import Any, Iterable, Self

from pydantic import BaseModel, ConfigDict


def snake_to_camel(name: str) -> str:
    """Преобразования названия из нотации snake_case в нотацию camelCase (стандартный формат для JavaScript приложений).

    Args:
        name (str): изначальное название в snake_case.

    Returns:
        str: полученное название в camelCase.
    """
    first, *rest = name.split("_")
    return first + "".join(map(str.capitalize, rest))


class BaseSchema(BaseModel):
    """
    Базовый класс для всех схем проекта.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=snake_to_camel,
    )

    @classmethod
    def model_validate_list(cls, models: Iterable[Any]) -> list[Self]:
        """Трансформация коллекции объектов в список объектов-схем.

        Args:
            models (Iterable[Any]): коллекция объектов (чаще всего ORM).

        Returns:
            list[Self]: список объектов-схем pydantic.
        """
        return [cls.model_validate(model) for model in models]
