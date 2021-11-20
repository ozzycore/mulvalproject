#!/bin/sh

ADAPTERSRCPATH=$MULVALROOT/src/adapter
export MALLOC_CHECK_=0

xsb_logfile="xsb_nessus_translate.log"
xsb 2>$xsb_logfile 1>&2 <<EOF
[results].
['$MULVALROOT/lib/libmulval'].
['$ADAPTERSRCPATH/nessus_translator'].
tell('nessus.P').
findall(vulProperty(A,B,C),vulProperty(A,B,C),L),list_apply(L,write_clause_to_stdout).

%findall(remote_client_vul_exists(A,B),remote_client_vul_exists(A,B),L),list_apply(L,write_clause_to_stdout).

findall(vulExists(A,B,C),vulExists(A,B,C),L),list_apply(L,write_clause_to_stdout).

findall(cvss(CVE, AC),cvss(CVE, AC),L),list_apply(L,write_clause_to_stdout).

findall(networkServiceInfo(Host, Program, Protocol, Port, someUser), networkServiceInfo(Host, Program, Protocol, Port, someUser), L), list_apply(L,write_clause_to_stdout).

%findall(hacl(Host, Host1, Protocol, Port), hacl(Host, Host1, Protocol, Port), L), list_apply(L,write_clause_to_stdout).

told.
halt.
EOF

if [ ! -e nessus.P ]; then
    echo "Error in translating NESSUS scan results. Please refer to $xsb_logfile."
    exit 1
fi

cat accountinfo.P >> nessus.P
echo "hacl(_,_,_,_).">>nessus.P
echo "Output can be found in nessus.P."


nessus_vul_summary.sh nessus.P
cat accountinfo.P >>summ_nessus.P
echo "hacl(_,_,_,_).">>summ_nessus.P
