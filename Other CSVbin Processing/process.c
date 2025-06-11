#include "process.h"
#include <stdint.h>

////File should be in the form of id, pkt, len of original data (Bytes), bytes to send. 10 bytes per line  
////counters is a variable that tracks, for each type of packet, how many bytes have been assigned
//int process_line(char* msg, struct can_msg* msg_table, int counter) {
//    struct can_msg M = {0};
//    M.id[0] = msg[0];
//    M.id[1] = msg[1];
//    M.pkt = msg[2];
//    M.start = msg[3];
//    M.len = msg[4];
//    M.bits[0] = msg[5];
//    M.bits[1] = msg[6];
//    M.bits[2] = msg[7];
//    M.lts = msg[8];
//    msg_table[counter] = M;
//    return counter++;
//}

struct can_msg* get_msg_type(char* msg, struct can_msg* msg_table) {
    //this should return the struct corresponding to the message that has been received
}