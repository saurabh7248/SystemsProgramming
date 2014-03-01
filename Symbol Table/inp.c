#include<stdio.h>

void main()

{

   int a=5,b=6,c,count=0;

      char d='k';

     float f;

   int i,jk;

     printf("Please enter a value for integer c");
     scanf("%d",&c);
   for(count=2;count<c;count++)
    {
      if(c%count==0)
         {
         printf("%d is not a prime number",c);
         exit(0);  
         }
    }
    prime:
    printf("%d is a prime number",c);
}
