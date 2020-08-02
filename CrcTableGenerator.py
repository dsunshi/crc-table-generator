#-----------------------------------------------------------------------------#
# Copyright (c) 2015 David Sunshine                                           #
# Author : David Sunshine                                                     #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see http://www.gnu.org/licenses/.         #
#-----------------------------------------------------------------------------#

if __name__ == "__main__":
    import argparse
    from mako.template import Template
    from mako.lookup import TemplateLookup

def auto_int(x):
    return int(x, 0)

def valid_width(value):
    x = int(value)
    if (x != 8) and (x != 16) and (x != 32):
        raise argparse.ArgumentTypeError("%s is not a valid width, must be: 8, 16 or 32!" % value)
    else:
        return x

class CrcTable:
    TABSTOP = '    '

    def __init__(self, width, poly, reverse):
        # Width in bits (8, 16 or 32)
        self.width   = width
        # The algorithm's polynomial
        self.poly    = poly
        # Reverse input bytes
        self.reverse = reverse

    # For more infomration on this function please see:
    # http://www.ross.net/crc/crcpaper.html
    def tab(self, ch):
        topbit = 1 << (self.width - 1)
        uch    = ch
        if self.reverse:
            uch = self.reflect(uch, 8)
        r = uch << (self.width - 8)
        for index in range(0, 8):
            if (r & topbit) != 0:
                r = (r << 1) ^ self.poly
            else:
                r = r << 1
        if self.reverse:
            r = self.reflect(r, self.width)
        return r & ( (1 << self.width) - 1 )

    def get(self):
        table = []
        for i in range(0, 256):
            table.append(self.tab(i))
        return table
        
    def reflect(self, value, bottom):
        result = value
        temp   = value
        for index in range(0, bottom):
            if temp & 1 != 0:
                result = result |  (1 << ((bottom - 1) - index))
            else:
                result = result & ~(1 << ((bottom - 1) - index))
            temp = temp >> 1
        return result

    def str(self, line_width):
        table_str = self.TABSTOP
        values    = self.get()
        if self.width == 8:
            form = '02X'
        elif self.width == 16:
            form = '04X'
        else:
            form = '08X'
        for idx in range (0, len(values) - 1):
            table_str += '0x'
            table_str += format(values[idx], form)
            table_str += ','
            if ((idx + 1) % line_width) == 0:
                table_str += '\n'
                table_str += self.TABSTOP
            else:
                table_str += ' '
        table_str += '0x'
        table_str += format(values[len(values) - 1], form)
        return table_str

    def __str__(self):
        return self.str(8)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CRC Table Generator')

    parser.add_argument('-i', '--input',                        help = 'Input file name',             required = True)
    parser.add_argument('-o', '--output',                       help = 'Output file name',            required = True)
    parser.add_argument('-w', '--width',   type=valid_width,    help = 'Width in bits (8, 16 or 32)', required = True)
    parser.add_argument('-p', '--poly',    type=auto_int,       help = 'The algorithm\'s polynomial', required = True)
    parser.add_argument('-r', '--reverse', action='store_true', help = 'Reverse input bytes?',        required = False)
    
    args = parser.parse_args()

    table = dict(
        width   = args.width,
        poly    = args.poly,
    )

    if args.width == 8:
        table['type'] = 'unsigned char'
    elif args.width == 16:
        table['type'] = 'unsigned short'
    else:
        table['type'] = 'unsigned int'

    table['reverse']  = args.reverse;

    crc_table = CrcTable(table['width'], table['poly'], table['reverse'])

    if (args.width == 8) or (args.width == 16):
        table['values'] = crc_table.str(8)
    else:
        table['values'] = crc_table.str(4)

    lookup = TemplateLookup(directories=['.'])
    template_file = Template(filename=args.input, lookup=lookup)
    f = open(args.output, "w")
    f.write(template_file.render(table=table))
    f.close()