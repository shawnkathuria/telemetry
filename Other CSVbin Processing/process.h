#ifndef _PROCESS_H_
#define _PROCESS_H_

struct can_msg {
    char id[2]; //2 bytes
    char pkt; //1 byte
    uint8_t start; //start byte in the packet, 1 byte
    uint8_t len; //number of bytes of data, 1 byte
    char bits[3]; //3 bytes (1 bit for whether each bytes enabled--max payload = 22 bytes --> 3 needed) 
    uint8_t lts; //number of bytes to send, 1 byte
};

int process_line(char* msg, struct can_msg* msg_table, int counter);

struct can_msg* get_msg_type(char* msg, struct can_msg* msg_table);

#endif