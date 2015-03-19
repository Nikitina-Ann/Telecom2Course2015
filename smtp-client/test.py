__author__ = 'Аня'
import unittest
import base64
from smtp import smtpClient
from smtp import MyError
class TestSmtpClient(unittest.TestCase):

    def setUp(self):
        self.client=smtpClient()
        #self.error=MyError()
        self.login='nikitina_ann'
        self.password='f-y-z-'
        self.mailFromAddr='nikitina_ann@rambler.ru'
        self.rcptToAddr= 'nikitina_ann@rambler.ru'
        self.bccString=''
        self.ccString=''
    def tearDown(self):
         self.client.sock.close()
    def test_a_ComConnect(self):
        self.assertFalse(self.client.connect)
        self.client.comConnect('smtp.rambler.ru')
        self.assertTrue(self.client.connect)
    def test_b_ComConnect(self):
        self.assertFalse(self.client.connect)
        self.assertRaises(Exception,self.client.comConnect,'name')
        self.assertFalse(self.client.connect)
    def test_encrBase64(self):
        temp=self.client.encrBase64('f-y-z-')
        self.assertEqual(temp,b'Zi15LXot\r\n')
    def test_a_auth(self):
        self.client.comConnect('smtp.rambler.ru')
        self.client.helo('rambler.ru')
        self.client.auth(self.login,self.password)
        self.assertTrue(self.client.connect)
    def test_b_auth(self):
        self.client.comConnect('smtp.rambler.ru')
        self.client.helo('rambler.ru')
        self.client.auth(self.login,'f-y-z-0')
        self.assertFalse(self.client.connect)
    def test_data(self):
        self.client.comConnect('smtp.rambler.ru')
        self.client.helo('rambler.ru')
        self.client.auth(self.login,self.password)
        self.client.sendFromTo('mailFrom',self.mailFromAddr)
        self.client.sendFromTo('rcptTo', self.rcptToAddr)
        self.client.bccCcRcpt(self.bccString)
        self.client.bccCcRcpt(self.bccString)
        data=self.client.sendData(self.mailFromAddr,self.rcptToAddr,self.ccString,self.bccString,'hi','hello ann')
        self.client.sendMessage(data)
        self.assertTrue(self.client.connect)

if __name__ == '__main__':
    unittest.main()