def perfectnumber(num):
    sum = 0
    for i in range(1,num):
        if num % i == 0:
            sum = sum+i
    if sum == num:
        print(f"{num} is a perfect number")
    else:
        print(f"{num} is not a perfect number")


num = int(input("Enter a number: "))        
perfectnumber(num)