def web1(ip_transmitter):
    try:
        session=requests.session()
        login='admin'
        password='root'
        url='http://192.168.1.110/cgi-bin/decoder.cgi'
        page=session.get(url=url, auth=(login, password))
        page.encoding="windows-1252"
        soup = BeautifulSoup(page.text, 'html.parser')
        variants = soup.find_all("input", {"name":"service_name"})
        print(variants)
        for i in variants:
            channel_rad=i.attrs['value']
        print(channel_rad)
        if channel_rad=="":
            channel_rad=str(parametr('.1.3.6.1.4.1.38295.31.4.1.0','public','192.168.1.110', 161))
            begin=int(channel_rad.find("=")+2)
            end=begin+15
            channel_rad=channel_rad[begin:end]
            channel_rad.strip()
            print(channel_rad)

           
except Exception as ex:
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print (message)
    input()

else:
    try:
        mail_recievers=['ukolov@25kadr-reklama.ru','kovalev@25kadr-reklama.ru', 'kazakov@@25kadr-reklama.ru']
        if channel_rad!="RADIO DACHA":
            # Настройки
            email = 'monitoring@25kadr-reklama.ru'
            mail_receiver = 'ukolov@25kadr-reklama.ru'
            password = 'panda-2016-panda'

            # Формируем тело письма
            subject = "Salehard:Wrong radio channel"
            email_text = "Host: Salehard, Dacha\n Channel:"+channel_rad 
          
            #цепляемся к серверу
            server = smtp.SMTP('smtp.yandex.ru', 587)
            server.ehlo() # Кстати, зачем это? 
            server.starttls()
            server.login(email, password)

            message = 'From: %s\nTo: %s\nSubject: %s\n\n%s' % (email,
                                                               mail_receiver,
                                                               subject,
                                                               email_text)

            #server.set_debuglevel(1) # Необязательно; так будут отображаться данные с сервера в консоли
            for i in mail_recievers:
                server.sendmail(email, i, message)
            server.quit()
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
        input()
try:
     metrics = [
        ZabbixMetric('Salekh_Dacha_Sat', 'S', 1, clock=None),
        ]
     zbx=ZabbixSender(zabbix_server='176.116.185.33',
                                zabbix_port=10051,
                                socket_wrapper=None, timeout=20)
     zbx.send(metrics)
except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
        
    
    return rezult

def web1(ip_transmitter):
try:
        session=requests.session()
        #login='admin'
        #password='root'
        url='http://192.168.1.202/tcf?cgi=show&$path=/Service'
        #page=session.get(url=url, auth=(login, password))
        page=session.get(url)
        page.encoding="windows-1252"
        soup = BeautifulSoup(page.text, 'html.parser')
        #print(page.text)
        #variants = soup.find_all("input", {"name":"service_name"})
        variant = soup.find_all("script")
        
        spisok_of_channels={
            392: 'RetroFM2',
            395: 'EuropaPlus4',
            1101: 'MTV',
            1102: 'Nickelodeon',
            1104: 'ShopShow',
            1105: 'ParamountChannel',
            1106: 'Nicktoons',
            1108: 'Paramount Comedy',
            1109: '2',
            1110: '1 2',
            1111: '3',
            1112: 'XXnonASCIIXX',
            1113: 'XXnonASCIIXX',
            1114: '24',
            1115: 'Leomax',
            1116: '4',
            1121: 'XXnonASCIIXX',
            1122: 'XXnonASCIIXX'
        }
        perem=0
        for i in range(0,2):
            rezult=variant.pop().text
            #print(rezult+'\n')
            if i==1:
                perem=rezult.find("Current Audio PID','")
                rezult=int(rezult[perem+21:perem+24])
                #print(channel_rad)
                break
        if rezult==294:
            channel_rad='294 - RetroFM4'
        else:
            try:
                channel_rad = spisok_of_channels[rezult]
            except KeyError as e:
                channel_rad="Unkknown"
        print(channel_rad)
        channel_rad.strip()


    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)

    else:
        metrics = [
            ZabbixMetric('Kansk_Retro_Sat', 'RAD', channel_rad, clock=None),
            ]
    zbx=ZabbixSender(zabbix_server='176.116.185.33',
                                    zabbix_port=10051,
                                    socket_wrapper=None, timeout=20)
    zbx.send(metrics)
    return rezult


