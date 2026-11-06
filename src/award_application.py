"""Демонстрационная логика обработки заявки на награждение.

Модуль моделирует проверку обязательных данных и переходы между статусами.
Он не выполняет настоящую криптографическую подпись УКЭП и не подключается к СМЭВ.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class ApplicationStatus(str, Enum):
    """Статусы наградной заявки в демонстрационной системе."""

    DRAFT = "Черновик"
    SUBMITTED = "Подана"
    UNDER_REVIEW = "На проверке"
    REVISION_REQUIRED = "На доработке"
    APPROVED = "Одобрена"
    REJECTED = "Отклонена"
    SIGNED = "Подписана"
    TRANSFERRED = "Передана"
    ARCHIVED = "Архивирована"


class ApplicationValidationError(ValueError):
    """Ошибка, возникающая при незаполненных обязательных полях."""


class InvalidStatusTransitionError(ValueError):
    """Ошибка недопустимого перехода заявки между статусами."""


@dataclass
class AwardApplication:
    """Заявка на награждение и операции над её статусом."""

    organization_name: str
    nominee_name: str
    award_type: str
    justification: str
    status: ApplicationStatus = ApplicationStatus.DRAFT
    status_history: List[ApplicationStatus] = field(
        default_factory=lambda: [ApplicationStatus.DRAFT]
    )

    def validate(self) -> None:
        """Проверяет заполнение обязательных сведений заявки."""
        required_fields = {
            "Наименование предприятия": self.organization_name,
            "ФИО представляемого к награждению": self.nominee_name,
            "Вид награды": self.award_type,
            "Обоснование награждения": self.justification,
        }
        missing = [name for name, value in required_fields.items() if not value.strip()]
        if missing:
            raise ApplicationValidationError(
                "Не заполнены обязательные поля: " + ", ".join(missing)
            )

    def _change_status(
        self,
        expected_status: ApplicationStatus,
        new_status: ApplicationStatus,
    ) -> None:
        """Выполняет переход, только если заявка находится в ожидаемом статусе."""
        if self.status != expected_status:
            raise InvalidStatusTransitionError(
                f"Нельзя изменить статус «{self.status.value}» на «{new_status.value}». "
                f"Ожидаемый текущий статус: «{expected_status.value}»."
            )
        self.status = new_status
        self.status_history.append(new_status)

    def submit(self) -> None:
        """Предприятие подаёт заполненную заявку."""
        self.validate()
        self._change_status(ApplicationStatus.DRAFT, ApplicationStatus.SUBMITTED)

    def start_review(self) -> None:
        """Сектор начинает проверку поданной заявки."""
        self._change_status(ApplicationStatus.SUBMITTED, ApplicationStatus.UNDER_REVIEW)

    def request_revision(self) -> None:
        """Сектор возвращает заявку на доработку."""
        self._change_status(
            ApplicationStatus.UNDER_REVIEW, ApplicationStatus.REVISION_REQUIRED
        )

    def resubmit(self) -> None:
        """Предприятие повторно подаёт исправленную заявку."""
        self.validate()
        self._change_status(
            ApplicationStatus.REVISION_REQUIRED, ApplicationStatus.SUBMITTED
        )

    def approve(self) -> None:
        """Фиксирует положительное решение после проверки/рассмотрения."""
        self._change_status(ApplicationStatus.UNDER_REVIEW, ApplicationStatus.APPROVED)

    def reject(self) -> None:
        """Фиксирует отрицательное решение."""
        self._change_status(ApplicationStatus.UNDER_REVIEW, ApplicationStatus.REJECTED)

    def sign(self) -> None:
        """Фиксирует факт подписания документа (без выполнения УКЭП)."""
        self._change_status(ApplicationStatus.APPROVED, ApplicationStatus.SIGNED)

    def mark_transferred(self) -> None:
        """Фиксирует передачу документа (без реального подключения к СМЭВ)."""
        self._change_status(ApplicationStatus.SIGNED, ApplicationStatus.TRANSFERRED)

    def archive(self) -> None:
        """Переводит переданный документ в архивный статус."""
        self._change_status(ApplicationStatus.TRANSFERRED, ApplicationStatus.ARCHIVED)
