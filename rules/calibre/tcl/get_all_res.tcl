#!/bin/env tclsh

set res_list {"res1" "res2" "res3" "res4" "res5"}
set fake_res_list(res1) {"net1" "net2"}
set fake_res_list(res2) {"net3" "net2"}
set fake_res_list(res3) {"net3" "net4"}
set fake_res_list(res4) {"net1" "net5"}
set fake_res_list(res5) {"net1" "net6"}
set net_visited {}
set all_res {}

proc get_all_res {net_name} {
    lappend ::net_visited $net_name
    set res_list [get_res_by_net_name $net_name]
    foreach m_res $res_list {
        foreach m_net_name $::fake_res_list($m_res) {
            if { [lsearch $::net_visited $m_net_name] == -1 } {
                get_all_res $m_net_name
            }
        }
        if {[lsearch $::all_res $m_res] == -1 } {
            lappend ::all_res $m_res
        }
    }
}

proc get_res_by_net_name { net_name } {
    set l_collect {}
    foreach res_name $::res_list {
        set m_nets $::fake_res_list($res_name)
        if { [lsearch $m_nets $net_name] != -1} {
            lappend l_collect $res_name
        }
    }
    return $l_collect
}

get_all_res "net1"
puts $all_res

