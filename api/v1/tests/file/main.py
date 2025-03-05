import sys
import urllib.parse
sys.path.append('c:\\Projects\\MANDARIN\\1c_tasks')

import asyncio
import json
import urllib
from src.bitrix.requests import upload_file


with open('src/tests/file/raw_response.json', 'rb') as file:
    data = json.load(file)


file_data: dict = data['attached_files'][0]

b64_message = urllib.parse.unquote(file_data['binary'])

async def main():
    result = await upload_file(file_data['name'], b64_message)
    print(result)
    return 1


result = asyncio.run(main())
print(result)

"""Отправка котика""" 
# with open('src/tests/file/test.jpg', 'rb') as file:
#     file_binary = file.read()


# b64_binary = base64.b64encode(file_binary)
# b64_message = b64_binary.decode('utf-8')


# async def main():
#     result = await upload_file('test.jpg', b64_message)
#     # print(result)


# asyncio.run(main())
