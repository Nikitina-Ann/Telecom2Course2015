__author__ = 'Аня'
import coverage
cov=coverage.coverage(branch = True, omit = ['flask/*', 'test.py','view.py'])
cov.start()
import unittest
import socket
from smtp import smtpClient
from mock_sock import MockSocketTrue
from mock_sock import MockSocketFalse

class TestMockSocketFalse(unittest.TestCase):
    def setUp(self):
        sock=MockSocketFalse()
        self.client=smtpClient(sock)
        self.login='nikitina_ann'
        self.password='f-y-z-'
    def tearDown(self):
         self.client.sock.close()
    def test_socketFalse(self):
        self.assertFalse(self.client.comConnect('smtp.rambler.ru',25))
        self.assertFalse(self.client.connect)
        self.assertFalse(self.client.helo('rambler.ru'))
        self.assertFalse(self.client.setAuth(self.login,self.password))
        self.assertFalse(self.client.auth)
        self.assertFalse(self.client.sendFromTo('mailFrom','nikitina_ann@rambler.ru'))#Команда mailfrom. ОК
        self.assertFalse(self.client.sendFromTo('rcptTo','nikitina_ann@rambler.ru'))#Команда rcptTo.
        self.assertFalse(self.client.sendMessage('nikitina_ann@rambler.ru','nikitina_ann@rambler.ru','','','hi','hello ann'))
        self.assertFalse(self.client.sendMessage('nikitina_ann@rambler.ru','','','','',''))
        self.assertFalse(self.client.connect)
        self.assertFalse(self.client.auth)
        self.assertFalse(self.client.quit())
class TestMockSocketTrue(unittest.TestCase):
    def setUp(self):
        sock=MockSocketTrue()
        self.client=smtpClient(sock)
        self.login='nikitina_ann'
        self.password='f-y-z-'
        self.mailFromAddr='nikitina_ann@rambler.ru'
        self.rcptToAddr= 'nikitina_ann@rambler.ru,annet-girl@mail.ru'
        self.bccString='uu'
        self.ccString='12'
    def tearDown(self):
         self.client.sock.close()
    def checkRandomBool(self,answer):
        if(self.client.sock.bool==True):
            self.assertTrue(answer)
        else:
            self.assertFalse(answer)
    def test_socketTrue(self):
        for i in [True,False]:
            self.client.sock.hasError=i
            self.checkRandomBool(self.client.comConnect('smtp.rambler.ru',25))
            self.checkRandomBool(self.client.helo('rambler.ru'))
            self.checkRandomBool(self.client.setAuth(self.login,self.password))
            self.checkRandomBool(self.client.sendFromTo('mailFrom',self.mailFromAddr))#Команда mailfrom. ОК
            self.checkRandomBool(self.client.sendFromTo('rcptTo','nikitina_annmail.ru'))#Команда rcptTo.
            self.checkRandomBool(self.client.sendFromTo('rcptTo','nikitina_ann@mail.ru'))#Команда rcptTo. Адрес верен
            self.checkRandomBool(self.client.sendMessage(self.mailFromAddr,'nikitina_ann@rambler.ru','nikitina_ann@rambler.ru',self.bccString,'hi','hello ann'))
            self.checkRandomBool(self.client.quit())

class TestSmtpConnect(unittest.TestCase):
    def setUp(self):
        sock=socket.socket()
        self.client=smtpClient(sock)
    def tearDown(self):
         self.client.sock.close()
    def test_a_ComConnect(self):
        self.assertFalse(self.client.connect)
        self.assertTrue(self.client.comConnect('smtp.rambler.ru',25))
        self.assertTrue(self.client.connect)
        self.assertTrue(self.client.helo('rambler.ru'))
        self.assertFalse(self.client.auth)
    def test_b_ComConnect(self):
        self.assertFalse(self.client.connect)
        self.assertRaises(Exception,self.client.comConnect,'name',25)
        self.assertFalse(self.client.connect)
        self.assertFalse(self.client.auth)
