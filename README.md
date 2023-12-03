# Sockets_Gr-12

Projekti është bërë në lëndën Rrjeta kompjuterike, në gjuhën python.
Punuar nga: Elda Reçica, Eljon Shala, Elma Ahmeti.

Përshkrimi: Ky projekt starton një server me një IP the port të caktuar, dhe klientët mund të kyqen në të. Klienti i cili e bën kërkesën (komandën) e parë regjistrohet si administrator. Klientët tjerë janë përdorues të rëndomtë. Admini ka të drejtë të bëjë këto komanda:
1) ls - list files and directories;
2) cd FolderName - go to FolderName;
3) cd .. - go to parentFolder;
4) mkdir folderName - create folder 'folderName';
5) read file.txt - read content of file.txt;
6) add file.txt - create file.txt;
7) remove file.txt - delete file.txt
8) execute file.txt - execute file.txt
9) edit file.txt A text - add the text 'A text' to file.txt on a new line;
10) clear file.txt - erase the content of file.txt;

Kurse përdoruesi i rëndomtë ka të drejtë vetëm këto komanda:
1) ls - list files and directories;
2) cd FolderName - go to FolderName;
3) cd .. - go to parentFolder;
4) read file.txt - read content of file.txt;

Libraritë e përdorura: socket (për krijimin e socketave dhe lidhja me server), io (për krijim/fshirje të fajllave dhe krijim të follderave), subprocess (për ekzekutim të fajllave), shutil(për fshirje të follderave) dhe threading (për lehtësim i punes duke e ndarë në threads).