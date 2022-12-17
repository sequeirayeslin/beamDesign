
import numpy as np
from copy import deepcopy
from beamDictKeys import *
from math import sqrt

#below dicts built from tables in IS456 Code

Asc_fact_dict={

    415:{
        0.05:0.63,
        0.10:0.63,
        0.15:0.65,
        0.20:0.68
    },

    500:{
        0.05:0.52,
        0.10:0.54,
        0.15:0.56,
        0.20:0.60
    }

}

Tc_dict = {
    15:{
        0.15:0.28,
        0.25:0.35,
        0.50:0.46,
        0.75:0.54,
        1.00:0.60,
        1.25:0.64,
        1.50:0.68,
        1.75:0.71,
        2.00:0.71,
        2.25:0.71,
        2.50:0.71,
        2.75:0.71,
        3.00:0.71
    },
    20:{
        0.15:0.28,
        0.25:0.36,
        0.50:0.48,
        0.75:0.56,
        1.00:0.62,
        1.25:0.67,
        1.50:0.72,
        1.75:0.75,
        2.00:0.79,
        2.25:0.81,
        2.50:0.82,
        2.75:0.82,
        3.00:0.82
    },
    25:{
        0.15:0.29,
        0.25:0.36,
        0.50:0.49,
        0.75:0.57,
        1.00:0.64,
        1.25:0.70,
        1.50:0.74,
        1.75:0.78,
        2.00:0.82,
        2.25:0.85,
        2.50:0.88,
        2.75:0.90,
        3.00:0.92
    },
    30:{
        0.15:0.29,
        0.25:0.37,
        0.50:0.50,
        0.75:0.59,
        1.00:0.66,
        1.25:0.71,
        1.50:0.76,
        1.75:0.80,
        2.00:0.84,
        2.25:0.88,
        2.50:0.91,
        2.75:0.94,
        3.00:0.96
    }
}

Tc_max_dict = {
    15: 2.5,
    20: 2.8,
    25: 3.1,
    30: 3.5
}

def calFemLeft(span):
    ''' Finds FEM at left side of span '''
    femL = 0
    
    
    
    for udl in span[udls]:
    
        integr = lambda x: -udl[mag] / span[L]**2 * ((span[L]**2 * x**2 / 2) - (2 * span[L] * x**3 / 3) + (x**4 / 4))
        femL += integr(udl[endPos]) - integr(udl[strPos])

    
    for pointL in span[pLs]:
        tmp = span[L] - pointL[pos]
        femL += -pointL[mag] * pointL[pos] * tmp**2 / span[L]**2
    
    return femL
    
def calFemRight(span):
    ''' Finds FEM at right side of span '''
    femR = 0
    
    for udl in span[udls]:
        
        integr = lambda x: udl[mag] / span[L]**2 * ((span[L] * x**3 / 3) - (x**4 / 4))
        femR += integr(udl[endPos]) - integr(udl[strPos])
    
    for pointL in span[pLs]:
        tmp = span[L] - pointL[pos]
        femR += pointL[mag] * pointL[pos]**2 * tmp / span[L]**2
    
    return femR
    
def calI(span):
    ''' Finds moment of inertia '''
    return span[b] * span[D]**3 / 12

def tmpVal(i, l_or_r, span, tot_spans):
    ''' Calculates a temporary value required for calculating distribution factor '''
    if i == 0 and l_or_r == l:
        raise ValueError('Invalid indice')
    elif i == tot_spans - 1 and l_or_r == r:
        raise ValueError('Invalid indice')
    
    if i == 0 and l_or_r == r:
        return 3 * span[I] /span [L]
    
    elif i == tot_spans-1 and l_or_r == l:
        return 3 * span[I] / span [L]
    
    return 4 * span[I] / span[L]

def calDFLeft(curSpan, prevSpan, i, tot_spans):
    ''' Calculates distribution factor on left side of span (curSpan) '''

    if i == 0:
        return 1
    
    tmp1 = tmpVal(i-1, r, prevSpan, tot_spans)
    tmp2 = tmpVal(i, l, curSpan, tot_spans)
    return tmp2 / (tmp1 + tmp2)

def calDFRight(curSpan, nxtSpan, i, tot_spans):
    ''' Calculates distribution factor on right side of span (curSpan) '''
    if i == tot_spans-1:
        return 1
    
    tmp1 = tmpVal(i, r, curSpan, tot_spans)
    tmp2 = tmpVal(i+1, l, nxtSpan, tot_spans)
    return tmp1 / (tmp1 + tmp2)
    
