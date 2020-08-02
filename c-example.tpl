
/******************************************************************************
*                              Local Data Types                               *
******************************************************************************/

/******************************************************************************
*                                                                             *
*  CRC LOOKUP TABLE                                                           *
*  ================                                                           *
*  The following CRC lookup table was generated automatically using the       *
*  following parameters:                                                      *
*                                                                             *
*     Width   : ${table['width']} bits                                                        *
*     Poly    : ${'0x' + format(table['poly'], '02X')}                                                          *
*     Reverse : ${table['reverse']}                                                         *
*                                                                             *
*  For more information on the on the tool used to generate this table please *
*  visit http://sunshin.es/crc.                                               *
******************************************************************************/
${table['type']} crctable[256] =
{
${table['values']}
};

/******************************************************************************
*                          Local Function Prototypes                          *
******************************************************************************/
${table['type']} calculate_crc (unsigned char *data, unsigned int length, ${table['type']} initial_value, ${table['type']} final_xor);


/******************************************************************************
*                          Local Function Definitions                         *
******************************************************************************/
${table['type']} calculate_crc (unsigned char *data, unsigned int length, ${table['type']} initial_value, ${table['type']} final_xor)
{
    unsigned int  i;
    ${table['type']} crc = initial_value;

    for (i = 0; i < length; i++)
    {
        crc = crctable[crc ^ data[i]];
    }
    
    return crc ^ final_xor;
}

int main (void)
{
    unsigned char data[2] = {0x01, 0x02};
    
    printf("CRC: 0x%X\n", calculate_crc(data, 2, 0x00, 0x00));
    
    return 0;
}
