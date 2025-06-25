from os.path import exists # required for checking if a file by the filename entered already exists

def qryCmmdVald(qry,vRespLst):
  '''query with command vaildation (a function that prints an error when a invalid command string is entered and requests for a response again. The valid strings must be put into a list and sent through the 2nd parameter)'''
  while True:
    resp=input(qry)
    resp = resp.lower() # QoL improvement, you can enter capitals now
    for vResp in vRespLst: # vResp -> Valid Response
      if resp==vResp:
        return resp
    print("\nERROR: Invalid command")

def qryTypeVald(qry,vType,lLim=-99999999999999999999,uLim=99999999999999999999, enterIsZero = False):
  '''query with input datatype validation, also has provision for specifing valid range for float and int'''
  while True:
    try:

      resp = input(qry)
      #provision to interpret no input as zero
      if (resp == "") & enterIsZero:
        resp = "0"
      
      resp=vType(resp)

      if vType==float or vType==int: #vType-> valid data type function object
        if resp>=lLim and resp<=uLim: #makes sure number is within specified limits
          return resp
        else:
          print("\nERROR: Input out of bounds. Enter a number between",lLim,"and",uLim)
      else:
        return resp
    except:
      print("\nERROR: Invalid input type")

def qryTypeCmmdVald(qry,vType,vRespLst,lLim=-99999999999999999,uLim=99999999999999999): 
  '''query with both command and datatype validation'''
  while True:
    try:
      resp=input(qry)
      resp=vType(resp)
      if vType==float or vType==int:
        if resp>=lLim and resp<=uLim:
          return resp
        else:
          print("\nERROR: Input out of bounds. Enter a number between",lLim,"and",uLim)
      else:
        return resp
    except:
      for vResp in vRespLst:
        if resp==vResp:
          return resp
      print("\nERROR: Invalid command")

def vFName(qry):
  '''function checks if user enters a valid filename (checks if file already exists or if invalid characters are there in filename), reasks for filename if invalid'''
  while True:
    valid=True
    resp=input(qry)
    if resp[-4:]==".txt": # makes program ignore if user types '.txt' at end of filename
      temp_str = ""   
      for a in range(len(resp)): 
        if not (a-len(resp)<=-1 and a-len(resp)>=-4): 
          temp_str = temp_str + resp[a]
      resp=temp_str
    for a in resp: #checks for invalid characters
      if a=='/' or a=='\\' or a==':' or a=='*' or a=='?' or a=='"' or a=='<' or a=='>' or a=='|' or (ord(a)<=0 and ord(a)<=31):
        print('''\nERROR: Invalid filename. Make sure your filename doesn't contain '/', '\\', ':', '*', '?', '"', '<', '>', '|' ''')
        valid=False
        break
    if exists('Results/'+resp+".txt") or exists('Results/'+resp+".eps") or exists('Log/'+resp+".json"):
      print("\nERROR: File already exists (as .txt/.esp in Results folder or as .json in Log folder). Enter a new name")
      valid=False
    if valid==True:
      return resp
 
def get_pl_dict(mag,pos):
  ''' Returns a dictionary containing point load information based on the mag and pos parameters '''
  point_load_info={
    'magnitude':mag,
    'position':pos,
  }
  return point_load_info
    
def get_udl_dict(mag,s_pos,e_pos):
  ''' Returns a dictionary containing udl information based on the mag, s_pos and e_pos parameters '''
  udl_info={
    'magnitude':mag,
    'start position':s_pos,
    'end position':e_pos,
    'equivalent point load':get_pl_dict(mag*(e_pos-s_pos), s_pos+(e_pos-s_pos)/2)
  }
  return udl_info
    
def get_span_dict():
  ''' Returns a dictionary to store span info. I have initialised the key value pairs so that the datastructure is easier to understand for me. '''
  span={

    'length':None,
    
    'width':None,
        
    'width mm':None,
        
    'depth':None,
        
    'depth mm':None,
        
    'effective depth':None,
        
    'effective depth mm':None,
    
    'span end positions':None,
    
    'steel grade':None,
    
    'concrete grade':None,
    
    'stirrup diameter mm':None,
    
    'stirrup area mm2':None,
    
    'inertia':None,
        
    'point loads':[],
        
    'UDLs':[],
    
    'fixed end moments':
    {
        'left':None,
        'right':None
    },
    
    'distribution factor':
    {
        'left':None,
        'right':None
    },
        
    
    
    'FBD':
    {
        'end moments':
        {
            'left':None,
            'right':None
        },
        'reactions':
        {
            'left':None,
            'right':None
        }
    },
    
    'moment values':None,
    
    'shear force values':None,
    
    'Xumax':None,
    
    'Ru':None,
    
    'Mulim':None,
    
    'area of steel under tension (at every 1/10 of span)':None,
    
    'area of steel under compression (at every 1/10 of span)':None,
    
    'stirrup spacing (at every 1/10 of span)':None
    
  }
  return span
    
