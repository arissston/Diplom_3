# Diplom_3

## Коллега, для установки зависимостей выполни команду: 

    pip3 install -r requirements.txt


## Для запуска теста с созданием отчётов Allure запусти поочерёдно:
    
    *Для тестирования:
    pytest --alluredir=allure_results
    
    *Для визуализации отчётов:
    allure serve allure_results
    
    *Для визуализации отчётов в конкретной папке:
    allure generate C:\***адрес***\allure_results -o C:\***адрес***\Allure_Report
    
    *Чтобы открыть отчёт запустите в терминале:
    allure open Allure_Report