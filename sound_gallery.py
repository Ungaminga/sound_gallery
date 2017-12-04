#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 15:04:38 2017

@author: loljkpro
"""
import os, sys, re

def generate_css():
    css = """/* Beautiexes */
body {
    font: inherit;
}
li, ul{
    list-style: none;
    padding: 0 0 0 5px;
}
ul{
    padding-top: 1px;
}
input{
    display:none;
}

input, label, a{
    cursor: pointer;
}

a[download] {
   text-decoration: none;
}

a[download] > span{
   position: relative;
}

@keyframes updown{
  from {
    top: -2px;
  }

  to {
    top: 2px;
  }
}
a[download]:hover > span{
    animation-duration: 0.5s;
    animation-name: updown;
    animation-iteration-count: infinite;
    animation-direction: alternate;
}

/* Directory show-hide */
input ~ ul{
    display: none;
}

input:checked:not(:disabled) ~ ul{
    display: block;
}

/* Custom input buttons */
span.checked{
    display: none;
}
input:checked:not(:disabled) ~ label>span.checked{
    display: inline;
}
input:checked:not(:disabled) ~ label>span.unchecked{
    display: none;
}

/* Play/stop button */
span.play {
    color:green; 
    font-size:20px;
}

/* A div for links */
div.links{
    right:5px;
    position:absolute;
    background-color: khaki;
    border: green 2px solid;
    padding: 2px;
}

/* For big directories */
div.big{
    display:block;
    width:99%;
}

td{
   vertical-align: top;
}

table{
      border: 1px solid black;
}

audio{
      display:block;
}"""
    open("style.css", "w").write(css)

def generate_html():
    html = """<!DOCTYPE html>
<html>
<head>
	<title>%s</title>
    <link href="style.css" rel="stylesheet" />
    <!-- Audio player !-->
    <script>
        var audio = "";
        var ele = "";
        function onended()
        {
            audio.controls = false;
            ele.nextElementSibling.appendChild(audio);
            delete audio;
            audio = ""
            var span = ele.querySelectorAll('span')[0]; // change state to default
            span.style.color = "green";
            span.innerHTML = "&#9658";
            ele.title = "play";
        }

        function play(_ele)
        {
            if (audio)
            {
                audio.pause();
                onended();
                if (ele == _ele)
                    return;
            }
            ele = _ele;
            file = ele.getAttribute("file");
            ele.title = "stop";
            audio = new Audio(file);
            audio.play();
            audio.volume = 0.4;
            audio.onended = onended;
            var span = ele.querySelectorAll('span')[0]; // play -> red stop square button
            span.style.color = "red";
            span.innerHTML = "&#9632 ";
            audio.onloadedmetadata = function(){
            if (audio.duration > 5){
                audio.controls = true;
                ele.nextElementSibling.appendChild(audio);
            }}
        }
    </script>
