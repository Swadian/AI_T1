import stopit
import copy
import os
import sys
import time


class NodParcurgere:
    def __init__(self, info, parinte, cost=0, h=0):
        self.info=info
        self.parinte=parinte #parintele din arborele de parcurgere
        self.g=cost 
        self.h=h
        self.f=self.g+self.h

    def obtineDrum(self):
        l=[self]
        nod=self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod=nod.parinte
        return l
        
    def afisDrum(self, out,afisCost=True, afisLung=False): #returneaza si lungimea drumului
        l=self.obtineDrum()
        k=1
        for nod in l:
            print("Nod:"+str(k),file=out)
            k=k+1
            print(str(nod),file=out)

        print("Timp: "+str(time.time()-start_time),file=out)
        if afisCost:
            print("Cost: ", self.g,file=out)
        if afisCost:
            print("Lungime: ", len(l),file=out)
        return len(l)


    def contineInDrum(self, infoNodNou):
        nodDrum=self
        while nodDrum is not None:
            if(infoNodNou==nodDrum.info):
                return True
            nodDrum=nodDrum.parinte
        
        return False
        
    def __repr__(self):
        sir=""        
        sir+=str(self.info)
        return(sir)


    
    def __str__(self):
        sir=""
        maxInalt=max([len(stiva) for stiva in self.info])
        for inalt in range(maxInalt, 0, -1):
            for stiva in self.info:
                if len(stiva)< inalt:
                    sir+="  "
                else:
                    sir+="|"+stiva[inalt-1]+"| "
            sir+="\n"
        sir+="-"*(2*len(self.info)-1)
        return sir

    
        

