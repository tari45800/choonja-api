def get_korean_category_label(category: str) -> str:
    category_map = {
        "task": "할 일",
        "schedule": "일정",
        "record": "기록",
        "routine": "루틴",
    }
    return category_map.get(category, category)
