from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    # constants
    MIN_IN_H: float = 60
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:

        """Получить среднюю скорость движения."""
        avg_speed_value = self.get_distance() / self.duration
        return avg_speed_value

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_massage = InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )
        return info_massage


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        spent_calories = ((
            self.CALORIES_MEAN_SPEED_MULTIPLIER
            * (self.get_mean_speed())
            + self.CALORIES_MEAN_SPEED_SHIFT
        )
            * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H
        )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories = ((
            self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight
            + (
                ((self.get_mean_speed() * self.KMH_IN_MSEC)**2)
                / (self.height / self.CM_IN_M)
            )
            * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight
        )
            * self.duration * self.MIN_IN_H
        )
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: float = 2.0

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:

        """Получить среднюю скорость движения."""
        avg_speed_value = (
            self.length_pool
            * self.count_pool / self.M_IN_KM / self.duration
        )
        return avg_speed_value

    def get_spent_calories(self) -> float:
        spent_calories = ((
            self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT
        )
            * self.CALORIES_WEIGHT_MULTIPLIER * self.weight * self.duration
        )
        return spent_calories


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    training_class: Training = workout[workout_type](*data)
    return training_class


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [('SWM', [720, 1, 80, 25, 40]),
                ('RUN', [15000, 1, 75]),
                ('WLK', [9000, 1, 75, 180])]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