class Graph: #graful problemei
    def __init__(self, f):

        def obtineStive(sir):
            stiveSiruri=sir.strip().split("\n") 
            listaStive=[sirStiva.strip().split('/') if sirStiva !="|" else [] for sirStiva in stiveSiruri]
            return listaStive



        continutFisier=f.read() #citesc tot continutul fisierului
        siruriStari=continutFisier.split("#")
        self.start=obtineStive(siruriStari[0])

    def testeaza_scop(self, nodCurent):
        scop = True
        stive = nodCurent.info
        for i in range(len(stive)-1):
            if len(stive[i]) and len(stive[i+1]) and not stive[i][0].isalpha() and not stive[i+1][0].isalpha() and len(stive[i])<len(stive[i+1]):
                scop=False
        alpha=0
        for i in range(len(stive)):
            for j in range(len(stive[i])):
                if stive[i][j].isalpha():
                    alpha+=1
        #numar literele
        if alpha!=0:
            alpha_dedicated_stack=False
            for i in range(len(stive)):
                if len(stive[i]) and stive[i][0].isalpha():
                    alpha_dedicated_stack=True
                    if len(stive[i])!=alpha:#daca n-am toate literele
                        scop = False
                    else:
                        for j in range(len(stive[i])-1): 
                            if stive[i][j].isalpha() and stive[i][j+1].isalpha() and ord(stive[i][j])<ord(stive[i][j+1]):
                                scop=False
                                break
                            #daca undeva nu-s in ordine alfabetica
            if not alpha_dedicated_stack:
                scop=False
        return scop



        





    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        listaSuccesori=[]
        stive_c=nodCurent.info # stivele din nodul curent
        nr_stive=len(stive_c)
        for idx in range(nr_stive):#idx= indicele stivei de pe care iau bloc
            if len(stive_c[idx])==0 :
                continue
            copie_interm=copy.deepcopy(stive_c)
            bloc=copie_interm[idx].pop() #iau varful stivei
            for j in range(nr_stive): #j = indicele stivei pe care pun blocul 
                if idx == j: # nu punem blocul de unde l-am luat
                    continue
                if not bloc.isalpha() and len(copie_interm[j]) and copie_interm[j][-1].isalpha():
                    continue#nu pun numar peste litera 
                if not bloc.isalpha() and len(copie_interm[j]) and not copie_interm[j][-1].isalpha() and int(copie_interm[j][-1]) < int(bloc):
                 #daca varful are valoare mai mica decat blocul de pus si nu e litera    
                    continue
                if not bloc.isalpha() and j>0:#daca exista o stanga
                    if len(copie_interm[j-1]) > len(copie_interm[j]):#daca in stanga exista o valoare
                        if not copie_interm[j-1][-1].isalpha() and int(copie_interm[j-1][-1])<int(bloc):#daca in stanga e o valoare mai mica
                            continue
                stive_n=copy.deepcopy(copie_interm)#lista noua de stive
                stive_n[j].append(bloc) # pun blocul
                costMutareBloc=idx                
                if not nodCurent.contineInDrum(stive_n):
                    nod_nou=NodParcurgere(stive_n,nodCurent, cost=nodCurent.g+costMutareBloc,h= self.calculeaza_h(stive_n, tip_euristica))
                    listaSuccesori.append(nod_nou)

        return listaSuccesori


    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        # euristica banala
        if tip_euristica=="euristica banala":
            scop = 1
            stive = infoNod
            for i in range(len(stive)-1):
                if len(stive[i])<len(stive[i+1]):
                    scop=0
            alpha=0
            for i in range(len(stive)):
                for j in range(len(stive[i])):
                    if stive[i][j].isalpha():
                        alpha+=1
            #numar literele
            if alpha!=0:
                alpha_dedicated_stack=False
                for i in range(len(stive)):
                    if len(stive[i]) and stive[i][0].isalpha():
                        alpha_dedicated_stack=True
                        if len(stive[i])!=alpha:#daca n-am toate literele
                            scop = 0
                        else:
                            for j in range(len(stive[i])-1): 
                                if stive[i][j].isalpha() and stive[i][j+1].isalpha() and ord(stive[i][j])<ord(stive[i][j+1]):
                                    scop=0
                                    break
                                #daca undeva nu-s in ordine alfabetica
                if not alpha_dedicated_stack:
                    scop=0
            return scop
            #n-am structura de nod, ci doar informatiile, deci nu pot sa apelez metoda si trebuie sa copiez codul
        elif tip_euristica=="euristica admisibila 1":
            ##Calculez cate stive nu se incadreaza in conditia finala (nu sunt mai inalte decat stiva de la dreapta)
            h=0
            for i in range(len(infoNod)-1):
                if len(infoNod[i]) and len(infoNod[i+1]) and not infoNod[i][0].isalpha() and not infoNod[i+1][0].isalpha() and len(infoNod[i])<len(infoNod[i+1]):
                    h=h+1
            return h
        elif tip_euristica=="euristica admisibila 2":
            #calculez cat de mari sunt diferentele dintre stive 
            h=0
            for i in range(len(infoNod)-1):
                if len(infoNod[i]) and len(infoNod[i+1]) and not infoNod[i][0].isalpha() and not infoNod[i+1][0].isalpha() and len(infoNod[i])<len(infoNod[i+1]):
                    h=h+(len(infoNod[i+1])-len(infoNod[i]))
            alpha=0
            for i in range(len(infoNod)):
                for j in range(len(infoNod[i])):
                    if infoNod[i][j].isalpha():
                        alpha+=1
            for i in range(len(infoNod)):
                if len(infoNod[i]) and infoNod[i][0].isalpha():
                    alpha-=len(infoNod[i])
                    break
            h+=alpha
             #adun cate litere nu-s in stiva de litere (foarte inexact, dar rezultatul e mai mic decat cel real mereu)
            return h
        else: #tip_euristica=="euristica neadmisibila"
            h=len(infoNod)
            #adaug valoarea de la baza stivei inmultita cu costul inmultita cu numarul de stive
            for i in range(len(infoNod)):
                if(len(infoNod[i])):
                    h+=len(infoNod[i][0])*i*len(infoNod)
            return h




    def __repr__(self):
        sir=""
        for (k,v) in self.__dict__.items() :
            sir+="{} = {}\n".format(k,v)
        return(sir)
        
