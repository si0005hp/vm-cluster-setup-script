from datetime import datetime, timedelta

m = {
    'foo': 'bar',
    'hoge': 'fuga',
}

# for k, v in m.items():
#     print(k, v)

# print(1)


# def foo():
#     a = 'foo'
#     print(a)
#     a = 'bar'
#     print(a)



# datetime.now().strftime("%Y/%m/%d %H:%M:%S")

now = datetime.now()
ten_min_ago = now - timedelta(minutes=10)

print(ten_min_ago)
print(now)