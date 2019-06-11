import vkcoin
import tab

merchant = vkcoin.VKCoin(user_id=99699481, key='**************************************')  # Ваш ID и ключ

@merchant.payment_handler(handler_type='longpoll')
def payment_received(data):
    """
    При получении платежа будет запущена эта функция. Она может называться как угодно
    :param data['to_id']: Ваш ID ВКонтакте
    :param data['id']: ID платежа
    :param data['created_at']: Unix timestamp, время когда был совершён платёж
    :param data['from_id']: ID отправителя платежа
    :param data['amount']: Количество полученных VK Coin
    """

    print(data)
    user_id = data['from_id']
    amount = int(data['amount'])/1000
    tab.update_user_money(user_id,amount)
    # print('Получен платёж на сумму {amount} от {user_id}'.format(amount=amount, user_id=user_id))
    # Вместо print вы можете выполнить ваши действия


merchant.run_longpoll(tx=[1]) # Запускаем LongPoll
