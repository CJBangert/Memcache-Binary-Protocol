import bmemcached

client = bmemcached.Client(('127.0.0.1:5000', ), '',
                            '')

client.set('Hello', 'World')

print(client.get('Hello'))
