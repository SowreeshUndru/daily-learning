
# t1=([1,2,3],1,2)
# t2 = tuple(t1) #tuple copy or
# t1[0].append(4)
# print(id(t1))
# print(id(t2))
# print((t1))
# print((t2))
# # t2=t1[:]
# # print(id(t1))
# # print(id(t2))

####################
string="hello"*4
print(string)

###################

t1 = (1, 2, 3)
print(id(t1))  # Let's say it's 1000

t1 = t1 + (4, 5) 
print(id(t1))  # New memory! (e.g., 2000)

t1 += (6, 7)
print(id(t1))  # New memory again! (e.g., 3000)

