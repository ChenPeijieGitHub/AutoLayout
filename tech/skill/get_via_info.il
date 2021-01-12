; *****************************************************************
; Description:
; function to get via infomation from tech
; *****************************************************************

procedure(
get_via_info_from_tech(lib_name @optional (o_file_name nil))
prog(
(lib tech o_file)
    lib = setof(x ddGetLibList() x~>name == lib_name)
    if(lib == nil
    then
        return(nil)
    )
    lib = car(lib)

    if(o_file_name == nil
    then
        o_file = outfile("via.txt")
    else
        o_file = outfile(o_file_name)
    )   
    
    via_info_table = makeTable("via_info_table" "") 
    
    tech = techGetTechFile(lib)

    cutCst = car(setof(x tech~>constraintGroups nindex(x~>name "cutClass")!=nil))
    foreach(x cutCst~>objects
        params = x~>params
        cut_cls_name = cadr(nth(0 params))
        cut_num = cadr(nth(1 params))
        layer = car(x~>layers)
        fprintf(o_file "%s %L %L\n" layer cut_cls_name cut_num)
        via_info_table[layer] = sprintf(nil "cutLayer:%s;cutClass:%s;cutNumber:%d" layer cut_cls_name cut_num)
        println(via_info_table[layer])
    )

    spaceCsts = setof(x tech~>constraintGroups nindex(x~>name "spacings")!=nil)
	foreach(m_cst spaceCsts
	    foreach(x m_cst~>objects
            println(x~>??)
            space = x~>value
	        params = x~>params
	        cut_cls_name = cadr(nth(0 params))
	        cut_num = cadr(nth(1 params))
	        layer = car(x~>layers)
	        fprintf(o_file "%s %f %L %L\n" layer space cut_cls_name cut_num)
	        ;via_info_table[layer] = sprintf(nil "cutLayer:%s;cutClass:%s;cutNumber:%d" layer cut_cls_name cut_num)
	        ;println(via_info_table[layer])
	    )
    )

    close(o_file)
); end of prog
); end of procedure

get_via_info_from_tech("tsmcN28")
