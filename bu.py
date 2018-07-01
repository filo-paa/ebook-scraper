fi = open("ebook-list.txt","r");
fo = open("ebook-list-downloaded.txt","w");

for line in fi:
    fo.write(line);

fo.close();
f1.close();