@stopit.threading_timeoutable(default="timed out")       
def breadth_first(gr, nrSolutiiCautate, out):

    c=[NodParcurgere(gr.start, None)]
    
    while len(c)>0:
        nodCurent=c.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie:",file=out)
            nodCurent.afisDrum(out,afisCost=True, afisLung=True)
            print("\n----------------\n",file=out)
            nrSolutiiCautate-=1
            if nrSolutiiCautate==0:
                return
        lSuccesori=gr.genereazaSuccesori(nodCurent)    
        c.extend(lSuccesori)

@stopit.threading_timeoutable(default="timed out")       
def a_star(gr, nrSolutiiCautate, tip_euristica,out):
    c=[NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    
    while len(c)>0:
        nodCurent=c.pop(0)
        
        if gr.testeaza_scop(nodCurent):
            print("Solutie:",file=out)
            nodCurent.afisDrum(out,afisCost=True, afisLung=True)
            print("\n----------------\n",file=out)
            nrSolutiiCautate-=1
            if nrSolutiiCautate==0:
                return
        lSuccesori=gr.genereazaSuccesori(nodCurent,tip_euristica=tip_euristica)    
        for s in lSuccesori:
            i=0
            gasit_loc=False
            for i in range(len(c)):
                if c[i].f>=s.f :
                    gasit_loc=True
                    break
            if gasit_loc:
                c.insert(i,s)
            else:
                c.append(s)


				
def df(nodCurent, nrSolutiiCautate,file):
	if nrSolutiiCautate<=0: #testul acesta s-ar valida doar daca in apelul initial avem df(start,if nrSolutiiCautate=0)
		return nrSolutiiCautate
	if gr.testeaza_scop(nodCurent):
		print("Solutie: \n", end="",file=file)
		nodCurent.afisDrum(file)
		print("\n----------------\n",file=file)
		nrSolutiiCautate-=1
		if nrSolutiiCautate==0:
			return nrSolutiiCautate
	lSuccesori=gr.genereazaSuccesori(nodCurent)	
	for sc in lSuccesori:
		if nrSolutiiCautate!=0:
			nrSolutiiCautate=df(sc, nrSolutiiCautate,file)
	return nrSolutiiCautate
@stopit.threading_timeoutable(default="timed out")       
def depth_first(gr, nrSolutiiCautate,file):
	df(NodParcurgere(gr.start,None), nrSolutiiCautate,file)


def dfi(nodCurent, adancime, nrSolutiiCautate,file):
	if adancime==1 and gr.testeaza_scop(nodCurent):
		print("Solutie: ", end="",file=file)
		nodCurent.afisDrum(file)
		print("\n----------------\n",file=file)
		nrSolutiiCautate-=1
		if nrSolutiiCautate==0:
			return nrSolutiiCautate
	if adancime>1:
		lSuccesori=gr.genereazaSuccesori(nodCurent)	
		for sc in lSuccesori:
			if nrSolutiiCautate!=0:
				nrSolutiiCautate=dfi(sc, adancime-1, nrSolutiiCautate,file)
	return nrSolutiiCautate
@stopit.threading_timeoutable(default="timed out")
def depth_first_iterativ(gr, nrSolutiiCautate,file):
	for i in range(1,100):
		if nrSolutiiCautate==0:
			return
		print("**************\nAdancime maxima: ", i,file=file)
		nrSolutiiCautate=dfi(NodParcurgere(gr.start, None),i, nrSolutiiCautate,file)

@stopit.threading_timeoutable(default="timed out")
def a_star_opt(gr,out):
	l_open=[NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
	

	l_closed=[]
	while len(l_open)>0:
		nodCurent=l_open.pop(0)
		l_closed.append(nodCurent)
		if gr.testeaza_scop(nodCurent):
			print("Solutie: ", end="",file=out)
			nodCurent.afisDrum(out)
			print("\n----------------\n",file=out)
			return
		lSuccesori=gr.genereazaSuccesori(nodCurent)	
		for s in lSuccesori:
			gasitC=False
			for nodC in l_open:
				if s.info==nodC.info:
					gasitC=True
					if s.f>=nodC.f:
						lSuccesori.remove(s)
					else:#s.f<nodC.f
						l_open.remove(nodC)
					break
			if not gasitC:
				for nodC in l_closed:
					if s.info==nodC.info:
						if s.f>=nodC.f:
							lSuccesori.remove(s)
						else:#s.f<nodC.f
							l_closed.remove(nodC)
						break
		for s in lSuccesori:
			i=0
			gasit_loc=False
			for i in range(len(l_open)):
				#diferenta fata de UCS e ca ordonez crescator dupa f
				#daca f-urile sunt egale ordonez descrescator dupa g
				if l_open[i].f>s.f or (l_open[i].f==s.f and l_open[i].g<=s.g) :
					gasit_loc=True
					break
			if gasit_loc:
				l_open.insert(i,s)
			else:
				l_open.append(s)

def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate,out):
	if nodCurent.f>limita:
		return nrSolutiiCautate, nodCurent.f
	if gr.testeaza_scop(nodCurent) and nodCurent.f==limita :
		print("Solutie: ",file=out)
		nodCurent.afisDrum(out)
		print("\n----------------\n",file=out)
		nrSolutiiCautate-=1
		if nrSolutiiCautate==0:
			return 0,"gata"
	lSuccesori=gr.genereazaSuccesori(nodCurent)	
	minim=float('inf')
	for s in lSuccesori:
		nrSolutiiCautate, rez=construieste_drum(gr, s, limita, nrSolutiiCautate,out)
		if rez=="gata":
			return 0,"gata"
		if rez<minim:
			minim=rez
	return nrSolutiiCautate, minim

@stopit.threading_timeoutable(default="timed out")
def ida_star(gr, nrSolutiiCautate,out):
	
	nodStart=NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))
	limita=nodStart.f
	while True:
		nrSolutiiCautate, rez= construieste_drum(gr, nodStart,limita,nrSolutiiCautate,out)
		if rez=="gata":
			break
		if rez==float('inf'):
			break
		limita=rez




