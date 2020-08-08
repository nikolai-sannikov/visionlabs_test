# Тестовое задание
## 
На сервере существует директория images/ с произвольным количеством изображений (jpg)

Необходмо создать web-сервис который:

+ Отдает изображения из вышеуказанной директории по эндпоинту http://<hostname>:<port>/images/<image name>.jpg
+ Имеет эндпоинт http://<hostname>:<port>/image с помощью которого можно:
    + Вывести список изображений в JSON формате который содержит имя файла, размер, время последнего изменения.
    + Удалить изображение по его имени
    + Создать новое изображение из переданной base64 строки

Пожелания по стеку:
python 3.7 или 3.8
web - aiohttp или flask

Дополнительным плюсом при решении задания будет использование docker-compose для деплоя




Clarifications:
    how to assign image names? randomly? 