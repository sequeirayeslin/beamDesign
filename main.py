#BEAM DESIGN PROGRAM
#Note: Install numpy and tabulate python modules before running

#for printing span information datastructure
import json
#for plotting graps
import plotAnything as pa
#all non-mathematical functions are stored here
from beamDependencies import *
#for printing tables
from tabulate import tabulate
#all mathematical functions are stored here
from beamMathFunctions import *
#for deepcopies, obviously
from copy import deepcopy
#stores variables that have dictionary keys, convenient as they improve the readablility of the datastructure and also allow shortening refrences to keys
from beamDictKeys import *
from math import pi
from os.path import exists

DEBUG=True

print('''
BEAM DESIGN PROGRAM

-> Moment sign convention: clockwise +ve, anticlockwise -ve
-> Enter all forces in kN, all moments in kNm, all lengths in m (except stirrup diameter)
-> Respond to all yes/no questions with 'y' for yes & ENTER for no
-> Stirrups are assumed to be 2 legged''')

queriesReq=True

if exists('input.json'):
    resp=qryCmmdVald("\nLoad json?\n->",['y',''])
    if resp=='y':
        queriesReq=False
    if not queriesReq:
        with open('input.json','r') as data_file:
            spans=json.loads(data_file.read())

        lMom=0
        rMom=0
        proj_name='random'

