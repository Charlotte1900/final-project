// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include<stdlib.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

unsigned int word_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    char lower_word[LENGTH + 1];
    int len = strlen(word);

    // 把输入的单词转换为全小写
    for (int i = 0; i < len; i++)
    {
        lower_word[i] = tolower(word[i]);
    }
    lower_word[len] = '\0';

    // 哈希查找
    int index = hash(lower_word);
    node *cursor = table[index];

    while (cursor != NULL)
    {
        if (strcmp(cursor->word, lower_word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    return false;
}


// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    char c = tolower(word[0]);
    if (c >= 'a' && c <= 'z')
    {
        return c - 'a';
    }
    return N - 1; // fallback bucket
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // Open the dictionary file
    // 初始化哈希表
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    FILE *source = fopen(dictionary,"r");

    if(source == NULL)
    {
        printf("plese open the dictionary correctly\n");
        return false;
    }

    char temp[LENGTH + 1 ];
    // Read each word in the file
    while(fgets(temp, LENGTH + 1, source) != NULL)
    {
        temp[strcspn(temp, "\n")] = '\0'; //手动去掉换行符

        // 转为小写（为 case-insensitive 匹配做准备）
        for (int i = 0; temp[i]; i++)
        {
            temp[i] = tolower(temp[i]);
        }

        // Create a new node
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            fclose(source);
            return false;
        }
        // Copy word into node
        strcpy(new_node->word, temp);
        new_node->next = NULL;

        // Hash the word
        unsigned int index = hash(temp);
        // Insert node into hash table

        new_node->next = table[index];
        table[index] = new_node;

        word_count ++;

    }

    // Close the dictionary file
    fclose(source);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;    // 暂存当前节点
            cursor = cursor->next;  // 前进到下一个节点
            free(temp);             // 释放当前节点
        }
    }
    return true;
}
