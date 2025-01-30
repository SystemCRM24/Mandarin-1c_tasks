from datetime import timedelta

import pytz


def generate_date_range(start, end, data):
    # Извлечение информации о рабочих днях и времени
    work_days = set(data["SHIFTS"][0]["WORK_DAYS"])
    work_time_start = data["SHIFTS"][0]["WORK_TIME_START"]
    work_time_end = data["SHIFTS"][0]["WORK_TIME_END"]

    # Извлечение исключений
    exclusions = data["CALENDAR"]["EXCLUSIONS"]
    excluded_dates = set()
    for year in exclusions:
        for month in exclusions[year]:
            for day in exclusions[year][month]:
                excluded_dates.add(f"{year}-{month}-{day}")

    # Определение начала и конца недели для start и end
    start_week_start = start - timedelta(days=start.isoweekday() - 1)  # Начало недели для start
    start_week_end = start_week_start + timedelta(days=6)  # Конец недели для start

    end_week_start = end - timedelta(days=end.isoweekday() - 1)  # Начало недели для end
    end_week_end = end_week_start + timedelta(days=6)  # Конец недели для end

    # Если start и end находятся в одной неделе, берем только эту неделю
    if start_week_start == end_week_start:
        current_date = start_week_start
        last_date = start_week_end
    else:
        # Иначе берем обе недели целиком
        current_date = start_week_start
        last_date = end_week_end

    result = []
    while current_date <= last_date:
        # Проверка, является ли день рабочим
        if str(current_date.isoweekday()) in work_days:
            date_str = current_date.strftime("%Y-%-m-%-d")
            if date_str not in excluded_dates:
                # Формирование времени начала и окончания работы
                start_time = current_date.replace(hour=0, minute=0, second=0) + timedelta(seconds=work_time_start)
                end_time = current_date.replace(hour=0, minute=0, second=0) + timedelta(seconds=work_time_end)

                # Добавление временной зоны (если не указана)
                if start_time.tzinfo is None:
                    start_time = pytz.utc.localize(start_time)
                if end_time.tzinfo is None:
                    end_time = pytz.utc.localize(end_time)

                # Добавление в результат
                result.append({"start": start_time.isoformat(), "end": end_time.isoformat()})

        # Переход к следующему дню
        current_date += timedelta(days=1)

    return result
