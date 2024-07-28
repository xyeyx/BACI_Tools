#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int nospace_memcpy(char* target, char*  source, int len){
    if ((source==NULL)||(target==NULL)) return -1;
    
    int i=0, j = 0;
    
    for (i=0; i<len; i++) {
        if(source[i] != ' ') target[j++]=source[i];
    }
    target[j]='\0';
    
    return j;
}



typedef struct ListHS {
    int BACI4d;
    int len;
    char CacheDt[5000];
    struct ListHS* next;
} ListHS;


void insertNode(ListHS **head_addr, int id){
    ListHS *newNode = (ListHS*) malloc(sizeof(ListHS));
    if (!newNode) {
        perror("Memory allocation error.");
        exit(EXIT_FAILURE);
    }
    (*newNode).BACI4d = id;
    (*newNode).len = 0;
    // CacheDt 
    
    (*newNode).next = *head_addr;
    *head_addr = newNode;
}

void writeCache(ListHS *head) {
    char filename[9];
    FILE *fout;
    if(head->len){
        sprintf(filename, "%04d.csv", head->BACI4d);
        fout = fopen(filename, "a");
        fprintf(fout, "%s", head->CacheDt);
    
        head->CacheDt[0]='\n';
        head->len=0;
    
        fclose(fout);        
    } 
}


void appendCache(ListHS **head_addr, char* data){
    char id[5];
    int i=0;
    
    ListHS *headmaster = *head_addr;

    
    for(i = 0; i<4; i++) {
        id[i]=data[i];
    }
    id[4]='\0';
    i = atoi(id);
    
    while (headmaster){
        if (headmaster->BACI4d==i){
           // printf("The data currently is: %s.\n", headmaster->CacheDt);
            break;
        }
        
        headmaster = (*headmaster).next;
    }
    
    if (headmaster){
        headmaster->len += nospace_memcpy(headmaster->CacheDt + headmaster->len, data, strlen(data));
        if (headmaster->len > 4950) {
            writeCache(headmaster);
        }

    }
    else {
        insertNode(head_addr, i);
        printf("New Node: %04d.\n", i);
        appendCache(head_addr, data);
    }
    
}
 



ListHS* initNode(){
    ListHS *newNode = (ListHS*) malloc(sizeof(ListHS));
    if (!newNode) {
        perror("Memory allocation error.");
        exit(EXIT_FAILURE);
    }
    (*newNode).BACI4d = -1;
    (*newNode).next = NULL;
    return newNode;
}



int main(){
    ListHS *head;
    ListHS *headmaster;
    char line[200];
    
    head = initNode();
    
    FILE *finput = fopen("DATAFILE_NAME.txt", "r");

    
    if (finput!=NULL) {
        // skip one line
        fgets(line, sizeof(line), finput);
        while(fgets(line, sizeof(line), finput)){
            if(line[0]!='\n') appendCache(&head, line);
            }
        fclose(finput);
    }
    else {
        fprintf(stderr, "Unable to open file.\n"); 
    }
    
    
    headmaster = head;
    while (headmaster){
        writeCache(headmaster);
        headmaster = headmaster->next;
    } 
    

    return 1;
}
