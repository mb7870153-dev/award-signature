"""Автоматические тесты логики обработки наградной заявки."""

import pytest

from src.award_application import (
    ApplicationStatus,
    ApplicationValidationError,
    AwardApplication,
    InvalidStatusTransitionError,
)


@pytest.fixture
def application():
    """Создаёт корректно заполненную тестовую заявку."""
    return AwardApplication(
        organization_name="ООО «Пример»",
        nominee_name="Иванов Иван Иванович",
        award_type="Почётная грамота",
        justification="За многолетний добросовестный труд",
    )


def test_valid_application_can_be_submitted(application):
    """Корректно заполненную заявку можно подать."""
    application.submit()
    assert application.status == ApplicationStatus.SUBMITTED


def test_application_with_missing_data_cannot_be_submitted(application):
    """Заявку с незаполненным обязательным полем подать нельзя."""
    application.nominee_name = "   "

    with pytest.raises(ApplicationValidationError):
        application.submit()

    assert application.status == ApplicationStatus.DRAFT


def test_application_can_be_returned_and_resubmitted(application):
    """Заявку можно вернуть на доработку и подать повторно."""
    application.submit()
    application.start_review()
    application.request_revision()

    assert application.status == ApplicationStatus.REVISION_REQUIRED

    application.resubmit()
    assert application.status == ApplicationStatus.SUBMITTED


def test_rejected_application_cannot_be_signed(application):
    """Отклонённую комиссией заявку нельзя подписать."""
    application.submit()
    application.start_review()
    application.reject()

    with pytest.raises(InvalidStatusTransitionError):
        application.sign()


def test_approved_application_can_complete_lifecycle(application):
    """Одобренная заявка проходит подписание, передачу и архивирование."""
    application.submit()
    application.start_review()
    application.approve()
    application.sign()
    application.mark_transferred()
    application.archive()

    assert application.status == ApplicationStatus.ARCHIVED
    assert application.status_history == [
        ApplicationStatus.DRAFT,
        ApplicationStatus.SUBMITTED,
        ApplicationStatus.UNDER_REVIEW,
        ApplicationStatus.APPROVED,
        ApplicationStatus.SIGNED,
        ApplicationStatus.TRANSFERRED,
        ApplicationStatus.ARCHIVED,
    ]


def test_cannot_skip_review_and_approve_directly(application):
    """Нельзя одобрить заявку, не пройдя этап проверки."""
    application.submit()

    with pytest.raises(InvalidStatusTransitionError):
        application.approve()
