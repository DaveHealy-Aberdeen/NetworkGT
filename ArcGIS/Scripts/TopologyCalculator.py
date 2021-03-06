#==================================
#Author Bjorn Burr Nyberg 
#University of Bergen
#Contact bjorn.nyberg@uib.no
#Copyright 2016
#==================================

'''This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

import  os,sys
import numpy as np

arcpy.env.overwriteOutput = True

def main (Topo,calc,p,ndv,Output):
    
    Topo = Topo.split(';')
    
    if len(Topo) < 2:
        arcpy.AddError("Require a minimum of two datasets to perform calculation")
    	sys.exit()

    field_check = set(['I','Y','X','No__Branch','Sample_No_'])
    check2 = None
    FID_Max = 0
    
    for shp in Topo: #Check dataset and get maximum Sample_No_
        curfields = set([f.name for f in arcpy.ListFields(shp)])
        check = field_check - curfields
        if not check2:
            check2 = len(curfields)
 
        if len(check) != 0 and len(curfields) == check2:
            arcpy.AddError("Datasets require the same number of fields and need to be topology datasets")
            sys.exit()
        with arcpy.da.SearchCursor(shp,"Sample_No_") as cursor:
            for row in cursor:
                if row[0] > FID_Max:
                    FID_Max = row[0]
                
    arcpy.AddMessage('Creating Feature and Fields')

    dname = os.path.dirname(Output)
    arcpy.CreateFeatureclass_management(dname,os.path.basename(Output),"POLYGON",Topo[0],'ENABLED','ENABLED',Topo[0])

    fields = []

    
    alias = {'E': 'No. E', 'U': 'No. U', 'I':'No. I', 'Y':'No. Y', 'X':'No. X', 'Sample_No_':'Sample No.','Circumfere':'Circumference','No__Nodes':'No. Nodes',
             'No__Branch': 'No. Branhces','No__Lines': 'No. Lines', 'F1D_Intens': '1D Intensity', 'F2D_Intens' : '2D Intensity',
             'No__Connec':'No. Connections','Branch_Fre':'Branch Frequency', 'Line_Freq': 'Line Frequency', 'NcFreq': 'Connecting Node Frequency',
             'Connect_Li': 'Connect/Line', 'Average_Li': 'Average Line Length', 'Average_Br': 'Average Branch Length',
             'Connect_Br':'Connect/Branch','Dimensionl':'Dimensionless Intensity','C___C': 'No. C - C','C___I':'No. C - I', 'I___I': 'No. I - I', 'C___U':
             'No. C - U', 'I___U':'No. I - U','U___U':'No. U - U','C___C_1': 'C - C Length','C___I_1':'C - I Length', 'I___I_1': 'I - I Length', 'C___U_1':
             'C - U Length', 'I___U_1':'I - U Length','U___U_1':'U - U Length','No__Bran_1':'No. Branches','Total_Trac': 'Total Trace Length'}

    for field in arcpy.ListFields(Topo[0]):
        if field.type == 'Double' or field.type == 'Integer':
            fields.append(field.name)
                    
    index = fields.index("Sample_No_")

    fields.extend(['Shape@'])
    field_check = set(['I','Y','X','No__Branch'])

    arcpy.AddMessage('Gathering Data and Updating')
    
    data = []
    for enum_shp,shp in enumerate(Topo):
        data_values = []
        FIDs = set([])
        with arcpy.da.SearchCursor(shp,fields[:-1]) as cursor:
            for row in cursor:
                values = []
                FIDs.add(row[index])
                         
                for enum,field in enumerate(fields[:-1]):
                    values.append(row[enum])

                data_values.append(values)

        Total_num = set(range(0,FID_Max))
        for na_value in Total_num - FIDs:   #Create NA values for sample numbers without data
            data_values.insert(na_value,[np.nan]*len(fields[:-1]))
        data.append(np.array(data_values))

    combine = ['+','-','*','/']

    if calc in combine: #Numpy operation
        curData = None
        for year in data:
            if curData == None:
                curData = year
            else:
                value = 'year %s curData'%(calc)
                value = eval(value)
                curData = value

    else:
        if ndv == 'true' and calc != 'ptp':
            calc = 'nan%s'%(calc)
            
        if calc == 'percentile':
            value = 'np.%s(data,%s,axis=0)'%(calc,p)
        else:
            value = 'np.%s(data,axis=0)'%(calc)
        value = eval(value)
        curData = value
   
    del data,value    

    with arcpy.da.InsertCursor(Output,fields) as cursor:
        for row in arcpy.da.SearchCursor(Topo[0],fields):
            FID = row[index]
            values = list(curData[FID])
            values[index]=FID
            values.extend([row[-1]])
            cursor.insertRow(values)

            
if __name__ == "__main__":        
    ###Inputs###
        
    infc = arcpy.GetParameterAsText(0)
    calc = arcpy.GetParameterAsText(1)
    p = arcpy.GetParameterAsText(2)
    ndv = arcpy.GetParameterAsText(4)
    output = arcpy.GetParameterAsText(3)
  
    main(infc,calc,p,ndv,output)