if queriesReq:
    ### Queries ??? ###

    proj_name=input('\nEnter project name: ')

    span_count = qryTypeVald('''
    How many spans?
    ->'''.replace('\n    ','\n'),int,lLim=1)

    #creates list of span dictionaries
    spans = [get_span_dict() for _ in range(span_count)]

    #provision in case spans, widths, depths are equal

    equalSpans = False
    equalWidth = False
    equalDepth = False
    equalStirDia = False

    if len(spans) > 1:

        resp = qryCmmdVald('''
        Are spans equal?
        ->'''.replace('\n        ','\n'),['y',''])

        if resp == 'y':
            equalSpans = True
        
        if equalSpans:    
            span_len_temp = qryTypeVald('\nEnter span length: ', float, lLim=0)
            
            for span in spans:
                # the elements of list 'spans' are all dictionaries. Iterator 'span' is an allias to them, therefore all value assingnments/mutations can be made to span, and the original will change too.
                span[L] = span_len_temp
                #calculates the span start and end positions and saves them to a tuple assingned to 'span end positions'
                beam_len_so_far = calBeamLen(spans)
                span[spanEnds] = (beam_len_so_far - span[L], beam_len_so_far)
        
        resp = qryCmmdVald('''
        Are widths equal?
        ->'''.replace('\n        ','\n'),['y',''])

        if resp == 'y':
            equalWidth = True
        
        if equalWidth:    
            width_temp = qryTypeVald('\nEnter width: ', float, lLim=0)
            
            for span in spans:
                span[b] = width_temp
                #stores an mm version of width, useful in future calculations
                span[b_mm] = span[b]*1000
        
        resp = qryCmmdVald('''
        Are depths equal?
        ->'''.replace('\n        ','\n'),['y',''])

        if resp == 'y':
            equalDepth = True
        
        if equalDepth:    
            depth_temp = qryTypeVald('\nEnter depth: ', float, lLim=0)
            
            for span in spans:
                span[D] = depth_temp
                #stores an mm version of depth, useful in future calculations
                span[D_mm] = span[D]*1000
                #finds effective depth
                span[d] = span[D]-0.05
                #stores an mm version of effective depth, useful in future calculations
                span[d_mm] = span[d]*1000
        
        resp = qryCmmdVald('''
        Are stirrup diameters equal?
        ->'''.replace('\n        ','\n'),['y',''])

        if resp == 'y':
            equalStirDia = True
        
        if equalStirDia:
            stirDia_tmp = qryTypeVald('\nEnter stirrup diameter (in mm): ',float,lLim=0)
            
            for span in spans:
                span[stirDia] = stirDia_tmp
                span[Asv] = 2 * pi * (span[stirDia]/2)**2

    resp=qryCmmdVald('''
    Steel grade?
    1)415
    2)500
    ->'''.replace('\n    ','\n')
    ,['1','2'])# takes steel grade

    if resp=='1':
      fy_tmp=415
    else:
      fy_tmp=500

    resp=qryCmmdVald('''
    Concrete grade? (Default -> M20)
    1)M15
    2)M20
    3)M25
    4)M30
    Hit Enter for default
    ->'''.replace('\n    ','\n')
    ,['1','2','3','4',''])#takes concrete grade

    if resp=="":
        resp='2'#default value

    fck_tmp=15+(int(resp)-1)*5

    for span in spans:
        span[fy] = fy_tmp
        span[fck] = fck_tmp

    for i,span in enumerate(spans):

        print('\nSPAN #{}:'.format(i+1))
        
        #requests span, width, depth if user says there're not equal for all spans
        if not equalSpans:
            span[L] = qryTypeVald('\nEnter span #{}: '.format(i+1), float, lLim=0)
            #calculates the span start and end positions and saves them to a tuple assingned to 'span end positions'
            beam_len_so_far = calBeamLen(spans)
            span[spanEnds] = (beam_len_so_far - span[L], beam_len_so_far)
        
        if not equalWidth:
            span[b] = qryTypeVald('\nEnter width #{}: '.format(i+1), float, lLim=0)
            #stores an mm version of width, useful in future calculations
            span[b_mm] = span[b] * 1000
        
        if not equalDepth:
            span[D] = qryTypeVald('\nEnter depth #{}: '.format(i+1), float, lLim=0)
            #stores an mm version of depth, useful in future calculations
            span[D_mm] = span[D] * 1000
            #finds effective depth
            span[d] = span[D] - 0.05
            #stores an mm version of effective depth, useful in future calculations
            span[d_mm] = span[d] * 1000
        
        if not equalStirDia:
        
            span[stirDia] = qryTypeVald('\nEnter stirrup diameter #{} (in mm): '.format(i+1),float,lLim=0)
            
            span[Asv] = 2 * pi * (span[stirDia]/2)**2
        
        
        #this while loop helps user decide number of iteration
        while True:
            resp = qryCmmdVald('''
            Do you want to enter
            1) Point loads OR
            2) UDLs?
            Hit ENTER when you're done
            (span #{})
            ->'''.replace('\n            ','\n').format(i+1), ['1','2',''])
            
            if resp == '1':
            
                while True:
                    resp = qryTypeCmmdVald('''\nEnter point load magnitude (Hit ENTER when you're done): ''', float, [''])
                    if resp == '':
                        break
                    pl_arg_tup = (resp,)
                    
                    pl_arg_tup += ( qryTypeVald('''\nEnter point load position: ''', float, 0, span[L]) ,)
                    
                    span[pLs].append( get_pl_dict(*pl_arg_tup) )
                
                #sorts point loads based on position
                span[pLs].sort(key=lambda pointL: pointL[pos])
                
                while True:
                    if len(span[pLs]) == 0:
                        break
                       
                    # creates  a 2D list that stores all values to be displayed on the table
                    tab_lst = [ [j+1, pointL[mag], pointL[pos]] for j,pointL in enumerate(span[pLs])]
                    

                    table = tabulate(tab_lst, headers=['Sr', 'Magnitude', 'Position'], tablefmt='orgtbl')

                    # displays the table
                    print('\n'+table)
                    
                    resp = qryCmmdVald('''
                    Do you want to change anything?
                    ->'''.replace('\n                    ','\n'), ['y', ''])
                    
                    if resp == '':
                        break
                    
                    j = qryTypeVald('\nEnter sr. no.: ', int, 1, len(span[pLs])) - 1
                    mag_temp = qryTypeVald('\nEnter magnitude: ', float)
                    pos_temp = qryTypeVald('\nEnter position: ',float, 0, span[L])
                    
                    span[pLs][j] = get_pl_dict(mag_temp, pos_temp)
                    span[pLs].sort(key=lambda pointL: pointL[pos])
                    
                    
            elif resp == '2':
            
                while True:
                    resp = qryTypeCmmdVald('''\nEnter udl magnitude (Hit ENTER if you're done): ''', float, [''])
                    if resp == '':
                        break
                    udl_arg_tup = (resp,)
                    
                    udl_arg_tup += ( qryTypeVald('''\nEnter udl start position: ''', float, 0, span[L]) ,)
                    
                    udl_arg_tup += ( qryTypeVald('''\nEnter udl end position: ''', float, udl_arg_tup[1], span[L]) ,)
                    
                    span[udls].append( get_udl_dict(*udl_arg_tup) )
                
                
                span[udls].sort(key=lambda udl: udl[strPos])
                
                while True:
                
                    if len(span[udls]) == 0:
                        break

                    # creates  a 2D list that stores all values to be displayed on the table
                    
                    tab_lst = [ [j+1, udl[mag], udl[strPos], udl[endPos]] for j,udl in enumerate(span[udls])]
                    
                    table = tabulate(tab_lst, headers=['Sr', 'Magnitude', 'Start Position', 'End Position'], tablefmt='orgtbl')

                    # displays the table
                    print('\n'+table)
                    
                    resp = qryCmmdVald('''
                    Do you want to change anything?
                    ->'''.replace('\n                    ','\n'), ['y', ''])
                    
                    if resp == '':
                        break
                    
                    j = qryTypeVald('\nEnter sr. no.: ', int, 1, len(span[udls])) - 1
                    
                    mag_temp = qryTypeVald('\nEnter magnitude: ', float)
                    s_pos_temp = qryTypeVald('\nEnter start position: ', float, 0, span[L])
                    e_pos_temp = qryTypeVald('\nEnter end position: ',float, s_pos_temp, span[L])
                    
                    span[udls][j] = get_udl_dict(mag_temp, s_pos_temp, e_pos_temp)
                    span[udls].sort(key=lambda udl: udl[strPos])
                    
            elif resp == '':
                break

    lMom=qryTypeVald('\nEnter left moment: ',float)
    rMom=qryTypeVald('\nEnter right moment: ',float)

    ### Queries ??? END ###

