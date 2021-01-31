#!/bin/env tclsh

set res_list {"res1" "res2" "res3" "res4" "res5"}
set fake_res_array(res1) {"net1" "net2"}
set fake_res_array(res2) {"net3" "net2"}
set fake_res_array(res3) {"net3" "net4"}
set fake_res_array(res4) {"net1" "net5"}
set fake_res_array(res5) {"net1" "net6"}
set fake_res_array(res6) {"net6" "net7"}
set fake_res_array(res7) {"net7" "net8"}
set fake_res_array(res8) {"net5" "net6"}
set fake_res_array(res9) {"net5" "net4"}
set net_visited {}
set res_list {}
foreach res_name [array names fake_res_array] {
     lappend res_list "$res_name $fake_res_array($res_name)"
}

proc get_path_res {net1 net2 r_list} {
    set net_list {}
    foreach m_res $r_list {
        set res_name [lindex $m_res 0]
        set left_list [lreplace $m_res 0 0]
        set res_array($res_name) $left_list
        set net_list [concat $net_list $left_list]
    }
    set net_list [lsort -unique $net_list]
    foreach m_net $net_list {
        set tmp_array($m_net) {}
    }
    foreach res_name [array names res_array] {
        foreach m_net_name $res_array($res_name) {
            lappend tmp_array($m_net_name) $res_name
        }
    }
    set remove_flag 0
    while { $remove_flag == 0 } {
        set remove_flag 1
        foreach m_net [array names tmp_array] {
            if { ([llength $tmp_array($m_net)] < 2) && ($m_net != $net1) && ($m_net != $net2)} {
                puts "*****************************"
                puts "remove $m_net"
                set res $tmp_array($m_net)
                puts "remove $res"
                unset tmp_array($m_net)
                foreach m_item [array names tmp_array] {
                    set idx [lsearch $tmp_array($m_item) $res]
                    if { $idx != -1 } {
                        set tmp_array($m_item) [lreplace $tmp_array($m_item) $idx $idx]
                    }
                }
                set remove_flag 0
            }
        }
    }
    set final_res {}
    foreach m_net [array names tmp_array] {
        set final_res [concat $final_res $tmp_array($m_net)]
    }
    set final_res [lsort -unique $final_res]
    return $final_res
}

set result [get_path_res "net1" "net5" $res_list]
puts "============================="
puts "result = $result"


