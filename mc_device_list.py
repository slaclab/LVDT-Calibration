class Collimator:
    def __init__(self, pv_name, mad_name, coll_name):
        self.pv_name   = pv_name
        self.mad_name  = mad_name
        self.coll_name = coll_name

collimators = [ 
#''' SC Only Collimators '''
Collimator('COLL:HTR:615:POSX'   , 'CEHTR-POSX'  ,'COLL:HTR:615'   ),  
Collimator('COLL:HTR:615:NEGX'   , 'CEHTR-NEGX'  ,'COLL:HTR:615'   ),  
Collimator('COLL:COL0:390:NEGY'  , 'CYC01-NEGY'  ,'COLL:COL0:390'  ),  
Collimator('COLL:COL0:390:POSY'  , 'CYC01-POSY'  ,'COLL:COL0:390'  ),  
Collimator('COLL:COL0:470:NEGX'  , 'CXC01-NEGX'  ,'COLL:COL0:470'  ),  
Collimator('COLL:COL0:470:POSX'  , 'CXC01-POSX'  ,'COLL:COL0:470'  ),  
Collimator('COLL:COL0:710:POSY'  , 'CYC03-POSY'  ,'COLL:COL0:710'  ),  
Collimator('COLL:COL0:710:NEGY'  , 'CYC03-NEGY'  ,'COLL:COL0:710'  ),  
Collimator('COLL:COL0:790:NEGX'  , 'CXC03-NEGX'  ,'COLL:COL0:790'  ),  
Collimator('COLL:COL0:790:POSX'  , 'CXC03-POSX'  ,'COLL:COL0:790'  ),  
Collimator('COLL:BC1B:450:POSX'  , 'CE11B-POSX'  ,'COLL:BC1B:450'  ),  
Collimator('COLL:BC1B:450:NEGX'  , 'CE11B-NEGX'  ,'COLL:BC1B:450'  ),  
Collimator('COLL:COL1:390:NEGY'  , 'CYC11-NEGY'  ,'COLL:COL1:390'  ),  
Collimator('COLL:COL1:390:POSY'  , 'CYC11-POSY'  ,'COLL:COL1:390'  ),  
Collimator('COLL:COL1:470:NEGX'  , 'CXC11-NEGX'  ,'COLL:COL1:470'  ),  
Collimator('COLL:COL1:470:POSX'  , 'CXC11-POSX'  ,'COLL:COL1:470'  ),  
Collimator('COLL:COL1:710:NEGY'  , 'CYC13-NEGY'  ,'COLL:COL1:710'  ),  
Collimator('COLL:COL1:710:POSY'  , 'CYC13-POSY'  ,'COLL:COL1:710'  ),  
Collimator('COLL:COL1:790:NEGX'  , 'CXC13-NEGX'  ,'COLL:COL1:790'  ),  
Collimator('COLL:COL1:790:POSX'  , 'CXC13-POSX'  ,'COLL:COL1:790'  ),  
Collimator('COLL:BC2B:535:POSX'  , 'CE21B-POSX'  ,'COLL:BC2B:535'  ),  
Collimator('COLL:BC2B:535:NEGX'  , 'CE21B-NEGX'  ,'COLL:BC2B:535'  ),  
Collimator('COLL:DOG:131:POSY'   , 'CEDOG-POSY'  ,'COLL:DOG:131'   ),  
Collimator('COLL:DOG:131:NEGY'   , 'CEDOG-NEGY'  ,'COLL:DOG:131'   ),  
Collimator('COLL:BPN21:424:NEGX' , 'CXBP21-NEGX' ,'COLL:BPN21:424' ),
Collimator('COLL:BPN21:424:POSX' , 'CXBP21-POSX' ,'COLL:BPN21:424' ),
Collimator('COLL:BPN22:424:NEGY' , 'CYBP22-NEGY' ,'COLL:BPN22:424' ),
Collimator('COLL:BPN22:424:POSY' , 'CYBP22-POSY' ,'COLL:BPN22:424' ),
Collimator('COLL:BPN25:424:NEGX' , 'CXBP25-NEGX' ,'COLL:BPN25:424' ),
Collimator('COLL:BPN25:424:POSX' , 'CXBP25-POSX' ,'COLL:BPN25:424' ),
Collimator('COLL:BPN26:424:NEGY' , 'CYBP26-NEGY' ,'COLL:BPN26:424' ),
Collimator('COLL:BPN26:424:POSY' , 'CYBP26-POSY' ,'COLL:BPN26:424' ),
#''' FACET Collimators '''
Collimator('COLL:LI11:334'  , 'CE11334-NEGX' , 'COLL:LI11:334'  ),  
Collimator('COLL:LI11:335'  , 'CE11334-POSX' , 'COLL:LI11:334'  ),  
Collimator('COLL:LI14:802'  , 'CE14802-NEGX' , 'COLL:LI14:802'  ),  
Collimator('COLL:LI14:803'  , 'CE14802-POSX' , 'COLL:LI14:802'  ),
Collimator('COLL:LI18:961'  , 'CX18960-NEGX' , 'COLL:LI18:961'  ),
Collimator('COLL:LI18:960'  , 'CX18960-POSX' , 'COLL:LI18:961'  ),
Collimator('COLL:LI18:962'  , 'CY18960-NEGY' , 'COLL:LI18:962'  ),
Collimator('COLL:LI18:963'  , 'CY18960-POSY' , 'COLL:LI18:962'  ),
Collimator('COLL:LI20:2085' , 'CX2085-NEGX'  , 'COLL:LI20:2085' ),
Collimator('COLL:LI20:2086' , 'CX2085-POSX'  , 'COLL:LI20:2085' ),
#''' NC Only Collimators '''
Collimator('COLL:LI21:235'  , 'CE11-NEGX' , 'COLL:LI11:235'  ),
Collimator('COLL:LI21:236'  , 'CE11-POSX' , 'COLL:LI11:235'  ),
Collimator('COLL:LI24:805'  , 'CE21-NEGX' , 'COLL:LI24:805'  ),
Collimator('COLL:LI24:806'  , 'CE21-POSX' , 'COLL:LI24:805'  ),
Collimator('COLL:LI28:916'  , 'C29096-NEGX' , 'COLL:LI28:916'  ),
Collimator('COLL:LI28:917'  , 'C29096-POSX' , 'COLL:LI28:916'  ),
Collimator('COLL:LI28:918'  , 'C29096-NEGY' , 'COLL:LI28:918'  ),
Collimator('COLL:LI28:919'  , 'C29096-POSY' , 'COLL:LI28:918'  ),
Collimator('COLL:LI29:146'  , 'C29146-NEGX' , 'COLL:LI29:146'  ),
Collimator('COLL:LI29:147'  , 'C29146-POSX' , 'COLL:LI29:146'  ),
Collimator('COLL:LI29:148'  , 'C29146-NEGY' , 'COLL:LI29:148'  ),
Collimator('COLL:LI29:149'  , 'C29146-POSY' , 'COLL:LI29:148'  ),
Collimator('COLL:LI29:446'  , 'C29446-NEGX' , 'COLL:LI29:446'  ),
Collimator('COLL:LI29:447'  , 'C29446-POSX' , 'COLL:LI29:446'  ),
Collimator('COLL:LI29:448'  , 'C29446-NEGY' , 'COLL:LI29:448'  ),
Collimator('COLL:LI29:449'  , 'C29446-POSY' , 'COLL:LI29:448'  ),
Collimator('COLL:LI29:546'  , 'C29546-NEGX' , 'COLL:LI29:546'  ),
Collimator('COLL:LI29:547'  , 'C29546-POSX' , 'COLL:LI29:546'  ),
Collimator('COLL:LI29:548'  , 'C29546-NEGY' , 'COLL:LI29:548'  ),
Collimator('COLL:LI29:549'  , 'C29546-POSY' , 'COLL:LI29:548'  ),
Collimator('COLL:LI29:956'  , 'C29956-NEGX' , 'COLL:LI29:956'  ),
Collimator('COLL:LI29:957'  , 'C29956-POSX' , 'COLL:LI29:956'  ),
Collimator('COLL:LI29:958'  , 'C29956-NEGY' , 'COLL:LI29:958'  ),
Collimator('COLL:LI29:959'  , 'C29956-POSY' , 'COLL:LI29:958'  ),
Collimator('COLL:LI30:146'  , 'C30146-NEGX' , 'COLL:LI30:146'  ),
Collimator('COLL:LI30:147'  , 'C30146-POSX' , 'COLL:LI30:146'  ),
Collimator('COLL:LI30:148'  , 'C30146-NEGY' , 'COLL:LI30:148'  ),
Collimator('COLL:LI30:149'  , 'C30146-POSY' , 'COLL:LI30:148'  ),
Collimator('COLL:LI30:446'  , 'C30446-NEGX' , 'COLL:LI30:446'  ),
Collimator('COLL:LI30:447'  , 'C30446-POSX' , 'COLL:LI30:446'  ),
Collimator('COLL:LI30:448'  , 'C30446-NEGY' , 'COLL:LI30:448'  ),
Collimator('COLL:LI30:449'  , 'C30446-POSY' , 'COLL:LI30:448'  ),
Collimator('COLL:LI30:546'  , 'C30546-NEGX' , 'COLL:LI30:546'  ),
Collimator('COLL:LI30:547'  , 'C30546-POSX' , 'COLL:LI30:546'  ),
Collimator('COLL:LI30:548'  , 'C30546-NEGY' , 'COLL:LI30:548'  ),
Collimator('COLL:LI30:549'  , 'C30546-POSY' , 'COLL:LI30:548'  ),
#''' Common LCLS Collimators. Post S30- In BSY and LTU '''
Collimator('COLL:BSYH:892:NEGX' , 'CXQ6-NEGX'   ,'COLL:BSYH:892' ),
Collimator('COLL:BSYH:892:POSX' , 'CXQ6-POSX'   ,'COLL:BSYH:892' ),
Collimator('COLL:SLTS:428:NEGX' , 'CXBP30-NEGX' ,'COLL:SLTS:428' ),
Collimator('COLL:SLTS:428:POSX' , 'CXBP30-POSX' ,'COLL:SLTS:428' ),
Collimator('COLL:BSYS:859:NEGX' , 'CXBP34-NEGX' ,'COLL:BSYS:859' ),
Collimator('COLL:BSYS:859:POSX' , 'CXBP34-POSX' ,'COLL:BSYS:859' ),
Collimator('COLL:LTUH:253:NEGX' , 'CEDL1-NEGX'  ,'COLL:LTUH:253' ),
Collimator('COLL:LTUH:253:POSX' , 'CEDL1-POSX'  ,'COLL:LTUH:253' ),
Collimator('COLL:LTUH:276:NEGY' , 'CYBX32-NEGY' ,'COLL:LTUH:276' ),
Collimator('COLL:LTUH:276:POSY' , 'CYBX32-POSY' ,'COLL:LTUH:276' ),
Collimator('COLL:LTUH:393:NEGX' , 'CXQT22-NEGX' ,'COLL:LTUH:393' ),
Collimator('COLL:LTUH:393:POSX' , 'CXQT22-POSX' ,'COLL:LTUH:393' ),
Collimator('COLL:LTUH:452:NEGX' , 'CEDL3-NEGX'  ,'COLL:LTUH:452' ),
Collimator('COLL:LTUH:452:POSX' , 'CEDL3-POSX'  ,'COLL:LTUH:452' ),
Collimator('COLL:LTUH:475:NEGY' , 'CYBX36-NEGY' ,'COLL:LTUH:475' ),
Collimator('COLL:LTUH:475:POSY' , 'CYBX36-POSY' ,'COLL:LTUH:475' ),
Collimator('COLL:LTUS:116:NEGY' , 'CYBX32-NEGY' ,'COLL:LTUS:116' ),
Collimator('COLL:LTUS:116:POSY' , 'CYBX32-POSY' ,'COLL:LTUS:116' ),
Collimator('COLL:LTUS:235:NEGX' , 'CXQT22-NEGX' ,'COLL:LTUS:235' ),
Collimator('COLL:LTUS:235:POSX' , 'CXQT22-POSX' ,'COLL:LTUS:235' ),
Collimator('COLL:LTUS:345:NEGY' , 'CYDL16-NEGY' ,'COLL:LTUS:345' ),
Collimator('COLL:LTUS:345:POSY' , 'CYDL16-POSY' ,'COLL:LTUS:345' )
]

def get_mad_name(pv_name_arg):
    for collimator in collimators:
        if collimator.pv_name == pv_name_arg:
            return collimator.mad_name
    return None
def get_pv_name(mad_name_arg):
    for collimator in collimators:
        if collimator.mad_name == mad_name_arg:
            return collimator.pv_name
    return None
def get_coll_name(mad_name_arg):
    for collimator in collimators:
        if collimator.mad_name == mad_name_arg:
            return collimator.coll_name
    return None