def perfMomDist(spans, canLMom, canRMom):
    ''' Performs moment distribution method on spans and returns a list of moments at each span '''
    if len(spans) == 1:
        return [[canLMom, canRMom]]

    fem_lst=[]
    dfArr=[]
    for span in spans:
        fem_lst.append([span[fems][l], span[fems][r]])
        dfArr.append([span[df][l], span[df][r]])

    #initial factors to sum#

    can_fact=np.array([[-canLMom, -canLMom/2]] + [[0,0]] * (len(spans)-2) + [[-canRMom/2, -canRMom]])

    fem_fact = np.array(fem_lst)

    tmp1 = -fem_fact[0][0]
    tmp2 = -fem_fact[-1][-1]

    init_fact = np.array([[tmp1, tmp1/2]] + [[0,0]] * (len(spans)-2) + [[tmp2/2, tmp2]])



    accum=np.array([[0,0]]*len(spans)) #accumulator

    inter = can_fact + fem_fact + init_fact #intermediate

    inter_prev = deepcopy(inter) #previous intermediate result, gives info to manipulate intermediate array

    accum = accum + inter

    #initial factors to sum (end)#

    #second initialising step#

    inter[0][0] = 0
    inter[0][1] = -(inter_prev[0][1] + inter_prev[1][0]) * dfArr[0][1]

    inter[-1][1] = 0
    inter[-1][0] = -(inter_prev[-2][1] + inter_prev[-1][0]) * dfArr[-1][0]


    for i in range(1, len(inter) - 1):
        inter[i][0] = -(inter_prev[i-1][1] + inter_prev[i][0]) * dfArr[i][0]
        inter[i][1] = -(inter_prev[i][1] + inter_prev[i+1][0]) * dfArr[i][1]

    accum = accum + inter


    #second initialising step (end)#

    maxVal=max([np.amax(inter), -np.amin(inter)])

    while maxVal>=0.01:

        inter = [valPair[::-1]/2 for valPair in inter]
        inter = np.array(inter)

        inter[0][0] = inter[-1][1] = 0

        accum = accum + inter

        inter_prev = deepcopy(inter)
        
        inter[0][0] = 0
        inter[0][1] = -(inter_prev[0][1] + inter_prev[1][0]) * dfArr[0][1]

        inter[-1][1] = 0
        inter[-1][0] = -(inter_prev[-2][1] + inter_prev[-1][0]) * dfArr[-1][0]


        for i in range(1, len(inter) - 1):
            inter[i][0] = -(inter_prev[i-1][1] + inter_prev[i][0]) * dfArr[i][0]
            inter[i][1] = -(inter_prev[i][1] + inter_prev[i+1][0]) * dfArr[i][1]
        
        accum = accum + inter
        
        maxVal=max([np.amax(inter), -np.amin(inter)])
            
    return accum

def calLeftReac(span):
    ''' Calculates reaction at left support of span '''
    r_acc = 0
  
    for pointL in span[pLs]:
        r_acc += pointL[mag] * (span[L] - pointL[pos])

    for udl in span[udls]:
        r_acc += udl[eqPL][mag] * (span[L] - udl[eqPL][pos])

    r_acc += -(span[fbd][endMoms][l] + span[fbd][endMoms][r])

    return r_acc/span[L]

def calRightReac(span):
    ''' Calculates reaction at right support of span '''
    r_acc = 0

    for pointL in span[pLs]:
        r_acc += pointL[mag] * pointL[pos]
    
    for udl in span[udls]:
        r_acc += udl[eqPL][mag] * udl[eqPL][pos]
    
    r_acc += (span[fbd][endMoms][l] + span[fbd][endMoms][r])
    
    return r_acc/span[L]

def calSf(x, span):
    ''' finds shear force at x position on span '''
    sf=span[fbd][reacs][l]#adds left reaction
  
    for pointL in span[pLs]:#subs point load forces at LHS of current position
        if pointL[pos] < x:
            sf -= pointL[mag]

    for udl in span[udls]:#subs force due to udls on LHS
        if udl[endPos] < x:#checks if x has crossed udl
            sf -= udl[eqPL][mag]
        elif udl[strPos] < x:#checks if x is within udl
            sf -= udl[mag] * (x - udl[strPos])

    return sf

def calMom(x, span):
    ''' finds moment at x position on span '''
    mom_acc = span[fbd][reacs][l]*x #adds moment due to left reaction
    mom_acc += span[fbd][endMoms][l]# adds moment at left support

    for pointL in span[pLs]:#subs moment due to point loads at LHS of current position
        if pointL[pos] <= x:
            mom_acc -= pointL[mag] * (x - pointL[pos])

    for udl in span[udls]: #subs moment due to udls
        if udl[endPos] <= x: #checks if curPos has crossed bth udl
            mom_acc -= udl[eqPL][mag] * (x - udl[eqPL][pos])
        elif udl[strPos] <= x:#checks if curPos is within bth udl
            mom_acc -= udl[mag] * (x - udl[strPos]) * (x - udl[strPos])/2

    return mom_acc

