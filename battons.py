import json

def get_button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }

markup_z = {
    "one_time": False,
    "buttons": [
    [get_button(label="Начать", color="positive")]
    ]
}

markup_z = json.dumps(markup_z, ensure_ascii=False).encode('utf-8')
markup_z = str(markup_z.decode('utf-8'))

markup_x = {
    "one_time": False,
    "buttons": [
    [get_button(label="Получить задание", color="positive")],
    [get_button(label="Проверить задание", color="negative")],
    [get_button(label="Отменить задание", color="positive")],
    [get_button(label="Добавить задание", color="negative")],
    [get_button(label="Проверить баланс", color="positive")],
    [get_button(label="Вывести коины", color="negative")],
    [get_button(label="Пополнить баланс", color="positive")]
    ]
}

markup_x = json.dumps(markup_x, ensure_ascii=False).encode('utf-8')
markup_x = str(markup_x.decode('utf-8'))

markup_a = {
    "one_time": False,
    "buttons": [
    [get_button(label="К началу", color="positive")]
    ]
}

markup_a = json.dumps(markup_a, ensure_ascii=False).encode('utf-8')
markup_a = str(markup_a.decode('utf-8'))
