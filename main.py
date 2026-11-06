"""Точка входа демонстрационного приложения обработки наградных заявок.

Программа показывает последовательность изменения статусов заявки.
Она не выполняет реальную криптографическую подпись УКЭП и не подключается к СМЭВ.
"""

from src.award_application import AwardApplication


def main() -> None:
    print("=" * 68)
    print("Информационная система «Электронное подписание наградных документов»")
    print("Демонстрационный режим, версия 1.0.0")
    print("=" * 68)

    application = AwardApplication(
        organization_name="ООО «СтройМонтаж»",
        nominee_name="Иванов Иван Иванович",
        award_type="Почётная грамота",
        justification="За многолетний добросовестный труд и вклад в развитие организации",
    )

    print("\n1. Заявка создана")
    print(f"   Предприятие: {application.organization_name}")
    print(f"   Представляемый к награждению: {application.nominee_name}")
    print(f"   Вид награды: {application.award_type}")
    print(f"   Статус: {application.status.value}")

    application.submit()
    print(f"\n2. Заявка подана. Статус: {application.status.value}")

    application.start_review()
    print(f"3. Сектор начал проверку. Статус: {application.status.value}")

    application.approve()
    print(f"4. Комиссия одобрила заявку. Статус: {application.status.value}")

    application.sign()
    print(
        "5. В демонстрации зафиксирован статус подписания: "
        f"{application.status.value}. Реальная УКЭП не выполняется."
    )

    application.mark_transferred()
    print(
        "6. В демонстрации зафиксирован статус передачи: "
        f"{application.status.value}. Реальная отправка в СМЭВ не выполняется."
    )

    application.archive()
    print(f"7. Документ помещён в архив. Статус: {application.status.value}")

    print("\nИстория изменения статусов:")
    for number, status in enumerate(application.status_history, start=1):
        print(f"   {number}. {status.value}")

    print("\n" + "=" * 68)
    print("Демонстрация завершена успешно.")
    print("=" * 68)


if __name__ == "__main__":
    main()