def calBeamLen(spans):
    acc_len=0
    for spanL in [span[L] for span in spans]:
        if spanL==None:
            continue
        acc_len+=spanL
    return acc_len

def scaleToBeam(fun, x, spans):
    ''' Makes finding value of certain parameter of beam (like moment, shear force; as defined by input function argument 'fun') at a certain beam position easy. '''
    
    for i, (leftEnd, rightEnd) in enumerate([span[spanEnds] for span in spans]):
        if x >= leftEnd and x <= rightEnd:
            x=x-leftEnd
            span_no=i
            break
        if i==len(spans)-1:
            x=x-leftEnd
            span_no=i

    return fun(x, spans[span_no])

def calXumax(span):
    return 700 / (1100 + 0.87 * span[fy]) * span[d_mm]

def calRu(span):
    tmp = span[Xumax] / span[d_mm]
    return 0.36 * span[fck] * tmp * (1 - 0.416 * tmp)

def calMulim(span):
    ''' Finds Mulim "in Nmm" '''
    return span[Ru] * span[b_mm] * span[d_mm]**2

def calAst(x,span):
    ''' Finds Area od steel in tension in mm2 '''
    #factored moment in Nmm
    Mu=1.5 * calMom(x,span) * 10**6
    if Mu <= span[Mulim]:
        tmp1 = 0.5 * span[fck] /span[fy]
        tmp2 = sqrt(1 - 4.6 * Mu / (span[fck] * span[b_mm] * span[d_mm]**2))
        retAst = tmp1 * (1 - tmp2) * span[b_mm] * span[d_mm]
    else:
        tmp1 = 0.5 * span[fck] /span[fy]
        tmp2 = sqrt(1 - 4.6 * span[Mulim] / (span[fck] * span[b_mm] * span[d_mm]**2))
        Ast1 = tmp1 * (1 - tmp2) * span[b_mm] * span[d_mm]
        
        tmp3 = span[d_mm]-50 # 50 is d dash
        Ast2 = (Mu - span[Mulim])/(0.87 * span[fy] * tmp3)
        retAst = Ast1 + Ast2
    
    return retAst

def getAst2Fact(span):
    if span[fy] == 415:
        return 0.6
    elif span[fy] == 500:
        return 0.5

def getAscFact(span):

    d_dash=50
    dRatio=d_dash/span[d_mm]
    dRatio = round(dRatio/5,2)*5
    dRatio = round(dRatio,2)
    if dRatio<0.05 or dRatio>0.2:
        raise ValueError("Cannot find Asc factor of d'/d ratio: {}".format(dRatio))
    
    return Asc_fact_dict[span[fy]][dRatio]


def calAsc(x,span):
    ''' Finds area of steel in compression (Asc) in mm2 '''
    Mu=1.5*calMom(x,span)*10**6

    if Mu<span[Mulim]:
        return 0
    else:
        d_dash=50
        Ast2= (Mu-span[Mulim])/(span[fy]*0.87*(span[d_mm]-d_dash))

    tmp = Ast2/getAst2Fact(span)
    
    Asc = tmp * getAscFact(span)

    return Asc

def calTv(x,span):
    ''' Calculates nominal shear stress in N/mm2 '''
    Vu = 1.5 * calSf(x,span) *1000
    return Vu/(span[b_mm]*span[d_mm])

def calTc(x,span):
    ''' Calculates design shear strength of concrete in N/mm2 '''
    st_per = 100 * calAst(x,span) / (span[b_mm] * span[d_mm])
    if st_per <= 0.15:
        st_per = 0.15
    else:
        st_per = round(st_per/25,2)*25
        st_per = round(st_per,2)
        if st_per>3.0:
            st_per = 3.0
            
    return Tc_dict[span[fck]][st_per]

def calSv(x,span):
    ''' Calculates stirrup spacing in mm '''
    Tv_tmp = calTv(x,span) # possible issue
    Tc_tmp = calTc(x,span) # possible issue

    if Tv_tmp > Tc_max_dict[span[fck]]:
        raise ValueError("Error: Tv > Tc_max!")
    if Tv_tmp<Tc_tmp:
        tmp = 0.87 * 415 * span[Asv] / (0.4 * span[b_mm]) # possible issue: span[Asv]
    else:
        Vu = 1.5 * calSf(x,span) * 1000 # possible issue: calSf(x,span)
        Vus = Vu - Tc_tmp * span[b_mm] * span[d_mm]
        tmp = 0.87 * 415 * span[Asv] * span[d_mm] / Vus
    
    # adjusting Sv according to indian standards (as per IS 456 2000)
    
    return min(tmp, 300, 0.75*span[d_mm])