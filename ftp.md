#Сервер протокола FTP, функционирующий в фктивном режиме
##Индивидуальное задание
Задание: разработать приложение для операционных систем семейства Windows или Linux, обеспечивающее функции FTP-сервера.     

Основные возможности. Приложение должно реализовывать следующие функции:   

1. Хранение идентификационной и аутентификационной информации нескольких пользователей
2. Поддержка анонимного входа (пользователь anonymous)
3. Обработка подключения клиента
4. Выдача по запросу клиента содержимого каталога
5. Навигация по системе каталогов
6. Создание нового каталога
7. Удаление каталога
8. Посылка по запросу клиента содержимого указанного файла
9. Приём по запросу клиента содержимого указанного файла
10. Удаление указанного файла
11. Протоколирование соединения сервера с клиентом

Поддерживаемые команды. Разработанное приложение должно реализовывать следующие команды протокола FTP:

- USER – получение от клиента идентификационной информации
пользователя
- PASS – получение от клиента пароля пользователя
- LIST – отправка клиенту расширенной информации о списке файлов
каталога
- NLST – отправка клиенту сокращённой информации о списке фай-
лов каталога
- CWD – смена текущего каталога сервера
- MKD – создание каталога
- RMD – удаление каталога
- DELE – удаление файла на сервере
- PORT – получение параметров сокета клиента (адреса и порта), осуществляющего приём и передачу данных
- RETR – посылка файла клиенту
- STOR – запись полученного от клиента файла
- TYPE – задание режима передачи данных
- QUIT – удаление всех помеченных сообщений и завершение сеанса

Настройки приложения. Разработанное приложение должно обеспечивать:

1. настройку номера порта сервера (по умолчанию – 21)
2. настройку корневого каталога сервера для каждого пользователя

Методика тестирования. Для тестирования приложения следует использовать стандартные FTP-клиенты, установленные в лаборатории (Mozilla Firefox, MS Explorer, Far, Total Commander).
С помощью имеющихся клиентов протокола FTP осуществляется подключение к серверу с различной аутентификационной информацией. В процессе тестирования проверяются основные возможности сервера по передаче, приёму, удалению файлов, навигации по файловой системе, функции по работе с каталогами.   

