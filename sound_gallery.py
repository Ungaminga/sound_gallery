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
a[download] {
   text-decoration: none;
}
input, label, a{
    cursor: pointer;
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
    right:0px;
    position:absolute;
    background-color: khaki;
    border: green 2px solid;
    padding: 2px;
}

/* For big directories */
div {
     display: inline;
     float: left;
     padding: 0px 20px 0px 0px;
}
div.big{
    display:block;
    width:99%;
}    """
    open("style.css", "w").write(css)

def generate_html():
    html = """<!DOCTYPE html>
<html>
<head>
	<title></title>
    <link href="style.css" rel="stylesheet" />
    <!-- Audio player !-->
    <script>
        var audio = "";
        var ele = "";
        function onended()
        {
            delete audio;
            audio = ""
            var span = ele.querySelectorAll('span')[0];
            span.style.color = "green";
            span.innerHTML = "&#9658";
            id = "";    
        }

        function play(_ele)
        {
            ele = _ele;
            if (audio)
            {
                audio.pause();
                onended();
            }
            else
            {
                file = ele.getAttribute("file");
                audio = new Audio(file);
                audio.play();
                audio.volume = 0.4;
                audio.onended = onended;
                var span = ele.querySelectorAll('span')[0];
                span.style.color = "red";
                span.innerHTML = "&#9632 ";
            }
        }
    </script>
</head>
<body>
%s
</body>
</html>"""%body
    open("index.html", "w").write(html)

# List-helper class for deteting directory and having it's name in it
class Directory(list):
    def __init__(self, name):
        self.name = name

# Recursive function to generate list of directory tree
# returns []
def generate_tree_dirs(dir, deep=False, subdir = []):
    dirs = subdir
    ld = os.listdir(dir)
    ld.sort()
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
            continue
        dirs.append(new_F)
    return dirs

# Recurisve function to generate <ul><li> of directories and files from tree
# returns []
def process_tree_dirs(tree):
    global body
    global label_num
    
    big = len(tree) > 20
    i = 0
    for itr in tree:
        if big and ((i % (len(tree)//columns) == 0)):
            if i == 0:
                body += '<div class="big">\n<div>\n'
            else:
                body += '</div><div>\n'

        if type(itr) is Directory:
            if i == 0:
                body += '<li><input type="checkbox" id="dir%i" checked = "checked" /> <label for="dir%i">'%(label_num, label_num)           
            else:
                body += '<li><input type="checkbox" id="dir%i" /> <label for="dir%i">'%(label_num, label_num)
            body += '<span class="unchecked">&#10149;</span><span class="checked">&#8863; </span>%s</label> <ul>\n'%(itr.name)
            label_num+=1
            process_tree_dirs(itr)
            body += '</ul></li>\n'
        else:
            short = re.split("^.*\/", itr)[1]
            body += '<li class="file"><a id="%s" onclick=\'play(this)\' file="%s">'%(short, itr)
            body += '<span class="play">&#9658</span>%s</a>'%(short)
            body += '<a href="%s" download>&#8659;</a></li>\n'%(itr)

        i+=1
    if big:
        body += '</div>\n</div><!--style block, width !-->\n'


if __name__ == "__main__":
    scan_dir = os.getcwd()
    if len(sys.argv) >= 2:
        scan_dir = (sys.argv[1])
    
    body = """ <div class="links">
<a href=https://github.com/Ungaminga/TES-L-Localizated-Sounds/archive/4e72e300ddee610d827ffcd05d9981a176bb1da2.zip>Download ru_</a>
<br><a href = https://github.com/Ungaminga/TES-L-Localizated-Sounds/archive/master.zip>Download all</a>
</div>
<ul>
    """
    
    label_num = 0
    columns = 8
    tree = generate_tree_dirs(scan_dir, scan_dir!="")
    process_tree_dirs(tree)
    body += "</ul>\n"
    generate_css()
    generate_html()