### Calculations +-/x ###

if DEBUG: print("\n\n------------------------------------DEBUG-INFO------------------------------------\n\n")

#calculates moment of inetia for all spans
for i, span in enumerate(spans):
    span[I]=calI(span)
    if DEBUG: print("moment of inertia (span#{}) = {} Kg m2".format(i+1, span[I]))


#these values are required only if there are more than one spans (for moment distribution method)
if len(spans) > 1:

    if DEBUG: print("\n----Handling CASE: spans more than 1, performing additional calcuations----\n")

    #calculates FEMs
    for i, span in enumerate(spans):
        span[fems][l] = calFemLeft(span)
        span[fems][r] = calFemRight(span)
        if DEBUG: print("Span #{}, FEM, Left    = {}".format(i+1, span[fems][l]))
        if DEBUG: print("Span #{}, FEM, Right   = {}".format(i+1, span[fems][r]))
        #span[I]=calI(span)
    if DEBUG: print()

    #calculates distribution factors for each span
    spansCopy = deepcopy(spans)
    prevSpans = [0] + spansCopy[:-1]
    nxtSpans = spansCopy[1:] + [0]

    for i, span, prevSpan in zip(range(len(spans)), spans, prevSpans):
        span[df][l] = calDFLeft(span, prevSpan, i, len(spans))
        if DEBUG: print("Span #{}, Distribution factor, Left    = {}".format(i+1, span[df][l]))

    for i, span, nxtSpan in zip(range(len(spans)), spans, nxtSpans):
        span[df][r] = calDFRight(span, nxtSpan, i, len(spans))
        if DEBUG: print("Span #{}, Distribution factor, Right   = {}".format(i+1, span[df][r]))

    if DEBUG: print("\n----------------------------Handling CASE: END----------------------------\n")

if DEBUG: print("\n**Performing moment disribution method on beam**\n")
#performs moment disribution method on beam
reacMomLst = perfMomDist(spans, lMom, rMom)

#stores moment at ends of span considering it in FBD form
for i, span, (leftEndMom, rightEndMom) in zip(range(len(spans)), spans, reacMomLst):
    span[fbd][endMoms][l] = leftEndMom
    span[fbd][endMoms][r] = rightEndMom
    if DEBUG: print("Span #{}, FBD, end moment, Left    = {}".format(i+1, span[fbd][endMoms][l]))
    if DEBUG: print("Span #{}, FBD, end moment, Right   = {}".format(i+1, span[fbd][endMoms][r]))

if DEBUG: print()

#stores reactions at ends of span considering it in FBD form, required for moment and shear force calculation
for i, span in enumerate(spans):
    span[fbd][reacs][l] = calLeftReac(span)
    span[fbd][reacs][r] = calRightReac(span)
    if DEBUG: print("Span #{}, Support Reaction, Left   = {}".format(i+1, span[fbd][reacs][l]))
    if DEBUG: print("Span #{}, Support Reaction, Right  = {}".format(i+1, span[fbd][reacs][r]))

#finds beam length, will be used in graph ploting
beamLen = calBeamLen(spans)

if DEBUG: print()

#finds Xumax, Ru and Mulim, required for Ast, Asc calculations
for i,span in enumerate(spans):
    span[Xumax]=calXumax(span)
    span[Ru]=calRu(span)
    span[Mulim]=calMulim(span)
    if DEBUG: print("Span #{}, Xumax    = {}".format(i+1, span[Xumax]))
    if DEBUG: print("Span #{}, Ru       = {}".format(i+1, span[Ru]))
    if DEBUG: print("Span #{}, Mulim    = {}".format(i+1, span[Mulim]))