#Ошибка в команде helo
    def test_b_helo(self):
        self.assertTrue(self.client.comConnect('smtp.rambler.ru',25))
        self.assertFalse(self.client.helo(''))
        self.assertFalse(self.client.auth)


class TestAuth(unittest.TestCase):
    def setUp(self):
        sock=socket.socket()
        self.client=smtpClient(sock)
        self.login='nikitina_ann'
        self.password='f-y-z-'
        self.client.comConnect('smtp.rambler.ru',25)
        self.client.helo('rambler.ru')
    def tearDown(self):
         self.client.sock.close()
        #AUTH Оk
    def test_a_auth(self):
        self.assertFalse(self.client.auth)
        self.assertTrue(self.client.setAuth(self.login,self.password))
        self.assertTrue(self.client.auth)
#AUTH Ошибка в команде Password
    def test_b_auth(self):
        self.assertFalse(self.client.auth)
        self.assertFalse(self.client.setAuth(self.login,"ii"))
        self.assertFalse(self.client.auth)
    def test_quit(self):
        self.assertTrue(self.client.connect)
        self.assertTrue(self.client.quit())
        self.assertFalse(self.client.connect)
        self.assertFalse(self.client.auth)


class TestSend(unittest.TestCase):
    def setUp(self):
        sock=socket.socket()
        self.client=smtpClient(sock)
        self.login='nikitina_ann'
        self.password='f-y-z-'
        self.mailFromAddr='nikitina_ann@rambler.ru'
        self.rcptToAddr= 'nikitina_ann@rambler.ru,annet-girl@mail.ru'
        self.bccString='uu'
        self.ccString='12'
        self.client.comConnect('smtp.rambler.ru',25)
        self.client.helo('rambler.ru')
        self.client.setAuth(self.login,self.password)
    def tearDown(self):
         self.client.sock.close()
    def test_sendtoFrom(self):
        self.assertFalse(self.client.sendFromTo('mailFrom','annet-girlmail.ru'))
        self.assertFalse(self.client.sendFromTo('rcptTo','annet-girl@mail.ru'))#Команда rcptTo. Адрес верен
        self.assertTrue(self.client.sendFromTo('mailFrom',self.mailFromAddr))#Команда mailfrom. ОК
        self.assertFalse(self.client.sendFromTo('rcptTo','nikitina_annmail.ru'))#Команда rcptTo. Ошибка в адресе rcptTo
        self.assertTrue(self.client.sendFromTo('rcptTo','nikitina_ann@mail.ru'))#Команда rcptTo. Адрес верен
        self.assertTrue(self.client.sendFromTo('rcptTo','annet-girl@mail.ru'))#Команда rcptTo. Адрес верен
        self.assertFalse(self.client.sendFromTo('rcptTo',' @mail.ru'))#Команда rcptTo. Ошибка в адресе rcptTo
        self.assertTrue(self.client.connect)
        self.assertTrue(self.client.auth)
        self.client.rset()
        self.assertFalse(self.client.connect)
        self.assertFalse(self.client.auth)
    def test_sendMessage(self):
        #Отправка  сообщений
        #self.assertTrue(self.client.sendMessage(self.mailFromAddr,self.rcptToAddr,self.ccString,self.bccString,'hi','hello ann'))
        #self.assertTrue(self.client.sendMessage(self.mailFromAddr,self.rcptToAddr,"", "", "", ""))
        self.assertFalse(self.client.sendMessage("","","", "", "", ""))
        self.assertFalse(self.client.sendMessage(self.mailFromAddr,"","", "", "", ""))
        self.assertTrue(self.client.quit())
        self.assertFalse(self.client.connect)
        self.assertFalse(self.client.auth)


if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    cov.report()
    cov.html_report(directory = '1')
    cov.erase()

