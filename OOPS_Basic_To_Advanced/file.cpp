#include<iostream>
using namespace std;
class A{
    private :
    int a;
    int b;
    public:
    
    static void fun(){
        static int st=0;
        cout<<st<<endl;
    }
};

 
int main(){ 
    A a;
    A::fun();
    return 0;
}