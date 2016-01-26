##COMMENTS/REPORT:  
##
##1. DESCRIPTION OF PROBLEM FORMULATION AND HOW THE SOLUTION WORKS:
##     
##   INGESTING DATA:
##   FOR EACH STATE, AN OBJECT N_STATE IS CREATED WHICH CONTAINS ITS NAME, A DICTIONARY OF NEXT NODES, AVAILABLE BANDWIDTHS
##   A FLAG TO INDICATE IF THE BANDWIDTH IS SET AND A FLAG TO INDICATE IF THE NODE HAS BEEN TRAVERSED BEFORE. THE GRAPH GRPH COMPRISES A 
##   DICTIONARY N_LIST WHICH HAS KEY AS STATE NAMES AND VALUES AS CORRESPONDING N_STATE OBJECTS.
##   AFTER INGESTING THE ADJACENT STATE DATA, THE PROGRAM ALSO CHECKS IF LEGACY CONSTRAINTS ARE PRESENT AND MAKES CHANGES TO THE CORRESPONDING
##   NODES (ASSIGNS THE BANDWIDTHS, SETS THE BANDWIDTH SET FLAG - OBJ.D_SET). 
## 
##   NODE SELECTION:
##   THE FUNCTION ORD_STCK ACCEPTS THE PRESENT NODE AND CHOOSES THE BEST CHILD NODE FOR EXPANSION.
##   FOR EXPANSION, THE NODE IS SELECTED BY CHECKING THE LENGTH OF AVAILABLE DOMAIN FOR EACH (CHILD) STATE, IF THE MANY CHILDREN HAVE THE 
##   SAME LENGHT FOR DOMAIN THEN THE ONE WITH THE HIGHEST NEIGHBORS IS SELECTED FOR EXPANSION.  
##
##   TRAVERSAL AND ASSIGNMENT:
##   THE PROGRAM USES DFS TO TRAVERSE THROUGH ALL THE STATES. A STACK IS MAINTAINED WHICH CONTAINS NODES SORTED USING ORD_STCK. 
##   IF ALL CHILDREN BELONGING TO  A PARENT HAVE BEEN ASSIGNED A BANDWIDTH THEN THE ELEMENTS FROM THE STACK ARE POPPED TILL WE GET A NODE
##   WHICH HASN'T YET BEEN ASSIGNED. IF ALL NODES HAVE BEEN TRAVERSED AND ASSIGNED, THE FUNCTION RETURNS AND OUTPUT IS PRINTED
##
##   FORWARDCHECKING AND BACKTRACKING:
##   AFTER EACH ASSIGNMENT IS MADE, THE FWD_CHK() IS CALLED TO RECTIFY THE DOMAINS OF THE NEIGHBORING NODES. IF THERE IS AN ISSUE, THE LATEST
##   ASSIGNMENT IS REVOKED AND A NEW ASSIGNMENT IS MADE. IF THE NODE HAS JUST ONE REMAINING DOMAIN THEN THE PROGRAM USES BACKTRACT TO START OVER.
##
##2. PROBLEMS FACED AND ASSUMPTIONS MADE:
##   SINCE THE STACK IS REQUIRED TO MAINTAIN THE NEXT BEST NODES, THE TREE BRANCHES COMPRISE DIFFERENT STATES INSTEAD OF DIFFERENT BANDWIDTH ASSIGNMENT
##   THUS, IF ONE HAS TO BACKTRACK, WE REQUIRE TO MAINTAIN A BACKUP OF THE STACK EVERYTIME IT CHANGES. SINCE THIS IS NOT FEASIBLE, I HAVE ASSUMED
##   THAT IF THE PROGRAM STARTS OVER WHEN IT HAS TO BACKTRACK, IT WILL MAKE DIFFERENT ASSIGNMENTS AND WILL LEAD TO A SOLUTION. THIS ASSUMPTION WORKS
##   EVEN IF IT IS A LESS EFFICIENT IMPLEMENTATION COMPARED TO CHANGING THE ASSIGNMENT OF THE PARENT NODE.
##
##3. BRIEF ANALYSIS OF HOW PROGRAM WORKS AND HOW IT MAY BE IMPROVED:
##   THE PROGRAM WORKS WELL WITH THE PROVIDED CONSTRAINT FILES. BACKTRACKING IS OBSERVED ONLY IN CONSTRAINT FILE 3. NUMBER OF BACKTRACKS RANGES
##   FROM 0 - 3 FOR THE THIRD FILE. A WAY TO IMPROVE THE PROGRAM IS BY ADDING ARC CONSISTENCY WHICH WILL FURTHER REDUCE THE NECESSITY TO 
##   BACKTRACK. ALSO, IN CERTAIN CASES, RECURSIVE FORWARD CHECKING MAY ALSO IMPROVE PERFORMANCE
##
##   COMMENTS END

