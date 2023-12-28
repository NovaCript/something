def element(num):
    nums = ''
    if num <= 0:
        return f'Must be > 0'
    for n in range(num+1):
        nums += str(n)*n
    return nums

print(element(4))
print(element(0))