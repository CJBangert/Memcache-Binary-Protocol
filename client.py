import bmemcached

client = bmemcached.Client(('127.0.0.1:5000', ), '',
                            '')

client.set('Hello', 'World')
client.set('Hell', 'Worl')
client.set('Hel', 'Wor')
client.set('He', 'Wo')

print(client.get('Hello'))
print(client.get("He"))