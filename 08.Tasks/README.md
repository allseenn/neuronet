# Нейронные сети

## Урок 8. GAN

### Домашнее задание

Сдавать как обычно.

- Задание - Обучите нейронную сеть любой архитектуры на каком-то производственном датасете. Сделайте анализ того, что вам помогло в улучшения работы нейронной сети.
- Можно сегментацию по Северстали.

В конце, обязательно подвести вывод.

## Решение

- [Разведочный анализ](https://github.com/allseenn/neuronet/blob/main/08.Tasks/08eda.ipynb)
- [Бинарный вывод в файл](https://strogino.duckdns.org/data.pkl)
- [Бинарная классификация](https://github.com/allseenn/neuronet/blob/main/08.Tasks/08binary.ipynb)
- [Бинарный вывод в файл (старая версия tensorflow)](https://strogino.duckdns.org/binary_Xception_3.h5) [Бинарный вывод в файл (новая версия tensorflow)](https://strogino.duckdns.org/binary_Xception_2.h5)
- [Многоклассовая классификация](https://github.com/allseenn/neuronet/blob/main/08.Tasks/08multi_label.ipynb)
- [Бинарный вывод в файл (новая версия tensorflow)](https://strogino.duckdns.org/multi_label.h5)
- [Сегментация](https://github.com/allseenn/neuronet/blob/main/08.Tasks/08segmentation.ipynb)
- [Бинарный вывод в файл по дефекту №1](https://strogino.duckdns.org/segmentation_defect_1.h5)
- [Финальный этап](https://github.com/allseenn/neuronet/blob/main/08.Tasks/08final.ipynb)

### Сегментация по Северстали

Работа основна на [решение](https://github.com/ml-projects-rana/Steel-Defect-Detection---Image-Segmentation-using-Keras-and-Tensorflow) индийского аналитика Дипаншу Рана

В ходе моего исследования возникли следующие проблемы:

1. Версионная совместимость кода
2. Вычислительные мощности
3. Распределенные вычисления
4. Проприетарные API

#### 1. Версионная совместимость кода

Код Рана последний раз редактировался более 3-х лет назад, на тот момент использовался Python 3.7, tensorflow 2.8.0, keras 2.8.0 и т.д. 
Из-за несовместимости пакетов, приходилось по брошенным исключениями экспериментировать с разными конфигурациями и версиями пакетов. Т.к. понижение версии, например keras, вызвало ошибки у других пакетов.

В процессе исследования приходилось сохранять промежуточные результаты в бинарные файлы, формат которых тоже имеет версионность и не совместим с разными версиями пакетов. 

Так, пришлось переделать первую и вторую часть данной работы, лишь только из-за того, что сохраненные параметры модели не поддерживаются новой версией tensorflow. А это многочасовые ожидания и затраты вычислительных мощностей.

#### 2. Вычислительные мощности

Вся работа по сегментации выявленных дефектов, состоит из нескольких этапов:
- [Разведочный анализ](https://github.com/allseenn/neuronet/blob/main/08.Tasks/08eda.ipynb)
- [Бинарная классификация](https://github.com/allseenn/neuronet/blob/main/08.Tasks/08binary.ipynb)
- [Многоклассовая классификация](https://github.com/allseenn/neuronet/blob/main/08.Tasks/08multi_label.ipynb)
- [Сегментация](https://github.com/allseenn/neuronet/blob/main/08.Tasks/08segmentation.ipynb)
- [Финальный этап](https://github.com/allseenn/neuronet/blob/main/08.Tasks/08final.ipynb)

Т.к. данные содержат около 20 тысяч картинок, а работа с изображениями очень требовательная к ресурсам задача, то каждый этап выполнялся в отдельном ноутбуке и исчерпывал ресурсы одной учетной записи гугл-колаба, промежуточные результаты сохранились в бинарные файлы, которые при старте следующего этапа, предварительно подгружались в память для использования их в новых расчетах.

Так, самым требовательным к ресурсам, оказался этап по сегментации, для каждого класса дефекта обучение модели подразумевает 25 эпох. Но, на самой мощной конфигурации GPU T4 от гугл-колаба, одна эпоха обучения и валидации длится более двух часов. Т.е. обучения только по одному типу дефектов необходимо 50 часов машинного времени колаба. На бесплатном тарифе машинного времени хватало максимум на пару эпох в результате чего виртуальная среда колаба останавливалась с предупреждением об исчерпании ресурсов.

Было принято решение этап сегментации провести частично, хотя бы для первого класса дефекта, с таким количеством эпох, которое позволит бесплатное время на Кагле.

Кагл позволяет одновременно использовать четыре видеокарты, в результате время выполннения одной эпохи обучения, происходило в четыре раза быстрее, что примерно составляло около 40 минут. Т.е. при выполнении обучения только по одному дефекту требует времени около 10 часов. Но, на четыре дефекта нужно времени около 40 часов. Что опять превышает лимиты, ограниченные бесплатным тарифом в 30 часов в неделю.

#### 3. Распределенные вычисления

Разбивка на этапы с сохранением результатов, позволяет производить распределенные вычисления, на разнородных системах. Используя несколько учетных записей, и на разных вычислительных системах (колаб, Кагл или локальный юпитер ноутбук).

Здесь основной проблемой выступает совместимость не только кода, но и возможности по взаимодействию с облачными системами.
Гугл позволяет взаимодействовать только в основном через гугл диск, Колаб имеет больше возможностей через открытые API.

#### 4. Проприетарные АPI

Гугл колаб не имеет открытых апи, более того его политика всячески запрещает использование стороннего ПО для взаимодействия с его виртуальном окружением. 
Кагл, в этом плане, более открытая платформа, имеющая набор открытого API, но процесс загрузки и выгрузки бинарных файлов затруднен.
Для этих целей пришлось разворачивать свой собственный веб-сервер.

## Выводы

Работа с нейросетями требует огромных, и не только вычислительных ресурсов.

Можно потратить сотни тысяч рублей на видеокарты, так карата NVIDIA T4 Tesla 16GB, аналогичная GPU T4 колаба, стоит около 200 тысяч рублей. 

Чтобы выйти на мощности Кагла с четырьмя ускорителями и остальным железом, необходимо вложить миллион рублей. И это без учета электричества, которые эти самые мощности будут потреблять. 

Так, одна видеокарта может потреблять до 500 Вт в час. А цена электричества за 1КВт/ч может достигать 7 рублей. Следовательно, система с 4 видеокартами может потреблять до 2КВт/ч, что в денежном эквиваленте  равно 14 рублям. Таким образом, только на этапе Сегментации, нужно заплатить за электроэнергию 280 рублей. Т.е. для расчета всех 5 этапов может уйти до тысячи рублей. Это без учета настройки, ошибок и экспериментов. Машинное обучение не из дешевых удовольствий.

Поэтому, перспективным для себя, вижу навыки devops-инженера, разработчика ПО и дата инженера.

Сейчас как никогда, актуальна разработка ПО, позволяющего прозрачно, т.е. незаметно для пользователя, объединить различные бесплатные облачные вычислительные ресурсы в один интерфейс, для разворачивания и обучения промышленных моделей уровня Северстали.

"Разработка Автоматизированного Рабочего Места Специалиста по работе с Данными, для централизованного управления, разворачивания и обучения крупных нейронных сетей, на базе разнородного комплекса бесплатных облачных решений" или сокращенно "АРМ DS".

Как Вам тема для дипломного проекта "АРМ DS"?