if DEBUG: print("\n(info) Not printing final values, please refer to output\n")

#calculates moments, shear forces, area of steel under compression and tension, and stirrup spacing
for i, span in enumerate(spans):
    spanDiv = span[L]/8
    span[momVals] = [calMom(spanDiv * j, span) for j in range(9)]
    span[sfVals] = [calSf(spanDiv * j,span) for j in range(9)]
    span[Ast] = [calAst(spanDiv * j, span) for j in range(9)]
    span[Asc] = [calAsc(spanDiv * j, span) for j in range(9)]
    span[Sv] = [calSv(spanDiv * j, span) for j in range(9)]



if DEBUG: print("\n\n----------------------------------DEBUG-INFO-END----------------------------------\n\n")

### Calculations +-/* END ###

### Output ->-> ###

#draws graphs

pa.drawGraph()
pa.drawSups(spans, beamLen/10)

#Shear force graph

drawableFun=lambda x: scaleToBeam(calSf, x, spans)

(xscl,yscl) = pa.drawFun(drawableFun, 0, beamLen, oneXUnt = beamLen/10, autoScaleY = True, clr='red', retScl = True)

pa.labelGraph('''
Shear Force Graph:
x-axis: 1 unit = {} m
y-axis: 1 unit = {} kN'''.format(xscl,yscl),(300,300),'red')

#Moment graph

drawableFun=lambda x: scaleToBeam(calMom, x, spans)

(xscl,yscl) = pa.drawFun(drawableFun, 0, beamLen, oneXUnt = beamLen/10 , autoScaleY = True, clr = 'blue', retScl = True)

pa.labelGraph('''
Moment Graph:
x-axis: 1 unit = {} m
y-axis: 1 unit = {} kNm'''.format(xscl,yscl),(-300,300),'blue')

#tables

output_accum = '''
Left Moment: {}
Right Moment: {}

'''.format(lMom, rMom)

for i,span in enumerate(spans):

    tab_lst=[[j+1, 0.125*j, momVal, sfVal, AstVal, AscVal, SvVal] for j, momVal, sfVal, AstVal, AscVal, SvVal in zip(range(9), span[momVals], span[sfVals], span[Ast], span[Asc], span[Sv])]
    
    table = tabulate(tab_lst, headers=['Sr', 'Distance Ratio', 'Moment (kNm)', 'Shear Force (kN)', 'Ast(mm2)', 'Asc (mm2)', 'Sv (mm)'], tablefmt='orgtbl')
    
    pl_tab_lst = [ [j+1, pointL[mag], pointL[pos]] for j,pointL in enumerate(span[pLs])]
    pl_table = tabulate(pl_tab_lst, headers=['Sr', 'Magnitude', 'Position'], tablefmt='orgtbl')

    udl_tab_lst = [ [j+1, udl[mag], udl[strPos], udl[endPos]] for j,udl in enumerate(span[udls])]
                    
    udl_table = tabulate(udl_tab_lst, headers=['Sr', 'Magnitude', 'Start Position', 'End Position'], tablefmt='orgtbl')

    output_accum+='''
    SPAN #{}:
    b (mm): {}
    D (mm): {}
    Stirrup Diameter (mm): {}
    Steel Grade (N/mm2): {}
    Concrete Grade: M{}
    

    Point Loads:

    {}

    UDLs:

    {}

    Output:

    {}
    
    '''.replace('\n    ','\n').format(i+1,span[b_mm], span[D_mm], span[stirDia], span[fy], span[fck], pl_table, udl_table, table)

output_accum += '''
---------------------------------------------------------------------------------------
-> Moment sign convention: clockwise +ve, anticlockwise -ve
-> All forces in kN, all moments in kNm, all lengths in m (except stirrup diameter)
-> Stirrups are assumed to be 2 legged'''

print(output_accum)




### Output ->-> END ###

### Saving Results ###

resp=qryCmmdVald('''
Do you want to save the results?
->'''
,["y",""])

if resp=="y":
    fName=vFName("\nEnter file name: ")
    
    with open('Results/'+fName+'.txt', 'w') as f:
        print('PROJECT: ' + proj_name + '\nFILENAME: '+ fName+'.txt' +'\n\n' + output_accum, file = f)

    resp=qryCmmdVald('''
    Do you want to save the graphs too?
    ->'''.replace('\n    ','\n'),['y',''])

    if resp=='y':
        pa.svGraph('Results/'+fName+'.eps')
    
    with open('Log/'+fName+'.json', 'w') as f:
        print(json.dumps(spans,indent=4), file = f)

    print("\nDone!")

### Saving Results END ###

input('\nHit enter to exit')