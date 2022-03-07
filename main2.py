def is_correct_mobile_phone_ru(number):
    NUMBERS = '0123456789'
    if not number:
        return False
    if number[0] == '+' and number[1] == '7' or number[0] == '8':
        if '--' not in number and number[-1] != '-':
            count1 = 0
            count2 = 0
            flag = True
            for i in number:
                if i == '(':
                    flag = False
                    if count2 > count1:
                        return False
                    if count1 - count2 > 1:
                        flag = False
                        return False
                    count1 += 1
                elif i == ')':
                    flag = True
                    if count2 > count1:
                        return False
                    if count1 - count2 > 1:
                        flag = False
                        return False
                    count2 += 1
            if count1 == count2 and flag:
                if number.count('(') > 1:
                    return False
                nums = [i for i in number if i in NUMBERS]
                if len(nums) == 11:
                    return True
                return False
        else:
            return False
    return False


print('YES' if is_correct_mobile_phone_ru(input()) else 'NO')