##Теоритические сведения протокола FTP 
Предоставленная информация соответсвует [RFC 959 [Postel and Reynolds 1985]-протокол FTP.] (http://www.soslan.ru/tcp/tcp27.html)   

FTP отличается от других приложений тем, что он использует два TCP соединения для передачи файла.

1. Управляющее соединение устанавливается как обычное соединение клиент-сервер. Сервер осуществляет пассивное открытие на заранее известный порт FTP (21) и ожидает запроса на соединение от клиента. Клиент осуществляет активное открытие на TCP порт 21, чтобы установить управляющее соединение. Управляющее соединение существует все время, пока клиент общается с сервером. Это соединение используется для передачи команд от клиента к серверу и для передачи откликов от сервера. Тип IP сервиса для управляющего соединения устанавливается для получения "минимальной задержки", так как команды обычно вводятся пользователем.    
2. Соединение данных открывается каждый раз, когда осуществляется передача файла между клиентом и сервером. Тип сервиса IP для соединения данных должен быть "максимальная пропускная способность", так как это соединение используется для передачи файлов.

###Команды и отклики FTP

Команды и отклики передаются по управляющему соединению между клиентом и сервером в формате NVT ASCII. В конце каждой строки команды или отклика присутствует пара CR, LF.   
Отклики состоят из 3-циферных значений в формате ASCII, и необязательных сообщений, которые следуют за числами. Подобное представление откликов объясняется тем, что программному обеспечению необходимо посмотреть только цифровые значения, чтобы понять, что ответил процесс, а дополнительную строку может прочитать человек. Поэтому пользователю достаточно просто прочитать сообщение (причем нет необходимости запоминать все цифровые коды откликов).
Каждая из трех цифр в коде отклика имеет собственный смысл. Ниже показаны значения первых и вторых цифр в коде отклика. Третья цифра дает дополнительное объяснение сообщению об ошибке. 

- 1yz	Положительный предварительный отклик. Действие началось, однако необходимо дождаться еще одного отклика перед отправкой следующей команды.
- 2yz	Положительный отклик о завершении. Может быть отправлена новая команда.
- 3yz	Положительный промежуточный отклик. Команда принята, однако необходимо отправить еще одну команду.
- 4yz	Временный отрицательный отклик о завершении. Требуемое действие не произошло, однако ошибка временная, поэтому команду необходимо повторить позже.
- 5yz	Постоянный отрицательный отклик о завершении. Команда не была воспринята и повторять ее не стоит.
- x0z	Синтаксическая ошибка.
- x1z	Информация.
- x2z	Соединения. Отклики имеют отношение либо к управляющему, либо к соединению данных.
- x3z	Аутентификация и бюджет. Отклик имеет отношение к логированию или командам, связанным с бюджетом.
- x4z	Не определено.
- x5z	Состояние файловой системы.

###Управление соединением

Использовать соединение данных можно тремя способами.

- Отправка файлов от клиента к серверу.
- Отправка файлов от сервера к клиенту.
- Отправка списка файлов или директорий от сервера к клиенту.

FTP сервер посылает список файлов по соединению данных, вместо того чтобы посылать многострочные отклики по управляющему соединению. При этом появляется возможность избежать любых ограничений в строках, накладывающихся на размер списка директории.
Конец файла обозначает закрытие соединения данных. Из этого следует, что для передачи каждого файла или списка директории требуется новое соединение данных. Обычная процедура FTP в активном режиме выглядит следующим образом:

1. Создание соединения данных осуществляется клиентом, потому что именно клиент выдает команды, которые требуют передать данные (получить файл, передать файл или список директории).
2. Клиент обычно выбирает динамически назначаемый номер порта на хосте клиента для своего конца соединения данных. Клиент осуществляет пассивное открытие с этого порта.
3. Клиент посылает этот номер порта на сервер по управляющему соединению с использованием команды PORT.
4. Сервер принимает номер порта с управляющего соединения и осуществляет активное открытие на этот порт хоста клиента. Сервер всегда использует порт 20 для соединения данных.   

![Команда PORT, передаваемая по управляющему соединению FTP.](http://www.soslan.ru/tcp/img/t27_4.gif "Дополнительное описание")   
![FTP сервер осуществляет активное открытие соединения данных.](http://www.soslan.ru/tcp/img/t27_5.gif "Дополнительное описание")

На первом рисунке показано состояние соединений, пока осуществляется шаг номер 3. Мы предполагаем, что динамически назначаемый порт клиента для управляющего соединения имеет номер 1173, а динамически назначаемый порт клиента для соединения данных имеет номер 1174. Команда, посылаемая клиентом - PORT, а ее аргументы это шесть десятичных цифр в формате ASCII, разделенные запятыми. Четыре первых числа - это IP адрес клиента, на который сервер должен осуществить активное открытие (140.252.13.34 в данном примере), а следующие два - это 16-битный номер порта. Так как 16-битный номер порта формируется из двух цифр, его значение в этом примере будет 4 x 256 + 150 = 1174.   
На втором рисунке показано состояние соединений, когда сервер осуществляет активное открытие на конец клиента соединения данных. Конечная точка сервера это порт 20.

Сервер всегда осуществляет активное открытие соединения данных. Обычно сервер также осуществляет активное закрытие соединения данных, за исключением тех случаев, когда клиент отправляет файл на сервер в потоковом режиме, который требует, чтобы клиент закрыл соединение (что делается с помощью уведомления сервера о конце файла).  

###Анонимный FTP

Существует невероятно популярная форма использования FTP. Она называется анонимный FTP (anonymous FTP). Если эта форма поддерживается сервером, она позволяет любому получить доступ к серверу и использовать FTP для передачи файлов. С помощью анонимного FTP можно получить доступ к огромному объему свободно распространяемой информации.    
Чтобы использовать анонимный FTP, мы входим в систему с именем пользователя "anonymous". Когда появляется приглашение ввести пароль, мы вводим наш адрес электронной почты.

##Архитектура приложения
###Команды клиента и ответы сервера
 
<table>
  <tr>
    <th>Команда</th>
    <th>Собщение положительного ответа сервера</th>
    <th>Код положительного ответа сервера</th>
  </tr>
  <tr>
    <td> QUIT</td>
    <td>Goodbye</td>
    <td>221</td>
  </tr>
  <tr>
    <td>TYPE [binary(ascii)]</td>
    <td>Type set to I(A)</td>
    <td>200</td>
  </tr>
  <tr>
    <td> XMKD [name]</td>
    <td>Folder [name] create</td>
    <td>257</td>
  </tr>
  <tr>
    <td> XRMD [name]</td>
    <td>Directory [name] deleted</td>
    <td>250</td>
  </tr>
  <tr>
    <td> DELE[name]</td>
    <td>File [name] deleted</td>
    <td>250</td>
  </tr>
  <tr>
    <td> AUTH [name]</td>
    <td>Write the password</td>
    <td>331</td>
  </tr>
   <tr>
    <td> [password]</td>
    <td>User [name] logged in</td>
    <td>230</td>
  </tr>
  <tr>
    <td> CWD</td>
    <td>Current directory is [ ]</td>
    <td>250</td>
  </tr>
   <tr>
    <td> CWDUP</td>
    <td>Current directory is [..]</td>
    <td>250</td>
  </tr>
    <tr>
    <td>PORT [ ]</td>
    <td>PORT command succesful</td>
    <td>200</td>
  </tr>
    <tr>
    <td> LIST, NLST, RETR [name], STOR [name]</td>
    <td>Accepted data connection</td>
    <td>150</td>
  </tr>
   </tr>
    <tr>
    <td> </td>
    <td>[data]</td>
    <td> </td>
  </tr>
    </tr>
    <tr>
    <td> </td>
    <td>Transfer complete</td>
    <td>226</td>
  </tr>
</table>