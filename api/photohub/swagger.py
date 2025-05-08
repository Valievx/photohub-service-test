tags = ['Photo Processing']

process_image = dict(
    operation_description='''
    ## Обработка изображения
    Запускает асинхронную обработку изображения через Celery.

    ### Статусы обработки:
    - `pending`: Задача в очереди
    - `processing`: Идет обработка
    - `completed`: Успешно завершено
    - `failed`: Ошибка обработки

    ### Пример запроса:
    ```curl
    curl -X POST -F "image=@photo.jpg" http://localhost:8000/api/photohub/process/
    ```

    ### Ответы:
    - 202 Accepted: Задача принята в обработку
    - 400 Bad Request: Отсутствует изображение
    ''',
    operation_summary="Запуск обработки изображения",
    tags=tags,
    examples=[
        {
            "name": "Success Example",
            "value": {
                "filename": "example.jpg",
                "number": 42,
                "status": "pending"
            },
            "status_codes": ["202"]
        }
    ]
)

image_results = dict(
    operation_description='''
    ## Результаты обработки
    Возвращает список всех загруженных изображений с их статусами обработки

    ### Фильтрация:
    - По умолчанию сортировка по дате загрузки (новые первыми)
    - Статистика по статусам в отдельном поле

    ### Пример ответа:
    ```json
    {
        "photos": [
            {
                "filename": "photo1.jpg",
                "number": 123,
                "status": "completed"
            }
        ],
        "stats": {
            "total": 5,
            "completed": 3,
            "pending": 2
        }
    }
    ```
    ''',
    operation_summary="Получение результатов обработки",
    tags=tags,
    parameters=[
        dict(
            name="status",
            description="Фильтр по статусу обработки",
            required=False,
            type=str,
            enum=["pending", "processing", "completed", "failed"]
        )
    ]
)