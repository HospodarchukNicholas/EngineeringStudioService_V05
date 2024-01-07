DEFAULT_LOCATION = 'Склад'
DEFAULT_COMPANY_NAME = 'DEFIR'
PROJECT_VERSION = 'v0.5'


QUANTITY_EXCEEDS_AVAILABLE_ERROR = 'Write-off quantity cannot exceed the available quantity.'
HELP_TEXT_WriteOff_reason = 'Коротко описуємо причину списання з балансу'
HELP_TEXT_WriteOffItem_item_location = 'Обираємо компонент для списання з конкретного місця'
HELP_TEXT_WriteOffItem_quantity = (
    "Обираємо кількість компонентів для списання з конкретного місця. "
    "Якщо кількість буде перевищувати доступну - буде викликано exeption, "
    "щоб запобігти некоректній операції"
)