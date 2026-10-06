#!/bin/bash

#Step 1 : User input
echo "Enter the URL :"
read -r url

#Step 2: Clean the URL
url=$(printf '%s' "$url" | tr -d ' \r\n')
url="${url%%\?*}"

#Step 3: URL verification
if [[ ! $url =~ ^https?://[A-Za-z0-9.-]+(:[0-9]+)?(/.*)?$ ]]; then
    echo "Invalid URL format" >&2
    exit 1
fi

status=$(curl -sIL -o /dev/null -w '%{http_code}' "$url")
if [ "$status" != "200" ]; then
    echo "Failed, HTTP status: $status" >&2
    exit 1
fi
echo "URL is reachable"
echo

#Step 4 : Downloading / Reading the data
trap 'rm -f data.csv' EXIT
if ! curl -sfL -o data.csv "$url"; then
    echo "Download failed" >&2
    exit 1
fi

#Step 5 : Extract company name, location, founding year and sort by year
tr -d '\r' < data.csv | gawk -v FPAT='([^,]*)|("[^"]*")' '
NR > 1 {
    name = $2; loc = $5; founded = $8
    gsub(/"/, "", name); gsub(/"/, "", loc)

    # Founded can look like "1851 (1892)"; keep the first 4-digit year
    year = ""
    if (match(founded, /[0-9][0-9][0-9][0-9]/))
        year = substr(founded, RSTART, RLENGTH)

    key  = (year == "") ? 9999 : year     # missing years sort last
    show = (year == "") ? "N/A" : year
    print key "|" show "|" name "|" loc
}' | sort -t'|' -k1,1n -k3,3 | awk -F'|' '
BEGIN {
    printf "%-40s %-35s %s\n", "COMPANY", "LOCATION", "FOUNDED"
    print "-------------------------------------------------------------------------------------"
}
{ printf "%-40s %-35s %s\n", $3, $4, $2 }'