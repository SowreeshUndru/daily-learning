# str1=input("type name")
# str2=str1
# str2="sowreeshundru"
# print(id(str2))
# print(id(str1))


string=input("type name : ")
print(string.count("$"))
print(string[0:3]) #[i:j] then [i,j)  
print(string[0:]) #[i:j] then [i,j) // here same as [0:size of string]   
print(string[:3]) #[i:j] then [i,j)  //here is same as [0:3]
#negative index .
string[1]=1

# age1=int(input("Write the value :"))
# age2=int(input("Write the value :"))
# age3=int(input("Write the value :"))


# if(age1%7==0):
#     print("multiple of 7")
# else :print("not a multiple of 7")

list_1=[1,2,"SowreeshUndru"]
list_1[0]=2212142
list_1[1]=7
# list_1[3]="lokesh" we cant do like this
#list_1[2][0]='l' we cant do like this
list_1.append("lokesh")
list_1+="Jayanth" #modifies existing list 
list_1=list_1+"Jayanth" #creates new list evry time

print(list_1)
list_1=[list_1,"hemanth"]
print(list_1)


lt=[1,4,4,"sowreesh"]
lt=[*lt,5]
print(lt)
lt.sort(reverse=True) #returns null  
#and one more thing it only compares the types of list should be same else it gives an error
print(lt)






































