import sys
import random
import operator


##REPRESENT STATES
class n_state: 
	
	def __init__(self, key):
		self.key = key
		self.nxt_nodes = {}
		self.d_set = False
		self.t_set = False
		self.av_bndwdts = ['A', 'B', 'C', 'D']

##ENABLE STATE LINKING	
class Graph:

	def __init__(self):	
		self.n_lst = {}

	def plus_node(self, node):
		if node in self.n_lst: 
			return self.n_lst[node]
		else:	
			n_obj= n_state(node)
			self.n_lst[node] = n_obj
			return n_obj

	def plus_nxt(self, pnode, cnode):
		if pnode not in self.n_lst:
			p_node = self.plus_node(pnode)
		else:
			p_node = self.n_lst[pnode]
			if cnode in p_node.nxt_nodes:
				return
		if cnode not in self.n_lst:
			c_node = self.plus_node(cnode)
		else:
			c_node = self.n_lst[cnode]
		p_node.nxt_nodes[cnode] = c_node
		return 

def fwd_chk(p_node):
	domain = p_node.av_bndwdts
	if p_node.nxt_nodes:
		for y in p_node.nxt_nodes:
			x = p_node.nxt_nodes[y]
			if x.d_set == False:
				if len(x.av_bndwdts) > 0:
					if domain in x.av_bndwdts:
						if (len(x.av_bndwdts) - 1) != 0:
							x.av_bndwdts.remove(domain)
						else: 
							# print "wrong assignment"
							return -1
				elif len(x.av_bndwdts) == 0:
					# print "wrong assignment"
					return -1
	return


def ord_stck(p_node):
	dict_c = {}
	dict_nc = {}
	dict_nc2 = {}
	l_c = []
	l_nc = []
	l_nc2 = []
	srtd_c = []
	srtd_d = []
	srtd_f = []
	

	for i in p_node.nxt_nodes:
		
		if len(p_node.nxt_nodes[i].av_bndwdts) == 1:
			if ((p_node.nxt_nodes[i].d_set == False) or (p_node.nxt_nodes[i].d_set == True and p_node.nxt_nodes[i].t_set == False)):
				dict_c[p_node.nxt_nodes[i]] = len(p_node.nxt_nodes[i].nxt_nodes)
				#contains all the nodes with just 1 constraint...should be given utmost importance
			else: pass		
		else:
			if ((p_node.nxt_nodes[i].d_set == False) or (p_node.nxt_nodes[i].d_set == True and p_node.nxt_nodes[i].t_set == False)):
				dict_nc[p_node.nxt_nodes[i]] = len(p_node.nxt_nodes[i].av_bndwdts)
				u = dict_nc[p_node.nxt_nodes[i]]
				#contains all the nodes with just more than 1 constraint...least should be given utmost importance
			else: pass
	
	if (not dict_c) and (not dict_nc):
		return 1
	
	if len(dict_nc) > 1:
		if all(v == u for v in dict_nc.values()):
			dict_nc = {}
			for i in p_node.nxt_nodes:
				if ((p_node.nxt_nodes[i].d_set == False) or (p_node.nxt_nodes[i].d_set == True and p_node.nxt_nodes[i].t_set == False)):
					#print 'Node: ', i,'  is not constrained'
					dict_nc2[p_node.nxt_nodes[i]] = len(p_node.nxt_nodes[i].nxt_nodes)
					#contains nodes sorted according to number of neighbors...highest should be given priority	
				else: pass
			
	if dict_c:
		l_c = sorted(dict_c.items(), key=operator.itemgetter(1))
		srtd_c = l_c
	
	if dict_nc:
		l_nc = sorted(dict_nc.items(), key=operator.itemgetter(1))
		srtd_c = srtd_c + l_nc

	if dict_nc2:
		l_nc2 = sorted(dict_nc2.items(), key=operator.itemgetter(1))
		srtd_d =  l_nc2 + srtd_c

	#ordering if dict_nc exists 
	if (not dict_nc) and (not dict_nc2) and (dict_c):
		for i in range(len(srtd_c)):
			obj = srtd_c[i]
			srtd_f.append(obj[0])

	if dict_nc:
		l = len(srtd_c)
		for n in range(l):
			srtd_f.append(0)
		for i in range(l):
			obj = srtd_c[i]
			srtd_f[l-i-1] = (obj[0])

	
	#ordering if dict_nc2 exists
	if dict_nc2:		
		for i in range(len(srtd_d)):
			obj = srtd_d[i]
			srtd_f.append(obj[0])

	return srtd_f 	