try:
        session=requests.session()
        login='admin'
        password='root'
        url='http://192.168.0.251/cgi-bin/decoder.cgi'
        page=session.get(url=url, auth=(login, password))
        page.encoding="windows-1252"
        soup = BeautifulSoup(page.text, 'html.parser')
        variants = soup.find_all("input", {"name":"service_name"})
        for i in variants:
            channel_rad=i.attrs['value']
            channel_rad=channel_rad.strip()

        print(channel_rad)

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)

    else:
        metrics=data('Nalchik_Autoradio_Sat')
        print('Настроил метрики')
        connection_internet=is_conencted()
        if connection_internet==True:
            try:
                connetion_zabbix=chek_port('176.116.185.33',10051)
                print('Забикс в порядке')
                zbx.send(metrics)
                print('Отправил данные'+'\n')
                    
            except (TimeoutError, ConnectionRefusedError):
                print('Соединение с Забиксом разорвано')
                while True:
                    try:
                        connetion_zabbix=chek_port('176.116.185.33',10051)
                        print('соединение с Забиксом восстановлено')
                        zbx.send(metrics)
                        print('Отправил данные')
                        break
                    except (TimeoutError, ConnectionRefusedError):
                        print('Соединение с Забиксом разорвано')
                    except ConnectionAbortedError:
                        print('Попытка соединения провалена')
                        while True:
                            try:
                                connection_internet=is_conencted()
                                if connection_internet==True:
                                    print('соединение с интернетом восстановлено')
                                    time.sleep(2)
                                    break
                            except:
                                print('Соединение с интернетом не удалось восстановить')
                                pass
                else:
                    print('соединение восстановлено')
                    zbx.send(metrics)
                    print('Отправил данные после перезагрузки')
                    break
                    
            except ConnectionAbortedError:
                print('Попытка соединения провалена')
                while True:
                    try:
                        connection_internet=is_conencted()
                        if connection_internet==True:
                            print('соединение с интернетом восстановлено')
                            time.sleep(2)
                            break
                    except:
                        print('Соединение с интернетом не удалось восстановить')
                        pass
        else:
            #если совсем нет интернета
            while True:
                connection_internet=is_conencted()
                if connection_internet==False:
                    print('соединение разорвано')
                    time.sleep(2)
                else:
                    print('соединение восстановлено')
                    zbx.send(metrics)
                    print('Отправил данные после перезагрузки')
                    break
    print('\n')
    #Европа+
    print('Европа+')
    try:
        session=requests.session()
        #login='ird'
        #password='ird'
        url='http://192.168.0.252/Status.asp'
        #page=session.get(url=url, auth=(login, password))
        page=session.get(url)
        #page.encoding="windows-1252"
        #print(page.text)
        soup = BeautifulSoup(page.text, 'html.parser')
        #variants = soup.find_all("tr", {"name":"service_name"})
        variants = soup.find_all("tr", class_='cell_out', nowrap="")
        #print(variants)
        
        for i in range(0,7):
            variants.pop()
        for i in range(-4,-1):
            variants.pop(i)
        variant=variants.pop()
        
        j=0
        for i in variant:
            #print(i.text)
            j=j+1
            if j==2:
                channel_rad=i.text
        #print('\n')
        #print(rezult)

        channel_rad.strip()
        print(channel_rad)
        
        
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)

    else:
        metrics=data('Nalchik_Europa_plus_Sat')
        print('Настроил метрики')
        connection_internet=is_conencted()
        if connection_internet==True:
            try:
                connetion_zabbix=chek_port('176.116.185.33',10051)
                print('Забикс в порядке')
                zbx.send(metrics)
                print('Отправил данные'+'\n')
                    
            except (TimeoutError, ConnectionRefusedError):
                print('Соединение с Забиксом разорвано')
                while True:
                    try:
                        connetion_zabbix=chek_port('176.116.185.33',10051)
                        print('соединение с Забиксом восстановлено')
                        zbx.send(metrics)
                        print('Отправил данные')
                        break
                    except (TimeoutError, ConnectionRefusedError):
                        print('Соединение с Забиксом разорвано')
                    except ConnectionAbortedError:
                        print('Попытка соединения провалена')
                        while True:
                            try:
                                connection_internet=is_conencted()
                                if connection_internet==True:
                                    print('соединение с интернетом восстановлено')
                                    time.sleep(2)
                                    break
                            except:
                                print('Соединение с интернетом не удалось восстановить')
                                pass
                else:
                    print('соединение восстановлено')
                    zbx.send(metrics)
                    print('Отправил данные после перезагрузки')
                    break
                    
            except ConnectionAbortedError:
                print('Попытка соединения провалена')
                while True:
                    try:
                        connection_internet=is_conencted()
                        if connection_internet==True:
                            print('соединение с интернетом восстановлено')
                            time.sleep(2)
                            break
                    except:
                        print('Соединение с интернетом не удалось восстановить')
                        pass
        else:
            #если совсем нет интернета
            while True:
                connection_internet=is_conencted()
                if connection_internet==False:
                    print('соединение разорвано')
                    time.sleep(2)
                else:
                    print('соединение восстановлено')
                    zbx.send(metrics)
                    print('Отправил данные после перезагрузки')
                    break
    print('\n')
    #Радио7
    print('Радио7')
    try:
        session=requests.session()
        #login='ird'
        #password='ird'
        url='http://192.168.0.250/Status.asp'
        #page=session.get(url=url, auth=(login, password))
        page=session.get(url)
        #page.encoding="windows-1252"
        #print(page.text)
        soup = BeautifulSoup(page.text, 'html.parser')
        #variants = soup.find_all("tr", {"name":"service_name"})
        variants = soup.find_all("tr", class_='cell_out', nowrap="")
        #print(variants)
        
        for i in range(0,7):
            variants.pop()
        for i in range(-4,-1):
            variants.pop(i)
        variant=variants.pop()
        
        j=0
        for i in variant:
            #print(i.text)
            j=j+1
            if j==2:
                channel_rad=i.text
        #print('\n')
        #print(rezult)

        channel_rad.strip()
        print(channel_rad)
        
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)

    else:
        metrics=data('Nalchik_Radio7_Sat')
        print('Настроил метрики')
        connection_internet=is_conencted()
        if connection_internet==True:
            try:
                connetion_zabbix=chek_port('176.116.185.33',10051)
                print('Забикс в порядке')
                zbx.send(metrics)
                print('Отправил данные'+'\n')
                    
            except (TimeoutError, ConnectionRefusedError):
                print('Соединение с Забиксом разорвано')
                while True:
                    try:
                        connetion_zabbix=chek_port('176.116.185.33',10051)
                        print('соединение с Забиксом восстановлено')
                        zbx.send(metrics)
                        print('Отправил данные')
                        break
                    except (TimeoutError, ConnectionRefusedError):
                        print('Соединение с Забиксом разорвано')
                    except ConnectionAbortedError:
                        print('Попытка соединения провалена')
                        while True:
                            try:
                                connection_internet=is_conencted()
                                if connection_internet==True:
                                    print('соединение с интернетом восстановлено')
                                    time.sleep(2)
                                    break
                            except:
                                print('Соединение с интернетом не удалось восстановить')
                                pass
                else:
                    print('соединение восстановлено')
                    zbx.send(metrics)
                    print('Отправил данные после перезагрузки')
                    break
                    
            except ConnectionAbortedError:
                print('Попытка соединения провалена')
                while True:
                    try:
                        connection_internet=is_conencted()
                        if connection_internet==True:
                            print('соединение с интернетом восстановлено')
                            time.sleep(2)
                            break
                    except:
                        print('Соединение с интернетом не удалось восстановить')
                        pass
        else:
            #если совсем нет интернета
            while True:
                connection_internet=is_conencted()
                if connection_internet==False:
                    print('соединение разорвано')
                    time.sleep(2)
                else:
                    print('соединение восстановлено')
                    zbx.send(metrics)
                    print('Отправил данные после перезагрузки')
                    break
    print('\n')

       try:
        session=requests.session()
        #login='admin'
        #password='root'
        url='http://192.168.1.11/web/getcurrent'
        #page=session.get(url=url, auth=(login, password))
        page=session.get(url)
        page.encoding="windows-1252"
        soup = BeautifulSoup(page.text, 'html.parser')
        #print(page.text)
        
        channel_rad = soup.find("e2servicename").text
        channel_rad.strip()
        #print(channel_rad)
        

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)


    else:
        metrics = [
            ZabbixMetric('NewUrengoy_Energy_Sat', 'RAD', channel_rad, clock=None),
            ]
    zbx=ZabbixSender(zabbix_server='176.116.185.33',
                                    zabbix_port=10051,
                                    socket_wrapper=None, timeout=20)
    zbx.send(metrics)



     try:
        session=requests.session()
        login='admin'
        password='root'
        url='http://192.168.0.110/cgi-bin/decoder.cgi'
        page=session.get(url=url, auth=(login, password))
        page.encoding="windows-1252"
        soup = BeautifulSoup(page.text, 'html.parser')
        variants = soup.find_all("input", {"name":"service_name"})
        #print(variants)
        for i in variants:
            channel_rad=i.attrs['value']
        #print(channel_rad)
        if channel_rad=="":
            num_channel_rad=int(parametr('.1.3.6.1.4.1.38295.31.1.3.4.0','public','192.168.0.110', 161))
            if num_channel_rad==32:
                channel_rad="RUSSIAN_RADIO_2H"
            else:
                channel_rad="Unknown"

    except:
        pass
    '''
    else:
        try:
            mail_recievers=['ukolov@25kadr-reklama.ru','kovalev@25kadr-reklama.ru', 'kozlov@25kadr-reklama.ru']
            if channel_rad!="RUSSIAN_RADIO_2H":
                # Настройки
                email = 'monitoring@25kadr-reklama.ru'
                password = 'panda-2016-panda'

                # Формируем тело письма
                subject = "Norilsk:Wrong radio channel"
                email_text = "Host: Norilsk, RusRadio\n Channel:"+channel_rad 
              
                #цепляемся к серверу
                server = smtp.SMTP('smtp.yandex.ru', 587)
                server.ehlo() # Кстати, зачем это? 
                server.starttls()
                server.login(email, password)


                #server.set_debuglevel(1) # Необязательно; так будут отображаться данные с сервера в консоли
                for i in mail_recievers:
                    message = 'From: %s\nTo: %s\nSubject: %s\n\n%s' % (email,
                                                                   mail_receiver,
                                                                   subject,
                                                                   email_text)
                    server.sendmail(email, i, message)
                server.quit()
        except:
            pass
    '''
    try:
         metrics = [
            ZabbixMetric('Norilsk_RusRadio_Sat', 'RAD', channel_rad, clock=None),
            ]
         zbx=ZabbixSender(zabbix_server='176.116.185.33',
                                    zabbix_port=10051,
                                    socket_wrapper=None, timeout=20)
         zbx.send(metrics)
         
    except:
        pass  

    try:
        session=requests.session()
        login='admin'
        password='root'
        url='http://192.168.0.114/cgi-bin/decoder.cgi'
        page=session.get(url=url, auth=(login, password))
        page.encoding="windows-1252"
        soup = BeautifulSoup(page.text, 'html.parser')
        variants = soup.find_all("input", {"name":"service_name"})
        #print(variants)
        for i in variants:
            channel_rad=i.attrs['value']
        #print(channel_rad)
        if channel_rad=="":
            num_channel_rad=int(parametr('.1.3.6.1.4.1.38295.31.1.3.4.0','public','192.168.0.114', 161))
            if num_channel_rad==32:
                channel_rad="Radio Chanson (0h)"
            else:
                channel_rad="Unknown"
            #print(channel_rad)

               
    except:
        pass
    '''
    else:
        try:
            mail_recievers=['ukolov@25kadr-reklama.ru','kovalev@25kadr-reklama.ru', 'kozlov@25kadr-reklama.ru']
            if channel_rad!="Radio Chanson (0h)":
                # Настройки
                email = 'monitoring@25kadr-reklama.ru'
                password = 'panda-2016-panda'

                # Формируем тело письма
                subject = "Norilsk:Wrong radio channel"
                email_text = "Host: Norilsk, Shanson\n Channel:"+channel_rad 
              
                #цепляемся к серверу
                server = smtp.SMTP('smtp.yandex.ru', 587)
                server.ehlo() # Кстати, зачем это? 
                server.starttls()
                server.login(email, password)


                #server.set_debuglevel(1) # Необязательно; так будут отображаться данные с сервера в консоли
                for i in mail_recievers:
                    message = 'From: %s\nTo: %s\nSubject: %s\n\n%s' % (email,
                                                                   i,
                                                                   subject,
                                                                   email_text)
                    
                    server.sendmail(email, i, message)
                server.quit()
            
                
                
        except:
            pass
    '''
    try:
         metrics = [
            ZabbixMetric('Norilsk_Shanson_Sat', 'RAD', channel_rad, clock=None),
            ]
         zbx=ZabbixSender(zabbix_server='176.116.185.33',
                                    zabbix_port=10051,
                                    socket_wrapper=None, timeout=20)
         zbx.send(metrics)
    except:
        pass  
        

    try:
        session=requests.session()
        login='admin'
        password='root'
        url='http://192.168.0.111/status.asp'
        page=session.get(url=url, auth=(login, password))
        page.encoding="windows-1252"
        #print(page.text)
        soup = BeautifulSoup(page.text, 'html.parser')
        variants=soup.find_all("td", class_="StatusDis", width="151", align="left", valign="middle", bgcolor="#EAEAEA")
        #print(variants)
        #for i in variants:
            #print(i.getText())
        #print(len(variants))
        for i in range(1,len(variants)+1):
            rezult=variants.pop()
            #print(str(i))
        #print(rezult)
        channel_rad=rezult.getText()
        channel_rad.strip()
        #print(channel_rad)

    except:
        pass

    else:
        metrics = [
            ZabbixMetric('Norilsk_Dacha_Sat', 'RAD', channel_rad, clock=None),
            ]
        zbx=ZabbixSender(zabbix_server='176.116.185.33',
                                    zabbix_port=10051,
                                    socket_wrapper=None, timeout=20)
        zbx.send(metrics)


    try:
        channel_rad=str(parametr('.1.3.6.1.4.1.38295.3200.1.2.2.2.0','public','192.168.0.113', 161))
        begin=int(channel_rad.find("=")+2)
        end=begin+15
        channel_rad=channel_rad[begin:end]
        channel_rad.strip()
        #print(channel_rad)
        
    except:
        pass
    else:
        metrics = [
            ZabbixMetric('Norilsk_Novoe_Sat', 'RAD', channel_rad, clock=None),
            ]
        zbx=ZabbixSender(zabbix_server='176.116.185.33',
                                    zabbix_port=10051,
                                    socket_wrapper=None, timeout=20)
        zbx.send(metrics)

    try:
        channel_rad=str(parametr('.1.3.6.1.4.1.38295.3200.1.2.2.2.0','public','192.168.0.112', 161))
        begin=int(channel_rad.find("=")+2)
        end=begin+15
        channel_rad=channel_rad[begin:end]
        channel_rad.strip()
        #print(channel_rad)
        
    except:
        pass
    else:
        metrics = [
            ZabbixMetric('Norilsk_Energy_Sat', 'RAD', channel_rad, clock=None),
            ]
        zbx=ZabbixSender(zabbix_server='176.116.185.33',
                                    zabbix_port=10051,
                                    socket_wrapper=None, timeout=20)
        zbx.send(metrics)


        try:
        channel_rad=str(parametr('.1.3.6.1.4.1.38295.3200.1.2.2.2.0','public','192.168.0.110', 161))
        begin=int(channel_rad.find("=")+2)
        end=begin+15
        channel_rad=channel_rad[begin:end]
        channel_rad.strip()
        print(channel_rad)
        
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
        input("Нажмите ENTER для выхода")
        
    else:
        metrics = [
            ZabbixMetric('UzhnoSah_Energy_Sat', 'RAD', channel_rad, clock=None),
            ]
        zbx=ZabbixSender(zabbix_server='176.116.185.33',
                                    zabbix_port=10051,
                                    socket_wrapper=None, timeout=20)
        zbx.send(metrics)







        try:
        session=requests.session()
        login='admin'
        password='root'
        url='http://192.168.0.110/cgi-bin/decoder.cgi'
        page=session.get(url=url, auth=(login, password))
        page.encoding="windows-1252"
        soup = BeautifulSoup(page.text, 'html.parser')
        variants = soup.find_all("input", {"name":"service_name"})
        #print(variants)
        for i in variants:
            channel_rad=i.attrs['value']
        #print(channel_rad)
        if channel_rad=="":
            num_channel_rad=str(parametr('.1.3.6.1.4.1.38295.31.1.3.4.0','public','192.168.1.110', 161))
            begin=int(num_channel_rad.find("=")+1)
            end=begin+3
            num_channel_rad=int(num_channel_rad[begin:end])
            #print(str(num_channel_rad))
            if num_channel_rad==15:
                channel_rad="Radio Dacha"
            else:
                channel_rad="Unknown"
        #print(channel_rad)

               
    except:
        pass
        
    '''
    else:
        try:
            mail_recievers=['ukolov@25kadr-reklama.ru','kovalev@25kadr-reklama.ru', 'kozlov@25kadr-reklama.ru']
            if channel_rad!="Radio Dacha":
                # Настройки
                email = 'monitoring@25kadr-reklama.ru'
                mail_receiver = 'ukolov@25kadr-reklama.ru'
                password = 'panda-2016-panda'

                # Формируем тело письма
                subject = "Salehard:Wrong change cannal"
                email_text = "Host: Salehard, Dacha\n Channel:"+channel_rad 
                  
                #цепляемся к серверу
                server = smtp.SMTP('smtp.yandex.ru', 587)
                server.ehlo() # Кстати, зачем это? 
                server.starttls()
                server.login(email, password)

                message = 'From: %s\nTo: %s\nSubject: %s\n\n%s' % (email,
                                                                    mail_receiver,
                                                                    subject,
                                                                    email_text)

                #server.set_debuglevel(1) # Необязательно; так будут отображаться данные с сервера в консоли
                for i in mail_recievers:
                    server.sendmail(email, i, message)
                server.quit()
        except:
            pass
    '''
    try:
         metrics = [
            ZabbixMetric('Salekh_Dacha_Sat', 'RAD', channel_rad, clock=None),
            ]
         zbx=ZabbixSender(zabbix_server='176.116.185.33',
                                    zabbix_port=10051,
                                    socket_wrapper=None, timeout=20)
         zbx.send(metrics)
    except:
        pass