</head>
<body>
%s
%s
</body>
</html>"""%(title, generate_links(), body)
    open("index.html", "w").write(html)

def generate_links():
    ret = ""
    if with_links == True and len(links):
        ret += '<div class="links">\n'
        for link in links:
            ret += '<a href="%s">%s</a><br>\n'%(link[0], link[1])
        ret += '</div>\n'
    return ret

# List-helper class for deteting directory and having it's name in it
class Directory(list):
    def __init__(self, name):
        self.name = name
        self.single_file = False
        self.no_subdirs = True

def custom_sort (to_sort):
    list1 = []
    list2 = []
    for el in to_sort:
        if el in sorting_order:
            list1.append(el)
        else:
            list2.append(el)

    list1.sort(key=lambda v:sorting_order.index(v))
    list2.sort()

    return list1+list2

# Recursive function to generate list of directory tree
# returns []
def generate_tree_dirs(dir, deep=False, subdir = []):
    dirs = subdir
    ld = os.listdir(dir)
    ld = custom_sort(ld)

    # single file in directory, must process only if dir.wav = dir
    if deep == True and len(ld) == 1:
        F = ld[0]
        if re.search("..*", F) and re.split("\..*", F)[0] == subdir.name:
            dirs.single_file = True

    for F in ld:
        if re.search("(.git|.py|.html|.css)", F):
            continue
        if F == scan_dir:
            continue
        new_F = F
        if deep == True:
            new_F = dir+os.sep+F
        if os.path.isdir(new_F):
            dirs.append(generate_tree_dirs(new_F, True, Directory(F)))
            if type(subdir) is Directory:
                subdir.no_subdirs = False

            continue
        dirs.append(new_F)
    return dirs

def check_bigdir_for_new_div(tree, i):
    if not(len(tree) - i > 10):
        return False

    if type(tree) is Directory and tree.no_subdirs == True:
        return i % (len(tree)//(columns_no_subdir - 1)) == 0;

    return i % (len(tree)//(columns-1)) == 0;

# Recurisve function to generate <ul><li> of directories and files from tree
# returns []
def process_tree_dirs(tree):
    global body
    global label_num
    global checked
    
    big = len(tree) > 20
    i = 0
    for itr in tree:
        if big and check_bigdir_for_new_div(tree, i):
            if i == 0:
                body += '<div class="big"><table>\n<tr>\n<td>'
            else:
                body += '</td><td>\n'

        if type(itr) is Directory:
            if itr.single_file == True:
                 process_tree_dirs(itr);
                 i+=1
                 continue;

            if checked == True:
                body += '<li><input type="checkbox" id="dir%i" checked = "checked" /> <label for="dir%i">'%(label_num, label_num)           
            else:
                body += '<li><input type="checkbox" id="dir%i" /> <label for="dir%i">'%(label_num, label_num)
            body += '<span class="unchecked">&#10149;</span><span class="checked">&#8863; </span>%s</label> <ul>\n'%(itr.name)
            label_num+=1
            process_tree_dirs(itr)
            checked = False
            body += '</ul></li>\n'
        else: #if type(itr) is Directory:
            short = re.split("^.*\/", itr)[1]
            body += '<li class="file"><a onclick=\'play(this)\' file="%s" title="play">'%(itr)
            body += '<span class="play">&#9658</span>%s</a>'%(short)
            body += '<a href="%s" download title="Download audio"><span>&#8659;</span></a>'%(itr)
            if with_mp3:
                mp3 = itr.replace(scan_dir, "mp3", 1)
                mp3 = mp3.replace(".wav", ".mp3")
                dir = os.path.dirname(mp3)
                if not os.path.exists(dir):
                    os.makedirs(dir)

                if not os.path.exists(mp3):
                    sound = pydub.AudioSegment.from_wav(itr)
                    sound.export(mp3, format="mp3")

                body += '| <a href="%s" download title="Download MP3"><span>&#8659;</span><sub>MP3</sub></a>'%mp3
            body += '\n'
        i+=1
    if big:
        body += '</td></tr>\n</table></div><!--style block, width !-->\n'


if __name__ == "__main__":
    argv = sys.argv
    scan_dir = ""
    with_links = False
    with_mp3 = False

    for i in range(1, 5):
        if len(argv) > i:
            if argv[i] == "--with-mp3":
                with_mp3 = True
                import pydub
                continue

            if (argv[i] == "--with-links"):
                with_links = True
                continue

            if scan_dir == "":
                scan_dir = str(argv[i])
                continue

    if scan_dir == "":
        scan_dir = os.getcwd()


    sorting_order = [
    "ru_cards_sound",
    "ru_portrait_shout",
    "en_cards_sound",
    "en_portrait_shout",
    "card_nonloc",
    "ambience",
    "ui"]
    
    # Default links to add. You can type whatever you want
    links = [
    ("https://github.com/Ungaminga/TES-L-Localizated-Sounds/archive/4e72e300ddee610d827ffcd05d9981a176bb1da2.zip", "Download ru_"),
    ("https://github.com/Ungaminga/TES-L-Localizated-Sounds/archive/master.zip", "Download all")]

    label_num = 0
    checked = True
    columns = 6
    columns_no_subdir = columns - 3
    title = "TES:L Sounds Gallery"
    tree = generate_tree_dirs(scan_dir, scan_dir!="")
    body = "<ul>\n"
    process_tree_dirs(tree)
    body += "</ul>\n"
    generate_css()
    generate_html()