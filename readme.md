# Khaba
### Твій найкращий асистент у світі студентського самоврядування

Уяви, що ти вигадав яскравий захід для університету.

Ти хочеш, щоб він був максимально крутим, тому тобі треба знайти чудовий звук, приміщення для проведення та 
смаколики для відвідувачів.

А ти знаєш, що для цього потрібно оформити? От і я не все згадаю, але вона - пам'ятає.

Вона - це Khaba, твій найкращий асистент у світі студентського самоврядування, що спілкуватиметься з тобою у Telegram.

Все дуже просто: пишеш який захід проводиш, що тобі для цього треба - і ти миттєво отримуєш відповідь з посиланнями 
на документи, у кого їх підписувати та приклади, як саме треба їх заповнювати.

Чому миттєво? Тому що це telegram-bot, написаний на мові Python з використанням бібліотеки aiogram.

Окрім цього, цілий рік ти можеш надавати інформацію про заходи, які ти проводив як голова ОСС разом з командою.

А що далі? Ти просто в кінці року, замість того щоб самому шукати всі ці назви та фото, просто натискаєш на кнопку 
"Отримати звіт", підтверджуєш цю дію і отримуєш презентацію з фоточками. Круто, правда?

## Використані інструменти:
- Aiogram, асинхронна бібліотека для створення телеграм-ботів
- SQLAlchemy, ORM за допомогою якою написані моделі бази даних
- GINO, легка ORM, що базується на SQLAlchemy, для легких асинхронних запитів до БД
- python-pptx - бібліотека, що генерує тобі презентацію
- Celery, асинхронна черга задач, для того щоб синхронний python-pptx не валив усього бота
- все інше ти легко знайдеш у requirements

## У розробці:
- Dockerfile для зручного деплою;