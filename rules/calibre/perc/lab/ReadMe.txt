
                Copyright Mentor Graphics Corporation 2014
                             All Rights Reserved.
         THIS WORK CONTAINS TRADE SECRET AND PROPRIETARY INFORMATION
            WHICH IS THE PROPERTY OF MENTOR GRAPHICS CORPORATION
              OR ITS LICENSORS AND IS SUBJECT TO LICENSE TERMS.

DISCLAIMER OF WARRANTY: Unless otherwise agreed in writing, Mentor Graphics software 
and associated files are provided "as is" and without warranty. Mentor Graphics has 
no obligation to support or otherwise maintain software. Mentor Graphics makes no 
warranties, express or implied with respect to software including any warranty of 
merchantability or fitness for a particular purpose.

LIMITATION OF LIABILITY: Mentor Graphics is not liable for any property damage, 
personal injury, loss of profits, interruption of business, or for any other special, 
consequential or incidental damages, however caused, whether for breach of warranty, 
contract, tort (including negligence), strict liability or otherwise. In no event 
shall Mentor Graphics' liability exceed the amount paid for the product giving rise 
to the claim.

=======================================================================================

For SVRF/TVF file use restrictions, please see:
               http://www.mentor.com/terms_conditions/svrf-tvf.html

=======================================================================================



src.net		: schematic netlist
perc.rules	: rules file

./run         	: script to execute Calibre PERC
./view        	: script to open the results in RVE 
./clean       	: script to delete all the generated files 


---------------------------------------------------

Expected Results:
=================

Cell TOP    3 Results    check_CDM    (Improper protection)  [ Net X4/A ]
                                      "Missing CDM up diode
                                      "No CDM down diode and No CDM nfet"
                         check_CDM    (Improper protection)  [ Net X3/A ]
                                      "Missing CDM up diode
                                      "CDM NFET: X3/M2,  has width less than 250um : 0.00022"
                         check_CDM    (Improper protection)  [ Net X1/A ]
                                      "CDM up diode: X1/D0, has perimeter less than 100um : 8e-5"

