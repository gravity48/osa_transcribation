#include <iostream>
#include <dlfcn.h>
#include <cstddef>
#include <fstream>
#include <vector>
#include <cstring>
#include <filesystem>
#include <unistd.h>

using namespace std;

long file_length(std::ifstream &file){
    long begin = file.tellg();
    file.seekg(0, ios::end);
    long end = file.tellg();
    long fsize = (end-begin);
    file.seekg(0, ios::beg);
    return fsize;
}

int main(int argc, char *argv[]) {
    if (argc !=4){
        cout << "invalid count parameters" << endl;
        return 0;
    }
    string params = argv[1];
    string library_path = argv[3];
    library_path += "/SpeechCodecs/gsm.so";
    size_t length;
    char *inputFile;
    if (params == "stdout"){
        length = stoi(argv[2]);
        inputFile = new char [length];
        fread(inputFile, 1, length, stdin);
    }
    if (params == "file"){
        FILE *fp = fopen(argv[2],"rb");
        fseek(fp, 0, SEEK_END);
        length = ftell(fp);
        fseek(fp, 0, SEEK_SET);
        inputFile = new char [length];
        fread(inputFile, 1, length, fp);
        fclose(fp);
    }
    auto *pInputBuffer = new  char [34];
    auto *pOutputBuffer = new  char [320];
    void *handle;
    int* (*DecodeProcess_Init)();
    void (*DecodeProcess_Free)(int *DecoderProcess_Init);
    void (*DecodeProcess)(int* DecodeInit, char* InputBuffer, char* OutputBuffer);
    //"/home/gravity/Work/CLionProjects/untitled/cmake-build-debug/gsm.so"
    handle = dlopen(library_path.c_str(), RTLD_LAZY);
    *(void**)(&DecodeProcess_Init) = dlsym(handle, "DecodeProcess_Init");
    *(void**)(&DecodeProcess) = dlsym(handle, "DecodeProcess");
    *(void**)(&DecodeProcess_Free) = dlsym(handle, "DecodeProcess_Free");
    int buffer_size = 34;
    // copies all data into buffer
    int loops = length / buffer_size;
    int *decode_init = DecodeProcess_Init();
    for (int i = 0; i < loops; i++) {
        memcpy(pInputBuffer, inputFile + (i*buffer_size), buffer_size);
        DecodeProcess(decode_init, (char*) pInputBuffer, (char *) pOutputBuffer);
        fwrite((char *)pOutputBuffer, 1, 320, stdout);
    }
    DecodeProcess_Free(decode_init);
    dlclose(handle);
    return 0;
}
