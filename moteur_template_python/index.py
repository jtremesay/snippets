print "Content-Type: text/html"     # HTML is following
print

import sys,traceback,time,cgi
import inspect

sys.stderr=sys.stdout

try:
    # lecture du fichier html
    root=""
    file=open("%stemplate.tpl"%(root))
    text=file.read()
    # mise en place des variables
    titre="Titre de la page"
    date=time.strftime("%d/%m/%Y")
    heure=time.strftime("%H heures %M minutes %S secondes")
    # affichage avec % magique !
    print text % {"titre":titre,"date":date,"heure":heure}
except:
    print ("<pre>")
    traceback.print_exc()
    print ("</pre>")
