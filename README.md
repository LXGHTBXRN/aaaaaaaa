Для правильного запуска проекта требуется распаковать папку 
из архива на рабочий стол по пути "C:\Users\*Пользователь*\Desktop", после чего открыть папку в Visual Studio. 
Далее во встроенном терминале файла main.py нужно прописать следующие команды:
________________________________________________________________________________________________________________________________
pip install -r requirements.txt

uvicorn main:app --reload
________________________________________________________________________________________________________________________________
После этого нужно перейти по ссылке: http://127.0.0.1:8000
