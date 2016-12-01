#include<stdio.h>
#include<stdlib.h>
#include <string.h>
#define MAX_LINE 1024

int main()
{    
	char buf[MAX_LINE];  
	FILE *fp,*fp1,*fp2;            
	int len,i;  
	long length;
	char *temp,*temp1;
	    
	system("dir /b .\\ >>.\\buf.Ock");//将目录导出到buf.Ock
	if((fp = fopen(".\\buf.Ock","r")) == NULL)
	{
		perror("fail to read");
		exit (1) ;
	}
	else
	{
		system("mkdir Resolved_Data");
		while(fgets(buf,MAX_LINE,fp) != NULL)
		{
			len = strlen(buf);
			buf[len-1] = '\0';
			if(strstr(buf, "textin.npy"))			
			{
				if((fp1 = fopen(buf,"rb"))==NULL)
				{
					perror("fail to read");
					exit(1);
				}
				else{
					fp2 = fopen(".\\Resolved_Data\\textin.bin","wb"); 
					fseek(fp1,0,2);   //指针：移动到文件尾部
    				length = ftell(fp1);   //返回指针偏离文件头的位置(即文件中字符个数)
					fseek(fp1,0x50,SEEK_SET); 
					
					temp = (char*)malloc(sizeof(char) * (length-0x50));
					fread(temp,1,(length-0x50),fp1);
					fwrite(temp,1,(length-0x50),fp2);
					free(temp);
					
					fclose(fp1);
					fclose(fp2);
				}
			}
			else if(strstr(buf, "textout.npy"))			
			{
				if((fp1 = fopen(buf,"rb"))==NULL)
				{
					perror("fail to read");
					exit(1);
				}
				else{
					fp2 = fopen(".\\Resolved_Data\\textout.bin","wb"); 
					fseek(fp1,0,SEEK_END);   //指针：移动到文件尾部
    				length = ftell(fp1);   //返回指针偏离文件头的位置(即文件中字符个数)
					fseek(fp1,0x50,SEEK_SET); 
					
					temp = (char*)malloc(sizeof(char) * (length-0x50));
					temp1 = (char*)malloc(sizeof(char) * ((length-0x50)/4));
					fread(temp,1,(length-0x50),fp1);
					
					for(i=0;i<(length-0x50)/4;i++)
					{
						temp1[i]=temp[i*4];
					}
					
					fwrite(temp1,1,(length-0x50)/4,fp2);
					free(temp);
					free(temp1);
					
					fclose(fp1);
					fclose(fp2);
				}
			}
		}
	}
	
	fclose(fp);
	system("del .\\buf.Ock");
	printf("successful!!!!\n");
	system("pause");
	
    return 0;
}
