from datetime import timedelta, datetime


d = datetime.utcnow()

print(d)

async def main():
    """Тестовая функция для проверки кодирования файла"""
    import base64
    with open("src/bitrix/test_cat.jpg", "rb") as binary_file:
        binary_file_data = binary_file.read()
    base64_encoded_data = base64.b64encode(binary_file_data)
    base64_message = base64_encoded_data.decode("utf-8")
    await upload_file("cat.jpg", base64_message)