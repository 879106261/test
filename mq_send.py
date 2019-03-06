import pika

username = 'admin'#指定远程rabbitmq的用户名密码
pwd = 'admin'
user_pwd = pika.PlainCredentials(username, pwd)
s_conn = pika.BlockingConnection(pika.ConnectionParameters('10.108.10.17', credentials=user_pwd))#创建连接
chan = s_conn.channel()  #在连接上创建一个频道

chan.queue_declare(queue='hello') #声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行
chan.basic_publish(exchange='',  #交换机
                   routing_key='hello',#路由键，写明将消息发往哪个队列，本例是将消息发往队列hello
                   body='2423424')#生产者要发送的消息
print("[生产者] send 'hello world")

s_conn.close()#当生产者发送完消息后，可选择关闭连接
