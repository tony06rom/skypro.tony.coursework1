![SkyPro_image](/data/images/for_readme_file/SkyPro.png)
![Python_image](/data/images/for_readme_file/Python.png)
![Git_image](/data/images/for_readme_file/Git.png)
![GitHub_image](/data/images/for_readme_file/GitHub.png)

# Курсовой проект № 1
## Приложение для анализа банковских операций

Приложение на данный момент содержит:
- в каждом модуле имеются свои функции
- gitignore настроен на работу с PyCharm
- подключены линтеры
- локальный Git связан с репозиторием на GitHub
- 
===============================================================================================

### Логика готовой программы



===============================================================================================

### Инструкции для модулей:

1. Модуль _**.....**_
   - Доступные функции:
     - .....
     - .....

     _Пример импорта:_
       ```
     from src.masks import get_mask_card_number
       ```

     <details>
     <summary>Пример работы:</summary>
      
     [![Example_masks][1]][1]
   
      [1]: /data/images/for_readme_file/Example_masks.png
      </details>
   
   
2. Модуль _**.....**_
    - Доступные функции:
      - .....
      - ..... 
      
      _Пример импорта:_
        ```
      from src.widget import mask_account_card
        ```

       <details>
       <summary>Пример работы:</summary>
      
       [![Example_widget][2]][2]
   
       [2]: /data/images/for_readme_file/Example_widget.png
       </details>

   
3. Модуль _**.....**_
    - Доступные функции:
      - ......
      - ....
      
      _Пример импорта:_
        ```
      from src.processing import get_mask_card_number
      ```

       <details>
       <summary>Пример работы:</summary>
      
       [![Example_processing][3]][3]
   
       [3]: /data/images/for_readme_file/Example_processing.png
       </details>

      
Все тесты функций можно выполнять из директории [moduls_test](/moduls_test)

===============================================================================================
## Pytest

Реализовано тестирование функций при помощи pytest.
Отчет реализован в импорте в [html](/htmlcov)
На данный момент покрыто тестами 90% функций проекта (скриншоты отчёта):

   <details>
   <summary>Проверка по файлам:</summary>
  
   [![Example_processing][5]][5]

   [5]: /data/images/for_readme_file/Pytest_files.png
   </details>

   <details>
   <summary>Проверка по функциям:</summary>
  
   [![Example_processing][6]][6]

   [6]: /data/images/for_readme_file/Pytest_functions.png
   </details>

   <details>
   <summary>Проверка по классам:</summary>
  
   [![Example_processing][7]][7]

   [7]: /data/images/for_readme_file/Pytest_classes.png
   </details>


===============================================================================================

## logging

На данный момент логирование реализовано для модулей **masks** и **utils**

### Директория логов: ```../logs```

### Доступные уровни логирования:
- critical
- error
- warning
- info
- debug

### Доступные форматы логирования:
* __%(asctime)s__ — дата и время события логирования
* __%(name)s__ — имя логера
* __%(levelname)s__ — уровень логирования
* __%(message)s__ — текст сообщения
* __%(filename)s__ — имя файла, в котором произошло событие
* __%(funcName)s__ — имя функции, в которой произошло событие
* __%(lineno)d__ — номер строки, в которой произошло событие
* __%(process)d__ — ID процесса
* __%(thread)d__ — ID потока

### Используемый формат логов:
```%(asctime)s | %(name)s | %(levelname)s | %(funcName)s: %(message)s```

   <details>
   <summary>Пример лога (utils):</summary>
  
   [![Example_logging][8]][8]

   [8]: /data/images/for_readme_file/Example_logging.png
   </details>


===============================================================================================

## Проблемы тестирования

## Полезные команды тестирования

Формирование отчёта в html:
```pytest --cov=src --cov-report=html```
Отчёт в консоли:
```run pytest --cov```
Проверка тестовых файлов:
```pytest -cov```

===============================================================================================

## Примечания по проекту



===============================================================================================

## Проблемы проекта




===============================================================================================

Этот проект выполняется совместно с [SkyPro](https://sky.pro/)
####  Автор проекта: **Romanenko Anton**
