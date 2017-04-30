if test -d /usr/class/cs351/project/ebay_data;then
    python gb_parser.py /usr/class/cs351/project/ebay_data/items-*.xml
elif test -d ebay_data;then
    python gb_parser.py ebay_data/items-*.xml
fi
