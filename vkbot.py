import vk
import tab
import time
import battons
import vkcoin

def auth(token):
    session = vk.Session(access_token=token)
    return vk.API(session, v='7')

def main():
    token_bot = '**************************************'
    token = '**************************************'
    vk_api = auth(token)
    merchant = vkcoin.VKCoin(user_id=99699481, key='**************************************')
    type_list = ["лайк", "репост", "комментарий", "подписка на пользователя", "подписка на сообщество"]

    while True:
        try:
            vk_bot = auth(token_bot)
            messages = vk_bot.messages.getConversations(count=200)
            if messages['count']>=1:
                f=1
                for i in messages['items']:
                    if i['conversation']['in_read'] != i['conversation']['out_read']:
                        user_id = i['last_message']['from_id']
                        check = vk_bot.groups.isMember(group_id="ontennis",user_id=user_id)
                        body = i['last_message']['text']
                        f=0
                        break
                if f==1:
                    user_id = messages['items'][0]['last_message']['from_id']
                    check = vk_bot.groups.isMember(group_id="ontennis",user_id=user_id)
                    body = messages['items'][0]['last_message']['text']

                if check:
                    if not tab.check_users(user_id):
                        tab.insert_user             vk_bot.messages.send(user_id=user_id , message='Вы были добавлены в список людей на выполненение заданий. Нажмите "Начать" чтобы приступить',keyboard=battons.markup_z)
                    elif (body == 'Начать')and(tab.get_user_status(user_id)=="z"):
                        vk_bot.messages.send(user_id=user_id , message='Выберите действие',keyboard=battons.markup_x)
                        tab.set_user_status(user_id,"x")
                    elif (tab.get_user_status(user_id)=="x")and(body!="К началу"):
                        if body == 'Получить задание':
                            if tab.get_user_date(user_id)[0].find("3")>-1:
                                vk_bot.messages.send(user_id=user_id , message='Вы еще не выполнили прошлое задание',keyboard=battons.markup_x)
                            else:
                                text = "Введите номер задание которое хотите выполнить(формат 'Задание-1'):\n\n"
                                for i in range(1,len(tab.get_num_list())):
                                    if tab.get_user_date(user_id)[0][i]=='0':
                                        ex = tab.get_exercise(i)
                                        text=text+'\n    Задание ' + str(i)+': '+ex[3]+"\n    Ссылка на задание: "+ex[0]+ "\n    Цена: "+str(ex[2])+ "\n\n"
                                vk_bot.messages.send(user_id=user_id , message=text,keyboard=battons.markup_a)
                                tab.set_user_status(user_id,"c")
                        elif body == 'Проверить баланс':
                            vk_bot.messages.send(user_id=user_id , message='Ваш баланс '+ str(tab.get_user_date(user_id)[1])+ ' коинов',keyboard=battons.markup_x)
                        elif body == 'Проверить задание':
                            if tab.get_user_date(user_id)[0].find("3")>-1:
                                num =  tab.get_user_date(user_id)[0].find("3")
                                if tab.check_exercise(user_id,num,vk_api):
                                    tab.exercise_completed(user_id, num)
                                    vk_bot.messages.send(user_id=user_id , message='Задание выполненно успешно, вам начислены коины. Приступайте к выполнению следующего)',keyboard=battons.markup_x)
                                else:
                                    ex = tab.get_exercise(num)
                                    text='Вы еще не выполнили задание ' + str(num)+': '+ex[3]+"\n    Ссылка на задание: "+ex[0]+ "\n    Цена: "+str(ex[2])+ "\n\n"
                                    vk_bot.messages.send(user_id=user_id , message=text,keyboard=battons.markup_x)
                            else:
                                vk_bot.messages.send(user_id=user_id , message='Вы уже выполнили последнее взятое задание',keyboard=battons.markup_x)
                        elif body == 'Отменить задание':
                            if tab.get_user_date(user_id)[0].find("3")>-1:
                                tab.exercise_cancel(user_id,tab.get_user_date(user_id)[0].find("3"))
                                vk_bot.messages.send(user_id=user_id , message='Задание отменено',keyboard=battons.markup_x)
                            else:
                                vk_bot.messages.send(user_id=user_id , message='Вы не выполняли задание',keyboard=battons.markup_x)
                        elif body == 'Добавить задание':
                            vk_bot.messages.send(user_id=user_id , message='Введите задание в данном формате:\n\nТекст задания\"\"Ссылка на задание[ссылка на страницу пользователя или сообщества,ссылка на запись на стене]\"\"Один из типов задания:[лайк, комментарий, репост, подписка на сообщество, подписка на пользователя]\"\"Цена за выполнение задания в коинах\"\"Количество выполнений\n\nК примеру:\nПодписаться на заданную группу\"\"vk.com/test\"\"подписка на сообщество\"\"100\"\"100\n\nГде \"\" - две двойные кавычки.\n\nПроверьте правильность здания перед отправкой!!! С вашего баланса баланса сразу же спишутся средства на выполения задания в случае правильной формы полей.',keyboard=battons.markup_a)
                            tab.set_user_status(user_id,"v")
                        elif body=='Вывести коины':
                            vk_bot.messages.send(user_id=user_id , message='Введите сумму',keyboard=battons.markup_a)
                            tab.set_user_status(user_id,"b")
                        elif body=='Пополнить баланс':
                            vk_bot.messages.send(user_id=user_id , message='Введите целове число коинов для пополнения (без тысяных долей)',keyboard=battons.markup_a)
                            tab.set_user_status(user_id,"n")
                        else:
                            vk_bot.messages.send(user_id=user_id , message='Не понимаю вас(Выберите действие)')
                    elif (tab.get_user_status(user_id)=="c")and(body!="К началу"):#Взятие задания
                        if body.startswith('Задание-'):
                            text = body[8:]
                            if (text.isdigit())and(tab.get_user_date(user_id)[0][int(text)]=="0"):
                                vk_bot.messages.send(user_id=user_id , message='Вы взяли задание с номером '+text+'. После выполнения зайдите в меню "Проверить задание"',keyboard=battons.markup_x)
                                tab.get_exercise_for_execution(user_id,int(text))
                                tab.set_user_status(user_id,"x")
                            else:
                                vk_bot.messages.send(user_id=user_id , message='Заданий c этим номером не доступно к выполнению',keyboard=battons.markup_a)
                        else:
                            vk_bot.messages.send(user_id=user_id , message='Не понимаю вас. Выберите задание или перейдите к началу диалога',keyboard=battons.markup_a)
                    elif (tab.get_user_status(user_id)=="v")and(body!="К началу"):#Добавление задания
                        arr = body.split('""')
                        text = 'Вы допустили следующие ошибки:'
                        if len(arr)!=5:
                            text+="\n   - пропущен или добален лишний параметр"
                        if (len(arr)==5)and((not arr[4].isdigit())or(not arr[3].isdigit())):
                            text+="\n   - числовые поля заполнены неверно"
                        if (len(arr)==5)and(not arr[2] in type_list):
                            text+="\n   - тип задания указан неверно"
                        if (len(arr)==5)and(not "vk.com" in arr[1]):
                            text+="\n   - ссылка указана неверно"
                        if len(text)<31:

                            arr2=[arr[0],arr[1],int(type_list.index(arr[2])),int(arr[3])*int(arr[4]),int(arr[3])]
                            print(arr2)
                            if arr[4]*arr[3]<=tab.get_user_date(user_id)[1]:
                                tab.insert_exercise(arr2[0], arr2[1], arr2[2], arr2[3], arr2[4])
                                tab.update_user_money_minus(user_id,arr[4]*arr[3])
                                vk_bot.messages.send(user_id=user_id , message='Задание добавленно',keyboard=battons.markup_x)
                                tab.set_user_status(user_id,"x")
                            else:
                                vk_bot.messages.send(user_id=user_id , message='Вам не хватает: '+arr[4]*arr[3]-tab.get_user_date(user_id)[1]+'. Пополните баланс и попробуйте снова.',keyboard=battons.markup_x)
                                tab.set_user_status(user_id,"x")

                        else:
                            text+="\n\nВведите задание заново в данном формате или перейдите к началу диалога:\n\nТекст задания\"\"Ссылка на задание[ссылка на страницу пользователя или сообщества,ссылка на запись на стене]\"\"Один из типов задания:[лайк, комментарий, репост, подписка на сообщество, подписка на пользователя]\"\"Цена за выполнение задания в коинах\"\"Количество выполнений\n\nК примеру:\nПодписаться на заданную группу\"\"vk.com/test\"\"подписка на сообщество\"\"100\"\"100\n\nГде \"\" - две двойные кавычки.\n\nПроверьте правильность здания перед отправкой!!! С вашего баланса баланса сразу же спишутся средства на выполения задания в случае правильной формы полей. Для возвращения к началу диалога напишите \"К началу\""
                            vk_bot.messages.send(user_id=user_id , message=text,keyboard=battons.markup_a)
                    elif (tab.get_user_status(user_id)=="b")and(body!="К началу"):#Добавление задания
                        if body.isdigit():
                            balance=tab.get_user_date(user_id)[2]
                            if (int(body)<=balance)and(int(body)>500):
                                    #merchant.send_coins(user_id, int(body))
                                    vk_api.messages.send(user_id=user_id , message='Вывод успешен!',keyboard=battons.markup_x)
                                    tab.set_user_status(user_id,"x")
                            elif int(body)>balance:
                                vk_api.messages.send(user_id=user_id , message='Вы хотите вывести больше, чем у вас на балансе!',keyboard=battons.markup_a)
                            elif int(body)<500:
                                vk_api.messages.send(user_id=user_id , message='Минимальная сумма вывода 500 коинов!',keyboard=battons.markup_a)
                    elif (tab.get_user_status(user_id)=="n")and(body!="К началу"):#Пополнение счета
                        if body.isdigit():
                            payment=int(round(float(body)))
                            result = merchant.get_payment_url(amount=payment*1000, payload=78922, free_amount=False)
                            vk_bot.messages.send(user_id=user_id , message='Вот ссылка на оплату '+result+' оплатите и после пополнения проверьте баланс или выберите другое действие если передумали',keyboard=battons.markup_x)
                            tab.set_user_status(user_id,"x")
                        else:
                            vk_bot.messages.send(user_id=user_id , message='Вы ввели не число, вернитесь к началу или попробуйте снвоа ввести число коинов',keyboard=battons.markup_a)
                    elif body=="К началу":
                        vk_bot.messages.send(user_id=user_id , message='Выберите действие',keyboard=battons.markup_x)
                        tab.set_user_status(user_id,"x")
                    else:
                        vk_bot.messages.send(user_id=user_id , message='Не понимаю вас(Выберите "Начать" для начала диалога)',keyboard=battons.markup_z)
                else:
                    vk_bot.messages.send(user_id=user_id , message='Подпишитесь, чтобы вы могли выполнять задания')
            else:
                continue
        except:
            time.sleep(1)
        finally:
            pass



if __name__ == '__main__':
    main()
