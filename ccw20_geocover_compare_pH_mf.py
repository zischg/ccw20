import numpy as np
import pandas as pd
myworkspace="D:/CCW20/GIS/Geocover_pH"

#bedrock
in_mf=pd.read_excel(myworkspace+"/"+"stat_geocoverV2_bedrock_mf.xls",0)
in_pH=pd.read_excel(myworkspace+"/"+"stat_geocoverV2_bedrock_pH.xls",0)
in_pHb=in_pH.drop(["OBJECTID", "RBED_LITSTRAT_LINK", "FREQUENCY", "COUNT_OBJECTID"], axis=1)
outdf=pd.merge(in_mf, in_pHb, on=["KIND", "RBED_TECTO", "RBED_FM_HOMOG", "RBED_ORIG_DESCR"])
outdf.min_pH=outdf.MIN_MIN_PH
outdf.max_pH=outdf.MAX_MAX_PH
outdf.mean_pH=outdf.MEAN_MEAN_PH
outdfb=outdf.drop(["MIN_MIN_PH","MAX_MAX_PH","MEAN_MEAN_PH"], axis=1)
outdfb.to_excel(myworkspace+"/"+"stat_geocoverV2_bedrock_mf_pH.xls", sheet_name='Sheet1', na_rep='', float_format="%.2f")

#sediments
in_mf2=pd.read_excel(myworkspace+"/"+"stat_geocoverV2_uncodesposit_mf.xls",0)
in_pH2=pd.read_excel(myworkspace+"/"+"stat_geocoverV2_uncodesposit_pH.xls",0)
in_pH2b=in_pH2.drop(["OBJECTID","FREQUENCY","RUNC_LITSRAT_LINK", "COUNT_OBJECTID"], axis=1)
outdf2=pd.merge(in_mf2, in_pH2b, on=["KIND", "RUNC_LITHO", "RUNC_LITSTRAT", "RUNC_STRUCTUR","RUNC_MORPHOLO","RUNC_GLAC_TYP","RUNC_ORIG_DESCR"])
outdf2.min_pH=outdf2.MIN_MIN_PH
outdf2.max_pH=outdf2.MAX_MAX_PH
outdf2.mean_pH=outdf2.MEAN_MEAN_PH
outdf2b=outdf2.drop(["MIN_MIN_PH","MAX_MAX_PH","MEAN_MEAN_PH"], axis=1)
outdf2b.to_excel(myworkspace+"/"+"stat_geocoverV2_uncodesposit_mf_pH.xls",sheet_name='Sheet1', na_rep='', float_format="%.2f")

