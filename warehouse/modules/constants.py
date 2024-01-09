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
HELP_TEXT_ShoppingCart_purpose = 'Необхідно коротко описати призначення даного замовлення.'
HELP_TEXT_ShoppingCart_status = (
    'Статус впливає як будуть оброблятись дані. '
    'Draft: це як шаблон, програма створює записи для кожного компоненти та саму корзину. '
    'Approved: замовлення сформовано але ще на етапі оформлення. '
    'Completed: всі компоненти доставленні, програма генерує для них записи, '
    'які відповідають реальному місцезнашодженню та кількості'
)
HELP_TEXT_ShoppingCart_google_sheet_link = (
    'Якщо добавити посилання - програма спробує автоматично '
    'згенерувати всі компоненти та добавити в корзину'
)
HELP_TEXT_ShoppingCart_created_by = (
    'Це поле автоматично обирає активного користувача. '
    'При потребі можна обрати іншу відповідальну особу.'
)