"""
here be the actual program
"""
lista_fisiere_input=os.listdir(sys.argv[1])
NSOL=int(sys.argv[2])
TTL=float(sys.argv[3])
if not os.path.exists("output"):
    os.mkdir("output")
for input in lista_fisiere_input:
    output="output_"+input
    fout=open("output/"+output,"w")
    fin=open(sys.argv[1]+input,"r")
    start_time=time.time()
    """
    here be the function calls
    """
    gr=Graph(fin)
    gr_copy=copy.deepcopy(gr)
    print("BFS:\n",file=fout)
    breadth_first(gr,NSOL,fout,timeout=TTL)
    gr=copy.deepcopy(gr_copy)
    print("DF:\n",file=fout)
    depth_first(gr,NSOL,fout,timeout=TTL/10)
    gr=copy.deepcopy(gr_copy)
    print("DFI:\n",file=fout)
    depth_first_iterativ(gr,NSOL,fout,timeout=TTL)
    gr=copy.deepcopy(gr_copy)
    print("A*(euristica banala):\n",file=fout)
    a_star(gr,NSOL,"euristica banala",fout,timeout=TTL)
    gr=copy.deepcopy(gr_copy)
    print("A*(euristica admisibila 1):\n",file=fout)
    a_star(gr,NSOL,"euristica admisibila 1",fout,timeout=TTL)
    gr=copy.deepcopy(gr_copy)
    print("A*(euristica admisibila 2):\n",file=fout)
    a_star(gr,NSOL,"euristica admisibila 2",fout,timeout=TTL)
    gr=copy.deepcopy(gr_copy)
    print("A*(euristica neadmisibila):\n",file=fout)
    a_star(gr,NSOL,"euristica neadmisibila",fout,timeout=TTL)
    gr=copy.deepcopy(gr_copy)
    print("A* optimizat:\n",file=fout)
    a_star_opt(gr,fout,timeout=TTL)
    gr=copy.deepcopy(gr_copy)
    print("IDA*:\n",file=fout)
    ida_star(gr,NSOL,fout,timeout=TTL)

    """
    here the calls are finished
    """
    fin.close()
    fout.close()
