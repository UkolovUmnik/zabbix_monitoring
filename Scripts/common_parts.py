def max_degree_of_2(number):
    max_degree=0
    current_number=1
    for i in range(0,24):
        current_number=current_number*2
        if current_number<=number: 
            max_degree+=1
        else:
            break            
    return max_degree