def dfs(p_node):
	global stk
	global a
	global b_strike
	
	##VISITED NODE
	p_node.t_set = True
	a.append(p_node)
	bkp_bndwths = []
	
	##REFRESH STACK
	if p_node.d_set == False:
		# print p_node.av_bndwdts
		if p_node.av_bndwdts: 
			bkp_bndwths = p_node.av_bndwdts 
			p_node.av_bndwdts = random.choice(p_node.av_bndwdts)
			p_node.d_set = True
			fwdchk = fwd_chk(p_node)
			
			while fwdchk == -1:
				if len(bkp_bndwths) > 1:
					p_node.d_set = False
					p_node.av_bndwdts = bkp_bndwths 
					p_node.av_bndwdts=random.choice(p_node.av_bndwdts)
					p_node.d_set = True
					fwdchk = fwd_chk(p_node)
				else:
					# print"\tBACKTRACKING"
					b_strike += 1
					stk = []
					grph.n_lst = {}
					a= []
					ingst_data()
					return

		#ADDED BACKTRACKING HERE! - 10:24
		else:
			# print"\tFATAL Error"
			# print"\tBACKTRACKING"
			b_strike += 1
			stk = []
			grph.n_lst = {}
			a= []
			ingst_data()
			return

	nxtlst =  ord_stck(p_node)
	
	# if nxtlst == 0:
	# 	print "WTF"
	# 	return

	if nxtlst == 1:
		if stk:
			nxt = stk.pop()
			while (nxt.t_set != False):
				if stk:
					nxt = stk.pop()
				else:
					return
		
		if stk: dfs(nxt)
		else: return

	else:
		for x in nxtlst:
			if x.t_set == True:
				pass
			# elif x.d_set == True:
			# 	pass
			else:
				stk.append(x)
	
	if stk:
		nxt = stk.pop()
		while (nxt.t_set != False):
			if stk:
				nxt = stk.pop()
			else:
				return
		dfs(nxt)
	else: return


##INGEST DATA AND START TRAVERSAL
def ingst_data():
	global fle
	global grph
	global stk
	global b_strike

	inpt  = open('adjacent-states', 'r')
	n_count = 0
	for line in inpt:
		L = line.split()
		if len(L) >= n_count:
			n_count = len(L)
			n_const = L[0]
		for word in range(len(L)):
			if word == 0:
				grph.plus_node(L[word])
			else:
				grph.plus_nxt(L[0], L[word])
	inpt.close()

	##READ CONSTRAINTS & TRIANGULATE VARIABLE
	inpt  = open(fle, 'r')
	s_nmax = 0
	const_lst = []
	for lines in inpt:
		M = lines.split()
		if M:
			##FIND THE MOST CONSTRAINING DOMAIN CONSTRAINED VARIABLE
			s_node = grph.n_lst[M[0]]
			s_node.av_bndwdts = M[1]
			s_node.d_set = True
			s_nlen = len(s_node.nxt_nodes)
			const_lst.append(s_node)
			if s_nlen >= s_nmax:
				s_nmax = s_nlen
				n_max = s_node
		else:
			##FIND THE MOST CONSTRAINING VARIABLE WHEN NO EXTERNAL CONSTRAINTS
			l_max = n_count
			n_max = grph.n_lst[n_const]
			n_max.av_bndwdts = random.choice(n_max.av_bndwdts)
			n_max.d_set = True
			break
	##ASSIGN VALUES FOR STATES W/O NEIGHBORS
	for states in grph.n_lst:
		if len(grph.n_lst[states].nxt_nodes) == 0:
			grph.n_lst[states].av_bndwdts = random.choice(grph.n_lst[states].av_bndwdts) 
	
	# FORWAARD CHECK FOR LEGACY CONSTRAINTS
	for r in const_lst:
	# 	print r.key, r.av_bndwdts
		fwd_chk(r)

	fwd_chk(n_max)
	
	##Avoid infinite loop
	if b_strike >= 10000:
		return

	##INITIATE TRAVERSAL
	if n_max.nxt_nodes:
		dfs(n_max)
	return


##INITIALIZE
fle = str((sys.argv[1]))
grph = Graph()
stk = []
b_strike = 0
a = []

ingst_data()

## FOR DEBUGGING
# for x in grph.n_lst:
# 	print "\nDEBUG", grph.n_lst[x].av_bndwdts,
# 	for n in grph.n_lst[x].nxt_nodes:
# 		print grph.n_lst[x].nxt_nodes[n].av_bndwdts,

otpt = open('results.txt', 'w')

for x in grph.n_lst:
	otpt.write(grph.n_lst[x].key + ' ' + grph.n_lst[x].av_bndwdts + '\n')

otpt.close()
	
print "Number of backtracks: ", b_strike