#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2014 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import RPi_Rx_swig as RPi_Rx

class qa_RPi_Rx (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
    	start = [-1]*15 + [1]*15 + [-1]*15
    	addr = [-1]*15 + [1]*15 + [-1]*(5*15) + [1]*15
    	pck_cnt = [-1]*15 + [-1]*15 + [1]*15
    	adhl = [-1]*(5*15)
    	ff = [1]*15 + [1]*(3*15) + [-1]*15
    	crc = [1]*(15) + [1]*15 + [-1]*15
    	data = [-1]*15 + [1]*15 + [-1]*45 + [1]*30 + [-1]*45  	
        src_data = start + addr + pck_cnt + adhl + ff + crc + data
        expected_result = (0.0,1.0,0.0,0.0,0.0,1.0,1.0,0.0)
        src = blocks.vector_source_f(src_data)
        fsk = RPi_Rx.RPi_Rx(1,15,32,65)
        dst = blocks.vector_sink_f()
        self.tb.connect(src, fsk)
        self.tb.connect(fsk, dst)
        self.tb.run()
        result_data = dst.data()
        self.assertFloatTuplesAlmostEqual(expected_result, result_data, 6)


if __name__ == '__main__':
    gr_unittest.run(qa_RPi_Rx, "qa_RPi_Rx.xml")
