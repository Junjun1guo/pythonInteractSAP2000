#-*-coding: UTF-8-*-
#########################################################################
#  Author: Junjun Guo
#  E-mail: guojj@tongji.edu.cn/guojj_ce@163.com/guojj01@gmail.com
#  Environemet: Successfully executed in python 3.8
#  Date: 2021-08-12
#########################################################################
#import necessary modules
import numpy as np
import matplotlib.pyplot as plt
import win32com.client
import sys
from itertools import chain
import math
import os
#########################################################################
#COM (component object model) is a technology from Microsoft that allows objects to communicate without the
#need for either object to know any details about the other, even the language it's implemented in.
#COM defines many interfaces but doesn't provide implementations for many of these interfaces. One commonly used
#interface,IDispatch, allows COM objects to be used from a scripting environment. Information about COM objects
#is stored in the Windows registry. Details about the object's class are stored. Classes are registered with a
#unique class ID and a friendly program ID, and program ID for an object is a short string that names the object
#and typically creates an instance of the object.
#python programs use the win32com.client.Dispatch()method to create COM objects from grogram ID.
#########################################################################
#########################################################################

class SAP2000Py():
    """---SAP2000 interface for python class---"""
    def __init__(self):
        self.SapObject=None
        self.SapModel = None

    def initializeNewModel(self,unitsTag=6):
        """
        ---initialize a new model---
        unitsTag:default=6 (kN_m_C)
        lb_in_F=1,lb_ft_F=2,kip_in_F=3,kip_ft_F=4,kN_mm_C=5,kN_m_C=6,kgf_mm_C=7,kgf_m_C=8
        N_mm_C=9,N_m_C=10,Ton_mm_C=11,Ton_m_C=12,kN_cm_C=13,kgf_cm_C=14,N_cm_C=15,Ton_cm_C=16
        """
        self.SapObject = win32com.client.Dispatch("CSI.SAP2000.API.SapObject")  # create SAP2000 object
        self.SapObject.ApplicationStart()  # start a SAP2000 program
        self.SapModel = self.SapObject.SapModel  # create SAP2000 model object
        self.SapModel.InitializeNewModel(unitsTag)#Clears the previous model and initializes a new model

    def newBlank(self):
        """
        ---create a new blank model---
        """
        self.SapModel.File.NewBlank()

    def closeModel(self):
        """
        ---close SAP2000 model---
        """
        # close SAP2000 model
        self.SapObject.ApplicationExit(True) #True means save the model before close,False otherwise.
        self.SapModel=0 # release the memory
        self.SapObject=0 # release the memory

    def changeUnits(self,unitsTag=6):
        """
        ---change the units of the current sap2000 model---
        unitsTag:default value is 6 (kN_m_C)
        lb_in_F=1,lb_ft_F=2,kip_in_F=3,kip_ft_F=4,kN_mm_C=5,kN_m_C=6,kgf_mm_C=7,kgf_m_C=8
        N_mm_C=9,N_m_C=10,Ton_mm_C=11,Ton_m_C=12,kN_cm_C=13,kgf_cm_C=14,N_cm_C=15,Ton_cm_C=16
        """
        self.SapModel.SetPresentUnits(unitsTag)

    def getUnits(self):
        """
        ---get the units number of the current sap2000 model---
        lb_in_F=1,lb_ft_F=2,kip_in_F=3,kip_ft_F=4,kN_mm_C=5,kN_m_C=6,kgf_mm_C=7,kgf_m_C=8
        N_mm_C=9,N_m_C=10,Ton_mm_C=11,Ton_m_C=12,kN_cm_C=13,kgf_cm_C=14,N_cm_C=15,Ton_cm_C=16
        """
        unitDict={1:"lb_in_F=1",2:"lb_ft_F=2",3:"kip_in_F=3",4:"kip_ft_F=4",5:"kN_mm_C=5",
                  6:"kN_m_C=6",7:"kgf_mm_C=7",8:"kgf_m_C=8",9:"N_mm_C=9",10:"N_m_C=10",
                  11:"Ton_mm_C=11",12:"Ton_m_C=12",13:"kN_cm_C=13",14:"kgf_cm_C=14",
                  15:"N_cm_C=15",16:"Ton_cm_C=16"}
        sapUnitsNum=self.SapModel.GetDatabaseUnits()
        sapUnitStr=unitDict[sapUnitsNum]
        print("The current model unit is:",sapUnitStr)
        return sapUnitStr

    def setUnits(self,unitsTag):
        """
        ---set units for the current sap2000 model---
        unitsTag:the number of the units
        lb_in_F=1,lb_ft_F=2,kip_in_F=3,kip_ft_F=4,kN_mm_C=5,kN_m_C=6,kgf_mm_C=7,kgf_m_C=8
        N_mm_C=9,N_m_C=10,Ton_mm_C=11,Ton_m_C=12,kN_cm_C=13,kgf_cm_C=14,N_cm_C=15,Ton_cm_C=16
        """
        self.SapModel.SetPresentUnits(unitsTag)

    def getFileName(self):
        """
        ---get the file name of the current model---
        """
        fileNameStr=self.SapModel.GetModelFilename()
        print("The current model file name is:",fileNameStr)
        return fileNameStr

    def getCoordSystem(self):
        """
        ---get the name of the present coordinate system---
        """
        currentCoordSysName = self.SapModel.GetPresentCoordSystem()
        print("The current coordinate system is:",currentCoordSysName)
        return currentCoordSysName

    def defineCoordSystem(self,cSysName,locRotList):
        """
        ---define new coordinate system---
        cSysName: name of the defined coordinate system,string
        locRotList: original location and rotation list in GLOBAL system, [locX,locY,locZ,rotZ,rotY,rotX]
        """
        x,y,z,rz,ry,rx=locRotList
        self.SapModel.CoordSys.SetCoordSys(cSysName,x,y,z,rz,ry,rx)

    def SetPresentCoordSystem(self,cSysName):
        """
        ---set the current coordinate system---
        cSysName: name of the coordinate system,string
        """
        self.SapModel.SetPresentCoordSystem(cSysName)

    def getSapVersion(self):
        """
        ---get the current SAP2000 program version---
        """
        currentVersion=self.SapModel.GetVersion()
        print("The current SAP2000 program version is:",currentVersion[1])
        return currentVersion[1]

    def getProjectInfo(self):
        """
        ---get the project information ---
        """
        projectInfo=self.SapModel.GetProjectInfo()
        print(projectInfo)

    def file_New2DFrame(self,TempType,NumberStorys,StoryHeight,NumberBays,BayWidth,Restraint=True,
                        Beam="Default",Column="Default",Brace="Default"):
        """
        ---Do not use this function to add to an existing model. This function should be used only for creating a new
         model and typically would be preceded by calls to ApplicationStart or InitializeNewModel.The function returns
         zero if the new 2D frame model is successfully created, otherwise it returns a nonzero value.---
        inputs:
        TempType(int)-One of the following 2D frame template types in the e2DFrameType enumeration.
            PortalFrame = 0,ConcentricBraced = 1,EccentricBraced = 2
        NumberStorys(int)-The number of stories in the frame.
        StoryHeight(float)-The height of each story. [L]
        NumberBays(int)-The number of bays in the frame.
        BayWidth(float)-The width of each bay. [L]
        Restraint(bool)-Joint restraints are provided at the base of the frame when this item is True.
        Beam(str)-The frame section property used for all beams in the frame. This must either be Default or
            the name of a defined frame section property.
        Column(str)-The frame section property used for all columns in the frame. This must either be Default
            or the name of a defined frame section property.
        Brace(str)-The frame section property used for all braces in the frame. This must either be Default or the
            name of a defined frame section property. This item does not apply to the portal frame.
        """
        self.SapModel.File.New2DFrame(TempType,NumberStorys,StoryHeight,NumberBays,BayWidth,Restraint,Beam,Column,Brace)

    def file_NewWall(self,NumberXDivisions,DivisionWidthX,NumberZDivisions,DivisionWidthZ,Restraint=True,Area="Default"):
        """
        ---Do not use this function to add to an existing model. This function should be used only for creating a new
        model and typically would be preceded by calls to ApplicationStart or InitializeNewModel.
        ---
        inputs:
        NumberXDivisions(int)-The number of area objects in the global X direction of the wall.
        DivisionWidthX(float)-The width of each area object measured in the global X direction. [L]
        NumberZDivisions(int)-The number of area objects in the global Z direction of the wall
        DivisionWidthZ(float)-The height of each area object measured in the global Z direction. [L]
        Restraint(bool)-Joint restraints are provided at the base of the wall when this item is True.
        Area(str)-The shell section property used for the wall. This must either be Default or the name of
            a defined shell section property.
        """
        self.SapModel.File.NewWall(NumberXDivisions,DivisionWidthX,NumberZDivisions,DivisionWidthZ,Restraint,Area)

    def file_New3DFrame(self,TempType,NumberStorys,StoryHeight,NumberBayX,BayWidthX,NumberBaysY,BayWidthY,
                        Restraint=True,Beam="Default",Column="Default",Area="Default",NumberXDivisions=4,NumberYDivisions=4):
        """
        ---Do not use this function to add to an existing model. This function should be used only for creating a
        new model and typically would be preceded by calls to ApplicationStart or InitializeNewModel
        ---
        inputs:
        TempType(int)-One of the following 3D frame template types in the e3DFrameType enumeration.
            OpenFrame = 0,PerimeterFrame = 1,BeamSlab = 2,FlatPlate = 3
        NumberStorys(int)-The number of stories in the frame
        StoryHeight(float)-The height of each story. [L]
        NumberBayX(int)-The number of bays in the global X direction of the frame.
        BayWidthX(float)-The width of each bay in the global X direction of the frame. [L]
        NumberBayY(int)-The number of bays in the global Y direction of the frame
        BayWidthY(float)-The width of each bay in the global Y direction of the frame. [L]
        Restraint(bool)-Joint restraints are provided at the base of the frame when this item is True
        Beam(str)-The frame section property used for all beams in the frame. This must either be Default or
            the name of a defined frame section property
        Column(str)-The frame section property used for all columns in the frame. This must either be Default or
            the name of a defined frame section property
        Area(str)-The shell section property used for all floor slabs in the frame. This must either be Default or the
            name of a defined shell section property. This item does not apply to the open and perimeter frames
        NumberXDivisions(int)-The number of divisions for each floor area object in the global X direction. This
            item does not apply to the open and perimeter frames
        NumberYDivisions(int)-The number of divisions for each floor area object in the global Y direction. This
            item does not apply to the open and perimeter frames
        """
        self.SapModel.File.New3DFrame(TempType,NumberStorys,StoryHeight,NumberBayX,BayWidthX,NumberBaysY,BayWidthY,
                        Restraint,Beam,Column,Area,NumberXDivisions,NumberYDivisions)

    def file_NewSolidBlock(self,XWidth,YWidth,Height,Restraint=True,Solid="Default",NumberXDivisions=5,
                           NumberYDivisions=8,NumberZDivisions=10):
        """
        ---The function returns zero if the new solid block model is successfully created, otherwise it returns a nonzero value---
        inputs:
        XWidth(float)-The total width of the solid block measured in the global X direction. [L]
        YWidth(float)-The total width of the solid block measured in the global Y direction. [L]
        Height(float)-The total height of the solid block measured in the global Z direction. [L]
        Restraint(bool)-Joint restraints are provided at the base of the solid block when this item is True
        Solid(str)-The solid property used for the solid block. This must either be Default or the name of a defined solid property
        NumberXDivisions(int)-The number of solid objects in the global X direction of the block
        NumberYDivisions(int)-The number of solid objects in the global Y direction of the block
        NumberZDivisions(int)-The number of solid objects in the global Z direction of the block
        """
        self.SapModel.File.NewSolidBlock(XWidth,YWidth,Height,Restraint,Solid,NumberXDivisions,
                           NumberYDivisions,NumberZDivisions)

    def file_Save(self,FileName):
        """
        ---If a file name is specified, it should have an .sdb extension. If no file name is specified, the file
        is saved using its current name.If there is no current name for the file (the file has not been saved
        previously) and this function is called with no file name specified, an error will be returned.This function
        returns zero if the file is successfully saved and nonzero if it is not saved
        ---
        inputs:
        FileName(str)-The full path to which the model file is saved
        """
        self.SapModel.File.Save(FileName) #eg."C:\SapAPI\x.sdb"

    def file_OpenFile(self,FileName):
        """
        ---This function opens an existing Sap2000 file. The file name must have an sdb, $2k, s2k, xlsx, xls, or
        mdb extension. Files with sdb extensions are opened as standard Sap2000 files. Files with $2k and s2k
        extensions are imported as text files. Files with xlsx and xls extensions are imported as Microsoft Excel
        files. Files with mdb extensions are imported as Microsoft Access files
        ---
        inputs:
        FileName(str)-The full path of a model file to be opened in the Sap2000 application
        """
        self.SapModel.File.OpenFile(FileName)


    def define_material_SetSSCurve(self,matName,strainList,stressList):
        """
        ---sets the material stress-strain curve for existing material ---
        inputs:
        matName(str)-the name of the defined material
        strainList(float)-This is an array that includes the strain at each point on the
                        stress strain curve. The strains must increase monotonically.
        stressList(flaot)-This is an array that includes the stress at each point on
                        the stress strain curve. [F/L2]
        Points that have a negative strain must have a zero or negative stress. Similarly,
        points that have a positive strain must have a zero or positive stress.
        There must be one point defined that has zero strain and zero stress.
        """
        numPoint=len(strainList)
        pointID=[i1 for i1 in range(numPoint)]
        self.SapModel.PropMaterial.SetSSCurve(matName,numPoint,pointID,strainList,stressList)

    def define_material_TendonUser(self,tendonName,weightPerV,E,temC):
        """
        ---user defined unixial tendon material  ---
        inputs:
        tendonName(str)-the name of the tendon material
        weightPerV(float)-The weight per unit volume for the material. [F/L3]
        E(float)-The modulus of elasticity. [F/L2]
        tempC(float)-The modulus of elasticity. [F/L2]
        """
        self.SapModel.PropMaterial.SetMaterial(tendonName,7) #eMatType_Tendon = 7
        self.SapModel.PropMaterial.SetWeightAndMass(tendonName, 1,weightPerV)#1 = Weight per unit volume
        self.SapModel.PropMaterial.SetMPUniaxial(tendonName,E,temC)

    def define_material_AddMaterial(self,name,matType,region,standard,grade):
        """
        ---adds a new standard material property to the model---
        name(str)-the name of the added material
        matType(int)-the material type number.eMatType_Steel = 1,eMatType_Concrete = 2,eMatType_NoDesign = 3
                    eMatType_Aluminum = 4,eMatType_ColdFormed = 5,eMatType_Rebar = 6,eMatType_Tendon = 7
        region(str)-different countries or user ["China","Europe","India","Italy","New Zealand","Russia",
                    "Spain","United States","Vietnam","User"]
        standard(str)-the standard name, for China it includes ["GB","JTG","TB","User"]
        grade(str)-the grade name of the material property, For China steel JTG--["GB/T 714-2008 Q345q",--235--,
                    --370--,--420--,--460--,--500--,--550--,--620--,--690--]
                    For China Concrete JTG--["JTG D62-2004 C15",--20--,--25--,--30--,...,--80--]
        """
        self.SapModel.PropMaterial.AddMaterial(name,matType,region,standard,grade)
        str_list = grade.split(" ")
        nameList=standard+"-"+str_list[-1]
        self.SapModel.PropMaterial.ChangeName(nameList,name)

    def define_material_GetMPIsotropic(self,matName):
        """
        ---get the the mechanical properties for a material with an isotropic directional symmetry type---
        intput:
                matName(str)-the name of an existing material property
        return:[weightPerV,massPerV,E,v,tempC,G]
                weightPerV-The weight per unit volume for the material. [F/L3]
                massPerV-The mass per unit volume for the material. [M/L3]
                E-The modulus of elasticity. [F/L2]
                v-Poisson’s ratio.
                tempC-The thermal coefficient. [1/T]
                G-The shear modulus. For isotropic materials this value is program calculated
                  from the modulus of elasticity and poisson’s ratio. [F/L2]
        """
        weightAndMass=self.SapModel.PropMaterial.GetWeightAndMass(matName)[1:]
        isoProperty=self.SapModel.PropMaterial.GetMPIsotropic(matName)[1:]
        weightPerV,massPerV=weightAndMass
        E,v,tempC,G=isoProperty
        returnMatPro=[weightPerV,massPerV,E,v,tempC,G]
        return returnMatPro

    def define_material_SetMatrial(self,matName,matType):
        """
        ---This function initializes a material property.---
        inputs:
                matName(str)-The name of an existing or new material property
                matType(int)-This is one of the following items in the eMatType enumeration
                eMatType_Steel = 1,eMatType_Concrete = 2,eMatType_NoDesign = 3
                eMatType_Aluminum = 4,eMatType_ColdFormed = 5,eMatType_Rebar = 6,eMatType_Tendon = 7
        """
        self.SapModel.PropMaterial.SetMaterial(matName,matType)

    def define_material_SetWeightAndMass(self,matName,weightPerV):
        """
        ---This function assigns weight per unit volume to a material property---
        inputs:
                matName(str)-The name of an existing material property.
                weightPerV(float)-This is the weight per unit volume,[F/L3]
        """
        # 1 = Weight per unit volume is specified,2 = Mass per unit volume is specified
        self.SapModel.PropMaterial.SetWeightAndMass(matName, 1,weightPerV)

    def define_material_SetMPIsotropic(self,matName,E,v,temC):
        """
        ---set the the mechanical properties for a material with an isotropic directional symmetry type---
        inputs: [matName,matType,weightPerV,massPerV,E,v,tempC,G]
                matName(str)-the name of the defined material
                E(float)-The modulus of elasticity. [F/L2]
                v(float)-Poisson’s ratio.
                tempC(float)-The thermal coefficient. [1/T]
        """
        self.SapModel.PropMaterial.SetMPIsotropic(matName,E,v,temC)

    def define_material_SetOSteel_1(self,matName,Fy,Fu,eFy,eFu,SSType,SSHysType=0,StrainAtHardening=0,
                                    StrainAtMaxStress=0,StrainAtRupture=0,FinalSlope=0):
        """
        ---This function sets the other material property data for steel materials---
        inputs:
                matName(str)-The name of an existing steel material property.
                Fy(flouat)-The minimum yield stress. [F/L2]
                Fu(float)-The minimum tensile stress. [F/L2]
                eFy(float)-The expected yield stress. [F/L2]
                eFu(float)-The expected tensile stress. [F/L2]
                SSType(int)-This is 0 or 1, indicating the stress-strain curve type.
                            0 = User defined,1 = Parametric - Simple
                SSHysType(int)-This is 0, 1 or 2, indicating the stress-strain hysteresis type.
                            0 = Elastic,1 = Kinematic,2 = Takeda
                StrainAtHardening(float)-This item applies only to parametric stress-strain curves.
                            It is the strain at the onset of strain hardening.
                StrainAtMaxStress(float)-This item applies only to parametric stress-strain curves.
                            It is the strain at maximum stress. This item must be larger than the
                            StrainAtHardening item.
                StrainAtRupture(float)-This item applies only to parametric stress-strain curves.
                            It is the strain at rupture. This item must be larger than the StrainAtMaxStress item
                FinalSlope(float)-This item applies only to parametric stress-strain curves. It is a multiplier on
                            the material modulus of elasticity, E. This value multiplied times E gives the final
                            slope of the curve.
        """
        self.SapModel.PropMaterial.SetOSteel_1(matName, Fy,Fu,eFy,eFu,SSType,SSHysType,StrainAtHardening,
                                    StrainAtMaxStress,StrainAtRupture,FinalSlope)

    def define_material_SetOConcrete_1(self,matName,fc,IsLightweight,fcsfactor,SSType,SSHysType=0,StrainAtfc=0,
                                       StrainUltimate=0,FinalSlope=0,FrictionAngle=0,DilatationalAngle=0):
        """
        ---This function sets the other material property data for concrete materials.---
        inputs:
        matName(str)-The name of an existing concrete material property.
        fc(float)-The concrete compressive strength. [F/L2]
        IsLightweight(bool)-If this item is True, the concrete is assumed to be lightweight concrete.
        fcsfactor(float)-The shear strength reduction factor for lightweight concrete.
        SSType(int)-This is 0, 1 or 2, indicating the stress-strain curve type. 0 = User defined,
            1 = Parametric - Simple,2 = Parametric - Mander
        SSHysType(int)-This is 0, 1 or 2, indicating the stress-strain hysteresis type.0 = Elastic
            1 = Kinematic,2 = Takeda
        StrainAtfc(float)-This item applies only to parametric stress-strain curves. It is the strain at
            the unconfined compressive strength.
        StrainUltimate(float)-This item applies only to parametric stress-strain curves. It is the ultimate
            unconfined strain capacity. This item must be larger than the StrainAtfc item
        FinalSlope(float)-This item applies only to parametric stress-strain curves. It is a multiplier on
            the material modulus of elasticity, E. This value multiplied times E gives the final slope on the
            compression side of the curve.
        FrictionAngle(float)-The Drucker-Prager friction angle, 0 <= FrictionAngle < 90. [deg]
        DilatationalAngle(float)-The Drucker-Prager dilatational angle, 0 <= DilatationalAngle < 90. [deg]
        """
        self.SapModel.PropMaterial.SetOConcrete_1(matName,fc,IsLightweight,fcsfactor,SSType,SSHysType,StrainAtfc,
                                       StrainUltimate,FinalSlope,FrictionAngle,DilatationalAngle)

    def define_material_SetORebar_1(self,matName,Fy,Fu,eFy,eFu,SSType,SSHysType=0,StrainAtHardening=0,
                                    StrainUltimate=0,FinalSlope=0,UseCaltransSSDefaults=False):
        """
        ---This function sets the other material property data for rebar materials..---
        inputs:
        matName(str)-The name of an existing rebar material property.
        Fy(float)-The minimum yield stress. [F/L2]
        Fu(float)-The minimum tensile stress. [F/L2]
        eFy(float)_The expected yield stress. [F/L2]
        eFu(float)-The expected tensile stress. [F/L2]
        SSType(int)-This is 0, 1 or 2, indicating the stress-strain curve type.0 = User defined
            1 = Parametric - Simple,2 = Parametric - Park
        SSHysType(int)-This is 0, 1 or 2, indicating the stress-strain hysteresis type.0 = Elastic
            1 = Kinematic,2 = Takeda
        StrainAtHardening(float)-This item applies only when parametric stress-strain curves are used and
            when UseCaltransSSDefaults is False. It is the strain at the onset of strain hardening
        StrainUltimate(float)-This item applies only when parametric stress-strain curves are used and when
            UseCaltransSSDefaults is False. It is the ultimate strain capacity. This item must be larger than the
            StrainAtHardening item.
        FinalSlope(float)-This item applies only to parametric stress-strain curves. It is a multiplier on the
            material modulus of elasticity, E. This value multiplied times E gives the final slope of the curve.
        UseCaltransSSDefaults(bool)-If this item is True, the program uses Caltrans default controlling strain
            values, which are bar size dependent.
        """
        self.SapModel.PropMaterial.SetORebar_1(matName,Fy,Fu,eFy,eFu,SSType,SSHysType,StrainAtHardening,
                                    StrainUltimate,FinalSlope,UseCaltransSSDefaults)

    def define_material_SetOTendon_1(self,matName,Fy,Fu,SSType,SSHysType=1,FinalSlope=1):
        """
        ---This function sets the other material property data for tendon materials---
        inputs:
        matName(str)-The name of an existing tendon material property.
        Fy(float)-The minimum yield stress. [F/L2]
        Fu(float)-The minimum tensile stress. [F/L2]
        SSType(int)-This is 0, 1 or 2, indicating the stress-strain curve type.0 = User defined
            1 = Parametric – 250 ksi strand,2 = Parametric – 270 ksi strand
        SSHysType(int)-This is 0, 1 or 2, indicating the stress-strain hysteresis type.0 = Elastic
            1 = Kinematic,2 = Takeda
        FinalSlope(float)-This item applies only to parametric stress-strain curves. It is a multiplier
            on the material modulus of elasticity, E. This value multiplied times E gives the final slope of the curve.
        """
        self.SapModel.PropMaterial.SetOTendon_1(matName,Fy,Fu,SSType,SSHysType,FinalSlope)

    def define_section_PropFrame_SetGeneral(self,sectName,matName,Area,As2,As3,I22,I33,J):
        """
        ---set a general frame section property---
        intput:
        sectName(str)-the name of the defined sections
        matName(str)-the name of the material used for current section
        Area(float)-The cross-sectional area. [L2]
        As2(float)-The shear area for forces in the section local 2-axis direction. [L2]
        As3(float)-The shear area for forces in the section local 3-axis direction. [L2]
        I22(float)-The moment of inertia for bending about the local 2 axis. [L4]
        I33(float)-The moment of inertia for bending about the local 3 axis. [L4]
        J(float)-The torsional constant. [L4]
        """
        self.SapModel.PropFrame.SetGeneral(sectName,matName,1,1,Area,As2,As3,J,I22,I33,1,1,1,1,1,1)

    def define_section_Tendon_SetProp(self,tendonName,matName,modelOpt,Area):
        """
        ---set a tendon property---
        inputs:
        tendonName-The name of new tendon property
        matName-The name of the material property assigned to the tendon property.
        modelOpt-1 = Model tendon as loads,2 = Model tendon as elements
        area-The cross-sectional area of the tendon. [L2]
        """
        self.SapModel.PropTendon.SetProp(tendonName,matName,modelOpt,Area)

    def define_section_Cable_SetPro(self,cableName,matName,Area):
        """
        ---set a cable property---
        intputs:
        cableName(str)-The name of  new cable property
        matName(str)-The name of the material property assigned to the cable property
        Area(float)-The cross-sectional area of the tendon. [L2]
        """
        self.SapModel.PropCable.SetProp(cableName,matName,Area)

    def define_section_Area_SetPlane(self,areaName,MyType,MatProp,Thickness,MatAng=0,Incompatible=True):
        """
        ---This function initializes a plane-type area property. If this function is called for an existing area
        property, all items for the property are reset to their default value.---
        inputs:
        areaName(str)-The name of an existing or new area property. If this is an existing property,
                that property is modified; otherwise, a new property is added.
        MyType(int)-This is either 1 or 2, indicating the plane type.1 = Plane-stress,2 = Plane-strain
        MatProp(str)-The name of the material property for the area property.
        MatAng(float)-The material angle. [deg]
        Thickness(float)-The plane thickness. [L]
        Incompatible(bool)-If this item is True, incompatible bending modes are included in the stiffness
            formulation. In general, incompatible modes significantly improve the bending behavior of the object.
        """
        self.SapModel.PropArea.SetPlane(areaName,MyType,MatProp,MatAng,Thickness,Incompatible)

    def define_section_Area_SetShell_1(self,name,ShellType,MatProp,Thickness,matAng=0):
        """
        ---This function initializes a shell-type area property. If this function is called for an existing
        area property, all items for the property are reset to their default value---
        inputs:
        name(str)-The name of an existing or new area property. If this is an existing property, that
            property is modified; otherwise, a new property is added.
        ShellType(int)-This is 1, 2, 3, 4, 5 or 6, indicating the shell type.1 = Shell - thin,2 = Shell - thick
            3 = Plate - thin,4 = Plate - thick,5 = Membrane6 = Shell layered/nonlinear
        MatProp(str)-The name of the material property for the area property. This item does not apply when
            ShellType = 6.
        Thickness(float)-The membrane thickness. [L],This item does not apply when ShellType = 6.
        matAng(float)-The material angle. [deg] This item does not apply when ShellType = 6.
        """
        self.SapModel.PropArea.SetShell_1(name,ShellType,False,MatProp,matAng,Thickness,Thickness)

    def define_section_PropSolid_SetProp(self,name,matProp,a=0,b=0,c=0,incompatible=True):
        """
        ---This function defines a solid property---
        inputs:
        name(str)-The name of an existing or new solid property. If this is an existing property, that property
            is modified; otherwise, a new property is added
        MatProp(str)-The name of the material property assigned to the solid property.
        a,b,c(float)-The material angle A,B,C [deg]
        incompatible(bool)-If this item is True, incompatible bending modes are included in the stiffness
            formulation. In general, incompatible modes significantly improve the bending behavior of the object.
        """
        self.SapModel.PropSolid.SetProp(name,matProp,a,b,c,incompatible)

    def define_section_PropLink_SetLinear(self,name,DOF,Fixed,Ke={},Ce={},dj2=0,dj3=0,KeCoupled=False,CeCoupled=False):
        """
        ---This function initializes a linear-type link property. If this function is called for
        an existing link property, all items for the property are reset to their default value.---
        inputs:
        name(str)-The name of an existing or new link property. If this is an existing property,
            that property is modified; otherwise, a new property is added.
        DOF(list)-This is str list,indicating if properties exist for a specified degree of freedom.e.g. ["U1"]
        Fixed(list)-This is str list, indicating if the specified degree of freedom is fixed (restrained).e.g. ["R1"]
        Ke(dict)-This is a dictionary of stiffness terms for the link property,
            e.g., uncouple:{"U1":2000,"R1":5000},coupled: {"U1R2":400}
        Ce(dict)-This is a dictionary of damping terms for the link property,
            e.g., uncouple:{"U1":0.03,"R1":0.05},coupled: {"U1R2":0.05}
        dj2(float)-The distance from the J-End of the link to the U2 shear spring.
            This item applies only when DOF(1) = True. [L]
        dj3(float)-The distance from the J-End of the link to the U3 shear spring.
            This item applies only when DOF(2) = True. [L]
        KeCoupled(bool)-This item is True if the link stiffness, Ke, is coupled.
        CeCoupled(bool)-This item is True if the link damping, Ce, is coupled.
        """
        DOFDict={"U1":0,"U2":1,"U3":2,"R1":3,"R2":4,"R3":5}
        DOFFinal=[False,False,False,False,False,False]
        for each in DOF:
            indexNum=DOFDict[each]
            DOFFinal[indexNum]=True
        FixedFinal = [False, False, False, False, False, False]
        for each1 in Fixed:
            indexNum1=DOFDict[each1]
            FixedFinal[indexNum1]=True
        keDict={"U1":0,"U2":1,"U3":2,"R1":3,"R2":4,"R3":5}
        keCoupleDict={"U1U1":0,"U1U2":1,"U2U2":2,"U1U3":3,"U2U3":4,"U3U3":5,"U1R1":6,
                      "U2R1":7,"U3R1":8,"R1R1":9,"U1R2":10,"U2R2":11,"U3R2":12,"R1R2":13,
                      "R2R2":14,"U1R3":15,"U2R3":16,"U3R3":17,"R1R3":18,"R2R3":19,"R3R3":20}
        keFinal=[0 for each in range(6)]
        keCouple=[0 for each in range(21)]
        if not KeCoupled:
            keInput=keFinal
            key2=Ke.keys()
            for each2 in key2:
                indexNum2=keDict[each2]
                keInput[indexNum2]=Ke[each2]
        else:
            keInput = keCouple
            key3 = Ke.keys()
            for each3 in key3:
                indexNum3=keCoupleDict[each3]
                keInput[indexNum3]=Ke[each3]
        ceFinal = [0 for each in range(6)]
        ceCouple = [0 for each in range(21)]
        if not CeCoupled:
            ceInput=ceFinal
            key4=Ce.keys()
            for each4 in key4:
                indexNum4=keDict[each4]
                ceInput[indexNum4]=Ce[each4]
        else:
            ceInput = ceCouple
            key5 = Ce.keys()
            for each5 in key5:
                indexNum5=keCoupleDict[each5]
                ceInput[indexNum5]=Ce[each5]
        self.SapModel.PropLink.SetLinear(name,DOFFinal,FixedFinal,keInput,ceInput,dj2,dj3,KeCoupled,CeCoupled)

    def define_section_PropLink_SetMultiLinearElastic(self,name,DOF,Fixed,Nonlinear,Ke={},Ce={},dj2=0,dj3=0):
        """
        ---This function initializes a multilinear elastic-type link property. If this function is called for an
        existing link property, all items for the property are reset to their default value.---
        inputs:
        name(str)-The name of an existing or new link property. If this is an existing property then.
            that property is modified; otherwise, a new property is added.
        DOF(list)-This is str list,indicating if properties exist for a specified degree of freedom.e.g. ["U1"]
        Fixed(list)-This is str list, indicating if the specified degree of freedom is fixed (restrained).e.g. ["R1"]
        Nonlinear(list)-This is str list, indicating if nonlinear properties exist for a specified degree of freedom.
            e.g. ["R1"]
        Ke(dict)-This is a dictionary of stiffness terms for the link property,e.g.,{"U1":2000,"R1":5000}
        Ce(dict)-This is a dictionary of damping terms for the link property,e.g.,{"U1":0.03,"R1":0.05}
        dj2(float)-The distance from the J-End of the link to the U2 shear spring.
            This item applies only when DOF(1) = True. [L]
        dj3(float)-The distance from the J-End of the link to the U3 shear spring.
            This item applies only when DOF(2) = True. [L]
        """
        DOFDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        DOFFinal = [False, False, False, False, False, False]
        for each in DOF:
            indexNum = DOFDict[each]
            DOFFinal[indexNum] = True
        FixedFinal = [False, False, False, False, False, False]
        for each1 in Fixed:
            indexNum1 = DOFDict[each1]
            FixedFinal[indexNum1] = True
        nonlinearFinal = [False, False, False, False, False, False]
        for each2 in Nonlinear:
            indexNum2=DOFDict[each2]
            nonlinearFinal[indexNum2]=True
        keDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        keInput = [0 for each in range(6)]
        key2 = Ke.keys()
        for each2 in key2:
            indexNum2 = keDict[each2]
            keInput[indexNum2] = Ke[each2]
        ceInput = [0 for each in range(6)]
        key3 = Ce.keys()
        for each3 in key3:
            indexNum3 = keDict[each3]
            ceInput[indexNum3] = Ce[each3]
        self.SapModel.PropLink.SetMultiLinearElastic(name,DOFFinal,FixedFinal,nonlinearFinal,keInput,ceInput,dj2,dj3)

    def define_section_PropLink_SetMultiLinearPoints(self,name,DOF,forceList,dispList,myType=0,
                                                     a1=0,a2=0,b1=0,b2=0,eta=0):
        """
        ---This function sets the force-deformation data for a specified degree of freedom in multilinear
        elastic and multilinear plastic link properties.---
        inputs:
        name(str)-The name of an existing multilinear elastic or multilinear plastic link property.
        DOF(int)-This is 1, 2, 3, 4, 5 or 6, indicating the degree of freedom to which the multilinear points apply.
            1 = U1,2 = U2,3 = U3,4 = R1,5 = R2,6 = R3
        forceList(float list)-that includes the force at each point. When DOF is U1, U2 or U3, this is a force.
            When DOF is R1, R2 or R3. this is a moment. [F] if DOF <= 3, and [FL} if DOF > 3
        dispList(float list)-that includes the displacement at each point. When DOF is U1, U2 or U3, this is
            a translation. When DOF is R1, R2 or R3, this is a rotation. [L] if DOF <= 3, and [rad] if DOF > 3
        myType(int)-This item applies only to multilinear plastic link properties. It is 1, 2 or 3, indicating
            the hysteresis type.0=Isotropic,1 = Kinematic,2 = Takeda,3 = Pivot
        a1,a2,b1,b2,eta(float)-This item applies only to multilinear plastic link properties that have a pivot
        hysteresis type (MyType = 3).
        """
        numberPoints=len(forceList)
        self.SapModel.PropLink.SetMultiLinearPoints(name,DOF,numberPoints,forceList,dispList,myType,
                                                    a1,a2,b1,b2,eta)

    def define_material_PropLink_SetMultiLinearPlastic(self,name,DOF,Fixed,Nonlinear,Ke={},Ce={},dj2=0,dj3=0):
        """
        ---This function initializes a multilinear plastic-type link property. If this function is
        called for an existing link property, all items for the property are reset to their default values.---
        inputs:
        name(str)-The name of an existing or new link property. If this is an existing property,
            that property is modified; otherwise, a new property is added.
         DOF(list)-This is str list,indicating if properties exist for a specified degree of freedom.e.g. ["U1"]
        Fixed(list)-This is str list, indicating if the specified degree of freedom is fixed (restrained).e.g. ["R1"]
        Nonlinear(list)-This is str list, indicating if nonlinear properties exist for a specified degree of freedom.
            e.g. ["R1"]
        Ke(dict)-This is a dictionary of stiffness terms for the link property,e.g.,{"U1":2000,"R1":5000}
        Ce(dict)-This is a dictionary of damping terms for the link property,e.g.,{"U1":0.03,"R1":0.05}
        dj2(float)-The distance from the J-End of the link to the U2 shear spring.
            This item applies only when DOF(1) = True. [L]
        dj3(float)-The distance from the J-End of the link to the U3 shear spring.
            This item applies only when DOF(2) = True. [L]
        """
        DOFDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        DOFFinal = [False, False, False, False, False, False]
        for each in DOF:
            indexNum = DOFDict[each]
            DOFFinal[indexNum] = True
        FixedFinal = [False, False, False, False, False, False]
        for each1 in Fixed:
            indexNum1 = DOFDict[each1]
            FixedFinal[indexNum1] = True
        nonlinearFinal = [False, False, False, False, False, False]
        for each2 in Nonlinear:
            indexNum2 = DOFDict[each2]
            nonlinearFinal[indexNum2] = True
        keDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        keInput = [0 for each in range(6)]
        key2 = Ke.keys()
        for each2 in key2:
            indexNum2 = keDict[each2]
            keInput[indexNum2] = Ke[each2]
        ceInput = [0 for each in range(6)]
        key3 = Ce.keys()
        for each3 in key3:
            indexNum3 = keDict[each3]
            ceInput[indexNum3] = Ce[each3]
        self.SapModel.PropLink.SetMultiLinearPlastic(name,DOFFinal,FixedFinal,nonlinearFinal,keInput,ceInput,dj2,dj3)

    def define_section_PropLink_SetDamper(self,name,DOF,Fixed,Nonliear,Ke={},Ce={},k={},c={},cexp={},dj2=0,dj3=0):
        """
        ---This function initializes an exponential damper-type link property---
        inputs:
        name(str)-The name of an existing or new link property. If this is an existing property, that property
            is modified; otherwise, a new property is added.
        DOF(list)-This is str list,indicating if properties exist for a specified degree of freedom.e.g. ["U1"]
        Fixed(list)-This is str list, indicating if the specified degree of freedom is fixed (restrained).e.g. ["R1"]
        Nonlinear(list)-This is str list, indicating if nonlinear properties exist for a specified degree of freedom.
            e.g. ["R1"]
        Ke(dict)-This is a dictionary of stiffness terms for the link property,e.g.,{"U1":2000,"R1":5000}
        Ce(dict)-This is a dictionary of damping terms for the link property,e.g.,{"U1":0.03,"R1":0.05}
        k(dict)-The initial stiffness applies for nonlinear analyses.e.g.,{"U1":10000}
        c(dict)-The nonlinear damping coefficient applies for nonlinear analyses.{"U1":2000}
        cexp(dict)-The nonlinear damping exponent applies for nonlinear analyses. It is applied to the velocity
            across the damper in the equation of motion.{"U1":0.3}
        dj2(float)-The distance from the J-End of the link to the U2 shear spring.
            This item applies only when DOF(1) = True. [L]
        dj3(float)-The distance from the J-End of the link to the U3 shear spring.
            This item applies only when DOF(2) = True. [L]
        """
        DOFDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        DOFFinal = [False, False, False, False, False, False]
        for each in DOF:
            indexNum = DOFDict[each]
            DOFFinal[indexNum] = True
        FixedFinal = [False, False, False, False, False, False]
        for each1 in Fixed:
            indexNum1 = DOFDict[each1]
            FixedFinal[indexNum1] = True
        nonlinearFinal = [False, False, False, False, False, False]
        for each2 in Nonliear:
            indexNum2 = DOFDict[each2]
            nonlinearFinal[indexNum2] = True
        keDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        keInput = [0 for each in range(6)]
        key2 = Ke.keys()
        for each2 in key2:
            indexNum2 = keDict[each2]
            keInput[indexNum2] = Ke[each2]
        ceInput = [0 for each in range(6)]
        key3 = Ce.keys()
        for each3 in key3:
            indexNum3 = keDict[each3]
            ceInput[indexNum3] = Ce[each3]
        kInput=[0 for each in range(6)]
        key4=k.keys()
        for each4 in key4:
            indexNum4 = keDict[each4]
            kInput[indexNum4] = k[each4]
        cInput = [0 for each in range(6)]
        key5 = c.keys()
        for each5 in key5:
            indexNum5 = keDict[each5]
            cInput[indexNum5] = c[each5]
        cexpInput = [0 for each in range(6)]
        key6 = cexp.keys()
        for each6 in key6:
            indexNum6 = keDict[each6]
            cexpInput[indexNum6] = cexp[each6]
        self.SapModel.PropLink.SetDamper(name,DOFFinal,FixedFinal,nonlinearFinal,keInput,ceInput,kInput,cInput,
                                         cexpInput,dj2,dj3)

    def define_section_PropLink_SetDamperBilinear(self,name,DOF,Fixed,Nonliear,Ke={},Ce={},k={},c={},
                                                  cy={},ForceLimit={},dj2=0,dj3=0):
        """
        ---This function initializes a bilinear damper-type link property---
        inputs:
        name(str)-The name of an existing or new link property. If this is an existing property, that property
            is modified; otherwise, a new property is added.
        DOF(list)-This is str list,indicating if properties exist for a specified degree of freedom.e.g. ["U1"]
        Fixed(list)-This is str list, indicating if the specified degree of freedom is fixed (restrained).e.g. ["R1"]
        Nonlinear(list)-This is str list, indicating if nonlinear properties exist for a specified degree of freedom.
            e.g. ["R1"]
        Ke(dict)-This is a dictionary of stiffness terms for the link property,e.g.,{"U1":2000,"R1":5000}
        Ce(dict)-This is a dictionary of damping terms for the link property,e.g.,{"U1":0.03,"R1":0.05}
        k(dict)-The initial stiffness applies for nonlinear analyses.e.g.,{"U1":10000}
        c(dict)-The nonlinear initial damping coefficient applies for nonlinear analyses.{"U1":2000}
        cy(dict)-The nonlinear yielded damping coefficient applies for nonlinear analyses.
        ForceLimit(dict)-nonlinear linear force limit terms for the link property. The linear force limit
            applies for nonlinear analyses.
        dj2(float)-The distance from the J-End of the link to the U2 shear spring.
            This item applies only when DOF(1) = True. [L]
        dj3(float)-The distance from the J-End of the link to the U3 shear spring.
            This item applies only when DOF(2) = True. [L]
        """
        DOFDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        DOFFinal = [False, False, False, False, False, False]
        for each in DOF:
            indexNum = DOFDict[each]
            DOFFinal[indexNum] = True
        FixedFinal = [False, False, False, False, False, False]
        for each1 in Fixed:
            indexNum1 = DOFDict[each1]
            FixedFinal[indexNum1] = True
        nonlinearFinal = [False, False, False, False, False, False]
        for each2 in Nonliear:
            indexNum2 = DOFDict[each2]
            nonlinearFinal[indexNum2] = True
        keDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        keInput = [0 for each in range(6)]
        key2 = Ke.keys()
        for each2 in key2:
            indexNum2 = keDict[each2]
            keInput[indexNum2] = Ke[each2]
        ceInput = [0 for each in range(6)]
        key3 = Ce.keys()
        for each3 in key3:
            indexNum3 = keDict[each3]
            ceInput[indexNum3] = Ce[each3]
        kInput = [0 for each in range(6)]
        key4 = k.keys()
        for each4 in key4:
            indexNum4 = keDict[each4]
            kInput[indexNum4] = k[each4]
        cInput = [0 for each in range(6)]
        key5 = c.keys()
        for each5 in key5:
            indexNum5 = keDict[each5]
            cInput[indexNum5] = c[each5]
        cyInput = [0 for each in range(6)]
        key6 = cy.keys()
        for each6 in key6:
            indexNum6 = keDict[each6]
            cyInput[indexNum6] = cy[each6]
        forceLimitInput = [0 for each in range(6)]
        key7 = ForceLimit.keys()
        for each7 in key7:
            indexNum7 = keDict[each7]
            forceLimitInput[indexNum7] = ForceLimit[each7]
        self.SapModel.PropLink.SetDamperBilinear(name,DOFFinal,FixedFinal,nonlinearFinal,keInput,ceInput,kInput,cInput,
                                                 cyInput,forceLimitInput,dj2,dj3)

    def define_section_PropLink_SetGap(self,name,DOF,Fixed,NonLinear,Ke={},Ce={},k={},disp={},dj2=0,dj3=0):
        """
        ---This function initializes a gap-type link property---
        inputs:
        name(str)-The name of an existing or new link property
        DOF(list)-This is str list,indicating if properties exist for a specified degree of freedom.e.g. ["U1"]
        Fixed(list)-This is str list, indicating if the specified degree of freedom is fixed (restrained).e.g. ["R1"]
        Nonlinear(list)-This is str list, indicating if nonlinear properties exist for a specified degree of freedom.
            e.g. ["R1"]
        Ke(dict)-This is a dictionary of stiffness terms for the link property,e.g.,{"U1":2000,"R1":5000}
        Ce(dict)-This is a dictionary of damping terms for the link property,e.g.,{"U1":0.03,"R1":0.05}
        k(dict)-The initial stiffness applies for nonlinear analyses.e.g.,{"U1":10000}
        disp(dict)-initial gap opening terms for the link property. The initial gap opening applies
            for nonlinear analyses.{"U1":1.2}
        dj2(float)-The distance from the J-End of the link to the U2 shear spring.
            This item applies only when DOF(1) = True. [L]
        dj3(float)-The distance from the J-End of the link to the U3 shear spring.
            This item applies only when DOF(2) = True. [L]
        """
        DOFDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        DOFFinal = [False, False, False, False, False, False]
        for each in DOF:
            indexNum = DOFDict[each]
            DOFFinal[indexNum] = True
        FixedFinal = [False, False, False, False, False, False]
        for each1 in Fixed:
            indexNum1 = DOFDict[each1]
            FixedFinal[indexNum1] = True
        nonlinearFinal = [False, False, False, False, False, False]
        for each2 in NonLinear:
            indexNum2 = DOFDict[each2]
            nonlinearFinal[indexNum2] = True
        keDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        keInput = [0 for each in range(6)]
        key2 = Ke.keys()
        for each2 in key2:
            indexNum2 = keDict[each2]
            keInput[indexNum2] = Ke[each2]
        ceInput = [0 for each in range(6)]
        key3 = Ce.keys()
        for each3 in key3:
            indexNum3 = keDict[each3]
            ceInput[indexNum3] = Ce[each3]
        kInput = [0 for each in range(6)]
        key4 = k.keys()
        for each4 in key4:
            indexNum4 = keDict[each4]
            kInput[indexNum4] = k[each4]
        dispInput = [0 for each in range(6)]
        key5 = disp.keys()
        for each5 in key5:
            indexNum5 = keDict[each5]
            dispInput[indexNum5] = disp[each5]
        self.SapModel.PropLink.SetGap(name,DOFFinal,FixedFinal,nonlinearFinal,keInput,ceInput,kInput,dispInput,dj2,dj3)

    def define_section_PropLink_SetHook(self,name,DOF,Fixed,NonLinear,Ke={},Ce={},k={},disp={},dj2=0,dj3=0):
        """
        ---This function initializes a hook-type link property---
        inputs:
        name(str)-The name of an existing or new link property
        DOF(list)-This is str list,indicating if properties exist for a specified degree of freedom.e.g. ["U1"]
        Fixed(list)-This is str list, indicating if the specified degree of freedom is fixed (restrained).e.g. ["R1"]
        Nonlinear(list)-This is str list, indicating if nonlinear properties exist for a specified degree of freedom.
            e.g. ["R1"]
        Ke(dict)-This is a dictionary of stiffness terms for the link property,e.g.,{"U1":2000,"R1":5000}
        Ce(dict)-This is a dictionary of damping terms for the link property,e.g.,{"U1":0.03,"R1":0.05}
        k(dict)-The initial stiffness applies for nonlinear analyses.e.g.,{"U1":10000}
        disp(dict)-initial hook opening terms for the link property. The initial gap opening applies
            for nonlinear analyses.{"U1":1.2}
        dj2(float)-The distance from the J-End of the link to the U2 shear spring.
            This item applies only when DOF(1) = True. [L]
        dj3(float)-The distance from the J-End of the link to the U3 shear spring.
            This item applies only when DOF(2) = True. [L]
        """
        DOFDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        DOFFinal = [False, False, False, False, False, False]
        for each in DOF:
            indexNum = DOFDict[each]
            DOFFinal[indexNum] = True
        FixedFinal = [False, False, False, False, False, False]
        for each1 in Fixed:
            indexNum1 = DOFDict[each1]
            FixedFinal[indexNum1] = True
        nonlinearFinal = [False, False, False, False, False, False]
        for each2 in NonLinear:
            indexNum2 = DOFDict[each2]
            nonlinearFinal[indexNum2] = True
        keDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        keInput = [0 for each in range(6)]
        key2 = Ke.keys()
        for each2 in key2:
            indexNum2 = keDict[each2]
            keInput[indexNum2] = Ke[each2]
        ceInput = [0 for each in range(6)]
        key3 = Ce.keys()
        for each3 in key3:
            indexNum3 = keDict[each3]
            ceInput[indexNum3] = Ce[each3]
        kInput = [0 for each in range(6)]
        key4 = k.keys()
        for each4 in key4:
            indexNum4 = keDict[each4]
            kInput[indexNum4] = k[each4]
        dispInput = [0 for each in range(6)]
        key5 = disp.keys()
        for each5 in key5:
            indexNum5 = keDict[each5]
            dispInput[indexNum5] = disp[each5]
        self.SapModel.PropLink.SetHook(name,DOFFinal,FixedFinal,nonlinearFinal,keInput,ceInput,kInput,dispInput,dj2,dj3)

    def define_section_PropLink_SetPlasticWen(self,name,DOF,Fixed,NonLinear,Ke={},Ce={},k={},yieldF={},Ratio={},
                                              exp={},dj2=0,dj3=0):
        """
        ---This function initializes a plastic Wen-type link property---
        inputs:
        name(str)-The name of an existing or new link property
        DOF(list)-This is str list,indicating if properties exist for a specified degree of freedom.e.g. ["U1"]
        Fixed(list)-This is str list, indicating if the specified degree of freedom is fixed (restrained).e.g. ["R1"]
        Nonlinear(list)-This is str list, indicating if nonlinear properties exist for a specified degree of freedom.
            e.g. ["R1"]
        Ke(dict)-This is a dictionary of stiffness terms for the link property,e.g.,{"U1":2000,"R1":5000}
        Ce(dict)-This is a dictionary of damping terms for the link property,e.g.,{"U1":0.03,"R1":0.05}
        k(dict)-The initial stiffness applies for nonlinear analyses.e.g.,{"U1":10000}
        yieldF(dict)-yield force terms for the link property. The yield force applies for nonlinear analyses.
        Ratio(dict)-post-yield stiffness ratio terms for the link property. The post-yield stiffness ratio
            applies for nonlinear analyses. It is the post-yield stiffness divided by the initial stiffness.
        exp(dict)-yield exponent terms for the link property. The yield exponent applies for nonlinear analyses.
            The yielding exponent that controls the sharpness of the transition from the initial stiffness to the
            yielded stiffness.
        dj2(float)-The distance from the J-End of the link to the U2 shear spring.
            This item applies only when DOF(1) = True. [L]
        dj3(float)-The distance from the J-End of the link to the U3 shear spring.
            This item applies only when DOF(2) = True. [L]
        """
        DOFDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        DOFFinal = [False, False, False, False, False, False]
        for each in DOF:
            indexNum = DOFDict[each]
            DOFFinal[indexNum] = True
        FixedFinal = [False, False, False, False, False, False]
        for each1 in Fixed:
            indexNum1 = DOFDict[each1]
            FixedFinal[indexNum1] = True
        nonlinearFinal = [False, False, False, False, False, False]
        for each2 in NonLinear:
            indexNum2 = DOFDict[each2]
            nonlinearFinal[indexNum2] = True
        keDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        keInput = [0 for each in range(6)]
        key2 = Ke.keys()
        for each2 in key2:
            indexNum2 = keDict[each2]
            keInput[indexNum2] = Ke[each2]
        ceInput = [0 for each in range(6)]
        key3 = Ce.keys()
        for each3 in key3:
            indexNum3 = keDict[each3]
            ceInput[indexNum3] = Ce[each3]
        kInput = [0 for each in range(6)]
        key4 = k.keys()
        for each4 in key4:
            indexNum4 = keDict[each4]
            kInput[indexNum4] = k[each4]
        yieldFInput = [0 for each in range(6)]
        key5 = yieldF.keys()
        for each5 in key5:
            indexNum5 = keDict[each5]
            yieldFInput[indexNum5] = yieldF[each4]
        RatioInput = [0 for each in range(6)]
        key6 = Ratio.keys()
        for each6 in key6:
            indexNum6 = keDict[each6]
            RatioInput[indexNum6] = Ratio[each6]
        expInput = [0 for each in range(6)]
        key7 = exp.keys()
        for each7 in key7:
            indexNum7 = keDict[each7]
            expInput[indexNum7] = exp[each7]
        self.SapModel.PropLink.SetPlasticWen(name,DOFFinal,FixedFinal,nonlinearFinal,keInput,ceInput,kInput,
                                             yieldFInput,RatioInput,expInput,dj2,dj3)

    def define_section_PropLink_SetRubberIsolator(self,name,DOF,Fixed,NonLinear,Ke={},Ce={},k={},YieldF={},
                                                  Ratio={},dj2=0,dj3=0):
        """
        ---This function initializes a rubber isolator-type link property---
        inputs:
        name(str)-The name of an existing or new link property
        DOF(list)-This is str list,indicating if properties exist for a specified degree of freedom.e.g. ["U1"]
        Fixed(list)-This is str list, indicating if the specified degree of freedom is fixed (restrained).e.g. ["R1"]
        Nonlinear(list)-This is str list, indicating if nonlinear properties exist for a specified degree of freedom.
            e.g. ["R1"]
        Ke(dict)-This is a dictionary of stiffness terms for the link property,e.g.,{"U1":2000,"R1":5000}
        Ce(dict)-This is a dictionary of damping terms for the link property,e.g.,{"U1":0.03,"R1":0.05}
        k(dict)-The initial stiffness applies for nonlinear analyses.e.g.,{"U1":10000}
            k(0) = U1, Not Used,k(1) = U2 [F/L],k(2) = U3 [F/L],k(3) = R1, Not Used,k(4) = R2, Not Used
            k(5) = R3, Not Used
        yieldF(dict)-yield force terms for the link property. The yield force applies for nonlinear analyses.
            k(0) = U1, Not Used,k(1) = U2 [F/L],k(2) = U3 [F/L],k(3) = R1, Not Used,k(4) = R2, Not Used
            k(5) = R3, Not Used
        Ratio(dict)-post-yield stiffness ratio terms for the link property. The post-yield stiffness ratio
            applies for nonlinear analyses. It is the post-yield stiffness divided by the initial stiffness.
            k(0) = U1, Not Used,k(1) = U2 [F/L],k(2) = U3 [F/L],k(3) = R1, Not Used,k(4) = R2, Not Used
            k(5) = R3, Not Used
        dj2(float)-The distance from the J-End of the link to the U2 shear spring.
            This item applies only when DOF(1) = True. [L]
        dj3(float)-The distance from the J-End of the link to the U3 shear spring.
            This item applies only when DOF(2) = True. [L]
        """
        DOFDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        DOFFinal = [False, False, False, False, False, False]
        for each in DOF:
            indexNum = DOFDict[each]
            DOFFinal[indexNum] = True
        FixedFinal = [False, False, False, False, False, False]
        for each1 in Fixed:
            indexNum1 = DOFDict[each1]
            FixedFinal[indexNum1] = True
        nonlinearFinal = [False, False, False, False, False, False]
        for each2 in NonLinear:
            indexNum2 = DOFDict[each2]
            nonlinearFinal[indexNum2] = True
        keDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        keInput = [0 for each in range(6)]
        key2 = Ke.keys()
        for each2 in key2:
            indexNum2 = keDict[each2]
            keInput[indexNum2] = Ke[each2]
        ceInput = [0 for each in range(6)]
        key3 = Ce.keys()
        for each3 in key3:
            indexNum3 = keDict[each3]
            ceInput[indexNum3] = Ce[each3]
        kInput = [0 for each in range(6)]
        key4 = k.keys()
        for each4 in key4:
            indexNum4 = keDict[each4]
            kInput[indexNum4] = k[each4]
        yieldFInput = [0 for each in range(6)]
        key5 = YieldF.keys()
        for each5 in key5:
            indexNum5 = keDict[each5]
            yieldFInput[indexNum5] = YieldF[each4]
        RatioInput = [0 for each in range(6)]
        key6 = Ratio.keys()
        for each6 in key6:
            indexNum6 = keDict[each6]
            RatioInput[indexNum6] = Ratio[each6]
        self.SapModel.PropLink.SetRubberIsolator(name,DOFFinal,FixedFinal,nonlinearFinal,keInput,ceInput,kInput,
                                             yieldFInput,RatioInput,dj2,dj3)

    def define_section_PropLink_SetFrictionIsolator(self,name,DOF,Fixed,Nonlinear,Ke={},Ce={},k={},slow={},fast={},
                                                    Rate={},Radius={},damping=0,dj2=0,dj3=0):
        """
        ---This function initializes a friction isolator-type link proper---
        inputs:
        name(str)-The name of an existing or new link property
        DOF(list)-This is str list,indicating if properties exist for a specified degree of freedom.e.g. ["U1"]
        Fixed(list)-This is str list, indicating if the specified degree of freedom is fixed (restrained).e.g. ["R1"]
        Nonlinear(list)-This is str list, indicating if nonlinear properties exist for a specified degree of freedom.
            e.g. ["R1"]
        Ke(dict)-This is a dictionary of stiffness terms for the link property,e.g.,{"U1":2000,"R1":5000}
        Ce(dict)-This is a dictionary of damping terms for the link property,e.g.,{"U1":0.03,"R1":0.05}
        k(dict)-The initial stiffness applies for nonlinear analyses.e.g.,{"U1":10000}
            k(0) = U1 [F/L],k(1) = U2 [F/L],k(2) = U3 [F/L],k(3) = R1, Not Used,k(4) = R2, Not Used,k(5) = R3, Not Used
        slow(dict)- the friction coefficient at zero velocity terms for the link property. This coefficient applies
            for nonlinear analyses.Slow(0) = U1, Not Used,Slow(1) = U2,Slow(2) = U3,Slow(3) = R1, Not Used,
            Slow(4) = R2, Not Used,Slow(5) = R3, Not Used
        fast(dict)-the friction coefficient at fast velocity terms for the link property. This coefficient applies
            for nonlinear analyses.Slow(0) = U1, Not Used,Slow(1) = U2,Slow(2) = U3,Slow(3) = R1, Not Used,
            Slow(4) = R2, Not Used,Slow(5) = R3, Not Used
        Rate(dict)-the inverse of the characteristic sliding velocity terms for the link property. This item applies
            for nonlinear analyses.Slow(0) = U1, Not Used,Slow(1) = U2,Slow(2) = U3,Slow(3) = R1, Not Used,
            Slow(4) = R2, Not Used,Slow(5) = R3, Not Used
        Radius(dict)-the radius of the sliding contact surface terms for the link property. Inputting 0 means
            there is an infinite radius, that is, the slider is flat. This item applies for nonlinear analyses.
            Slow(0) = U1, Not Used,Slow(1) = U2,Slow(2) = U3,Slow(3) = R1, Not Used,
            Slow(4) = R2, Not Used,Slow(5) = R3, Not Used
        damping(float)-the nonlinear damping coefficient used for the axial translational degree of freedom,
            U1. This item applies for nonlinear analyses. [F/L]
        dj2(float)-The distance from the J-End of the link to the U2 shear spring.
            This item applies only when DOF(1) = True. [L]
        dj3(float)-The distance from the J-End of the link to the U3 shear spring.
            This item applies only when DOF(2) = True. [L]
        """
        DOFDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        DOFFinal = [False, False, False, False, False, False]
        for each in DOF:
            indexNum = DOFDict[each]
            DOFFinal[indexNum] = True
        FixedFinal = [False, False, False, False, False, False]
        for each1 in Fixed:
            indexNum1 = DOFDict[each1]
            FixedFinal[indexNum1] = True
        nonlinearFinal = [False, False, False, False, False, False]
        for each2 in Nonlinear:
            indexNum2 = DOFDict[each2]
            nonlinearFinal[indexNum2] = True
        keDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        keInput = [0 for each in range(6)]
        key2 = Ke.keys()
        for each2 in key2:
            indexNum2 = keDict[each2]
            keInput[indexNum2] = Ke[each2]
        ceInput = [0 for each in range(6)]
        key3 = Ce.keys()
        for each3 in key3:
            indexNum3 = keDict[each3]
            ceInput[indexNum3] = Ce[each3]
        kInput = [0 for each in range(6)]
        key4 = k.keys()
        for each4 in key4:
            indexNum4 = keDict[each4]
            kInput[indexNum4] = k[each4]
        slowInput = [0 for each in range(6)]
        key5 = slow.keys()
        for each5 in key5:
            indexNum5 = keDict[each5]
            slowInput[indexNum5] = slow[each5]
        fastInput = [0 for each in range(6)]
        key6 = fast.keys()
        for each6 in key6:
            indexNum6 = keDict[each6]
            fastInput[indexNum6] = fast[each6]
        rateInput = [0 for each in range(6)]
        key7 = Rate.keys()
        for each7 in key7:
            indexNum7 = keDict[each7]
            rateInput[indexNum7] = Rate[each7]
        radiusInput = [0 for each in range(6)]
        key8 = Radius.keys()
        for each8 in key8:
            indexNum8 = keDict[each8]
            radiusInput[indexNum8] = Radius[each8]
        self.SapModel.PropLink.SetFrictionIsolator(name,DOFFinal,FixedFinal,nonlinearFinal,keInput,ceInput,kInput,
                                                    slowInput,fastInput,rateInput,radiusInput,damping,dj2,dj3)

    def define_section_PropLink_SetWeightAndMass(self,name,w,mass=0,R1=0,R2=0,R3=0):
        """
        ---This function assigns weight and mass values to a link property.---
        inputs:
        name(str)-The name of an existing link property.
        w(float)-The weight of the link. [F]
        mass(float)-The translational mass of the link. [M]
        R1,R2,R3(float)-The rotational inertia of the link about its local 1,2,3 axis. [ML2]
        """
        self.SapModel.PropLink.SetWeightAndMass(name,w,mass,R1,R2,R3)

    def define_SourceMass_SetMassSource(self,Name,MassFromElements,MassFromMasses,MassFromLoads,IsDefault,
                                        NumberLoads,LoadPat,SF):
        """
        ---This function adds a new mass source to the model or reinitializes an existing mass source---
        inputs:
        name(str)-The mass source name.
        MassFromElements(bool)-If this item is True then element self mass is included in the mass.
        MassFromMasses(bool)-If this item is True then assigned masses are included in the mass.
        MassFromLoads(bool)-If this item is True then specified load patterns are included in the mass.
        IsDefault(bool)-If this item is True then the mass source is the default mass source.  Only one mass source
            can be the default mass source so when this assignment is True all other mass sources are automatically
            set to have the IsDefault flag False.
        NumberLoads(int)-The number of load patterns specified for the mass source.  This item is only applicable
            when the MassFromLoads item is True.
        LoadPat(str)-This is an array of load pattern names specified for the mass source.
        S

        """


    def define_jointConstraints_SetBody(self,name,value,Csys="Global"):
        """
        ---This function defines a Body constraint.---
        inputs:
        name(str)-The name of an existing constraint.
        value(list)-indicate which joint degrees of freedom are included in the constraint. In order, the degrees of freedom
            addressed in the list are UX, UY, UZ, RX, RY and RZ.
        Csys(str)-The name of the coordinate system in which the constraint is defined.
        """
        valueDict = {"UX": 0, "UY": 1, "UZ": 2, "RX": 3, "RY": 4, "RZ": 5}
        valueFinal = [False, False, False, False, False, False]
        for each in value:
            indexNum = valueDict[each]
            valueFinal[indexNum] = True
        self.SapModel.ConstraintDef.SetBody(name,valueFinal,Csys)

    def define_jointConstraints_SetBeam(self,name,Axis=4,Csys="Global"):
        """
        ---This function defines a Beam constraint---
        inputs:
        name(str)-The name of a constraint.
        Axis(int)-This is one of the following items from the eConstraintAxis enumeration.
            It specifies the axis in the specified coordinate system that is parallel to the axis of the constraint.
            If AutoAxis is specified, the axis of the constraint is automatically determined from the joints assigned
            to the constraint.X = 1,Y = 2,Z = 3,AutoAxis = 4
        Csys(str)-The name of the coordinate system in which the constraint is defined.
        """
        self.SapModel.ConstraintDef.SetBeam(name,Axis,Csys)

    def define_jointConstraints_SetDiaphragm(self,name,Axis=4,Csys="Global"):
        """
        ---This function defines a Diaphragm constraint.---
        name(str)-The name of a constraint.
        Axis(int)-This is one of the following items from the eConstraintAxis enumeration.
            It specifies the axis in the specified coordinate system that is parallel to the axis of the constraint.
            If AutoAxis is specified, the axis of the constraint is automatically determined from the joints assigned
            to the constraint.X = 1,Y = 2,Z = 3,AutoAxis = 4
        Csys(str)-The name of the coordinate system in which the constraint is defined.
        """
        self.SapModel.ConstraintDef.SetDiaphragm(name,Axis,Csys)

    def define_jointConstraints_SetEqual(self,name,value,Csys="Global"):
        """
        ---This function defines an Equal constraint.---
        inputs:
        name(str)-The name of an existing constraint.
        value(list)-indicate which joint degrees of freedom are included in the constraint. In order, the degrees of freedom
            addressed in the list are UX, UY, UZ, RX, RY and RZ.
        Csys(str)-The name of the coordinate system in which the constraint is defined.
        """
        valueDict = {"UX": 0, "UY": 1, "UZ": 2, "RX": 3, "RY": 4, "RZ": 5}
        valueFinal = [False, False, False, False, False, False]
        for each in value:
            indexNum = valueDict[each]
            valueFinal[indexNum] = True
        self.SapModel.ConstraintDef.SetEqual(name,valueFinal,Csys)

    def define_jointConstraints_SetLine(self,name,value,Csys="Global"):
        """
        ---This function defines a Line constraint---
        inputs:
        name(str)-The name of an existing constraint.
        value(list)-indicate which joint degrees of freedom are included in the constraint. In order, the degrees of freedom
            addressed in the list are UX, UY, UZ, RX, RY and RZ.
        Csys(str)-The name of the coordinate system in which the constraint is defined.
        """
        valueDict = {"UX": 0, "UY": 1, "UZ": 2, "RX": 3, "RY": 4, "RZ": 5}
        valueFinal = [False, False, False, False, False, False]
        for each in value:
            indexNum = valueDict[each]
            valueFinal[indexNum] = True
        self.SapModel.ConstraintDef.SetLine(name,valueFinal,Csys)

    def define_jointConstraints_SetLocal(self,name,value):
        """
        ---This function defines a Local constraint---
        inputs:
        name(str)-The name of an existing constraint.
        value(list)-indicate which joint degrees of freedom are included in the constraint. In order, the degrees of freedom
            addressed in the list are U1, U2, U3, R1, R2 and R3.
        """
        valueDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        valueFinal = [False, False, False, False, False, False]
        for each in value:
            indexNum = valueDict[each]
            valueFinal[indexNum] = True
        self.SapModel.ConstraintDef.SetLocal(name,valueFinal)

    def define_jointConstraints_SetPlate(self,name,Axis=4,Csys="Global"):
        """
        ---This function defines a Plate constraint---
        inputs:
        name(str)-The name of a constraint.
        Axis(int)-the eConstraintAxis enumeration. It specifies the axis in the specified coordinate system
            that is perpendicular to the plane of the constraint. If AutoAxis is specified, the axis of the
            constraint is automatically determined from the joints assigned to the constraint.X = 1,Y = 2,Z = 3
            AutoAxis = 4
        Csys(str)-The name of the coordinate system in which the constraint is defined.
        """
        self.SapModel.ConstraintDef.SetPlate(name,Axis,Csys)

    def define_jointConstraints_SetRod(self,name,Axis=4,Csys="Global"):
        """
        ---This function defines a Rod constraint---
        inputs:
        name(str)-The name of a constraint.
        Axis(int)-This is one of the following items from the eConstraintAxis enumeration. It specifies the axis
            in the specified coordinate system that is parallel to the axis of the constraint. If AutoAxis is
            specified, the axis of the constraint is automatically determined from the joints assigned to the
            constraint.X = 1,Y = 2,Z = 3,AutoAxis = 4
        Csys(str)-The name of the coordinate system in which the constraint is defined.
        """
        self.SapModel.ConstraintDef.SetRod(name,Axis,Csys)

    def define_jointConstraints_SetWeld(self,name,value,Tolerance,Csys="Global"):
        """
        ---This function defines a Weld constraint---
        inputs:
        name(str)-The name of an existing constraint.
        value(list)-indicate which joint degrees of freedom are included in the constraint. In order,
            the degrees of freedom addressed in the array are UX, UY, UZ, RX, RY and RZ.
        Tolerance(float)-Joints within this distance of each other are constrained together.
        Csys(str)-The name of the coordinate system in which the constraint is defined.
        """
        valueDict = {"UX": 0, "UY": 1, "UZ": 2, "RX": 3, "RY": 4, "RZ": 5}
        valueFinal = [False, False, False, False, False, False]
        for each in value:
            indexNum = valueDict[each]
            valueFinal[indexNum] = True
        self.SapModel.ConstraintDef.SetWeld(name,valueFinal,Tolerance)

    def define_Groups_SetGroup(self,name,color=-1,SpecifiedForSelection=True,SpecifiedForSectionCutDefinition=True,
                               SpecifiedForSteelDesign=True,SpecifiedForConcreteDesign=True,SpecifiedForAluminumDesign=True,
                               SpecifiedForColdFormedDesign=True,SpecifiedForStaticNLActiveStage=True,
                               SpecifiedForBridgeResponseOutput=True,SpecifiedForAutoSeismicOutput=True,
                               SpecifiedForAutoWindOutput=True,SpecifiedForMassAndWeight=True):
        """
        ---The function returns zero if the group data is successfully set, otherwise it returns a nonzero value---
        inputs:
        name(str)-This is the name of a group
        color(float)-The display color for the group specified as a Long. If this value is input as –1
        SpecifiedForSelection(bool)-This item is True if the group is specified to be used for selection;
            otherwise it is False.
        SpecifiedForSectionCutDefinition(bool)-This item is True if the group is specified to be used for
            defining section cuts; otherwise it is False.
        SpecifiedForSteelDesign(bool)-This item is True if the group is specified to be used for defining steel
            frame design groups; otherwise it is False.
        SpecifiedForConcreteDesign(bool)-This item is True if the group is specified to be used for defining
            concrete frame design groups; otherwise it is False.
        SpecifiedForAluminumDesign(bool)-This item is True if the group is specified to be used for defining
            aluminum frame design groups; otherwise it is False.
        SpecifiedForColdFormedDesign(bool)-This item is True if the group is specified to be used for defining
            cold formed frame design groups; otherwise it is False.
        SpecifiedForStaticNLActiveStage(bool)-This item is True if the group is specified to be used for defining
            stages for nonlinear static analysis; otherwise it is False.
        SpecifiedForBridgeResponseOutput(bool)-This item is True if the group is specified to be used for reporting
            bridge response output; otherwise it is False.
        SpecifiedForAutoSeismicOutput(bool)-This item is True if the group is specified to be used for reporting auto
            seismic loads; otherwise it is False.
        SpecifiedForAutoWindOutput(bool)-This item is True if the group is specified to be used for reporting auto
            wind loads; otherwise it is False.
        SpecifiedForMassAndWeight(bool)-This item is True if the group is specified to be used for reporting group
            masses and weight; otherwise it is False.
        """
        self.SapModel.GroupDef.SetGroup(name,color,SpecifiedForSelection,SpecifiedForSectionCutDefinition,
                                        SpecifiedForSteelDesign,SpecifiedForConcreteDesign,SpecifiedForAluminumDesign,
                                        SpecifiedForColdFormedDesign,SpecifiedForStaticNLActiveStage,
                                        SpecifiedForBridgeResponseOutput,SpecifiedForAutoSeismicOutput,
                                        SpecifiedForAutoWindOutput,SpecifiedForMassAndWeight)

    def define_generalizedDisplacements_Add(self,name,myType):
        """
        ---This function adds a new generalized displacement with the specified name and type.---
        inputs:
        name(str)-The name of a new generalized displacement.
        myType(int)-This is 1 or 2 indicating the generalized displacement type.1 = Translational,2 = Rotational
        """
        self.SapModel.GDispl.Add(name,myType)

    def define_generalizedDisplacements_SetPoint(self,name,pointName,SF):
        """
        ---This function adds a point object and its scale factors to a generalized displacement definition,
        or, if the point object already exists in the generalized displacement definition, it modifies the
        scale factors.---
        inputs:
        name(str)-The name of an existing generalized displacement.
        pointName(str)-The name of a point object to be included in the generalized displacement definition.
        SF(dict)-unitless scale factors for the point object displacement degrees of freedom.e.g. {"U1":0.5}
        """
        sfDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        sfInput = [0 for each in range(6)]
        key2 = SF.keys()
        for each2 in key2:
            indexNum2 = sfDict[each2]
            sfInput[indexNum2] = SF[each2]
        self.SapModel.GDispl.SetPoint(name,pointName,sfInput)

    def define_generalizedDisplacements_SetTypeOAPI(self,name,myType):
        """
        ---This function sets the generalized displacement type.---
        inputs:
        name(str)-The name of an existing generalized displacement.
        myType(int)-This is 1 or 2, indicating the generalized displacement type.1 = Translational,2 = Rotational
        """
        self.SapModel.GDispl.SetTypeOAPI(name,myType)

    def define_functions_FuncRS_SetChinese2010(self,name,JGJ32010AlphaMax,JGJ32010SI,JGJ32010Tg,JGJ32010PTDF,DampRatio):
        """
        ---This function defines a Chinese 2010 response spectrum function.---
        inputs:
        name(str)-The name of an existing or new function
        JGJ32010AlphaMax(float)-The maximum influence factor
        JGJ32010SI(int)-This is 1, 2, 3, 4, 5 or 6, indicating the seismic intensity.1 = 6 (0.05g),2 = 7 (0.10g)
            3 = 7 (0.15g),4 = 8 (0.20g),5 = 8 (0.30g),6 = 9 (0.40g)
        JGJ32010Tg(float)-The characteristic ground period, Tg > 0.1. [s]
        JGJ32010PTDF(float)-The period time discount factor
        DampRatio(float)-The damping ratio for the function, 0 <= DampRatio < 1.
        """
        self.SapModel.Func.FuncRS.SetChinese2010(name,JGJ32010AlphaMax,JGJ32010SI,JGJ32010Tg,JGJ32010PTDF,DampRatio)

    def define_functions_FuncRS_SetJTGB022013(self,name,direction,peakAccel,Tg,Ci,Cs,dampRatio):
        """
        ---This function defines a JTG B02-2013 response spectrum function---
        inputs:
        name(str)-The name of an existing or new function
        direction(int)-This is 1, 2 or 3, indicating the response spectrum direction.1 = Horizontal,2 = Vertical-Rock
            3 = Vertical-Soil
        peakAccel(float)-The peak acceleration, A.
        Tg(float)-The characteristic ground period, Tg > 0.1. [s]
        Ci(float)-The importance coefficient.
        Cs(float)-The site soil coefficient.
        dampRatio(float)-The damping ratio for the function, 0 <= DampRatio < 1.
        """
        self.SapModel.Func.FuncRS.SetJTGB022013(name,direction,peakAccel,Tg,Ci,Cs,dampRatio)

    def define_functions_FuncRS_SetCJJ1662011(self,name,direction,peakAccel,Tg,dampRatio):
        """
        ---This function defines a CJJ 166-2011 response spectrum function---
        inputs:
        name(str)-The name of an existing or new function.
        direction(int)-This is 1 or 2, indicating the response spectrum direction.1 = Horizontal,2 = Vertical
        peakAccel(float)-The peak acceleration, A.
        Tg(float)-The characteristic ground period, Tg > 0.1. [s]
        dampRatio(float)-The damping ratio for the function, 0 <= DampRatio < 1.
        """
        self.SapModel.Func.FuncRS.SetCJJ1662011(name,direction,peakAccel,Tg,dampRatio)

    def define_functions_FuncRS_SetUser(self,name,period,value,dampRatio):
        """
        ---This function defines a user response spectrum function.---
        inputs:
        name(str)-The name of an existing or new function.
        period(list)-This is a list that includes the period for each data point. [s]
        value(list)-This is a list that includes the function value for each data point.
        dampRatio(float)-The damping ratio for the function, 0 <= DampRatio < 1.
        """
        numberItems=len(period)
        self.SapModel.Func.FuncRS.SetUser(name,numberItems,period,value,dampRatio)

    def define_functions_FuncTH_SetUser(self,name,myTime,value):
        """
        ---This function defines a user time history function.---
        inputs:
        name(str)-The name of an existing or new function
        myTime(list)-This is a list that includes the time for each data point. [s]
        value(list)-This is a list that includes the function value for each data point.
        """
        numberItems=len(myTime)
        self.SapModel.Func.FuncTH.SetUser(name,numberItems,myTime,value)

    def define_LoadPatterns_Add(self,name,myType,SelfWTMultiplier=0,AddLoadCase=True):
        """
        ---This function adds a new load pattern---
        inputs:
        name(str)-The name for the new load pattern.
        myType(int)-This is one of the following items in the eLoadPatternType enumeration:
            LTYPE_DEAD = 1,LTYPE_SUPERDEAD = 2,LTYPE_LIVE = 3,LTYPE_REDUCELIVE = 4,LTYPE_QUAKE = 5
            LTYPE_WIND= 6,LTYPE_SNOW = 7,LTYPE_OTHER = 8,LTYPE_MOVE = 9,LTYPE_TEMPERATURE = 10
            LTYPE_ROOFLIVE = 11,LTYPE_NOTIONAL = 12,LTYPE_PATTERNLIVE = 13,LTYPE_WAVE= 14,LTYPE_BRAKING = 15
            LTYPE_CENTRIFUGAL = 16,LTYPE_FRICTION = 17,LTYPE_ICE = 18,LTYPE_WINDONLIVELOAD = 19
            LTYPE_HORIZONTALEARTHPRESSURE = 20,LTYPE_VERTICALEARTHPRESSURE = 21,LTYPE_EARTHSURCHARGE = 22
            LTYPE_DOWNDRAG = 23,LTYPE_VEHICLECOLLISION = 24,LTYPE_VESSELCOLLISION = 25,LTYPE_TEMPERATUREGRADIENT = 26
            LTYPE_SETTLEMENT = 27,LTYPE_SHRINKAGE = 28,LTYPE_CREEP = 29,LTYPE_WATERLOADPRESSURE = 30,LTYPE_LIVELOADSURCHARGE = 31
            LTYPE_LOCKEDINFORCES = 32,LTYPE_PEDESTRIANLL = 33,LTYPE_PRESTRESS = 34,LTYPE_HYPERSTATIC = 35,LTYPE_BOUYANCY = 36
            LTYPE_STREAMFLOW = 37,LTYPE_IMPACT = 38,LTYPE_CONSTRUCTION = 39
        SelfWTMultiplier(float)-The self weight multiplier for the new load pattern.
        AddLoadCase(bool)-If this item is True, a linear static load case corresponding to the new load pattern is added.
        """
        self.SapModel.LoadPatterns.Add(name,myType,SelfWTMultiplier,AddLoadCase)

    def define_LoadCases_StaticLinear_SetCase(self,name):
        """
        ---This function initializes a static linear load case---
        inputs:
        name(str)-The name of an existing or new load case.
        """
        self.SapModel.LoadCases.StaticLinear.SetCase(name)

    def define_LoadCases_StaticLinear_SetInitialCase(self,name,initialCase=None):
        """
        ---This function sets the initial condition for the specified load case---
        inputs:
        name(str)-The name of an existing static linear load case.
        initialCase-This is blank, None or the name of an existing analysis case. This item specifies if the
            load case starts from zero initial conditions, that is, an unstressed state, or if it starts using
            the stiffness that occurs at the end of a nonlinear static or nonlinear direct integration time
            history load case.
        """
        self.SapModel.LoadCases.StaticLinear.SetInitialCase(name,initialCase)

    def define_LoadCases_StaticLinear_SetLoads(self,name,numberLoads,loadType,loadName,scaleFactor):
        """
        ---This function sets the load data for the specified analysis case.---
        inputs:
        name(str)-The name of an existing static linear load case.
        numberLoads(int)-The number of loads assigned to the specified analysis case.
        loadType(str list)-This is a list that includes either Load or Accel, indicating the type of each
            load assigned to the load case.
        loadName(str list)-This is a list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.
            If the LoadType item is Accel, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction of the load.
        scaleFactor(float list)-This is a list that includes the scale factor of each load assigned to the load case.
            [L/s2] for Accel UX UY and UZ; otherwise unitless
        """
        self.SapModel.LoadCases.StaticLinear.SetLoads(name,numberLoads,loadType,loadName,scaleFactor)

    def define_LoadCases_StaticLinearMultistep_SetCase(self,name):
        """
        ---This function initializes a static linear multistep analysis case.---
        inputs:
        name(str)-The name of an existing or new load case.
        """
        self.SapModel.LoadCases.StaticLinearMultistep.SetCase(name)

    def define_loadCases_StaticLinearMultistep_SetInitialCase(self,name,InitialCase=None):
        """
        ---This function sets the initial condition for the specified load case---
        inputs:
        name(str)-The name of an existing static linear multistep analysis case.
        initialCase-This is blank, None, or the name of an existing analysis case. This item specifies if
            the load case starts from zero initial conditions, that is, an unstressed state, or if it
            starts using the stiffness that occurs at the end of a nonlinear static or nonlinear direct
            integration time history load case.If the specified initial case is a nonlinear static or
            nonlinear direct integration time history load case, the stiffness at the end of that case
            is used. If the initial case is anything else, zero initial conditions are assumed.
        """
        self.SapModel.LoadCases.StaticLinearMultistep.SetInitialCase(name,InitialCase)

    def define_loadCases_StaticLinearMultistep_SetLoads_1(self,name,numberLoads,LoadType,LoadName,scaleFactor,
                            stepRange,firstLoadStep,lastLoadStep,startCaseStep,extrapolateOption):
        """
        ---This function sets the load data for the specified analysis case.---
        inputs:
        name(str)-The name of an existing static linear multistep analysis case.
        numberLoads(int)-The number of loads assigned to the specified analysis case.
        loadType(str list)-This is a list that includes either Load or Accel, indicating the type of
            each load assigned to the load case.
        loadName(str list)-This is list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.If the LoadType
            item is Accel, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction of the load.
        scaleFactor(float list)-This is a list that includes the scale factor of each load assigned to
            the load case. [L/s2] for Accel UX UY and UZ; otherwise unitless
        stepRange(int list)-This is a list that identifies the step range type to consider for each load
        assigned to the load case. The allowed values are:0 = All,1 = User
        FirstLoadStep(int list)-This is a list that specifies the first load step to consider for each
            load assigned to the load case. This value is only applicable when StepRange = User.
        lastLoadStep(int list)-This is a list that specifies the last load step to consider for each
            load assigned to the load case. This value is only applicable when StepRange = User.
        StartCaseStep(int list)-This is a list that specifies the load case step at which to start
            applying each load assigned to the load case.
        extrapolateOption(int list)-This is a list that identifies the extrapolation option for each load
            assigned to the load case. The allowed values are:0 = None,1 = Last Step,2 = Repeat Range
        """

        self.SapModel.LoadCases.StaticLinearMultistep.SetLoads_1(name,numberLoads,LoadType,LoadName,scaleFactor,
                stepRange,firstLoadStep,lastLoadStep,startCaseStep,extrapolateOption)

    def define_LoadCases_StaticNonlinear_SetCase(self,name):
        """
        ---This function initializes a static nonlinear analysis case---
        inputs:
        name(str)-The name of an existing or new load case.
        """
        self.SapModel.LoadCases.StaticNonlinear.SetCase(name)

    def define_loadCases_StaticNonlinear_SetGeometricNonlinearity(self,name,NLGeomType=0):
        """
        ---This function sets the geometric nonlinearity option for the specified load case.---
        inputs:
        name(str)-The name of an existing static nonlinear load case.
        NLGeomType(int)-This is 0, 1 or 2, indicating the geometric nonlinearity option selected for the load case.
            0 = None,1 = P-delta,2 = P-delta plus large displacements
        """
        self.SapModel.LoadCases.StaticNonlinear.SetGeometricNonlinearity(name,NLGeomType)

    def define_loadCases_StaticNonlinear_SetHingeUnloading(self,name,UnloadType):
        """
        ---This function sets the hinge unloading option for the specified load case.---
        inputs:
        name(str)-The name of an existing static nonlinear load case.
        UNLoadType(int)-This is 1, 2 or 3, indicating the hinge unloading option selected for the load case.
            1 = Unload entire structure,2 = Apply local redistribution,3 = Restart using secant stiffness
        """
        self.SapModel.LoadCases.StaticNonlinear.SetHingeUnloading(name,UnloadType)

    def define_loadCases_StaticNonlinear_SetInitialCase(self,name,initialCase=None):
        """
        ---This function sets the initial condition for the specified load case.---
        inputs:
        name(str)-The name of an existing static nonlinear load case.
        initialCase-This is blank, None, or the name of an existing analysis case. This item specifies if
            the load case starts from zero initial conditions, that is, an unstressed state, or if it starts
            from the state at the end of a nonlinear static or nonlinear direct integration time history load case.
            If the specified initial case is a nonlinear static or nonlinear direct integration time history
            load case, the state at the end of that case is used. If the initial case is anything else, zero initial
            conditions are assumed.
        """
        self.SapModel.LoadCases.StaticNonlinearMultistep.SetInitialCase(name,initialCase)

    def define_loadCases_StaticNonlinear_SetLoadApplication(self,name,LoadControl,DispType,Displ,Monitor,DOF,
                                                            PointName,GDispl):
        """
        ---This function sets the load application control parameters for the specified load case---
        inputs:
        name(str)-The name of an existing static nonlinear load case.
        LoadControl(int)-This is either 1 or 2, indicating the load application control method.1 = Full load,
            2 = Displacement control
        DispType(int)-This is either 1 or 2 indicating the control displacement type.1 = Conjugate displacement,
            2 = Monitored displacement
        Displ(float)-This item applies only when displacement control is used, that is, LoadControl = 2. The
            structure is loaded to a monitored displacement of this magnitude. [L] when DOF = 1, 2 or 3 and [rad]
            when DOF = 4, 5 or 6
        Monitor(int)-This is either 1 or 2, indicating the monitored displacement.1 = Displacement at a specified
            point object,2 = Generalized displacement
        DOF(int)-This is 1, 2, 3, 4, 5 or 6, indicating the degree of freedom for which the displacement at a point
            object is monitored.1 = U1,2 = U2,3 = U3,4 = R1,5 = R2,6 = R3,This item applies only when Monitor = 1.
        PointName(str)-The name of the point object at which the displacement is monitored. This item applies only
            when Monitor = 1.
        GDispl(str)-The name of the generalized displacement for which the displacement is monitored. This item
            applies only when Monitor = 2.
        """
        self.SapModel.LoadCases.StaticNonlinear.SetLoadApplication(name,LoadControl,DispType,Displ,Monitor,
                        DOF,PointName,GDispl)

    def define_loadCases_StaticNonlinear_SetLoads(self,name,NumberLoads,LoadType,LoadName,SF):
        """
        ---This function sets the load data for the specified analysis case---
        inputs:
        name(str)-The name of an existing static nonlinear load case.
        NumberLoads(int)-The number of loads assigned to the specified analysis case.
        LoadType(str list)-This is a list that includes either Load or Accel, indicating the type of
            each load assigned to the load case.
        LoadName(str list)-This is a list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.
            If the LoadType item is Accel, this item is UX, UY, UZ, RX, RY or RZ indicating the direction
            of the load.
        SF(float list)-This is a list that includes the scale factor of each load assigned to the load case.
            [L/s2] for Accel UX UY and UZ; otherwise unitless
        """
        self.SapModel.LoadCases.StaticNonlinear.SetLoads(name,NumberLoads,LoadType,LoadName,SF)

    def define_loadCases_StaticNonlinear_SetMassSource(self,name,Source=""):
        """
        ---This function sets the mass source to be used for the specified load case.---
        inputs:
        name(str)-The name of an existing static nonlinear load case.
        Source(str)-This is the name of an existing mass source or a blank string. Blank indicates to use the
        mass source from the previous load case or the default mass source if the load case starts from zero
        initial conditions.
        """
        self.SapModel.LoadCases.StaticNonlinear.SetMassSource(name,Source)

    def define_loadCases_StaticNonlinear_SetModalCase(self,name,ModalCase):
        """
        ---This function sets the modal case for the specified analysis case---
        inputs:
        name(str)-The name of an existing static nonlinear load case.
        ModalCase(str)-This is the name of an existing modal load case. It specifies the modal load case
            on which any mode-type load assignments to the specified load case are based.
        """
        self.SapModel.LoadCases.StaticNonlinear.SetModalCase(name,ModalCase)

    def define_loadCases_StaticNonlinear_SetResultsSaved(self,name,SaveMultipleSteps,MinSavedStates=10,
                                                         MaxSavedStates=100,PositiveOnly=True):
        """
        ---This function sets the results saved parameters for the specified load case---
        inputs:
        name(str)-The name of an existing static nonlinear load case.
        SaveMultipleSteps(bool)-This item is True if multiple states are saved for the nonlinear analysis.
            It is False only if the final state is saved.
        MinSavedStates(int)-This item only applies when SaveMultipleSteps = True. It is the minimum number
            of saved steps.
        MaxSavedStates(int)-This item only applies when SaveMultipleSteps = True. It is the maximum number
            of saved steps.
        PositiveOnly(bool)-If this item is True, only positive displacement increments are saved. If it is False,
            all displacement increments are saved.
        """
        self.SapModel.LoadCases.StaticNonlinear.SetResultsSaved(name,SaveMultipleSteps,MinSavedStates,
                                                                MaxSavedStates,PositiveOnly)

    def define_loadCases_StaticNonlinear_SetSolControlParameters(self,name,MaxTotalSteps,MaxFailedSubSteps,
        MaxIterCS,MaxIterNR,TolConvD,UseEventStepping,TolEventD,MaxLineSearchPerIter,TolLineSearch,LineSearchStepFact):
        """
        ---This function sets the solution control parameters for the specified load case---
        inputs:
        name(str)-The name of an existing static nonlinear load case.
        MaxTotalSteps(int)-The maximum total steps per stage.
        MaxFailedSubSteps(int)-The maximum null (zero) steps per stage.
        MaxIterCS(int)-The maximum constant-stiffness iterations per step.
        MaxIterNR(int)-The maximum Newton_Raphson iterations per step.
        TolConvD(float)-The relative iteration convergence tolerance.
        UseEventStepping(bool)-This item is True if event-to-event stepping is used.
        TolEventD(float)-The relative event lumping tolerance.
        MaxLineSearchPerIter(int)-The maximum number of line searches per iteration.
        TolLineSearch(float)-The relative line-search acceptance tolerance.
        LineSearchStepFact(float)-The line-search step factor.
        """
        self.SapModel.LoadCases.StaticNonlinear.SetSolControlParameters(name,MaxTotalSteps,MaxFailedSubSteps,
        MaxIterCS,MaxIterNR,TolConvD,UseEventStepping,TolEventD,MaxLineSearchPerIter,TolLineSearch,LineSearchStepFact)

    def define_loadCases_StaticNonlinear_SetTargetForceParameters(self,name,TolConvF,MaxIter,AccelFact,NoStop):
        """
        ---This function sets the target force iteration parameters for the specified load case---
        inputs:
        name(str)-The name of an existing static nonlinear load case.
        TolConvF(float)-The relative convergence tolerance for target force iteration.
        MaxIter(int)-The maximum iterations per stage for target force iteration.
        AccelFact(float)-The acceleration factor.
        NoStop(bool)-If this item is True, the analysis is continued when there is no convergence in the target
            force iteration.
        """
        self.SapModel.LoadCases.StaticNonlinear.SetTargetForceParameters(name,TolConvF,MaxIter,AccelFact,NoStop)

    def define_loadCases_Buckling_SetCase(self,name):
        """
        ---This function initializes a buckling load case.---
        inputs:
        name(str)-The name of an existing or new load case.
        """
        self.SapModel.LoadCases.Buckling.SetCase(name)

    def define_loadCases_Buckling_SetInitialCase(self,name,InitialCase=None):
        """
        ---This function sets the initial condition for the specified load case.---
        inputs:
        name(str)-The name of an existing buckling load case.
        InitialCase-This is blank, None or the name of an existing analysis case. This item specifies if the
            load case starts from zero initial conditions, that is, an unstressed state, or if it starts using
            the stiffness that occurs at the end of a nonlinear static or nonlinear direct integration time
            history load case.If the specified initial case is a nonlinear static or nonlinear direct integration
            time history load case, the stiffness at the end of that case is used. If the initial case is anything
            else, zero initial conditions are assumed.
        """
        self.SapModel.LoadCases.Buckling.SetInitialCase(name,InitialCase)

    def define_loadCases_Buckling_SetLoads(self,name,NumberLoads,LoadType,LoadName,SF):
        """
        ---This function sets the load data for the specified analysis case---
        inputs:
        name(str)-The name of an existing buckling load case.
        NumberLoads(int)-The number of loads assigned to the specified analysis case.
        LoadType(str list)-This is a list that includes either Load or Accel, indicating the type of each
            load assigned to the load case.
        LoadName(str list)-This is a list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.
            If the LoadType item is Acce, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction of the load.
        SF(float list)-This is a list that includes the scale factor of each load assigned to the load case.
            [L/s2] for Accel UX UY and UZ; otherwise unitless
        """
        self.SapModel.LoadCases.Buckling.SetLoads(name,NumberLoads,LoadType,LoadName,SF)

    def define_loadCases_Buckling_SetParameters(self,name,NumBucklingModes=6,EigenTol=1.0e-9):
        """
        ---This function sets various parameters for the specified buckling load case---
        inputs:
        name(str)-The name of an existing buckling load case.
        NumBucklingModes(int)-The number of buckling modes requested.
        EigenTol(float)-The relative convergence tolerance for eigenvalues.
        """
        self.SapModel.LoadCases.Buckling.SetParameters(name,NumBucklingModes,EigenTol)

    def define_loadCases_DirHistLinear_SetCase(self,name):
        """
        ---This function initializes a linear direct integration time history load case---
        inputs:
        name(str)-The name of an existing or new load case.
        """
        self.SapModel.LoadCases.DirHistLinear.SetCase(name)

    def define_loadCases_DirHistLinear_SetDampProportional(self,name,DampType,Dampa,Dampb,Dampf1=0,
                                                           Dampf2=0,Dampd1=0,Dampd2=0):
        """
        ---This function sets proportional modal damping data for the specified load case---
        inputs:
        name(str)-The name of an existing linear direct integration time history load case.
        DampType(int)-This is 1, 2 or 3, indicating the proportional modal damping type.1 = Mass and stiffness
            proportional damping by direct specification,2 = Mass and stiffness proportional damping by period
            3 = Mass and stiffness proportional damping by frequency
        Dampa(float)-The mass proportional damping coefficient. This item applies only when DampType = 1.
        Dampb(float)-The stiffness proportional damping coefficient. This item applies only when DampType = 1.
        Dampf1(float)-This is the period or the frequency (depending on the value of the DampType item) for point 1.
            [s] for DampType = 2 and [cyc/s] for DampType = 3
        Dampf2(float)-This is either the period or the frequency (depending on the value of the DampType item)
            for point 2. [s] for DampType = 2 and [cyc/s] for DampType = 3
        Dampd1(float)-This is the damping at point 1 (0 <= Dampd1 < 1).This item applies only when DampType = 2 or 3.
        Dampd2(float)-This is the damping at point 2 (0 <= Dampd2 < 1).This item applies only when DampType = 2 or 3.
        """
        self.SapModel.LoadCases.DirHistLinear.SetDampProportional(name,DampType,Dampa,Dampb,Dampf1,Dampf2,Dampd1,Dampd2)

    def define_loadCases_DirHistLinear_SetInitialCase(self,name,initialCase=None):
        """
        ---This function sets the initial condition for the specified load case---
        inputs:
        name(str)-The name of an existing linear direct integration time history load case.
        initialCase-This is blank, None, or the name of an existing analysis case. This item specifies if the load
            case starts from zero initial conditions, that is, an unstressed state, or if it starts using the
            stiffness that occurs at the end of a nonlinear static or nonlinear direct integration time history
            load case.If the specified initial case is a nonlinear static or nonlinear direct integration time
            history load case. the stiffness at the end of that case is used. If the initial case is anything else,
            zero initial conditions are assumed.
        """
        self.SapModel.LoadCases.DirHistLinear.SetInitialCase(name,initialCase)

    def define_loadCases_DirHistLinear_SetLoads(self,name,NumberLoads,LoadType,LoadName,Func,SF=None,TF=None,AT=None,
                                                CSys=None,Ang=None):
        """
        ---This function sets the load data for the specified analysis case---
        inputs:
        name(str)-The name of an existing linear direct integration time history load case.
        NumberLoads(int)-The number of loads assigned to the specified analysis case.
        LoadType(str list)-This is a str list that includes Load or Accel, indicating the type of each load
            assigned to the load case.
        LoadName(str list)-This is a str list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.
            If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of the load.
        Func(str list)-This is a str list that includes the name of the time history function associated with each load.
        SF(float list)-This is a str list that includes the scale factor of each load assigned to the load case.
            [L/s2] for U1 U2 and U3; otherwise unitless
        TF(float list)-This is a str list that includes the time scale factor of each load assigned to the load case.
        AT(float list)-This is a str list that includes the arrival time of each load assigned to the load case.
        CSys(str float)-This is a str list that includes the name of the coordinate system associated with each load.
            If this item is a blank string, the Global coordinate system is assumed.This item applies only when the
            LoadType item is Accel.
        Ang(float list)-This is a float list that includes the angle between the acceleration local 1 axis and
            the +X-axis of the coordinate system specified by the CSys item. The rotation is about the Z-axis
            of the specified coordinate system. [deg] This item applies only when the LoadType item is Accel.
        """
        if SF==None:
            SF=[1.0 for each in range(NumberLoads)]
        if TF==None:
            TF=[1.0 for each in range(NumberLoads)]
        if AT==None:
            AT=[0.0 for each in range(NumberLoads)]
        if CSys==None:
            CSys=["Global" for each in range(NumberLoads)]
        if Ang == None:
            Ang=[0.0 for each in range(NumberLoads)]
        self.SapModel.LoadCases.DirHistLinear.SetLoads(name,NumberLoads,LoadType,LoadName,Func,SF,TF,AT,CSys,Ang)

    def define_loadCases_DirHistLinear_SetTimeIntegration(self,name,IntegrationType=4):
        """
        ---This function sets time integration data for the specified load case---
        inputs:
        name(str)-The name of an existing linear direct integration time history load case.
        IntegrationType(int)-This is 1, 2, 3, 4 or 5, indicating the time integration type.1 = Newmark,2 = Wilson,
        3 = Collocation,4 = Hilber-Hughes-Taylor,5 = Chung and Hulbert
        """
        Alpha,Beta,Gamma,Theta,m=0.0,0.0,0.0,0.0,0.0
        if IntegrationType==1:
            Gamma,Beta=0.5,0.25
        if IntegrationType==2:
            Theta=1.0
        if IntegrationType==3:
            Gamma,Beta,Theta=0.5,0.1667,1.0
        if IntegrationType==4:
            Alpha=0.0
        if IntegrationType==5:
            Gamma,Beta,Alpha,m=0.5,0.25,0.0,0.0
        self.SapModel.LoadCases.DirHistLinear.SetTimeIntegration(name,IntegrationType,Alpha,Beta,Gamma,Theta,m)

    def define_loadCases_DirHistLinear_SetTimeStep(self,name,nstep,DT):
        """
        ---This function sets the time step data for the specified load case---
        inputs:
        name(str)-The name of an existing linear direct integration time history load case.
        nstep(int)-The number of output time steps.
        DT(float)-The output time step size.
        """
        self.SapModel.LoadCases.DirHistLinear.SetTimeStep(name,nstep,DT)

    def define_loadCases_DirHistNonlinear_SetCase(self,name):
        """
        ---This function initializes a nonlinear direct integration time history load case---
        inputs:
        name(str)-The name of an existing or new load case
        """
        self.SapModel.LoadCases.DirHistNonlinear.SetCase(name)

    def define_loadCases_DirHistNonlinear_SetDampProportional(self,name,DampType,Dampa,Dampb,Dampf1=0,
                                                           Dampf2=0,Dampd1=0,Dampd2=0):
        """
         ---This function sets proportional modal damping data for the specified load case---
         inputs:
         name(str)-The name of an existing linear direct integration time history load case.
         DampType(int)-This is 1, 2 or 3, indicating the proportional modal damping type.1 = Mass and stiffness
             proportional damping by direct specification,2 = Mass and stiffness proportional damping by period
             3 = Mass and stiffness proportional damping by frequency
         Dampa(float)-The mass proportional damping coefficient. This item applies only when DampType = 1.
         Dampb(float)-The stiffness proportional damping coefficient. This item applies only when DampType = 1.
         Dampf1(float)-This is the period or the frequency (depending on the value of the DampType item) for point 1.
             [s] for DampType = 2 and [cyc/s] for DampType = 3
         Dampf2(float)-This is either the period or the frequency (depending on the value of the DampType item)
             for point 2. [s] for DampType = 2 and [cyc/s] for DampType = 3
         Dampd1(float)-This is the damping at point 1 (0 <= Dampd1 < 1).This item applies only when DampType = 2 or 3.
         Dampd2(float)-This is the damping at point 2 (0 <= Dampd2 < 1).This item applies only when DampType = 2 or 3.
         """
        self.SapModel.LoadCases.DirHistNonlinear.SetDampProportional(name,DampType,Dampa,Dampb,Dampf1,Dampf2,Dampd1,Dampd2)

    def define_loadCases_DirHistNonlinear_SetGeometricNonlinearity(self,name,NLGeomType=0):
        """
        ---This function sets the geometric nonlinearity option for the specified load case---
        inputs:
        name(str)-The name of an existing nonlinear direct integration time history load case.
        NLGeomType(int)-This is 0, 1 or 2, indicating the geometric nonlinearity option selected for the load case.
            0 = None,1 = P-delta,2 = P-delta plus large displacements
        """
        self.SapModel.LoadCases.DirHistNonlinear.SetGeometricNonlinearity(name,NLGeomType)

    def define_loadCases_DirHistNonlinear_SetInitialCase(self,name,initialCase=None):
        """
        ---This function sets the initial condition for the specified load case.---
        inputs:
        name(str)-The name of an existing nonlinear direct integration time history load case.
        initialCase-This is blank, None or the name of an existing analysis case. This item specifies if the load
            case starts from zero initial conditions, that is, an unstressed state, or if it starts from the state
            at the end of a nonlinear static or nonlinear direct integration time history load case.If the specified
            initial case is a nonlinear static or nonlinear direct integration time history load case, the state at
            the end of that case is used. If the initial case is anything else, zero initial conditions are assumed.
        """
        self.SapModel.LoadCases.DirHistNonlinear.SetInitialCase(name,initialCase)

    def define_loadCases_DirHistNonlinear_SetLoads(self,name,NumberLoads,LoadType,LoadName,Func,SF=None,
                                                   TF=None,AT=None,CSys=None,Ang=None):
        """
        ---This function sets the load data for the specified analysis case---
        inputs:
        name(str)-The name of an existing nonlinear direct integration time history load case.
        NumberLoads(int)-The number of loads assigned to the specified analysis case.
        LoadType(str list)-This is a str list that includes Load or Accel, indicating the type of each load
            assigned to the load case.
        LoadName(str list)-This is a str list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.
            If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of the load.
        Func(str list)-This is a str list that includes the name of the time history function associated with each load.
        SF(float list)-This is a str list that includes the scale factor of each load assigned to the load case.
            [L/s2] for U1 U2 and U3; otherwise unitless
        TF(float list)-This is a str list that includes the time scale factor of each load assigned to the load case.
        AT(float list)-This is a str list that includes the arrival time of each load assigned to the load case.
        CSys(str float)-This is a str list that includes the name of the coordinate system associated with each load.
            If this item is a blank string, the Global coordinate system is assumed.This item applies only when the
            LoadType item is Accel.
        Ang(float list)-This is a float list that includes the angle between the acceleration local 1 axis and
            the +X-axis of the coordinate system specified by the CSys item. The rotation is about the Z-axis
            of the specified coordinate system. [deg] This item applies only when the LoadType item is Accel.
        """
        if SF==None:
            SF=[1.0 for each in range(NumberLoads)]
        if TF==None:
            TF=[1.0 for each in range(NumberLoads)]
        if AT==None:
            AT=[0.0 for each in range(NumberLoads)]
        if CSys==None:
            CSys=["Global" for each in range(NumberLoads)]
        if Ang == None:
            Ang=[0.0 for each in range(NumberLoads)]
        self.SapModel.LoadCases.DirHistNonlinear.SetLoads(name,NumberLoads,LoadType,LoadName,Func,SF,TF,AT,CSys,Ang)

    def define_loadCases_DirHistNonlinear_SetMassSource(self,name,source=""):
        """
        ---This function sets the mass source to be used for the specified load case.---
        inputs:
        name(str)-The name of an existing nonlinear direct integration time history load case.
        source(str)-This is the name of an existing mass source or a blank string. Blank indicates to use the mass
            source from the previous load case or the default mass source if the load case starts from zero initial
            conditions.
        """
        self.SapModel.LoadCases.DirHistNonlinear.SetMassSource(name,source)

    def define_loadCases_DirHistNonlinear_SetSolControlParameters(self,name,DTMax=0,DTMin=0,MaxIterCS=10,MaxIterNR=40,
                TolConvD=1e-4,UseEventStepping=False,TolEventD=0.01,MaxLineSearchPerIter=20,TolLineSearch=0.1,
                                                                  LineSearchStepFact=1.618):
        """
        ---This function sets the solution control parameters for the specified load case---
        inputs:
        name(str)-The name of an existing nonlinear direct integration time history load case.
        DTMax(float)-The maximum substep size
        DTMin(float)-The minimum substep size.
        MaxIterCS(int)-The maximum constant-stiffness iterations per step.
        MaxIterNR(int)-The maximum Newton_Raphson iterations per step.
        TolConvD(float)-The relative iteration convergence tolerance.
        UseEventStepping(bool)-This item is True if event-to-event stepping is used.
        TolEventD(float)-The relative event lumping tolerance.
        MaxLineSearchPerIter(int)-The maximum number of line searches per iteration.
        TolLineSearch(float)-The relative line-search acceptance tolerance.
        LineSearchStepFact(float)-The line-search step factor.
        """
        self.SapModel.LoadCases.DirHistNonlinear.SetSolControlParameters(name,DTMax,DTMin,MaxIterCS,MaxIterNR,
                TolConvD,UseEventStepping,TolEventD,MaxLineSearchPerIter,TolLineSearch,LineSearchStepFact)

    def define_loadCases_DirHistNonlinear_SetTimeIntegration(self,name,IntegrationType=4):
        """
         ---This function sets time integration data for the specified load case---
         inputs:
         name(str)-The name of an existing linear direct integration time history load case.
         IntegrationType(int)-This is 1, 2, 3, 4 or 5, indicating the time integration type.1 = Newmark,2 = Wilson,
         3 = Collocation,4 = Hilber-Hughes-Taylor,5 = Chung and Hulbert
         """
        Alpha, Beta, Gamma, Theta, m = 0.0, 0.0, 0.0, 0.0, 0.0
        if IntegrationType == 1:
            Gamma, Beta = 0.5, 0.25
        if IntegrationType == 2:
            Theta = 1.0
        if IntegrationType == 3:
            Gamma, Beta, Theta = 0.5, 0.1667, 1.0
        if IntegrationType == 4:
            Alpha = 0.0
        if IntegrationType == 5:
            Gamma, Beta, Alpha, m = 0.5, 0.25, 0.0, 0.0
        self.SapModel.LoadCases.DirHistNonlinear.SetTimeIntegration(name,IntegrationType,Alpha,Beta,Gamma,Theta,m)

    def define_loadCases_DirHistNonlinear_SetTimeStep(self,name,nstep,DT):
        """
        ---This function sets the time step data for the specified load case---
        inputs:
        name(str)-The name of an existing linear direct integration time history load case.
        nstep(int)-The number of output time steps.
        DT(float)-The output time step size.
        """
        self.SapModel.LoadCases.DirHistNonlinear.SetTimeStep(name,nstep,DT)

    def define_loadCases_ModalEigen_SetCase(self,name):
        """
        ---This function initializes a modal eigen load case---
        inputs:
        name(str)-The name of an existing or new load case.
        """
        self.SapModel.LoadCases.ModalEigen.SetCase(name)

    def define_loadCases_ModalEigen_SetInitialCase(self,name,initialCase=None):
        """
        ---This function sets the initial condition for the specified load case---
        inputs:
        name(str)-The name of an existing modal eigen load case.
        initialCase-This is blank, None, or the name of an existing analysis case. This item specifies if the
            load case starts from zero initial conditions, that is, an unstressed state, or if it starts using
            the stiffness that occurs at the end of a nonlinear static or nonlinear direct integration time
            history load case.If the specified initial case is a nonlinear static or nonlinear direct integration
            time history load case, the stiffness at the end of that case is used. If the initial case is anything
            else, zero initial conditions are assumed.
        """
        self.SapModel.LoadCases.ModalEigen.SetInitialCase(name,initialCase)

    def define_loadCases_ModalEigen_SetLoads(self,name,NumberLoads,LoadType,LoadName,TargetPar=None,StaticCorrect=None):
        """
        ---This function sets the load data for the specified analysis case---
        inputs:
        name(str)-The name of an existing modal eigen load case.
        NumberLoads(int)-The number of loads assigned to the specified analysis case.
        LoadTyp(str list)-This is a str list that includes Load, Accel or Link, indicating the type of each load
            assigned to the load case.
        LoadName(str list)-This is a str list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.If the LoadType item
            is Accel, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction of the load.If the LoadType
            item is Link, this item is not used.
        TargetPar(float list)-This is a float list that includes the target mass participation ratio.
        StaticCorrect(int list)-This is a int list that includes either 0 or 1, indicating if static correction
            modes are to be calculated.
        """
        if TargetPar==None:
            TargetPar=[99 for each in range(NumberLoads)]
        if StaticCorrect==None:
            StaticCorrect=[0 for each in range(NumberLoads)]
        self.SapModel.LoadCases.ModalEigen.SetLoads(name,NumberLoads,LoadType,LoadName,TargetPar,StaticCorrect)

    def define_loadCases_ModalEigen_SetNumberModes(self,name,MaxModes=12,MinModes=1):
        """
        ---This function sets the number of modes requested for the specified load case---
        inputs:
        name(str)-The name of an existing modal eigen load case.
        MaxModes(int)-The maximum number of modes requested.
        MinModes(int)-The minimum number of modes requested.
        """
        self.SapModel.LoadCases.ModalEigen.SetNumberModes(name,MaxModes,MinModes)

    def define_loadCases_ModalEigen_SetParameters(self,name,EigenShiftFreq=0,EigenCutOff=0,EigenTol=1e-9,
                                                  AllowAutoFreqShift=1):
        """
        ---This function sets various parameters for the specified modal eigen load case---
        inputs:
        name(str)-The name of an existing modal eigen load case.
        EigenShiftFreq(float)-The eigenvalue shift frequency. [cyc/s]
        EigenCutOff(float)-The eigencutoff frequency radius. [cyc/s]
        EigenTol(float)-The relative convergence tolerance for eigenvalues.
        AllowAutoFreqShift(int)-This is either 0 or 1, indicating if automatic frequency shifting is allowed.
            0 = Automatic frequency shifting is NOT allowed,1 = Automatic frequency shifting is allowed
        """
        self.SapModel.LoadCases.ModalEigen.SetParameters(name,EigenShiftFreq,EigenCutOff,EigenTol,AllowAutoFreqShift)

    def define_loadCases_ModalRitz_SetCase(self,name):
        """
        ---This function initializes a modal ritz load case---
        inputs:
        name(str)-The name of an existing or new load case.
        """
        self.SapModel.LoadCases.ModalRitz.SetCase(name)

    def define_loadCases_ModalRitz_SetInitialCase(self,name,initialCase=None):
        """
        ---This function sets the initial condition for the specified load case---
        inputs:
        name(str)-The name of an existing modal eigen load case.
        initialCase-This is blank, None, or the name of an existing analysis case. This item specifies if the
            load case starts from zero initial conditions, that is, an unstressed state, or if it starts using
            the stiffness that occurs at the end of a nonlinear static or nonlinear direct integration time
            history load case.If the specified initial case is a nonlinear static or nonlinear direct integration
            time history load case, the stiffness at the end of that case is used. If the initial case is anything
            else, zero initial conditions are assumed.
        """
        self.SapModel.LoadCases.ModalRitz.SetInitialCase(name,initialCase)

    def define_loadCases_ModalRitz_SetLoads(self,name,NumberLoads,LoadType,LoadName,RitzMaxCyc=None,TargetPar=None):
        """
        ---This function sets the load data for the specified analysis case---
        inputs:
        name(str)-The name of an existing modal ritz load case.
        NumberLoads(int)-The number of loads assigned to the specified analysis case.
        LoadType(str list)-This is a str list that includes Load, Accel or Link, indicating the type of each
            load assigned to the load case.
        LoadName(str list)-This is a str list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.
            If the LoadType item is Accel, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction of the load.
            If the LoadType item is Link, this item is not used.
        RitzMaxCyc(int list)-This is a int list that includes the maximum number of generation cycles to be performed
            for the specified ritz starting vector. A value of 0 means there is no limit on the number of cycles.
        TargetPar(float list)-This is a float list that includes the target dynamic participation ratio.
        """
        if RitzMaxCyc==None:
            RitzMaxCyc=[0 for each in range(NumberLoads)]
        if TargetPar==None:
            TargetPar=[99 for each in range(NumberLoads)]
        self.SapModel.LoadCases.ModalRitz.SetLoads(name,NumberLoads,LoadType,LoadName,RitzMaxCyc,TargetPar)

    def define_loadCases_ModalRitz_SetNumberModes(self,name,MaxModes=12,MinModes=1):
        """
        ---This function sets the number of modes requested for the specified load case---
        inputs:
        name(str)-The name of an existing modal ritz load case.
        MaxModes(int)-The maximum number of modes requested.
        MinModes(int)-The minimum number of modes requested.
        """
        self.SapModel.LoadCases.ModalRitz.SetNumberModes(name,MaxModes,MinModes)

    def define_loadCases_ModHistLinear_SetCase(self,name):
        """
        ---This function initializes a linear modal history analysis case---
        name(str)-The name of an existing or new load case.
        """
        self.SapModel.LoadCases.ModHistLinear.SetCase(name)

    def define_loadCases_ModHistLinear_SetDampConstant(self,name,Damp):
        """
        ---This function sets constant modal damping for the specified load case---
        inputs:
        name(str)-The name of an existing linear modal history analysis case.
        Damp(float)-The constant damping for all modes (0 <= Damp < 1).
        """
        self.SapModel.LoadCases.ModHistLinear.SetDampConstant(name,Damp)

    def define_loadCases_ModHistLinear_SetDampInterpolated(self,name,DampType,NumberItems,Time,Damp):
        """
        ---This function sets interpolated modal damping data for the specified load case---
        inputs:
        name(str)-The name of an existing linear modal history analysis case.
        DampType(int)-This is 5 or 6, indicating the interpolated modal damping type.
            5 = Interpolated damping by period,6 = Interpolated damping by frequency
        NumberItems(int)-The number of Time and Damp pairs.
        Time(float list)-This is a float list that includes the period or the frequency, depending on the
            value of the DampType item. [s] for DampType = 5 and [cyc/s] for DampType = 6
        Damp(float list)-This is a float list that includes the damping for the specified period of frequency
            (0 <= Damp < 1).
        """
        self.SapModel.LoadCases.ModHistLinear.SetDampInterpolated(name,DampType,NumberItems,Time,Damp)

    def define_loadCases_ModHistLinear_SetDampProportional(self,name,DampType,Dampa,Dampb,Dampf1=0,Dampf2=0,
                                                           Dampd1=0,Dampd2=0):
        """
         ---This function sets proportional modal damping data for the specified load case---
         inputs:
         name(str)-The name of an existing linear direct integration time history load case.
         DampType(int)-This is 1, 2 or 3, indicating the proportional modal damping type.1 = Mass and stiffness
             proportional damping by direct specification,2 = Mass and stiffness proportional damping by period
             3 = Mass and stiffness proportional damping by frequency
         Dampa(float)-The mass proportional damping coefficient. This item applies only when DampType = 1.
         Dampb(float)-The stiffness proportional damping coefficient. This item applies only when DampType = 1.
         Dampf1(float)-This is the period or the frequency (depending on the value of the DampType item) for point 1.
             [s] for DampType = 2 and [cyc/s] for DampType = 3
         Dampf2(float)-This is either the period or the frequency (depending on the value of the DampType item)
             for point 2. [s] for DampType = 2 and [cyc/s] for DampType = 3
         Dampd1(float)-This is the damping at point 1 (0 <= Dampd1 < 1).This item applies only when DampType = 2 or 3.
         Dampd2(float)-This is the damping at point 2 (0 <= Dampd2 < 1).This item applies only when DampType = 2 or 3.
         """
        self.SapModel.LoadCases.ModHistLinear.SetDampProportional(name,DampType,Dampa,Dampb,Dampf1,Dampf2,Dampd1,Dampd2)

    def define_loadCases_ModHistLinear_SetLoads(self,name,NumberLoads,LoadType,LoadName,Func,SF=None,
                                                   TF=None,AT=None,CSys=None,Ang=None):
        """
        ---This function sets the load data for the specified analysis case---
        inputs:
        name(str)-The name of an existing nonlinear direct integration time history load case.
        NumberLoads(int)-The number of loads assigned to the specified analysis case.
        LoadType(str list)-This is a str list that includes Load or Accel, indicating the type of each load
            assigned to the load case.
        LoadName(str list)-This is a str list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.
            If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of the load.
        Func(str list)-This is a str list that includes the name of the time history function associated with each load.
        SF(float list)-This is a str list that includes the scale factor of each load assigned to the load case.
            [L/s2] for U1 U2 and U3; otherwise unitless
        TF(float list)-This is a str list that includes the time scale factor of each load assigned to the load case.
        AT(float list)-This is a str list that includes the arrival time of each load assigned to the load case.
        CSys(str float)-This is a str list that includes the name of the coordinate system associated with each load.
            If this item is a blank string, the Global coordinate system is assumed.This item applies only when the
            LoadType item is Accel.
        Ang(float list)-This is a float list that includes the angle between the acceleration local 1 axis and
            the +X-axis of the coordinate system specified by the CSys item. The rotation is about the Z-axis
            of the specified coordinate system. [deg] This item applies only when the LoadType item is Accel.
        """
        if SF==None:
            SF=[1.0 for each in range(NumberLoads)]
        if TF==None:
            TF=[1.0 for each in range(NumberLoads)]
        if AT==None:
            AT=[0.0 for each in range(NumberLoads)]
        if CSys==None:
            CSys=["GLOBAL" for each in range(NumberLoads)]
        if Ang == None:
            Ang=[0.0 for each in range(NumberLoads)]
        self.SapModel.LoadCases.ModHistLinear.SetLoads(name,NumberLoads,LoadType,LoadName,Func,SF,TF,AT,CSys,Ang)

    def define_loadCases_ModHistLinear_SetModalCase(self,name,modalCase):
        """
        ---This function sets the modal case for the specified analysis case---
        inputs:
        name(str)-The name of an existing linear modal history analysis case.
        modalCase(str)-This is the name of an existing modal load case.
        """
        self.SapModel.LoadCases.ModHistLinear.SetModalCase(name,modalCase)

    def define_loadCases_ModHistLinear_SetTimeStep(self,name,nstep,DT):
        """
        ---This function sets the time step data for the specified load case---
        inputs:
        name(str)-The name of an existing linear modal history analysis case.
        nstep(int)-The number of output time steps.
        DT(float)-The output time step size.
        """
        self.SapModel.LoadCases.ModHistLinear.SetTimeStep(name,nstep,DT)

    def define_loadCases_ModHistNonlinear_SetCase(self,name):
        """
        ---This function initializes a nonlinear modal history analysis case.---
        inputs:
        name(str)-The name of an existing or new load case
        """
        self.SapModel.LoadCases.ModHistNonlinear.SetCase(name)

    def define_loadCases_ModHistNonlinear_SetDampConstant(self,name,damp):
        """
        ---This function sets constant modal damping for the specified load case---
        inputs:
        name(str)-The name of an existing nonlinear modal history analysis case.
        damp(float)-The constant damping for all modes (0 <= Damp < 1).
        """
        self.SapModel.LoadCases.ModHistNonlinear.SetDampConstant(name,damp)

    def define_loadCases_ModHistNonlinear_SetDampInterpolated(self,name,DampType,NumberItems,Time,Damp):
        """
        ---This function sets interpolated modal damping data for the specified load case---
        inputs:
        name(str)-The name of an existing linear modal history analysis case.
        DampType(int)-This is 5 or 6, indicating the interpolated modal damping type.
            5 = Interpolated damping by period,6 = Interpolated damping by frequency
        NumberItems(int)-The number of Time and Damp pairs.
        Time(float list)-This is a float list that includes the period or the frequency, depending on the
            value of the DampType item. [s] for DampType = 5 and [cyc/s] for DampType = 6
        Damp(float list)-This is a float list that includes the damping for the specified period of frequency
            (0 <= Damp < 1).
        """
        self.SapModel.LoadCases.ModHistNonlinear.SetDampInterpolated(name,DampType,NumberItems,Time,Damp)

    def define_loadCases_ModHistNonlinear_SetDampOverrides(self,name,NumberItems,Mode,Damp):
        """
        ---This function sets the modal damping overrides for the specified load case---
        inputs:
        name(str)-The name of an existing nonlinear modal history analysis case.
        NumberItems(int)-The number of Mode and Damp pairs.
        Mode(int list)-This is a int list that includes a mode number.
        Damp(float list)-This is a float list that includes the damping for the specified mode (0 <= Damp < 1).
        """
        self.SapModel.LoadCases.ModHistNonlinear.SetDampOverrides(name,NumberItems,Mode,Damp)

    def define_loadCases_ModHistNonlinear_SetDampProportional(self,name,DampType,Dampa,Dampb,Dampf1=0,
                                                           Dampf2=0,Dampd1=0,Dampd2=0):
        """
         ---This function sets proportional modal damping data for the specified load case---
         inputs:
         name(str)-The name of an existing linear direct integration time history load case.
         DampType(int)-This is 1, 2 or 3, indicating the proportional modal damping type.1 = Mass and stiffness
             proportional damping by direct specification,2 = Mass and stiffness proportional damping by period
             3 = Mass and stiffness proportional damping by frequency
         Dampa(float)-The mass proportional damping coefficient. This item applies only when DampType = 1.
         Dampb(float)-The stiffness proportional damping coefficient. This item applies only when DampType = 1.
         Dampf1(float)-This is the period or the frequency (depending on the value of the DampType item) for point 1.
             [s] for DampType = 2 and [cyc/s] for DampType = 3
         Dampf2(float)-This is either the period or the frequency (depending on the value of the DampType item)
             for point 2. [s] for DampType = 2 and [cyc/s] for DampType = 3
         Dampd1(float)-This is the damping at point 1 (0 <= Dampd1 < 1).This item applies only when DampType = 2 or 3.
         Dampd2(float)-This is the damping at point 2 (0 <= Dampd2 < 1).This item applies only when DampType = 2 or 3.
         """
        self.SapModel.LoadCases.ModHistNonlinear.SetDampProportional(name,DampType,Dampa,Dampb,Dampf1,Dampf2,Dampd1,Dampd2)

    def define_loadCases_ModHistNonlinear_SetInitialCase(self,name,initialCase=None):
        """
        ---This function sets the initial condition for the specified load case---
        inputs:
        name(str)-The name of an existing nonlinear modal history analysis case.
        initialCase-This is blank, None or the name of an existing analysis case. This item specifies if the
            load case starts from zero initial conditions, that is, an unstressed state, or if it continues
            from the end of another nonlinear modal time history load case.If the specified initial case is
            not a nonlinear modal time history load case, zero initial conditions are assumed
        """
        self.SapModel.LoadCases.ModHistNonlinear.SetInitialCase(name,initialCase)

    def define_loadCases_ModHistNonlinear_SetLoads(self,name,NumberLoads,LoadType,LoadName,Func,SF=None,
                                                   TF=None,AT=None,CSys=None,Ang=None):
        """
        ---This function sets the load data for the specified analysis case---
        inputs:
        name(str)-The name of an existing nonlinear direct integration time history load case.
        NumberLoads(int)-The number of loads assigned to the specified analysis case.
        LoadType(str list)-This is a str list that includes Load or Accel, indicating the type of each load
            assigned to the load case.
        LoadName(str list)-This is a str list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.
            If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of the load.
        Func(str list)-This is a str list that includes the name of the time history function associated with each load.
        SF(float list)-This is a str list that includes the scale factor of each load assigned to the load case.
            [L/s2] for U1 U2 and U3; otherwise unitless
        TF(float list)-This is a str list that includes the time scale factor of each load assigned to the load case.
        AT(float list)-This is a str list that includes the arrival time of each load assigned to the load case.
        CSys(str float)-This is a str list that includes the name of the coordinate system associated with each load.
            If this item is a blank string, the Global coordinate system is assumed.This item applies only when the
            LoadType item is Accel.
        Ang(float list)-This is a float list that includes the angle between the acceleration local 1 axis and
            the +X-axis of the coordinate system specified by the CSys item. The rotation is about the Z-axis
            of the specified coordinate system. [deg] This item applies only when the LoadType item is Accel.
        """
        if SF==None:
            SF=[1.0 for each in range(NumberLoads)]
        if TF==None:
            TF=[1.0 for each in range(NumberLoads)]
        if AT==None:
            AT=[0.0 for each in range(NumberLoads)]
        if CSys==None:
            CSys=["GLOBAL" for each in range(NumberLoads)]
        if Ang == None:
            Ang=[0.0 for each in range(NumberLoads)]
        self.SapModel.LoadCases.ModHistNonlinear.SetLoads(name,NumberLoads,LoadType,LoadName,Func,SF,TF,AT,CSys,Ang)

    def define_loadCases_ModHistNonlinear_SetModalCase(self,name,modalCase):
        """
        ---This function sets the modal case for the specified analysis case---
        inputs:
        name(str)-The name of an existing nonlinear modal history analysis case.
        modalCase(str)-This is the name of an existing modal load case
        """
        self.SapModel.LoadCases.ModHistNonlinear.SetModalCase(name,modalCase)

    def define_loadCases_ModHistNonlinear_SetSolControlParameters(self,name,tstat=0,dtmax=0,dtmin=0,ftol=1e-5,
                                                                  etol=1e-5,itmax=100,itmin=2,Cf=1):
        """
        ---This function sets the solution control parameters for the specified load case---
        inputs:
        name(str)-The name of an existing nonlinear modal time history analysis case.
        tstat(float)-The static period.
        dtmax(float)-The maximum substep size.
        dtmin(float)-The minimum substep size.
        ftol(float)-The relative force convergence tolerance.
        etol(float)-The relative energy convergence tolerance
        itmax(int)-The maximum iteration limit.
        itmin(int)-The minimum iteration limit.
        Cf(float)-The convergence factor.
        """
        self.SapModel.LoadCases.ModHistNonlinear.SetSolControlParameters(name,tstat,dtmax,dtmin,ftol,etol,itmax,itmin,Cf)

    def define_loadCases_ModHistNonlinear_SetTimeStep(self,name,nstep,DT):
        """
        ---This function sets the time step data for the specified load case---
        inputs:
        name(str)-The name of an existing nonlinear modal history analysis case.
        nstep(int)-The number of output time steps.
        DT(float)-The output time step size.
        """
        self.SapModel.LoadCases.ModHistNonlinear.SetTimeStep(name,nstep,DT)

    def define_loadCases_ResponseSpectrum_SetCase(self,name):
        """
        ---This function initializes a response spectrum analysis case---
        name(str)-The name of an existing or new load case.
        """
        self.SapModel.LoadCases.ResponseSpectrum.SetCase(name)

    def define_loadCases_ResponseSpectrum_SetDampConstant(self,name,damp):
        """
        ---This function sets constant modal damping for the specified load case---
        inputs:
        name(str)-The name of an existing response spectrum load case.
        damp(float)-The constant damping for all modes (0 <= Damp < 1).
        """
        self.SapModel.LoadCases.ResponseSpectrum.SetDampConstant(name,damp)

    def define_loadCases_ResponseSpectrum_SetDampInterpolated(self,name,DampType,NumberItems,Time,Damp):
        """
        ---This function sets interpolated modal damping data for the specified load case---
        inputs:
        name(str)-The name of an existing response spectrum load case.
        DampType(int)-This is either 5 or 6, indicating the interpolated modal damping type.
            5 = Interpolated damping by period,6 = Interpolated damping by frequency
        NumberItems(int)-The number of Time and Damp pairs
        Time(float list)-This is a float list that includes the period or the frequency depending on the value
            of the DampType item. [s] for DampType = 5 and [cyc/s] for DampType = 6
        Damp(float list)-This is a float list that includes the damping for the specified period of frequency
        (0 <= Damp < 1).
        """
        self.SapModel.LoadCases.ResponseSpectrum.SetDampInterpolated(name,DampType,NumberItems,Time,Damp)

    def define_loadCases_ResponseSpectrum_SetDampOverrides(self,name,NumberItems,Mode,Damp):
        """
        ---This function sets the modal damping overrides for the specified load case---
        inputs:
        name(str)-The name of an existing response spectrum load case.
        NumberItems(int)-The number of Mode and Damp pairs.
        Mode(int list)-This is a int list that includes a mode number.
        Damp(float list)-This is a float list that includes the damping for the specified mode (0 <= Damp < 1).
        """
        self.SapModel.LoadCases.ResponseSpectrum.SetDampOverrides(name,NumberItems,Mode,Damp)

    def define_loadCases_ResponseSpectrum_SetDampProportional(self,name,DampType,Dampa,Dampb,Dampf1=0,
                                                              Dampf2=0,Dampd1=0,Dampd2=0):
        """
        ---This function sets proportional modal damping data for the specified load case---
        inputs:
        name(str)-The name of an existing linear direct integration time history load case.
        DampType(int)-This is 1, 2 or 3, indicating the proportional modal damping type.1 = Mass and stiffness
            proportional damping by direct specification,2 = Mass and stiffness proportional damping by period
            3 = Mass and stiffness proportional damping by frequency
        Dampa(float)-The mass proportional damping coefficient. This item applies only when DampType = 1.
        Dampb(float)-The stiffness proportional damping coefficient. This item applies only when DampType = 1.
        Dampf1(float)-This is the period or the frequency (depending on the value of the DampType item) for point 1.
            [s] for DampType = 2 and [cyc/s] for DampType = 3
        Dampf2(float)-This is either the period or the frequency (depending on the value of the DampType item)
            for point 2. [s] for DampType = 2 and [cyc/s] for DampType = 3
        Dampd1(float)-This is the damping at point 1 (0 <= Dampd1 < 1).This item applies only when DampType = 2 or 3.
        Dampd2(float)-This is the damping at point 2 (0 <= Dampd2 < 1).This item applies only when DampType = 2 or 3.
        """
        self.SapModel.LoadCases.ResponseSpectrum.SetDampProportional(name,DampType,Dampa,Dampb,Dampf1,
                                                              Dampf2,Dampd1,Dampd2)

    def define_loadCases_ResponseSpectrum_SSetDiaphragmEccentricityOverride(self,name,Diaph,Eccen,Delete=False):
        """
        ---This function assigns diaphragm eccentricity overrides for response spectrum load cases---
        inputs:
        name(str)-The name of an existing response spectrum load case.
        Diaph(int)-The name of an existing special rigid diaphragm constraint, that is, a diaphragm constraint
            with the following features:1. The constraint type is CONSTRAINT_DIAPHRAGM = 2.2. The constraint
            coordinate system is Global.3. The constraint axis is Z.
        Eccen(float)-The eccentricity applied to the specified diaphragm. [L]
        Delete(bool)-If this item is True, the eccentricity override for the specified diaphragm is deleted.
        """
        self.SapModel.LoadCases.ResponseSpectrum.SetDiaphragmEccentricityOverride(name,Diaph,Eccen,Delete)

    def define_loadCases_ResponseSpectrum_SetDirComb(self,name,MyType,SF=0):
        """
        ---This function sets the directional combination option for the specified load case---
        inputs:
        name(str)-The name of an existing response spectrum load case
        MyType(int)-This is 1, 2, or 3,  indicating the directional combination option.1 = SRSS,2 = ABS,3 = CQC3
        SF(float)-This item applies only when MyType = 2. It is the ABS scale factor.
        """
        self.SapModel.LoadCases.ResponseSpectrum.SetDirComb(name,MyType,SF)

    def define_loadCases_ResponseSpectrum_SetEccentricity(self,name,Eccen):
        """
        ---This function sets the eccentricity ratio that applies to all diaphragms for the specified load case---
        inputs:
        name(str)-The name of an existing response spectrum load case.
        Eccen(float)-The eccentricity ratio that applies to all diaphragms.
        """
        self.SapModel.LoadCases.ResponseSpectrum.SetEccentricity(name,Eccen)

    def define_loadCases_ResponseSpectrum_SetLoads(self,name,NumberLoads,LoadName,Func,SF=None,
                                                   CSys=None,Ang=None):
        """
        ---This function sets the load data for the specified analysis case---
        inputs:
        name(str)-The name of an existing nonlinear direct integration time history load case.
        NumberLoads(int)-The number of loads assigned to the specified analysis case.
        LoadName(str list)-This is a str list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.
            If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of the load.
        Func(str list)-This is a str list that includes the name of the time history function associated with each load.
        SF(float list)-This is a str list that includes the scale factor of each load assigned to the load case.
            [L/s2] for U1 U2 and U3; otherwise unitless
        CSys(str float)-This is a str list that includes the name of the coordinate system associated with each load.
            If this item is a blank string, the Global coordinate system is assumed.This item applies only when the
            LoadType item is Accel.
        Ang(float list)-This is a float list that includes the angle between the acceleration local 1 axis and
            the +X-axis of the coordinate system specified by the CSys item. The rotation is about the Z-axis
            of the specified coordinate system. [deg] This item applies only when the LoadType item is Accel.
        """
        if SF==None:
            SF=[1.0 for each in range(NumberLoads)]
        if CSys==None:
            CSys=["GLOBAL" for each in range(NumberLoads)]
        if Ang == None:
            Ang=[0.0 for each in range(NumberLoads)]
        self.SapModel.LoadCases.ResponseSpectrum.SetLoads(name,NumberLoads,LoadName,Func,SF,CSys,Ang)

    def define_loadCases_ResponseSpectrum_SetModalCase(self,name,ModalCase):
        """
        ---This function sets the modal case for the specified analysis case---
        inputs:
        name(str)-The name of an existing response spectrum load case.
        ModalCase(str)-This is the name of an existing modal load case. It specifies the modal load case on
            which any mode-type load assignments to the specified load case are based.
        """
        self.SapModel.LoadCases.ResponseSpectrum.SetModalCase(name,ModalCase)

    def define_loadCases_ResponseSpectrum_SetModalComb_1(self,name,MyType,F1=1,F2=0,PeriodicRigidCombType=1,td=60):
        """
        ---This function sets the modal combination option for the specified load case---
        inputs:
        name(str)-The name of an existing response spectrum load case.
        MyType(int)-This is 1, 2, 3, 4, 5 or 6, indicating the modal combination option.1 = CQC,2 = SRSS,3 = Absolute
            4 = GMC,5 = NRC 10 percent,6 = Double sum
        F1(float)-The GMC f1 factor. This item does not apply when MyType = 3. [cyc/s]
        F2(float)-The GMC f2 factor. This item does not apply when MyType = 3. [cyc/s]
        PeriodicRigidCombType(int)-This is 1 or 2, indicating the periodic plus rigid modal combination option.
            1 = SRSS,2 = Absolute
        td(float)-This item applies only when MyType = 6. It is the factor td. [s]
        """
        self.SapModel.LoadCases.ResponseSpectrum.SetModalComb_1(name,MyType,F1,F2,PeriodicRigidCombType,td)

    def define_SourceMass_SetDefault(self,name):
        """
        ---This function sets the default mass source---
        inputs:
        name(str)-The name of the mass source to be flagged as the default mass source.
        """
        self.SapModel.SourceMass.SetDefault(name)

    def define_SourceMass_SetMassSource(self,name,MassFromElements,MassFromMasses,MassFromLoads,
                                                  IsDefault,NumberLoads=0,LoadPat=[],SF=[]):
        """
        ---This function adds a new mass source to the model or reinitializes an existing mass source---
        inputs:
        name(str)-The mass source name.
        MassFromElements(bool)-If this item is True then element self mass is included in the mass.
        MassFromMasses(bool)-If this item is True then assigned masses are included in the mass.
        MassFromLoads(bool)-If this item is True then specified load patterns are included in the mass.
        IsDefault(bool)-If this item is True then the mass source is the default mass source.  Only one
            mass source can be the default mass source so when this assignment is True all other mass sources
            are automatically set to have the IsDefault flag False.
        NumberLoads(int)-The number of load patterns specified for the mass source.  This item is only applicable
            when the MassFromLoads item is True.
        LoadPat(str list)-This is an array of load pattern names specified for the mass source.
        SF(float list)-This is an array of load pattern multipliers specified for the mass source.
        """
        self.SapModel.SourceMass.SetMassSource(name,MassFromElements,MassFromMasses,MassFromLoads,
                                                  IsDefault,NumberLoads,LoadPat,SF)

    def define_RespCombo_Add(self,name,comboType):
        """
        ---This function adds a new load combination---
        inputs:
        name(str)-The name of a new load combination.
        comboType(int)-This is 0, 1, 2, 3 or 4 indicating the load combination type.0 = Linear Additive,
            1 = Envelope,2 = Absolute Additive,3 = SRSS,4 = Range Additive
        """
        self.SapModel.RespCombo.Add(name,comboType)

    def define_RespCombo_SetCaseList(self,name,CNameType,CName,SF):
        """
        ---This function adds or modifies one load case or response combination in the list of
        cases included in the load combination specified by the Name item.---
        inputs:
        name(str)-The name of an existing load combination.
        CNameType(int)-This is one of the following items in the eCNameType enumeration:LoadCase = 0,
            LoadCombo = 1,This item indicates if the CName item is an load case (LoadCase) or a load
            combination (LoadCombo).
        CName(str)-The name of the load case or load combination to be added to or modified in the combination
            specified by the Name item. If the load case or combination already exists in the combination specified
            by the Name item, the scale factor is modified as indicated by the SF item for that load case or
            combination. If the analysis case or combination does not exist in the combination specified by the
            Name item, it is added.
        SF(float)-The scale factor multiplying the case or combination indicated by the CName item.
        """
        self.SapModel.RespCombo.SetCaseList(name,CNameType,CName,SF)

    def assign_PointObj_AddCartesian(self,x,y,z,Name="",UserName="",CSys="Global",MergeOff=False,MergeNumber=0):
        """
        ---This function adds a point object to a model.The added point object will be tagged as a Special
        Point except if it was merged with another point object. Special points are allowed to exist in
        the model with no objects connected to them.---
        inputs:
        x,y,z-The X,Y,Z(float)-coordinates of the added point object in the specified coordinate system. [L]
        Name(str)-This is the name that the program ultimately assigns for the point object. If no UserName
            is specified, the program assigns a default name to the point object. If a UserName is specified
            and that name is not used for another point, the UserName is assigned to the point; otherwise a
            default name is assigned to the point.If a point is merged with another point, this will be the
            name of the point object with which it was merged.
        UserName(str)-This is an optional user specified name for the point object. If a UserName is specified
            and that name is already used for another point object, the program ignores the UserName.
        CSys(str)-The name of the coordinate system in which the joint coordinates are defined.
        MergeOff(bool)-If this item is False, a new point object that is added at the same location as an existing
            point object will be merged with the existing point object (assuming the two point objects have the
            same MergeNumber) and thus only one point object will exist at the location.If this item is True, the
            points will not merge and two point objects will exist at the same location.
        MergeNumber(int)-Two points objects in the same location will merge only if their merge number assignments
            are the same. By default all pointobjects have a merge number of zero.
        """
        self.SapModel.PointObj.AddCartesian(x,y,z,Name,UserName,CSys,MergeOff,MergeNumber)

    def assign_PointObj_AddCylindrical(self,r,theta,z,Name="",UserName="",CSys="Global",MergeOff=False,MergeNumber=0):
        """
        ---This function adds a point object to a model. The added point object will be tagged as a Special Point
        except if it was merged with another point object. Special points are allowed to exist in the model with
        no objects connected to them---
        inputs:
        r(float)-The radius for the added point object in the specified coordinate system. [L]
        theta(float)-The angle for the added point object in the specified coordinate system. The angle is measured
            in the XY plane from the positive global X axis. When looking in the XY plane with the positive Z axis
            pointing toward you, a positive Theta angle is counter clockwise. [deg]
        z(float)-The Z-coordinate of the added point object in the specified coordinate system. [L]
        Name(str)-This is the name that the program ultimately assigns for the point object. If no UserName
            is specified, the program assigns a default name to the point object. If a UserName is specified
            and that name is not used for another point, the UserName is assigned to the point; otherwise a
            default name is assigned to the point.If a point is merged with another point, this will be the
            name of the point object with which it was merged.
        UserName(str)-This is an optional user specified name for the point object. If a UserName is specified
            and that name is already used for another point object, the program ignores the UserName.
        CSys(str)-The name of the coordinate system in which the joint coordinates are defined.
        MergeOff(bool)-If this item is False, a new point object that is added at the same location as an existing
            point object will be merged with the existing point object (assuming the two point objects have the
            same MergeNumber) and thus only one point object will exist at the location.If this item is True, the
            points will not merge and two point objects will exist at the same location.
        MergeNumber(int)-Two points objects in the same location will merge only if their merge number assignments
            are the same. By default all pointobjects have a merge number of zero.
        """
        self.SapModel.PointObj.AddCartesian(r,theta,z,Name,UserName,CSys,MergeOff,MergeNumber)

    def assign_PointObj_AddSpherical(self,r,a,b,Name="",UserName="",CSys="Global",MergeOff=False,MergeNumber=0):
        """
        ---This function adds a point object to a model. The added point object will be tagged as a Special Point
        except if it was merged with another point object. Special points are allowed to exist in the model with
        no objects connected to them---
        inputs:
        r(float)-The radius for the added point object in the specified coordinate system. [L]
        a(float)-The plan angle for the added point object in the specified coordinate system. This angle is
            measured in the XY plane from the positive global X axis. When looking in the XY plane with the
            positive Z axis pointing toward you, a positive a angle is counterclockwise. [deg]
        b(float)-The elevation angle for the added point object in the specified coordinate system. This angle
            is measured in an X'Z plane that is perpendicular to the XY plane with the positive X' axis oriented
            at angle a from the positive global X axis. Angle b is measured from the positive global Z axis. When
            looking in the X’Z plane with the positive Y' axis pointing toward you, a positive b angle is counter
            clockwise. [deg]
        Name(str)-This is the name that the program ultimately assigns for the point object. If no UserName
            is specified, the program assigns a default name to the point object. If a UserName is specified
            and that name is not used for another point, the UserName is assigned to the point; otherwise a
            default name is assigned to the point.If a point is merged with another point, this will be the
            name of the point object with which it was merged.
        UserName(str)-This is an optional user specified name for the point object. If a UserName is specified
            and that name is already used for another point object, the program ignores the UserName.
        CSys(str)-The name of the coordinate system in which the joint coordinates are defined.
        MergeOff(bool)-If this item is False, a new point object that is added at the same location as an existing
            point object will be merged with the existing point object (assuming the two point objects have the
            same MergeNumber) and thus only one point object will exist at the location.If this item is True, the
            points will not merge and two point objects will exist at the same location.
        MergeNumber(int)-Two points objects in the same location will merge only if their merge number assignments
            are the same. By default all pointobjects have a merge number of zero.
        """
        self.SapModel.PointObj.AddSpherical(r,a,b,Name,UserName,CSys,MergeOff,MergeNumber)

    def assign_PointObj_ChangeName(self,name,newName):
        """
        ---The function returns zero if the new name is successfully applied, otherwise it returns a nonzero value---
        inputs:
        name(str)-The existing name of a point object.
        newName(str)-The new name for the point object.
        """
        self.SapModel.PointObj.ChangeName(name,newName)

    def assign_PointObj_Count(self):
        """
        ---This function returns the total number of point objects in the model---
        """
        pointNum=self.SapModel.PointObj.Count()
        return pointNum

    def assign_PointObj_GetCommonTo(self,name):
        """
        ---This function returns the total number of objects (line, area, solid and link) that connect to the
        specified point object.---
        inputs:
        name(str)-The name of a point object or a group depending on the value selected for ItemType item.
        return:
        [numberItem,CommonTo]
        CommonTo(int)-The total number of objects (line, area, solid and link) that connect to the specified point object.
        """
        numbers=self.SapModel.PointObj.GetCommonTo(name)
        return numbers

    def assign_PointObj_GetConnectivity(self,name):
        """
        ---This function returns a list of objects connected to a specified point object---
        inputs:
        name(str)-The name of an existing point object.
        return:list
        [numberItem,totalObject,objectTypeList,objectNameList,_]

        """
        results=self.SapModel.PointObj.GetConnectivity(name)
        return results

    def assign_PointObj_GetConstraint(self,name):
        """
        ---This function returns a list of constraint assignments made to one or more specified point objects.---
        inputs:
        name(str)-The name of an existing point object or group, depending on the value of the ItemType item.
        return:
        [numberItem,totalNumConstrait,pointNameturple,constraintNameTurple]
        """
        result=self.SapModel.PointObj.GetConstraint(name)
        return result

    def assign_PointObj_GetCoordCartesian(self,name,Csys="Global"):
        """
        --- If successful, the function returns the x, y and z coordinates of the specified point object in the
        Present Units. The coordinates are reported in the coordinate system specified by Csys.---
        inputs:
        name(str)-The name of a defined point object.
        Csys(str)-The name of a defined coordinate system. If Csys is not specified, the Global coordinate s
            ystem is assumed.
        return:
        x,y,z(float)-The X,Y,Z-coordinate of the specified point object in the specified coordinate system. [L]
        [numItem,x,y,z]
        """
        x,y,z=0.0,0.0,0.0
        result=self.SapModel.PointObj.GetCoordCartesian(name,x,y,z,Csys)
        return result

    def assign_PointObj_GetCoordCylindrical(self,name,Csys="Global"):
        """
        ---If successful, the function returns the r, theta and z coordinates of the specified point object in
        the Present Units. The coordinates are reported in the coordinate system specified by CSys.---
        inputs:
        name(str)-The name of a defined point object.
        Csys(str)-The name of a defined coordinate system. If Csys is not specified, the Global coordinate s
            ystem is assumed.
        return:
        [numItem,r,theta,z]
        r(float)-The radius for the specified point object in the specified coordinate system. [L]
        Theta(float)-The angle for the specified point object in the specified coordinate system. The angle is
            measured in the XY plane from the positive X axis. When looking in the XY plane with the positive
            Z axis pointing toward you, a positive Theta angle is counter clockwise [deg]
        z(float)-The Z-coordinate of the specified point object in the specified coordinate system. [L]
        """
        r,theta,z=0,0,0
        result=self.SapModel.PointObj.GetCoordCylindrical(name,r,theta,z,Csys)
        return result

    def assign_PointObj_GetCoordSpherical(self,name,Csys="Global"):
        """
        ---If successful, the function returns the r, a and b coordinates of the specified point object in the
        Present Units. The coordinates are reported in the coordinate system specified by CSys.---
        inputs:
        name(str)-The name of an existing point object.
        Csys(str)-The name of a defined coordinate system. If Csys is not specified, the Global coordinate s
            ystem is assumed.
        return:
        [numItem,r,a,b]
        r(float)-The radius for the point object in the specified coordinate system. [L]
        a(float)-The plan angle for the point object in the specified coordinate system. This angle is measured
            in the XY plane from the positive global X axis. When looking in the XY plane with the positive Z axis
            pointing toward you, a positive a angle is counter clockwise. [deg]
        b(float)-The elevation angle for the point object in the specified coordinate system. This angle is measured
            in an X'Z plane that is perpendicular to the XY plane with the positive X' axis oriented at angle a from
            the positive global X axis. Angle b is measured from the positive global Z axis. When looking in the X’Z
            plane with the positive Y' axis pointing toward you, a positive b angle is counter clockwise. [deg]
        """
        r,a,b=0,0,0
        result =self.SapModel.PointObj.GetCoordSpherical(name,r,a,b,Csys)
        return result

    def assign_PointObj_GetGroupAssign(self,name):
        """
        ---This function retrieves the names of the groups to which a specified point object is assigned---
        inputs:
        name(str)-The name of an existing point object.
        return:
        [numberItem,numberGroups,Groups]
        NumberGroups(int)-The number of group names retrieved.
        Groups(str)-The names of the groups to which the point object is assigned.
        """
        result=self.SapModel.PointObj.GetGroupAssign(name)
        return result

    def assign_PointObj_GetLoadDispl(self,name,ItemType=0):
        """
        ---This function retrieves the ground displacement load assignments to point objects---
        inputs:
        name(str)-The name of an existing point object or group, depending on the value of the ItemType item.
        ItemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0
            Group = 1
            SelectedObjects = 2
            If this item is Object, the load assignments are retrieved for the point object specified by the Name item.
            If this item is Group, the assignments are retrieved for all point objects in the group specified by the
            Name item.
            If this item is SelectedObjects, the load assignments are retrieved for all selected point objects,
            and the Name item is ignored.
        return:
        [numberItem,NumberItems, PointName, LoadPat, LCStep, CSys, U1, U2, U3, R1, R2, R3]
        NumberItems(int)-This is the total number of joint ground displacement assignments returned.
        PointName(str list)-This is an array that includes the name of the point object to which the specified ground
            displacement assignment applies
        LoadPat(str list)-This is an array that includes the name of the load pattern for the ground displacement load
        LCStep(int list)-This is an array that includes the load pattern step for the ground displacement load. In most
            cases, this item does not apply and will be returned as 0
        CSys(str list)-This is an array that includes the name of the coordinate system for the ground displacement
            load. This is Local or the name of a defined coordinate system
        U1(float list)-This is an array that includes the assigned translational ground displacement in the local
            1-axis or coordinate system X-axis direction, depending on the specified CSys. [L]
        U2(float list)-This is an array that includes the assigned translational ground displacement in the local
            2-axis or coordinate system Y-axis direction, depending on the specified CSys. [L]
        U3(float list)-This is an array that includes the assigned translational ground displacement in the local
            3-axis or coordinate system Y-axis direction, depending on the specified CSys. [L]
        R1(float list)-This is an array that includes the assigned rotational ground displacement about the local
            1-axis or coordinate system X-axis, depending on the specified CSys. [rad]
        R2(float list)-This is an array that includes the assigned rotational ground displacement about the local
            2-axis or coordinate system X-axis, depending on the specified CSys. [rad]
        R3(float list)-This is an array that includes the assigned rotational ground displacement about the local
            3-axis or coordinate system X-axis, depending on the specified CSys. [rad]
        """
        NumberItems=0
        PointName=[]
        LoadPat=[]
        LCStep=[]
        CSys=[]
        U1,U2,U3,R1,R2,R3=[],[],[],[],[],[]

        result=self.SapModel.PointObj.GetLoadDispl(name,NumberItems, PointName, LoadPat, LCStep, CSys,
                                                   U1, U2, U3, R1, R2, R3,ItemType)
        return result

    def assign_PointObj_GetLocalAxes(self,name):
        """
        ---This function retrieves the local axes angles for a point object.---
        inputs:
        name(str)-The name of an existing point object
        return:
        [numberItem,a,b,c,Advanced]
        a,b,c(float)-The local axes of the point are defined by first setting the positive local 1, 2 and 3 axes
            the same as the positive global X, Y and Z axes and then doing the following: [deg]
            1. Rotate about the 3 axis by angle a.
            2. Rotate about the resulting 2 axis by angle b.
            3. Rotate about the resulting 1 axis by angle c.
        Advanced(bool)-This item is True if the point object local axes orientation was obtained using advanced local
            axes parameters.
        """
        result=self.SapModel.PointObj.GetLocalAxes(name)
        return result

    def assign_PointObj_GetMass(self,name):
        """
        ---This function retrieves the point mass assignment values for a point object. The masses are always
        returned in the point local coordinate system.---
        inputs:
        name(str)-The name of an existing point object
        return:
        m(float list)-This is a foat list of six mass assignment values.
            Value(0) = U1 [M]
            Value(1) = U2 [M]
            Value(2) = U3 [M]
            Value(3) = R1 [ML2]
            Value(4) = R2 [ML2]
            Value(5) = R3 [ML2]
        """
        result=self.SapModel.PointObj.GetMass(name)
        return result

    def assign_PointObj_GetNameList(self):
        """
        ---This function retrieves the names of all defined point objects---
        return:
        []
        NumberNames(int)-The number of point object names retrieved by the program.
        MyName(str list)-This is a one-dimensional list of point object names.
        """
        result=self.SapModel.PointObj.GetNameList()
        return result

    def assign_PointObj_GetRestraint(self,name):
        """
        ---This function retrieves the restraint assignments for a point object. The restraint assignments
        are always returned in the point local coordinate system.---
        inputs:
        name(str)-The name of an existing point object.
        return:
        value
        """
        result=self.SapModel.PointObj.GetRestraint(name)
        return result


    def assign_PointObj_GetSpring(self,name):
        """
        ---This function retrieves uncoupled spring stiffness assignments for a point object, that is,
        it retrieves the diagonal terms in the 6x6 spring matrix for the point object---
        inputs:
        name(str)-The name of an existing point object.
        return:
        [numberItem,k]
        k(float list)-This is a float list of six spring stiffness values.Value(0) = U1 [F/L],Value(1) = U2 [F/L],
            Value(2) = U3 [F/L],Value(3) = R1 [FL/rad],Value(4) = R2 [FL/rad],Value(5) = R3 [FL/rad]
        """
        k=[0,0,0,0,0,0]
        result=self.SapModel.PointObj.GetSpring(name,k)
        return result

    def assign_PointObj_GetSpringCoupled(self,name):
        """
        ---This function retrieves coupled spring stiffness assignments for a point object.The spring stiffnesses
        reported are the sum of all springs assigned to the point object. The spring stiffness values are reported
        in the point local coordinate system.---
        input:
        name(str)-The name of an existing point object.
        return:

        k(float list)-This is an array of twenty one spring stiffness values.
            Value(0) = U1U1 [F/L]
            Value(1) = U1U2 [F/L]
            Value(2) = U2U2 [F/L]
            Value(3) = U1U3 [F/L]
            Value(4) = U2U3 [F/L]
            Value(5) = U3U3 [F/L]
            Value(6) = U1R1 [F/rad]
            Value(7) = U2R1 [F/rad]
            Value(8) = U3R1 [F/rad]
            Value(9) = R1R1 [FL/rad]
            Value(10) = U1R2 [F/rad]
            Value(11) = U2R2 [F/rad]
            Value(12) = U3R2 [F/rad]
            Value(13) = R1R2 [FL/rad]
            Value(14) = R2R2 [FL/rad]
            Value(15) = U1R3 [F/rad]
            Value(16) = U2R3 [F/rad]
            Value(17) = U3R3 [F/rad]
            Value(18) = R1R3 [FL/rad]
            Value(19) = R2R3 [FL/rad]
            Value(20) = R3R3 [FL/rad]
        """
        k=[0 for each in range(21)]
        result=self.SapModel.PointObj.GetSpringCoupled(name,k)
        return result

    def assign_PointObj_IsSpringCoupled(self,name):
        """
        ---This function indicates if the spring assignments to a point object are coupled, that is, if they have
        off-diagonal terms in the 6x6 spring matrix for the point object---
        inputs:
        name(str)-The name of an existing point object.
        return:
        [numberItem,IsCoupled]
        IsCoupled(bool)-This item is True if the spring assigned to the specified point object is coupled, otherwise
            it is False.
        """
        result=self.SapModel.PointObj.IsSpringCoupled(name)
        return result

    def assign_PointObj_SetConstraint(self,name,ConstraintName,ItemType=0,Replace=True):
        """
        ---This function makes joint constraint assignments to point objects.---
        inputs:
        name(str)-The name of an existing point object or group depending on the value of the ItemType item.
        ConstraintName(str)-The name of an existing joint constraint.
        ItemType(int)-This is one of the following items in the eItemType enumeration:Object = 0,Group = 1,
            SelectedObjects = 2,If this item is Object, the constraint assignment is made to the point object
            specified by the Name item.If this item is Group,  the constraint assignment is made to all point
            objects in the group specified by the Name item.If this item is SelectedObjects, the constraint
            assignment is made to all selected point objects and the Name item is ignored.
        Replace(bool)-If this item is True, all previous joint constraints, if any, assigned to the specified
            point object(s) are deleted before making the new assignment.
        """
        self.SapModel.PointObj.SetConstraint(name,ConstraintName)

    def assign_PointObj_SetGroupAssign(self,name,GroupName,Remove=False,ItemType=0):
        """
        ---This function adds or removes point objects from a specified group.---
        inputs:
        name(str)-The name of an existing point object or group depending on the value of the ItemType item.
        GroupName(str)-The name of an existing group to which the assignment is made.
        Remove(bool)-If this item is False, the specified point objects are added to the group specified by the
            GroupName item. If it is True, the point objects are removed from the group.
        ItemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0
            Group = 1
            SelectedObjects = 2
            If this item is Object, the point object specified by the Name item is added or removed from the group
            specified by the GroupName item.If this item is Group, all point objects in the group specified by the
            Name item are added or removed from the group specified by the GroupName item.If this item is
            SelectedObjects, all selected point objects are added or removed from the group specified by the
            GroupName item and the Name item is ignored.
        """
        self.SapModel.PointObj.SetGroupAssign(name,GroupName,Remove,ItemType)

    def assign_PointObj_SetLoadDispl(self,name,LoadPat,Value,Replace=False,CSys="Global",ItemType=0):
        """
        ---This function makes ground displacement load assignments to point objects.---
        inputs:
        name(str)-The name of an existing point object or group depending on the value of the ItemType item.
        LoadPat(str)-The name of the load pattern for the ground displacement load.
        Value(float list)-This is an array of six ground displacement load values.
            Value(0) = U1 [L]
            Value(1) = U2 [L]
            Value(2) = U3 [L]
            Value(3) = R1 [rad]
            Value(4) = R2 [rad]
            Value(5) = R3 [rad]
        Replace(bool)-If this item is True, all previous ground displacement loads, if any, assigned to the specified
            point object(s) in the specified load pattern are deleted before making the new assignment.
        CSys(str)-The name of the coordinate system for the considered ground displacement load. This is Local or
            the name of a defined coordinate system.
        ItemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0
            Group = 1
            SelectedObjects = 2
            If this item is Object, the load assignment is made to the point object specified by the Name item.
            If this item is Group, the load assignment is made to all point objects in the group specified by the Name item.
            If this item is SelectedObjects, the load assignment is made to all selected point objects and the Name
            item is ignored.
        """
        self.SapModel.PointObj.SetLoadDispl(name,LoadPat,Value,Replace,CSys,ItemType)

    def assign_PointObj_SetLoadForce(self,name,loadPat,value,Replace=False,CSys="Global",ItemType=0):
        """
        ---This function makes point load assignments to point objects.---
        inputs:
        name(str)-The name of an existing point object or group depending on the value of the ItemType item.
        loadPat(str)-The name of the load pattern for the point load.
        value(float list)-This is an array of six point load values.
            Value(0) = F1 [F]
            Value(1) = F2 [F]
            Value(2) = F3 [F]
            Value(3) = M1 [FL]
            Value(4) = M2 [FL]
            Value(5) = M3 [FL]
        Replace(bool)-If this item is True, all previous ground displacement loads, if any, assigned to the specified
            point object(s) in the specified load pattern are deleted before making the new assignment.
        CSys(str)-The name of the coordinate system for the considered ground displacement load. This is Local or
            the name of a defined coordinate system.
        ItemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0
            Group = 1
            SelectedObjects = 2
            If this item is Object, the load assignment is made to the point object specified by the Name item.
            If this item is Group, the load assignment is made to all point objects in the group specified by the Name item.
            If this item is SelectedObjects, the load assignment is made to all selected point objects and the Name
            item is ignored.
        """
        self.SapModel.PointObj.SetLoadForce(name,loadPat,value,Replace,CSys,ItemType)

    def assign_PointObj_SetLocalAxes(self,name,a,b,c,itemType=0):
        """
        ---This function sets the local axes angles for point objects.---
        inputs:
        name(str)-The name of an existing point object or group depending on the value of the ItemType item.
        a,b,c(float)-The local axes of the point are defined by first setting the positive local 1, 2 and 3 axes
            the same as the positive global X, Y and Z axes and then doing the following: [deg]
            1. Rotate about the 3 axis by angle a.
            2. Rotate about the resulting 2 axis by angle b.
            3. Rotate about the resulting 1 axis by angle c.
        ItemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0
            Group = 1
            SelectedObjects = 2
            If this item is Object, the load assignment is made to the point object specified by the Name item.
            If this item is Group, the load assignment is made to all point objects in the group specified by the Name item.
            If this item is SelectedObjects, the load assignment is made to all selected point objects and the Name
            item is ignored.
        """
        self.SapModel.PointObj.SetLocalAxes(name,a,b,c,itemType)

    def assign_PointObj_SetMass(self,name,m,itemType=0,isLocalCSys=True,Replace=False):
        """
        ---This function assigns point mass to a point object.---
        inputs:
        name(str)-The name of an existing point object or group depending on the value of the ItemType item.
        m(float list)-This is an array of six mass assignment values.
            Value(0) = U1 [M]
            Value(1) = U2 [M]
            Value(2) = U3 [M]
            Value(3) = R1 [ML2]
            Value(4) = R2 [ML2]
            Value(5) = R3 [ML2]
        ItemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0
            Group = 1
            SelectedObjects = 2
            If this item is Object, the load assignment is made to the point object specified by the Name item.
            If this item is Group, the load assignment is made to all point objects in the group specified by the Name item.
            If this item is SelectedObjects, the load assignment is made to all selected point objects and the Name
            item is ignored.
        isLocalCSys(bool)-If this item is True, the specified mass assignments are in the point object local coordinate
            system. If it is False, the assignments are in the Global coordinate system.
        Replace(bool)-If this item is True, all existing point mass assignments to the specified point object(s) are
            deleted prior to making the assignment. If it is False, the mass assignments are added to any existing assignments.
        """
        self.SapModel.PointObj.SetMass(name,m,itemType,isLocalCSys,Replace)

    def assign_PointObj_SetRestraint(self,name,value,itemType=0):
        """
        ---This function assigns the restraint assignments for a point object. The restraint assignments are always
        set in the point local coordinate system.---
        inputs:
        name(str)-The name of an existing point object or group depending on the value of the ItemType item.
        value(bool list)-This is an array of six restraint values.
            Value(0) = U1
            Value(1) = U2
            Value(2) = U3
            Value(3) = R1
            Value(4) = R2
            Value(5) = R3
        ItemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0
            Group = 1
            SelectedObjects = 2
            If this item is Object, the load assignment is made to the point object specified by the Name item.
            If this item is Group, the load assignment is made to all point objects in the group specified by the Name item.
            If this item is SelectedObjects, the load assignment is made to all selected point objects and the Name
            item is ignored.
        """
        self.SapModel.PointObj.SetRestraint(name,value,itemType)




    def assign_PointObj_SetSpring(self,name,k,ItemType=0,IsLocalCSys=False,Replace=False):
        """
        ---This function assigns uncoupled springs to a point object.---
        inputs:
        name(str)-The name of an existing point object or group depending on the value of the ItemType item.
        k(float list)-This is an array of six spring stiffness values.
            Value(0) = U1 [F/L]
            Value(1) = U2 [F/L]
            Value(2) = U3 [F/L]
            Value(3) = R1 [FL/rad]
            Value(4) = R2 [FL/rad]
            Value(5) = R3 [FL/rad]
        ItemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0
            Group = 1
            SelectedObjects = 2
            If this item is Object, the spring assignment is made to the point object specified by the Name item.
            If this item is Group, the spring assignment is made to all point objects in the group specified by the Name item.
            If this item is SelectedObjects, the spring assignment is made to all selected point objects and the Name
            item is ignored.
        IsLocalCSys(bool)-If this item is True, the specified spring assignments are in the point object local
            coordinate system. If it is False, the assignments are in the Global coordinate system.
        Replace(bool)-If this item is True, all existing point spring assignments to the specified point object(s)
            are deleted prior to making the assignment. If it is False, the spring assignments are added to any
            existing assignments.
        """
        self.SapModel.PointObj.SetSpring(name,k,ItemType,IsLocalCSys,Replace)

    def assign_PointObj_SetSpringCoupled(self,name,k,ItemType=0,IsLocalCSys=False,Replace=False):
        """
        ---This function assigns coupled springs to a point object---
        inputs:
        name(str)-The name of an existing point object or group depending on the value of the ItemType item.
        k(float list)-This is an array of twenty one spring stiffness values.
            Value(0) = U1U1 [F/L]
            Value(1) = U1U2 [F/L]
            Value(2) = U2U2 [F/L]
            Value(3) = U1U3 [F/L]
            Value(4) = U2U3 [F/L]
            Value(5) = U3U3 [F/L]
            Value(6) = U1R1 [F/rad]
            Value(7) = U2R1 [F/rad]
            Value(8) = U3R1 [F/rad]
            Value(9) = R1R1 [FL/rad]
            Value(10) = U1R2 [F/rad]
            Value(11) = U2R2 [F/rad]
            Value(12) = U3R2 [F/rad]
            Value(13) = R1R2 [FL/rad]
            Value(14) = R2R2 [FL/rad]
            Value(15) = U1R3 [F/rad]
            Value(16) = U2R3 [F/rad]
            Value(17) = U3R3 [F/rad]
            Value(18) = R1R3 [FL/rad]
            Value(19) = R2R3 [FL/rad]
            Value(20) = R3R3 [FL/rad]
        ItemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0
            Group = 1
            SelectedObjects = 2
            If this item is Object, the spring assignment is made to the point object specified by the Name item.
            If this item is Group, the spring assignment is made to all point objects in the group specified by the Name item.
            If this item is SelectedObjects, the spring assignment is made to all selected point objects and the Name
            item is ignored.
        IsLocalCSys(bool)-If this item is True, the specified spring assignments are in the point object local
            coordinate system. If it is False, the assignments are in the Global coordinate system.
        Replace(bool)-If this item is True, all existing point spring assignments to the specified point object(s)
            are deleted prior to making the assignment. If it is False, the spring assignments are added to any
            existing assignments.
        """
        self.SapModel.PointObj.SetSpringCoupled(name,k,ItemType,IsLocalCSys,Replace)

    def assign_FrameObj_AddByCoord(self,xi,yi,zi,xj,yj,zj,propName="Default",userName="",Csys="Global"):
        """
        ---This function adds a new frame object whose end points are at the specified coordinates---
        inputs:
        xi,yi,zi(float)-The coordinates of the I-End of the added frame object. The coordinates are in the
            coordinate system defined by the CSys item.
        xj,yj,zj(float)-The coordinates of the I-End of the added frame object. The coordinates are in
            the coordinate system defined by the CSys item.
        propName(str)-This is Default, None, or the name of a defined frame section property.If it is Default,
            the program assigns a default section property to the frame object. If it is None, no section
            property is assigned to the frame object. If it is the name of a defined frame section property,
            that property is assigned to the frame object.
        userName(str)-This is an optional user specified name for the frame object. If a UserName is specified
            and that name is already used for another frame object, the program ignores the UserName.
        Csys(str)-The name of the coordinate system in which the frame object end point coordinates are defined.
        """
        #name(str)-This is the name that the program ultimately assigns for the frame object. If no UserName is
        #specified, the program assigns a default name to the frame object. If a UserName is specified and
        #that name is not used for another frame, cable or tendon object, the UserName is assigned to the
        #frame object, otherwise a default name is assigned to the frame object.
        name=""
        self.SapModel.FrameObj.AddByCoord(xi,yi,zi,xj,yj,zj,name,propName,userName,Csys)

    def assign_FrameObj_AddByPoint(self,Point1,Point2,propName="Default",userName=""):
        """
        ---This function adds a new frame object whose end points are specified by name---
        inputs:
        Point1(str)-The name of a defined point object at the I-End of the added frame object.
        Point2(str)-The name of a defined point object at the J-End of the added frame object.
        propName(str)-This is Default, None, or the name of a defined frame section property.If it is Default,
            the program assigns a default section property to the frame object. If it is None, no section
            property is assigned to the frame object. If it is the name of a defined frame section property,
            that property is assigned to the frame object.
        userName(str)-This is an optional user specified name for the frame object. If a UserName is specified
            and that name is already used for another frame object, the program ignores the UserName.
        """
        # name(str)-This is the name that the program ultimately assigns for the frame object. If no UserName is
        # specified, the program assigns a default name to the frame object. If a UserName is specified and
        # that name is not used for another frame, cable or tendon object, the UserName is assigned to the
        # frame object, otherwise a default name is assigned to the frame object.
        name = ""
        self.SapModel.FrameObj.AddByPoint(Point1,Point2,name,propName,userName)

    def assign_FrameObj_ChangeName(self,name,newName):
        """
        ---The function returns zero if the new name is successfully applied, otherwise it returns a nonzero value---
        inputs:
        name(str)-The existing name of a defined frame object.
        newName(str)-The new name for the frame object.
        """
        self.SapModel.FrameObj.ChangeName(name,newName)

    def assign_FrameObj_Count(self,myType="All"):
        """
        ---This function returns a count of the frame objects in the model. Depending on the value of the MyType item,
            the count may be of all frame objects in the model, just the straight frame objects in the model or just
            the curved frame objects in the model---
        inputs:
        myType(str)-This is All, Straight, or Curved.
            All returns a count of all frame objects in the model, including both straight and curved frame objects.
            Straight returns a count of all straight frame objects in the model. Curved returns a count of all curved
            frame objects in the model.
        """
        countNum=self.SapModel.FrameObj.Count(myType)
        return countNum

    def assign_FrameObj_Delete(self,name,itemType=0):
        """
        ---The function deletes frame objects.---
        inputs:
        name(str)-The name of an existing frame object or group depending on the value of the ItemType item.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored.
        """
        self.SapModel.FrameObj.Delete(name,itemType)

    def assign_FrameObj_SetAutoMesh(self,name,autoMesh,AutoMeshAtPoints,AutoMeshAtLines,
                                    umSegs,AutoMeshMaxLength,ItemType=0):
        """
        ---This function makes automatic meshing assignments to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        AutoMesh(bool)-This item is True if the frame object is to be automatically meshed by the program when
            the analysis model is created.
        AutoMeshAtPoints(bool)-This item is applicable only when the AutoMesh item is True. If this item is True,
            the frame object is automatically meshed at intermediate joints along its length
        AutoMeshAtLines(bool)-This item is applicable only when the AutoMesh item is True. If this item is True,
            the frame object is automatically meshed at intersections with other frames, area object edges and
            solid object edges.
        NumSegs(int)-This item is applicable only when the AutoMesh item is True. It is the minimum number of elements
            into which the frame object is automatically meshed. If this item is zero, the number of elements is not
            checked when the automatic meshing is done.
        AutoMeshMaxLength(float)-This item is applicable only when the AutoMesh item is True. It is the maximum length
            of auto meshed frame elements. If this item is zero, the element length is not checked when the automatic
            meshing is done. [L]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored.
        """
        self.SapModel.FrameObj.SetAutoMesh(name,autoMesh,AutoMeshAtPoints,AutoMeshAtLines,
                                    umSegs,AutoMeshMaxLength,ItemType)

    def assign_FrameObj_SetDesignProcedure(self,name,myType,itemType=0):
        """
        ---This function sets the design procedure for frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        myType(int)-This is 1 or 2, indicating the design procedure type desired for the specified frame object.
            1 = Default from material,2 = No design
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored.
        """
        self.SapModel.FrameObj.SetDesignProcedure(name,myType,itemType)

    def assign_FrameObj_SetEndLengthOffset(self,name,AutoOffset,Length1=0,Length2=0,rz=0,ItemType=0):
        """
        ---This function assigns frame object end offsets along the 1-axis of the object---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        AutoOffset(bool)-If this item is True, the end length offsets are automatically determined by the program
            from object connectivity, and the Length1, Length2 and rz items are ignored.
        Length1(float)-The offset length along the 1-axis of the frame object at the I-End of the frame object. [L]
        Length2(float)-The offset along the 1-axis of the frame object at the J-End of the frame object. [L]
        rz(float)-The rigid zone factor.  This is the fraction of the end offset length assumed to be rigid for
            bending and shear deformations.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored.
        """
        self.SapModel.FrameObj.SetEndLengthOffset(name,AutoOffset,Length1,Length2,rz,ItemType)

    def assign_FrameObj_SetEndSkew(self,name,skewI,skewJ,itemType=0):
        """
        ---This function assigns frame object end skew data. End skew data is used in the program to plot the
        extruded view of bridge objects that have been updated as spine models only.---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        skewI(float)-The angle in degrees measured counter clockwise from the positive local 3-axis to a line
            parallel to the I-End of the frame object (-90 < SkewI < 90). [deg]
        skewJ(float)-TThe angle in degrees measured counter clockwise from the positive local 3-axis to a line
            parallel to the J-End of the frame object (-90 < SkewJ < 90). [deg]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored.
        """
        self.SapModel.FrameObj.SetEndSkew(name,skewI,skewJ,itemType)

    def assign_FrameObj_SetGroupAssign(self,name,groupName,remove=False,itemType=0):
        """
        ---This function adds or removes frame objects from a specified group---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        groupName(str)-TThe name of an existing group to which the assignment is made.
        remove(bool)-If this item is False, the specified frame objects are added to the group specified by
            the GroupName item. If it is True, the frame objects are removed from the group.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored.
        """
        self.SapModel.FrameObj.SetGroupAssign(name,groupName,remove,itemType)

    def assign_FrameObj_SetInsertionPoint(self,name,CardinalPoint,Mirror2,StiffTransform,Offset1,Offset2,
                                          CSys="Local",itemType=0):
        """
        ---This function assigns frame object insertion point data. The assignments include the cardinal
            point and end joint offsets---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        CardinalPoint(int)-This is a numeric value from 1 to 11 that specifies the cardinal point for the frame
            object. The cardinal point specifies the relative position of the frame section on the line representing
            the frame object.
            1 = bottom left
            2 = bottom center
            3 = bottom right
            4 = middle left
            5 = middle center
            6 = middle right
            7 = top left
            8 = top center
            9 = top right
            10 = centroid
            11 = shear center
        Mirror2(bool)-If this item is True, the frame object section is assumed to be mirrored (flipped) about
            its local 2-axis.
        StiffTransform(bool)-If this item is True, the frame object stiffness is transformed for cardinal point
            and joint offsets from the frame section centroid.
        Offset1(float list)-This is an array of three joint offset distances, in the coordinate directions specified
            by CSys, at the I-End of the frame object. [L]
            Offset1(0) = Offset in the 1-axis or X-axis direction
            Offset1(1) = Offset in the 2-axis or Y-axis direction
            Offset1(2) = Offset in the 3-axis or Z-axis direction
        Offset2(float list)-This is an array of three joint offset distances, in the coordinate directions specified
            by CSys, at the J-End of the frame object. [L]
            Offset2(0) = Offset in the 1-axis or X-axis direction
            Offset2(1) = Offset in the 2-axis or Y-axis direction
            Offset2(2) = Offset in the 3-axis or Z-axis direction
        CSys(str)-This is Local or the name of a defined coordinate system. It is the coordinate system in which
            the Offset1 and Offset2 items are specified.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored.
        """
        self.SapModel.FrameObj.SetInsertionPoint(name,CardinalPoint,Mirror2,StiffTransform,Offset1,Offset2,CSys,itemType)

    def assign_FrameObj_SetLoadDeformation(self,name,loadPat,DOF,d,itemType=0):
        """
        ---This function assigns deformation loads to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        DOF(bool list)-This is a array of boolean values indicating if the considered degree of freedom has a deformation load.
            DOF(1) = U1,DOF(2) = U2,DOF(3) = U3,DOF(4) = R1,DOF(5) = R2,DOF(6) = R3
        d(float list)-This is a array of deformation load values. The deformations specified for a given degree of
            freedom are applied only if the corresponding DOF item for that degree of freedom is True.
                d(1) = U1 deformation [L]
                d(2) = U2 deformation [L]
                d(3) = U3 deformation [L]
                d(4) = R1 deformation [rad]
                d(5) = R2 deformation [rad]
                d(6) = R3 deformation [rad]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored.
        """
        self.SapModel.FrameObj.SetLoadDeformation(name,loadPat,DOF,d,itemType)

    def assign_FrameObj_SetLoadDistributed(self,name,loadPat,myType,Dir,Dist1,Dist2,Val1,Val2,
                                           CSys="Global",RelDist=True,Replace=True,ItemType=0):
        """
        ---This function assigns distributed loads to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        myType(int)-This is 1 or 2, indicating the type of distributed load.
            1 = Force per unit length,2 = Moment per unit length
        Dir(int)-This is an integer between 1 and 11, indicating the direction of the load.
            1 = Local 1 axis (only applies when CSys is Local)
            2 = Local 2 axis (only applies when CSys is Local)
            3 = Local 3 axis (only applies when CSys is Local)
            4 = X direction (does not apply when CSys is Local)
            5 = Y direction (does not apply when CSys is Local)
            6 = Z direction (does not apply when CSys is Local)
            7 = Projected X direction (does not apply when CSys is Local)
            8 = Projected Y direction (does not apply when CSys is Local)
            9 = Projected Z direction (does not apply when CSys is Local)
            10 = Gravity direction (only applies when CSys is Global)
            11 = Projected Gravity direction (only applies when CSys is Global)
            The positive gravity direction (see Dir = 10 and 11) is in the negative Global Z direction.
        Dist1(float)-This is the distance from the I-End of the frame object to the start of the distributed load.
            This may be a relative distance (0 <= Dist1 <= 1) or an actual distance, depending on the value of the
            RelDist item. [L] when RelDist is False
        Dist2(float)-This is the distance from the I-End of the frame object to the end of the distributed load.
            This may be a relative distance (0 <= Dist2 <= 1) or an actual distance, depending on the value of the
            RelDist item. [L] when RelDist is False
        Val1(float)-This is the load value at the start of the distributed load. [F/L] when MyType is 1 and [FL/L]
            when MyType is 2
        Val2(float)-This is the load value at the end of the distributed load. [F/L] when MyType is 1 and [FL/L]
            when MyType is 2
        CSys(str)-This is Local or the name of a defined coordinate system. It is the coordinate system in which
            the loads are specified.
        RelDist(bool)-If this item is True, the specified Dist item is a relative distance, otherwise it is an actual distance.
        Replace(bool)-If this item is True, all previous distributed loads, if any, assigned to the specified frame
            object(s), in the specified load pattern, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored.
        """
        self.SapModel.FrameObj.SetLoadDistributed(name,loadPat,myType,Dir,Dist1,Dist2,Val1,Val2,CSys,RelDist,Replace,ItemType)

    def assign_FrameObj_SetLoadGravity(self,name,loadPat,x,y,z,Replace=True,CSys="Global",itemType=0):
        """
        ---This function assigns gravity load multipliers to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        x,y,z(float)-These are the gravity load multipliers in the x, y and z directions of the specified coordinate system.
        Replace(bool)-If this item is True, all previous gravity loads, if any, assigned to the specified frame
            object(s), in the specified load pattern, are deleted before making the new assignment.
        CSys(str)-The coordinate system in which the x, y and z multipliers are specified
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored.
        """
        self.SapModel.FrameObj.SetLoadGravity(name,loadPat,x,y,z,Replace,CSys,itemType)

    def assign_FrameObj_SetLoadPoint(self,name,loadPat,myType,Dir,Dist,Val,
                                     CSys="Global",RelDist=True,Replace=True,itemType=0):
        """
        ---This function assigns point loads to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        myType(int)-This is 1 or 2, indicating the type of point load.
            1 = Force,2 = Moment
        Dir(int)-This is an integer between 1 and 11, indicating the direction of the load.
            1 = Local 1 axis (only applies when CSys is Local)
            2 = Local 2 axis (only applies when CSys is Local)
            3 = Local 3 axis (only applies when CSys is Local)
            4 = X direction (does not apply when CSys is Local)
            5 = Y direction (does not apply when CSys is Local)
            6 = Z direction (does not apply when CSys is Local)
            7 = Projected X direction (does not apply when CSys is Local)
            8 = Projected Y direction (does not apply when CSys is Local)
            9 = Projected Z direction (does not apply when CSys is Local)
            10 = Gravity direction (only applies when CSys is Global)
            11 = Projected Gravity direction (only applies when CSys is Global)
            The positive gravity direction (see Dir = 10 and 11) is in the negative Global Z direction.
        Dist(float)-This is the distance from the I-End of the frame object to the load location. This may
            be a relative distance (0 <= Dist <= 1) or an actual distance, depending on the value of the
            RelDist item. [L] when RelDist is False
        Val(float)-This is the value of the point load. [F] when MyType is 1 and [FL] when MyType is 2
        CSys(str)-This is Local or the name of a defined coordinate system. It is the coordinate system in
            which the loads are specified.
        RelDist(bool)-If this item is True, the specified Dist item is a relative distance, otherwise it is
            an actual distance.
        Replace(bool)-If this item is True, all previous loads, if any, assigned to the specified frame object(s),
            in the specified load pattern, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.FrameObj.SetLoadPoint(name,loadPat,myType,Dir,Dist,Val,CSys,RelDist,Replace,itemType)

    def assign_FrameObj_SetLoadStrain(self,name,loadPat,DOF,Val,Replace=True,PatternName="",itemType=0):
        """
        ---This function assigns strain loads to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        DOF(int)-This is 1, 2, 3, 4, 5 or 6, indicating the degree of freedom to which the strain load is applied.
            1 = Strain11,2 = Strain12,3 = Strain13,4 = Curvature1,5 = Curvature2,6 = Curvature3
        Val(float)-This is the strain load value. [L/L] for DOF = 1, 2 and 3 and [1/L] for DOF = 4, 5 and 6
        Replace(bool)-If this item is True, all previous strain loads, if any, assigned to the specified frame object(s),
            in the specified load pattern, for the specified degree of freedom, are deleted before making the new assignment.
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the strain load for the
            frame object is uniform along the object at the value specified by Val.If PatternName is the name of a
            defined joint pattern, the strain load for the frame object is based on the specified strain value
            multiplied by the pattern value at the joints at each end of the frame object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.FrameObj.SetLoadStrain(name,loadPat,DOF,Val,Replace,PatternName,itemType)

    def assign_FrameObj_SetLoadTargetForce(self,name,loadPat,DOF,f,RD,itemType=0):
        """
        ---This function assigns target forces to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        DOF(bool list)-This is a array of boolean values indicating if the considered degree of freedom has a target force.
            DOF(1) = P,DOF(2) = V2,DOF(3) = V3,DOF(4) = T,DOF(5) = M2,DOF(6) = M3
        f(float list)-This is a array of target force values. The target forces specified for a given degree of freedom
            are applied only if the corresponding DOF item for that degree of freedom is True.
            f(1) = P [F],f(2) = V2 [F],f(3) = V3 [F],f(4) = T [FL],f(5) = M2 [FL],f(6) = M3 [FL]
        RD(float list)-This is a array of relative distances along the frame objects where the target force values apply.
            The relative distances specified for a given degree of freedom are applicable only if the corresponding DOF
            item for that degree of freedom is True. The relative distance must be between 0 and 1, 0 <= RD <=1.
            RD(1) = relative location for P target force
            RD(2) = relative location for V2 target force
            RD(3) = relative location for V3 target force
            RD(4) = relative location for T target force
            RD(5) = relative location for M2 target force
            RD(6) = relative location for M3 target force
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.FrameObj.SetLoadTargetForce(name,loadPat,DOF,f,RD,itemType)

    def assign_FrameObj_SetLoadTemperature(self,name,loadPat,myType,Val,PatternName="",Replace=True,itemType=0):
        """
        ---This function assigns temperature loads to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        myType(int)-This is 1, 2 or 3, indicating the type of temperature load.
            1 = Temperature,2 = Temperature gradient along local 2 axis,3 = Temperature gradient along local 3 axis
        Val(float)-This is the temperature change value. [T] for MyType = 1 and [T/L] for MyType = 2 and 3
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank the temperature load
            for the frame object is uniform along the object at the value specified by Val.If PatternName is the
            name of a defined joint pattern, the temperature load for the frame object is based on the specified
            temperature value multiplied by the pattern value at the joints at each end of the frame object.
        Replace(bool)-If this item is True, all previous temperature loads, if any, assigned to the specified frame
            object(s), in the specified load case, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.FrameObj.SetLoadTemperature(name,loadPat,myType,Val,PatternName,Replace,itemType)

    def assign_FrameObj_SetLoadTransfer(self,name,Val,itemType=0):
        """
        ---This function returns the load transfer option for frame objects.  It indicates whether the frame
        receives load from an area object when the area object is loaded with a load of type uniform to frame---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        Val(bool)-This boolean value indicates if load is allowed to be transferred from area objects to this frame object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.FrameObj.SetLoadTransfer(name,Val,itemType)

    def assign_FrameObj_SetLocalAxes(self,name,Ang,itemType=0):
        """
        ---This function assigns a local axis angle to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        Ang(float)-This is the angle that the local 2 and 3 axes are rotated about the positive local 1 axis,
            from the default orientation or, if the Advanced item is True, from the orientation determined by
            the plane reference vector. The rotation for a positive angle appears counter clockwise when the
            local +1 axis is pointing toward you. [deg]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.FrameObj.SetLocalAxes(name,Ang,itemType)

    def assign_FrameObj_SetMass(self,name,massOverL,Replace=False,itemType=0):
        """
        ---This function assigns mass per unit length to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        massOverL(float)-The mass per unit length assigned to the frame object. [M/L]
        Replace(bool)-If this item is True, all existing mass assignments to the frame object are removed before
            assigning the specified mas. If it is False, the specified mass is added to any existing mass already
            assigned to the frame object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.FrameObj.SetMass(name,massOverL,Replace,itemType)

    def assign_FrameObj_SetMaterialOverwrite(self,name,proName,itemType=0):
        """
        ---This function sets the material overwrite assignment for frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        propName(str)-This is None or a blank string, indicating that any existing material overwrites assigned
            to the specified frame objects are to be removed, or it is the name of an existing material property.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.FrameObj.SetMaterialOverwrite(name,proName,itemType)

    def assign_FrameObj_SetMatTemp(self,name,temp,patternName="",itemType=0):
        """
        ---This function assigns material temperatures to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        temp(float)-This is the material temperature value assigned to the frame object. [T]
        patternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the material temperature
            for the frame object is uniform along the object at the value specified by Temp.If PatternName is the name
            of a defined joint pattern, the material temperature for the frame object may vary from one end to the other.
            The material temperature at each end of the object is equal to the specified temperature multiplied by the
            pattern value at the joint at the end of the frame object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.FrameObj.SetMatTemp(name,temp,patternName,itemType)

    def assign_FrameObj_SetModifiers(self,name,value,itemType=0):
        """
        ---This function sets the frame modifier assignment for frame objects. The default value for all modifiers is one.---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        value(float list)-This is an array of eight unitless modifiers.
            Value(0) = Cross sectional area modifier
            Value(1) = Shear area in local 2 direction modifier
            Value(2) = Shear area in local 3 direction modifier
            Value(3) = Torsional constant modifier
            Value(4) = Moment of inertia about local 2 axis modifier
            Value(5) = Moment of inertia about local 3 axis modifier
            Value(6) = Mass modifier
            Value(7) = Weight modifier
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.FrameObj.SetModifiers(name,value,itemType)

    def assign_FrameObj_SetNotionalSize(self,name,stype,value):
        """
        ---This function assigns the method to determine the notional size of a frame section for the creep and
            shrinkage calculations. This function is currently worked for the steel/aluminum sections - I/Wide
            Flange, Channel, Tee, Angle, Double Angle, Double Channel, Pipe and Tube sections, and all the concrete
            sections - Rectangular, Circular, Pipe, Tube, Precast I.---
        inputs:
        name(str)-The name of an existing frame section property.
        stype(str)-The type to define the notional size of a section. It can be:
            "Auto" = Program will determine the notional size based on the average thickness of an area element.
            "User" = The notional size is based on the user-defined value.
            "None" = Notional size will not be considered. In other words, the time-dependent effect of this section
                will not be considered.
        value(float)-For stype is "Auto", the Value represents for the scale factor to the program-determined notional
            size; for stype is “User”, the Value represents for the user-defined notional size [L]; for stype is “None”,
            the Value will not be used and can be set to 1.
        """
        self.SapModel.PropFrame.SetNotionalSize(name,stype,value)

    def assign_FrameObj_SetOutputStations(self,name,myType,settingValue,NoOutPutAndDesignAtElementEnds=False,
                                          NoOutPutAndDesignAtPointLoads=False,itemType=0):
        """
        ---This function assigns frame object output station data---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        myType(int)-This is 1 or 2, indicating how the output stations are specified.
            1 = maximum segment size, that is, maximum station spacing
            2 = minimum number of stations
        settingValue(float/int)-the corresponding value for myType
            The maximum segment size, that is, the maximum station spacing. This item applies only when MyType = 1. [L]
            The minimum number of stations. This item applies only when MyType = 2.
        NoOutPutAndDesignAtElementEnds(bool)-If this item is True, no additional output stations are added at the ends
            of line elements when the frame object is internally meshed.
        NoOutPutAndDesignAtPointLoads(bool)-If this item is True, no additional output stations are added at point load
            locations.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.FrameObj.SetOutputStations(name,myType,settingValue,NoOutPutAndDesignAtElementEnds,
                                          NoOutPutAndDesignAtPointLoads,itemType)

    def assign_FrameObj_SetPDeltaForce(self,name,PDeltaForce,Dir,Replace,CSys="Global",itemType=0):
        """
        ---This function assigns P-Delta forces to straight frame objects. P-Delta force assignments do not apply to
            curved frames.---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        PDeltaForce(float)-The P-Delta force assigned to the frame object. [F]
        Dir(int)-This is 0, 1, 2 or 3, indicating the direction of the P-Delta force assignment.
            0 = Frame object local 1-axis direction
            1 = Projected X direction in CSys coordinate system
            2 = Projected Y direction in CSys coordinate system
            3 = Projected Z direction in CSys coordinate system
        Replace(bool)-If this item is True, all existing P-Delta force assignments to the frame object are removed
            before assigning the specified P-Delta force. If it is False, the specified P-Delta force is added to any
            existing P-Delta forces already assigned to the frame object.
        Csys(str)-This is the name of the coordinate system in which the projected X, Y or Z direction P-Delta forces
            are defined. This item does not apply if the Dir item is zero (frame object local 1-axis direction).
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.FrameObj.SetPDeltaForce(name,PDeltaForce,Dir,Replace,CSys,itemType)

    def assign_FrameObj_SetReleases(self,name,ii,jj,startValue=[0,0,0,0,0,0],endValue=[0,0,0,0,0,0],itemType=0):
        """
        ---This function makes end release and partial fixity assignments to frame objects.The function returns zero
        if the assignments are successfully retrieved, otherwise it returns a nonzero value.Partial fixity assignments
        are made to degrees of freedom that have been released only.Some release assignments would cause instability
        in the model. An error is returned if this type of assignment is made. Unstable release assignments include
        the following:
        U1 released at both ends
        U2 released at both ends
        U3 released at both ends
        R1 released at both ends
        R2 released at both ends and U3 at either end
        R3 released at both ends and U2 at either end
        ---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        ii,jj(bool list)-These are arrays of six booleans indicating the I-End and J-End releases for the frame object.
            ii(0) and jj(0) = U1 release
            ii(1) and jj(1) = U2 release
            ii(2) and jj(2) = U3 release
            ii(3) and jj(3) = R1 release
            ii(4) and jj(4) = R2 release
            ii(5) and jj(5) = R3 release
        StartValue, EndValue(float list)-These are arrays of six values indicating the I-End and J-End partial fixity
            springs for the frame object.
            StartValue(0) and EndValue(0) = U1 partial fixity [F/L]
            StartValue(1) and EndValue(1) = U2 partial fixity [F/L]
            StartValue(2) and EndValue(2) = U3 partial fixity [F/L]
            StartValue(3) and EndValue(3) = R1 partial fixity [FL/rad]
            StartValue(4) and EndValue(4) = R2 partial fixity [FL/rad]
            StartValue(5) and EndValue(5) = R3 partial fixity [FL/rad]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.FrameObj.SetReleases(name,ii,jj,startValue,endValue,itemType)

    def assign_FrameObj_SetSection(self,name,propName,itemType=0,sVarTotalLength=0,sVarRelStartLoc=0):
        """
        ---This function assigns a frame section property to a frame object---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        propName(str)-This is None or the name of a frame section property to be assigned to the specified frame object(s).
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        sVarTotalLength(float)-This is the total assumed length of the nonprismatic section. Enter 0 for this item to
            indicate that the section length is the same as the frame object length.This item is applicable only when
            the assigned frame section property is a nonprismatic section.
        sVarRelStartLoc(float)-This is the relative distance along the nonprismatic section to the I-End (start) of the
            frame object. This item is ignored when the sVarTotalLengthitem is 0.This item is applicable only when the
            assigned frame section property is a nonprismatic section, and the sVarTotalLengthitem is greater than zero.
        """
        self.SapModel.FrameObj.SetSection(name,propName,itemType,sVarTotalLength,sVarRelStartLoc)

    def assign_FrameObj_SetSpring(self,name,myType,s=0,simpleSpringType=1,LinkProp="",springLocalOneType=1,Dir=1,
                                  Plane23Angle=0,Vec=[1,0,0],Ang=0,Replace=False,CSys="Local",itemType=0):
        """
        ---This function makes spring assignments to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        myType(int)-This is 1 or 2, indicating the spring property type.1 = Simple spring,2 = Link property
        s(float)-The simple spring stiffness per unit length of the frame object. This item applies only when MyType = 1. [F/L2]
        simpleSpringType(int)-This is 1, 2 or 3, indicating the simple spring type. This item applies only when MyType = 1.
            1 = Spring resists tension and compression
            2 = Spring resists compression only
            3 = Spring resists tension only
        LinkProp(str)-The name of the link property assigned to the spring. This item applies only when MyType = 2.
        springLocalOneType(int)-This is 1, 2 or 3, indicating the method used to specify the spring positive local
            1-axis orientation.
            1 = Parallel to frame object local axis
            2 = In the frame object 2-3 plane
            3 = User specified direction vector
        Dir(int)-This is 1, 2, 3, -1, -2 or -3, indicating the frame object local axis that corresponds to the positive
            local 1-axis of the spring. This item applies only when SpringLocalOneType = 1.
        Plane23Angle(float)-This is the angle in the frame object 2-3 plane measured counter clockwise from the frame
            positive 2-axis to the spring positive 1-axis. This item applies only when SpringLocalOneType = 2. [deg]
        Vec(float list)-This is an array of three values that define the direction vector of the spring positive local
            1-axis. The direction vector is in the coordinate system specified by the CSys item. This item applies only
            when SpringLocalOneType = 3.
        Ang(float)-This is the angle that the link local 2-axis is rotated from its default orientation. This item
            applies only when MyType = 2. [deg]
        Replace(bool)-If this item is True, all existing spring assignments to the frame object are removed before
            assigning the specified spring. If it is False, the specified spring is added to any existing springs
            already assigned to the frame object.
        CSys(str)-This is Local (meaning the frame object local coordinate system) or the name of a defined coordinate
            system. This item is the coordinate system in which the user specified direction vector, Vec, is specified.
            This item applies only when SpringLocalOneType = 3.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.FrameObj.SetSpring(name,myType,s,simpleSpringType,LinkProp,springLocalOneType,Dir,
                                  Plane23Angle,Vec,Ang,Replace,CSys,itemType)

    def assign_FrameObj_SetTCLimits(self,name,LimitCompressionExists,LimitCompression,LimitTensionExists,LimitTension,
                                    itemType=0):
        """
        ---This function makes tension/compression force limit assignments to frame objects.
        The function returns zero if the assignments are successfully applied, otherwise it returns a nonzero value.
        Note that the tension and compression limits are only used in nonlinear analyses
        ---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        LimitCompressionExists(bool)-This item is True if a compression force limit exists for the frame object.
        LimitCompression(float)-The compression force limit for the frame object. [F]
        LimitTensionExists(bool)-This item is True if a tension force limit exists for the frame object.
        LimitTension(float)-The tension force limit for the frame object. [F]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.FrameObj.SetTCLimits(name,LimitCompressionExists,LimitCompression,LimitTensionExists,LimitTension,
                                    itemType)

    def assign_FrameObj_GetAutoMesh(self,name):
        """
        ---This function retrieves the automatic meshing assignments to frame objects---
        inputs:
        name(str)-The name of an existing frame object.
        return:[index,AutoMesh,AutoMeshAtPoints,AutoMeshAtLines,NumSegs,AutoMeshMaxLength]
        AutoMesh(bool)-This item is True if the frame object is to be automatically meshed by the program when the
            analysis model is created.
        AutoMeshAtPoints(bool)-This item is applicable only when the AutoMesh item is True. If this item is True, the
            frame object is automatically meshed at intermediate joints along its length.
        AutoMeshAtLines(bool)-This item is applicable only when the AutoMesh item is True. If this item is True, the
            frame object is automatically meshed at intersections with other frames, area object edges and solid object edges.
        NumSegs(int)-This item is applicable only when the AutoMesh item is True. It is the minimum number of elements
            into which the frame object is automatically meshed. If this item is zero, the number of elements is not
            checked when the automatic meshing is done.
        AutoMeshMaxLength(float)-This item is applicable only when the AutoMesh item is True. It is the maximum length
            of auto meshed frame elements. If this item is zero, the element length is not checked when the automatic
            meshing is done. [L]
        """
        result=self.SapModel.FrameObj.GetAutoMesh(name)
        return result

    def assign_FrameObj_GetGroupAssign(self,name):
        """
        ---This function retrieves the names of the groups to which a specified frame object is assigned---
        inputs:
        name(str)-The name of an existing frame object.
        return:[index,numberGroups,Groups]
        numberGroups(int)-The number of group names retrieved.
        Groups(str list)-The names of the groups to which the frame object is assigned.
        """
        result=self.SapModel.FrameObj.GetGroupAssign(name)
        return result

    def assign_FrameObj_GetLoadDeformation(self,name):
        """
        ---This function retrieves the deformation load assignments to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        return:[index,NumberItems,FrameName,LoadPat,dof1, dof2, dof3, dof4, dof5, dof6,U1, U2, U3, R1, R2, R3]
        NumberItems(int)-The total number of deformation loads retrieved for the specified frame objects.
        FrameName(str list)-This is an array that includes the name of the frame object associated with each deformation load.
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each deformation load.
        dof1,dof2,dof3,dof4,dof5,dof6(bool)-These are arrays of boolean values indicating if the considered degree of
            freedom has a deformation load.
            dof1 = U1,dof2 = U2,dof3 = U3,dof4 = R1,dof5 = R2,dof6 = R3
        U1, U2, U3, R1, R2, R3(float)-These are arrays of deformation load values. The deformations specified for a
            given degree of freedom are applicable only if the corresponding DOF item for that degree of freedom is True.
            U1 = U1 deformation [L]
            U2 = U2 deformation [L]
            U3 = U3 deformation [L]
            R1 = R1 deformation [rad]
            R2 = R2 deformation [rad]
            R3 = R3 deformation [rad]
        """
        result=self.SapModel.FrameObj.GetLoadDeformation(name)
        return result

    def assign_FrameObj_GetLoadDistributed(self,name):
        """
        ---This function retrieves the distributed load assignments to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        return:[index,NumberItems,FrameName,LoadPat,MyType,CSys,Dir,RD1,RD2,Dist1,Dist2,Val1,Val2]
        NumberItems(int)-The total number of distributed loads retrieved for the specified frame objects.
        FrameName(str list)-This is an array that includes the name of the frame object associated with each
            distributed load.
        LoadPat(str list)-This is an array that includes the name of the coordinate system in which the distributed
            loads are specified.
        MyType(int list)-This is an array that includes 1 or 2, indicating the type of distributed load.
            1 = Force,2 = Moment
        CSys(str list)-This is an array that includes the name of the coordinate system in which each distributed
            load is defined. It may be Local or the name of a defined coordinate system.
        Dir(int list)-This is an array that includes an integer between 1 and 11, indicating the direction of the load.
            1 = Local 1 axis (only applies when CSys is Local)
            2 = Local 2 axis (only applies when CSys is Local)
            3 = Local 3 axis (only applies when CSys is Local)
            4 = X direction (does not apply when CSys is Local)
            5 = Y direction (does not apply when CSys is Local)
            6 = Z direction (does not apply when CSys is Local)
            7 = Projected X direction (does not apply when CSys is Local)
            8 = Projected Y direction (does not apply when CSys is Local)
            9 = Projected Z direction (does not apply when CSys is Local)
            10 = Gravity direction (only applies when CSys is Global)
            11 = Projected Gravity direction (only applies when CSys is Global)
            The positive gravity direction (see Dir = 10 and 11) is in the negative Global Z direction.
        RD1(float list)-This is an array that includes the relative distance from the I-End of the frame object
            to the start of the distributed load.
        RD2(float list)-This is an array that includes the relative distance from the I-End of the frame object
            to the end of the distributed load.
        Dist1(float list)-This is an array that includes the actual distance from the I-End of the frame object
            to the start of the distributed load. [L]
        Dist2(float list)-This is an array that includes the actual distance from the I-End of the frame object
            to the end of the distributed load. [L]
        Val1(float list)-This is an array that includes the load value at the start of the distributed load.
            [F/L] when MyType is 1 and [FL/L] when MyType is 2
        Val2(float list)-This is an array that includes the load value at the end of the distributed load.
            [F/L] when MyType is 1 and [FL/L] when MyType is 2
        """
        result=self.SapModel.FrameObj.GetLoadDistributed(name)
        return result

    def assign_FrameObj_GetLoadGravity(self,name):
        """
        ---This function retrieves the gravity load assignments to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        return:[index,NumberItems,FrameName,LoadPat,CSys,x,y,z]
        NumberItems(int)-The total number of gravity loads retrieved for the specified frame objects.
        FrameName(str list)-This is an array that includes the name of the frame object associated with each gravity load.
        LoadPat(str list)-This is an array that includes the name of the coordinate system in which the gravity load
            multipliers are specified.
        CSys(str list)-This is an array that includes the name of the coordinate system associated with each gravity load.
        x,y,z(float)-These are arrays of gravity load multipliers in the x, y and z directions of the specified
            coordinate system.
        """
        result=self.SapModel.FrameObj.GetLoadGravity(name)
        return result

    def assign_FrameObj_GetLoadPoint(self,name):
        """
        ---This function retrieves the point load assignments to frame objects.---
        inputs:
        name(str)-The name of an existing frame object or group depending on the value of the ItemType item.
        return:
        [index,NumberItems,FrameName,LoadPat,MyType,CSys,Dir,RelDist,Dist,Val]

        NumberItems(int)-The total number of point loads retrieved for the specified frame objects.
        FrameName(str list)-This is an array that includes the name of the frame object associated with each point load.
        LoadPat(str list)-This is an array that includes the name of the coordinate system in which the point loads are
            specified.
        MyType(int list)-This is an array that includes 1 or 2, indicating the type of point load.
            1 = Force,2 = Moment
        CSys(str list)-This is an array that includes the name of the coordinate system in which each point load is
            defined. It may be Local or the name of a defined coordinate system.
        Dir(int list)-This is an array that includes an integer between 1 and 11 indicating the direction of the load.
            1 = Local 1 axis (only applies when CSys is Local)
            2 = Local 2 axis (only applies when CSys is Local)
            3 = Local 3 axis (only applies when CSys is Local)
            4 = X direction (does not apply when CSys is Local)
            5 = Y direction (does not apply when CSys is Local)
            6 = Z direction (does not apply when CSys is Local)
            7 = Projected X direction (does not apply when CSys is Local)
            8 = Projected Y direction (does not apply when CSys is Local)
            9 = Projected Z direction (does not apply when CSys is Local)
            10 = Gravity direction (only applies when CSys is Global)
            11 = Projected Gravity direction (only applies when CSys is Global)
            The positive gravity direction (see Dir = 10 and 11) is in the negative Global Z direction.
        RelDist(float list)-This is an array that includes the relative distance from the I-End of the frame
            object to the location where the point load is applied.
        Dist(float list)-This is an array that includes the actual distance from the I-End of the frame object
            to the location where the point load is applied. [L]
        Val(float list)-This is an array that includes the value of the point load. [F] when MyType is 1 and [FL]
            when MyType is 2
        """
        result=self.SapModel.FrameObj.GetLoadPoint(name)
        return result

    def assign_FrameObj_GetLoadStrain(self,name):
        """
        ---This function retrieves the strain load assignments to frame objects.---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        return:
        [NumberItems,FrameName,LoadPat,DOF,Val,PatternName]

        NumberItems(int)-The total number of strain loads retrieved for the specified frame objects.
        FrameName(str list)-This is an array that includes the name of the frame object associated with each strain load.
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each strain load.
        DOF(int)-This is an array that includes 1, 2, 3, 4, 5 or 6, indicating the degree of freedom associated with
            each strain load.
            1 = Strain11,2 = Strain12,3 = Strain13,4 = Curvature1,5 = Curvature2,6 = Curvature3
        Val(float list)-This is an array that includes the strain value. [L/L] for DOF = 1, 2 and 3 and [1/L] for
            DOF = 4, 5 and 6
        """
        result=self.SapModel.FrameObj.GetLoadStrain(name)
        return result

    def assign_FrameObj_GetLoadTargetForce(self,name):
        """
        ---This function retrieves the target force assignments to frame objects.---
        :param name:
        :return:
        [index,numberItems,FrameName,LoadPat,dof1, dof2, dof3, dof4, dof5, dof6,P, V2, V3, T, M2, M3,T1, T2, T3, T4, T5, T6]

        numberItems(int)-The total number of deformation loads retrieved for the specified frame objects.
        FrameName(str list)-This is an array that includes the name of the frame object associated with each target force.
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each target force.
        dof1, dof2, dof3, dof4, dof5, dof6(bool list)-These are arrays of boolean values indicating if the considered
            degree of freedom has a target force assignment.
            dof1 = P,dof2 = V2,dof3 = V3,dof4 = T,dof5 = M2,dof6 = M3
        P, V2, V3, T, M2, M3(float list)-These are arrays of target force values. The target forces specified for a
            given degree of freedom are applicable only if the corresponding DOF item for that degree of freedom is True.
            U1 = U1 deformation [L]
            U2 = U2 deformation [L]
            U3 = U3 deformation [L]
            R1 = R1 deformation [rad]
            R2 = R2 deformation [rad]
            R3 = R3 deformation [rad]
        T1, T2, T3, T4, T5, T6(float list)-These are arrays of the relative distances along the frame objects where the
            target force values apply. The relative distances specified for a given degree of freedom are applicable
            only if the corresponding dofn item for that degree of freedom is True.
            T1 = relative location for P target force
            T2 = relative location for V2 target force
            T3 = relative location for V3 target force
            T4 = relative location for T target force
            T5 = relative location for M2 target force
            T6 = relative location for M3 target force
        """
        result=self.SapModel.FrameObj.GetLoadTargetForce(name)
        return result

    def assign_FrameObj_GetLoadTemperature(self,name):
        """
        ---This function retrieves the temperature load assignments to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        return:
        [index,NumberItems,FrameName,LoadPat,MyType,Val,PatternName]

        NumberItems(int)-The total number of temperature loads retrieved for the specified frame objects.
        FrameName(str list)-This is an array that includes the name of the frame object associated with each temperature load.
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each temperature load.
        MyType(int)-This is an array that includes 1, 2 or 3, indicating the type of temperature load.
            1 = Temperature
            2 = Temperature gradient along local 2 axis
            3 = Temperature gradient along local 3 axis
        Val(float list)-This is an array that includes the temperature load value. [T] for MyType= 1 and [T/L] for
            MyType= 2 and 3
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the
            temperature load.
        """
        result=self.SapModel.FrameObj.GetLoadTemperature(name)
        return result

    def assign_FrameObj_GetLocalAxes(self,name):
        """
        ---This function retrieves the frame local axis angle assignment for frame objects---
        inputs:
        name(str)-The name of an existing frame object.
        return:
        [index Ang,Advanced]

        Ang(float)-This is the angle that the local 2 and 3 axes are rotated about the positive local 1 axis,
            from the default orientation or, if the Advanced item is True, from the orientation determined by
            the plane reference vector. The rotation for a positive angle appears counter clockwise when the
            local +1 axis is pointing toward you. [deg]
        Advanced(bool)-This item is True if the line object local axes orientation was obtained using advanced
            local axes parameters.
        """
        result=self.SapModel.FrameObj.GetLocalAxes(name)
        return result

    def assign_FrameObj_GetMass(self,name):
        """
        ---This function retrieves the frame mass per unit length assignment for frame objects---
        inputs:
        name(str)-The name of an existing frame object.
        return:
        [index,MassOverL]
        MassOverL(float)-The mass per unit length assigned to the frame object. [M/L]
        """
        result=self.SapModel.FrameObj.GetMass(name)
        return result

    def assign_FrameObj_GetMatTemp(self,name):
        """
        ---This function retrieves the material temperature assignments to frame objects---
        inputs:
        name(str)-The name of an existing frame object
        return:
        [index,Temp,PatternName]
        Temp(float)-This is the material temperature value assigned to the frame object. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the material temperature
            for the frame object is uniform along the object at the value specified by Temp.If PatternName is the name
            of a defined joint pattern, the material temperature for the frame object may vary from one end to the other.
            The material temperature at each end of the object is equal to the specified temperature multiplied by the
            pattern value at the joint at the end of the frame object.
        """
        result=self.SapModel.FrameObj.GetMatTemp(name)
        print(result)

    def assign_FrameObj_GetNameList(self):
        """
        ---This function retrieves the names of all defined frame objects---
        inputs:
        return:
        [index,NumberNames,MyName]
        NumberNames(int)-The number of frame object names retrieved by the program.
        MyName(str list)-This is a one-dimensional array of frame object names.
        """
        result=self.SapModel.FrameObj.GetNameList()
        return result

    def assign_FrameObj_GetPDeltaForce(self,name):
        """
        ---This function retrieves the P-Delta force assignments to frame objects. P-Delta forces do not apply to
        curved frame objects. If you request data for a curved frame, an error is returned.
        ---
        inputs:
        name(str)-The name of an existing straight frame object.
        return:
        [index,NumberForces,PDeltaForce,Dir,CSys]
        NumberForces(int)-The number of P-Delta forces assigned to the frame object.
        PDeltaForce(float list)-This is an array of the P-Delta force values assigned to the frame object. [F]
        Dir(int list)-This is an array that contains 0, 1, 2 or 3, indicating the direction of each P-Delta force assignment.
            0 = Frame object local 1-axis direction
            1 = Projected X direction in CSys coordinate system
            2 = Projected Y direction in CSys coordinate system
            3 = Projected Z direction in CSys coordinate system
        CSys(str list)-This is an array that contains the name of the coordinate system in which each projected P-Delta
            force is defined. This item is blank when the Dir item is zero, that is, when the P-Delta force is defined
            in the frame object local 1-axis direction.
        """
        result=self.SapModel.FrameObj.GetPDeltaForce(name)
        return result

    def assign_FrameObj_GetPoints(self,name):
        """
        ---This function retrieves the names of the point objects at each end of a specified frame object---
        inputs:
        name(str)-The name of a defined frame object.
        return:
        [index,Point1,Point2]
        Point1(str)-The name of the point object at the I-End of the specified frame object.
        Point2(str)-The name of the point object at the J-End of the specified frame object.
        """
        result=self.SapModel.FrameObj.GetPoints(name)
        return result

    def assign_FrameObj_GetReleases(self,name):
        """
        ---This function retrieves the frame object end release and partial fixity assignments.---
        inputs:
        name(str)-The name of an existing frame object.
        return:
        [index,ii,jj,startValue,endValue]
        ii,jj(bool list)-These are arrays of six booleans indicating the I-End and J-End releases for the frame object.
            ii(0) and jj(0) = U1 release
            ii(1) and jj(1) = U2 release
            ii(2) and jj(2) = U3 release
            ii(3) and jj(3) = R1 release
            ii(4) and jj(4) = R2 release
            ii(5) and jj(5) = R3 release
        startValue,endValue(float list)-These are arrays of six values indicating the I-End and J-End partial fixity
            springs for the frame object.
            StartValue(0) and EndValue(0) = U1 partial fixity [F/L]
            StartValue(1) and EndValue(1) = U2 partial fixity [F/L]
            StartValue(2) and EndValue(2) = U3 partial fixity [F/L]
            StartValue(3) and EndValue(3) = R1 partial fixity [FL/rad]
            StartValue(4) and EndValue(4) = R2 partial fixity [FL/rad]
            StartValue(5) and EndValue(5) = R3 partial fixity [FL/rad]
        """
        result=self.SapModel.FrameObj.GetReleases(name)
        return result

    def assign_FrameObj_GetSection(self,name):
        """
        ---This function retrieves the frame section property assigned to a frame object---
        inputs:
        name(str)-The name of a defined frame object.
        return:
        [index,PropName,SAuto]
        PropName(str)-If no auto select list is assigned to the frame object, this is the name of the frame section
            property assigned to the frame object. If an auto select list is assigned to the frame object, this is
            the name of the frame section property, within the auto select list, which is currently being used as
            the analysis property for the frame object. If this item is None, no frame section property is assigned
            to the frame object.
        SAuto(str)-This is the name of the auto select list assigned to the frame object, if any. If this item is
            returned as a blank string, no auto select list is assigned to the frame object.
        """
        result=self.SapModel.FrameObj.GetSection(name)
        return result

    def assign_FrameObj_GetSpring(self,name):
        """
        ---This function retrieves the spring assignments to a frame object---
        inputs:
        name(str)-The name of an existing frame object.
        return:
        [index,NUmberSprings,MyType,s,SimpleSpringType,LinkProp,SpringLocalOneType,Dir,Plane23Angle,VecX,VecY,VecZ,
        CSys,Ang]
        NumberSprings(int)-The number of springs assignments made to the specified frame object.
        MyType(int list)-Each value in this array is either 1 or 2, indicating the spring property type.
            1 = Simple spring,2 = Link property
        s(float list)-Each value in this array is the simple spring stiffness per unit length of the frame object.
            This item applies only when the corresponding MyType = 1. [F/L2]
        SimpleSpringType(int list)-Each value in this array is 1, 2 or 3, indicating the simple spring type.
            This item applies only when the corresponding MyType = 1.
            1 = Spring resists tension and compression
            2 = Spring resists compression only
            3 = Spring resists tension only
        LinkProp(str list)-Each value in this array is the name of the link property assigned to the spring.
            This item applies only when the corresponding MyType = 2.
        SpringLocalOneType(int list)-Each value in this array is 1, 2 or 3, indicating the method used to specify
            the spring positive local 1-axis orientation.
            1 = Parallel to frame object local axis
            2 = In the frame object 2-3 plane
            3 = User specified direction vector
        Dir(int list)-Each value in this array is 1, 2, 3, -1, -2 or -3, indicating the frame object local axis that
            corresponds to the positive local 1-axis of the spring. This item applies only when the corresponding
            SpringLocalOneType = 1.
        Plane23Angle(float list)-Each value in this array is the angle in the frame object 2-3 plane measured counter
            clockwise from the frame positive 2-axis to the spring positive 1-axis. This item applies only when the
            corresponding SpringLocalOneType = 2. [deg]
        VecX(float list)-Each value in this array is the X-axis or frame local 1-axis component (depending on the
            CSys specified) of the user specified direction vector for the spring local 1-axis. The direction
            vector is in the coordinate system specified by the CSys item. This item applies only when the
            corresponding SpringLocalOneType = 3.
        VecY(float list)-Each value in this array is the Y-axis or frame local 2-axis component (depending on the
            CSys specified) of the user specified direction vector for the spring local 1-axis. The direction vector
            is in the coordinate system specified by the CSys item. This item applies only when the corresponding
            SpringLocalOneType = 3.
        VecZ(float list)-Each value in this array is the X-axis or frame local 3-axis component (depending on the
            CSys specified) of the user specified direction vector for the spring local 1-axis. The direction vector
            is in the coordinate system specified by the CSys item. This item applies only when the corresponding
            SpringLocalOneType = 3.
        CSys(str list)-Each value in this array is Local (meaning the frame object local coordinate system) or the
            name of a defined coordinate system. This item is the coordinate system in which the user specified
            direction vector, Vec, is specified. This item applies only when the corresponding SpringLocalOneType = 3.
        Ang(float list)-Each value in this array is the angle that the link local 2-axis is rotated from its default
            orientation. This item applies only when the corresponding MyType = 2. [deg]
        """
        result=self.SapModel.FrameObj.GetSpring(name)
        return result

    def assign_FrameObj_GetTCLimits(self,name):
        """
        ---This function retrieves the tension/compression force limit assignments to frame objects.The function
        returns zero if the assignments are successfully retrieved, otherwise it returns a nonzero value.Note that
        the tension and compression limits are used only in nonlinear analyses.
        ---
        inputs:
        name(str)-The name of an existing frame object.
        return:
        [index,LimitCompressionExists,LimitCompression,LimitTensionExists,LimitTension]
        LimitCompressionExists(bool)-This item is True if a compression force limit exists for the frame object.
        LimitCompression(float)-The compression force limit for the frame object. [F]
        LimitTensionExists(bool)-This item is True if a tension force limit exists for the frame object.
        LimitTension(float)-The tension force limit for the frame object. [F]
        """
        result=self.SapModel.FrameObj.GetTCLimits(name)
        return result

    def assign_FrameObj_GetTransformationMatrix(self,name):
        """
        ---The function returns zero if the frame object transformation matrix is successfully retrieved; otherwise
        it returns a nonzero value.
        ---
        inputs:
        name(str)-The name of an existing frame object.
        return:
        [index,value]
        value(float list)-Value is an array of nine direction cosines that define the transformation matrix.The following
            matrix equation shows how the transformation matrix is used to convert items from the frame object local
            coordinate system to the global coordinate system.
            In the equation, c0 through c8 are the nine values from the transformation array, (Local1, Local2, Local3)
            are an item (such as a load) in the object local coordinate system, and (GlobalX, GlobalY, GlobalZ) are
            the same item in the global coordinate system.The transformation from the local coordinate system to the
            present coordinate system is the same as that shown above for the global system if you substitute the
            present system for the global system.
        """
        result=self.SapModel.FrameObj.GetTransformationMatrix(name)
        return result

    def assign_CableObj_AddByCoord(self,xi,yi,zi,xj,yj,zj,propName="Default",UserName="",CSys="Global"):
        """
        ---This function adds a new cable object whose end points are at the specified coordinates.---
        inputs:
        xi,yi,zi(float)-The coordinates of the I-End of the added cable object. The coordinates are in the coordinate
            system defined by the CSys item.
        xj,yj,zj(float)-The coordinates of the J-End of the added cable object. The coordinates are in the coordinate
            system defined by the CSys item.
        propName(str)-This is Default or the name of a defined cable property.If it is Default, the program assigns
            a default cable property to the cable object. If it is the name of a defined cable property, that property
            is assigned to the cable object.
        UserName(str):This is an optional user specified name for the cable object. If a UserName is specified and that
            name is already used for another cable object, the program ignores the UserName.
        CSys(str)-The name of the coordinate system in which the cable object end point coordinates are defined.
        """
        #This is the name that the program ultimately assigns for the cable object. If no UserName is specified,n
        # the program assigns a default name to the cable object. If a UserName is specified and that name is not
        # used for another frame, cable or tendon object, the UserName is assigned to the cable object; otherwise a
        # default name is assigned to the cable object.
        name=""
        self.SapModel.CableObj.AddByCoord(xi,yi,zi,xj,yj,zj,name,propName,UserName,CSys)

    def assign_CableObj_AddByPoint(self,Point1,Point2,PropName="Default",UserName=""):
        """
        ---This function adds a new cable object whose end points are specified by name---
        inputs:
        Point1(str)-The name of a defined point object at the I-End of the added cable object.
        Point2(str)-The name of a defined point object at the J-End of the added cable object.
        PropName(str)-This is Default or the name of a defined cable property.If it is Default, the program assigns a
            default cable property to the cable object. If it is the name of a defined cable property, that property
            is assigned to the cable object.
        UserName(str)-This is an optional user specified name for the cable object. If a UserName is specified and that
        name is already used for another cable object, the program ignores the UserName.
        """
        # This is the name that the program ultimately assigns for the cable object. If no UserName is specified,n
        # the program assigns a default name to the cable object. If a UserName is specified and that name is not
        # used for another frame, cable or tendon object, the UserName is assigned to the cable object; otherwise a
        # default name is assigned to the cable object.
        name = ""
        self.SapModel.CableObj.AddByPoint(Point1,Point2,name,PropName,UserName)

    def assign_CableObj_ChangeName(self,name,newName):
        """
        ---The function returns zero if the new name is successfully applied, otherwise it returns a nonzero value.---
        inputs:
        name(str)-The existing name of a defined cable object.
        newName(str)-The new name for the cable object.
        """
        self.SapModel.CableObj.ChangeName(name,newName)

    def assign_CableObj_Count(self):
        """
        ---This function returns a count of the cable objects in the model.---
        """
        result=self.SapModel.CableObj.Count()
        return result

    def assign_CableObj_SetCableData(self,name,CableType,NumSegs,Weight,ProjectedLoad,Value,UseDeformedGeom=False,
                                     ModelUsingFrames=False):
        """
        ---This function assigns the cable definition parameters to a cable object.---
        inputs:
        name(str)-The name of a defined cable object.
        CableType(int)-This is 1, 2, 3, 4, 5, 6, 7, 8, or 9, indicating the cable definition parameter.
            1 = Minimum tension at I-End
            2 = Minimum tension at J-End
            3 = Tension at I-End
            4 = Tension at J-End
            5 = Horizontal tension component
            6 = Maximum vertical sag
            7 = Low-point vertical sag
            8 = Undeformed length
            9 = Relative undeformed length
        NumSegs(int)-This is the number of segments into which the program internally divides the cable.
        Weight(float)-The added weight per unit length used when calculating the cable shape. [F/L]
        ProjectedLoad(float)-The projected uniform gravity load used when calculating the cable shape. [F/L]
        Value(float list)-This is the value of the parameter used to define the cable shape. The item that Value
            represents depends on the CableType item.
            CableType = 1: Not Used
            CableType = 2: Not Used
            CableType = 3: Tension at I-End [F]
            CableType = 4: Tension at J-End [F]
            CableType = 5: Horizontal tension component [F]
            CableType = 6: Maximum vertical sag [L]
            CableType = 7: Low-point vertical sag [L]
            CableType = 8: Undeformed length [L]
            CableType = 9: Relative undeformed length
        UseDeformedGeom(bool)-If this item is True, the program uses the deformed geometry for the cable object;
            otherwise it uses the undeformed geometry.
        ModelUsingFrames(bool)-If this item is True, the analysis model uses frame elements to model the cable
            instead of using cable elements.
        """
        self.SapModel.CableObj.SetCableData(name,CableType,NumSegs,Weight,ProjectedLoad,Value,UseDeformedGeom,ModelUsingFrames)

    def assign_CableObj_SetGroupAssign(self,name,groupName,Remove=False,itemType=0):
        """
        ---This function adds or removes cable objects from a specified group---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        groupName(str)-The name of an existing group to which the assignment is made.
        Remove(bool)-If this item is False, the specified cable objects are added to the group specified by
            the GroupName item. If it is True, the cable objects are removed from the group.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.CableObj.SetGroupAssign(name,groupName,Remove,itemType)

    def assign_CableObj_SetLoadDeformation(self,name,loadPat,d,itemType=0):
        """
        ---This function assigns deformation loads to cable objects---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        d(float)-This is the axial deformation load value. [L]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.CableObj.SetLoadDeformation(name,loadPat,d,itemType)

    def assign_CableObj_SetLoadDistributed(self,name,loadPat,myType,Dir,Value,CSys="Global",Replace=True,itemType=0):
        """
        ---This function assigns uniform distributed loads over the full length of cable objects---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        myType(int)-This is 1 or 2, indicating the type of distributed load.
            1 = Force per unit length,2 = Moment per unit length
        Dir(int)-This is 1, 2, 3, 4, 5, 6 or 10, indicating the direction of the load.
            1 = Local 1 axis (only applies when CSys is Local)
            2 = Local 2 axis (only applies when CSys is Local)
            3 = Local 3 axis (only applies when CSys is Local)
            4 = X direction (does not apply when CSys is Local)
            5 = Y direction (does not apply when CSys is Local)
            6 = Z direction (does not apply when CSys is Local)
            10 = Gravity direction (only applies when CSys is Global)
            The positive gravity direction (see Dir = 10) is in the negative Global Z direction.
        Value(float)-This is the load value of the distributed load. The distributed load is applied over
            the full length of the cable. [F/L] when MyType is 1 and [FL/L] when MyType is 2
        CSys(str)-This is Local or the name of a defined coordinate system. It is the coordinate system
            in which the loads are specified.
        Replace(bool)-If this item is True, all previous loads, if any, assigned to the specified cable object(s),
            in the specified load pattern, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.CableObj.SetLoadDistributed(name,loadPat,myType,Dir,Value,CSys,Replace,itemType)

    def assign_CableObj_SetLoadGravity(self,name,loadPat,x,y,z,Replace=True,CSys="Global",itemType=0):
        """
        ---This function assigns gravity load multipliers to cable objects---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        x,y,z(float)-These are the gravity load multipliers in the x, y and z directions of the specified coordinate system.
        Replace(bool)-If this item is True, all previous gravity loads, if any, assigned to the specified cable object(s),
            in the specified load pattern, are deleted before making the new assignment.
        CSys(str)-The coordinate system in which the x, y and z multipliers are specified.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.CableObj.SetLoadGravity(name,loadPat,x,y,z,Replace,CSys,itemType)

    def assign_CableObj_SetLoadStrain(self,name,loadPat,Strain,Replace=True,PatternName="",itemType=0):
        """
        ---This function assigns strain loads to cable objects---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        Strain(float)-This is the axial strain load value. [L/L]
        Replace(bool)-If this item is True, all previous strain loads, if any, assigned to the specified cable
            object(s), in the specified load pattern, are deleted before making the new assignment.
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the strain load for
            the cable object is uniform along the object at the value specified by Strain.If PatternName is the
            name of a defined joint pattern, the strain load for the cable object is based on the specified
            strain value multiplied by the pattern value at the joints at each end of the cable object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.CableObj.SetLoadStrain(name,loadPat,Strain,Replace,PatternName,itemType)

    def assign_CableObj_SetLoadTargetForce(self,name,loadPat,P,RD,itemType=0):
        """
        ---This function assigns target forces to cable objects---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        P(float)-This is the axial target force value. [F]
        RD(float)-This is the relative distance along the cable object to the location where the target force
            value applies. The relative distance must be between 0 and 1, 0 <= RD <=1.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.CableObj.SetLoadTargetForce(name,loadPat,P,RD,itemType)

    def assign_CableObj_SetLoadTemperature(self,name,loadPat,Val,PatternName="",Replace=True,itemType=0):
        """
        ---This function assigns temperature loads to cable objects---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        Val(float)-This is the temperature change value. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the temperature load
            for the cable object is uniform along the object at the value specified by Val.If PatternName is the name
            of a defined joint pattern, the temperature load for the cable object is based on the specified temperature
            value multiplied by the pattern value at the joints at each end of the cable object.
        Replace(bool)-If this item is True, all previous temperature loads, if any, assigned to the specified cable
            object(s), in the specified load case, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.CableObj.SetLoadTemperature(name,loadPat,Val,PatternName,Replace,itemType)

    def assign_CableObj_SetMass(self,name,MassOverL,Replace=False,itemType=0):
        """
        ---This function assigns mass per unit length to cable objects---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        MassOverL(float)-The mass per unit length assigned to the cable object. [M/L]
        Replace(bool)-If this item is True, all existing mass assignments to the cable object are removed before
            assigning the specified mas. If it is False, the specified mass is added to any mass already assigned
            to the cable object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.CableObj.SetMass(name,MassOverL,Replace,itemType)

    def assign_CableObj_SetMatTemp(self,name,Temp,PatternName="",itemType=0):
        """
        ---This function assigns material temperatures to cable objects.---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        Temp(float)-This is the material temperature value assigned to the cable object. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the material temperature
            for the cable object is uniform along the object at the value specified by Temp.If PatternName is the name
            of a defined joint pattern, the material temperature for the cable object may vary from one end to the
            other. The material temperature at each end of the object is equal to the specified temperature multiplied
            by the pattern value at the joint at the end of the cable object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.CableObj.SetMatTemp(name,Temp,PatternName,itemType)

    def assign_CableObj_SetProperty(self,name,PropName,itemType=0):
        """
        ---This function assigns a cable property to a cable object---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        PropName(str)-The name of a cable property to be assigned to the specified cable object(s).
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.CableObj.SetProperty(name,PropName,itemType)

    def assign_CableObj_GetCableData(self,name):
        """
        ---This function retrieves definition data for a specified cable object.---
        inputs:
        name(str)-The name of a defined cable object.
        retrurn:
        [index,CableType,NumSegs,Weight,ProjectedLoad,UseDeformedGeom,ModelUsingFrames,Parameter]
        CableType(int)-This is 1, 2, 3, 4, 5, 6, 7, 8, or 9, indicating the cable definition parameter.
            1 = Minimum tension at I-End
            2 = Minimum tension at J-End
            3 = Tension at I-End
            4 = Tension at J-End
            5 = Horizontal tension component
            6 = Maximum vertical sag
            7 = Low-point vertical sag
            8 = Undeformed length
            9 = Relative undeformed length
        NumSegs(int)-This is the number of segments into which the program internally divides the cable.
        Weight(float)-The added weight per unit length used when calculating the cable shape. [F/L]
        ProjectedLoad(float)-The projected uniform gravity load used when calculating the cable shape. [F/L]
        UseDeformedGeom(bool)-If this item is True, the program uses the deformed geometry for the cable object;
            otherwise it uses the undeformed geometry.
        ModelUsingFrames(bool)-If this item is True, the analysis model uses frame elements to model the cable
            instead of using cable elements.
        Parameter(float list)-This is an array of parameters related to the cable shape. The array is dimensioned by Sap2000.
            Parameter(0) = Tension at I-End [F]
            Parameter(1) = Tension at J-End [F]
            Parameter(2) = Horizontal tension component [F]
            Parameter(3) = Maximum deformed vertical sag [L]
            Parameter(4) = Deformed low-point vertical sag [L]
            Parameter(5) = Deformed length [L]
            Parameter(6) = Deformed relative length
            Parameter(7) = Maximum undeformed vertical sag [L]
            Parameter(8) = Undeformed low-point vertical sag [L]
            Parameter(9) = Undeformed length [L]
            Parameter(10) = Undeformed relative length
        """
        result=self.SapModel.CableObj.GetCableData(name)
        return result

    def assign_CableObj_GetCableGeometry(self,name):
        """
        ---This function retrieves geometric data for a specified cable object---
        inputs:
        name(str)-The name of a defined cable object.
        return:
        [index,NumberPoints,x,y,z,sag,distance,RD]
        NumberPoints(int)-The number of points defining the cable geometry.
        x,y,z(float)-The x, y and z coordinates of the considered point on the cable in the coordinate system
            specified by the CSys item. [L]
        sag(float)-The cable vertical sag, measured from the chord, at the considered point. [L]
        Distance(float)-The distance along the cable, measured from the cable I-End, to the considered point. [L]
        RD(float)-The relative distance along the cable, measured from the cable I-End, to the considered point.
        """
        result=self.SapModel.CableObj.GetCableGeometry(name)
        return result

    def assign_CableObj_GetGroupAssign(self,name):
        """
        ---This function retrieves the names of the groups to which a specified cable object is assigned---
        inputs:
        name(str)-The name of an existing cable object.
        return:
        [index,NumberGroups,Groups]
        NumberGroups(int)-The number of group names retrieved.
        Groups(str)-The names of the groups to which the cable object is assigned.
        """
        result=self.SapModel.CableObj.GetGroupAssign(name)
        return result

    def assign_CableObj_GetLoadDeformation(self,name):
        """
        ---This function retrieves the deformation load assignments to cable objects.---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        return:
        [index,numberItems,CableName,LoadPat,U1]
        numberItems(int)-The total number of deformation loads retrieved for the specified cable objects.
        CableName(str list)-This is an array that includes the name of the cable object associated with each deformation load.
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each deformation load.
        U1(float list)-This is an array of axial deformation load values. [L]
        """
        result=self.SapModel.CableObj.GetLoadDeformation(name)
        return result

    def assign_CableObj_GetLoadDistributed(self,name):
        """
        ---This function retrieves the distributed load assignments to cable objects. The loads are uniformly
        distributed over the full length of cable objects.
        ---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        return:
        [index,numberItems,CableName,loadPat,MyType,CSys,Dir,Value]
        numberItems(int)-The total number of distributed loads retrieved for the specified cable objects.
        cableName(str list)-This is an array that includes the name of the cable object associated with each distributed load.
        loadPat(str list)-This is an array that includes the name of the coordinate system in which the distributed
            loads are specified.
        myType(int list)-This is an array that includes 1 or 2, indicating the type of distributed load.
            1 = Force,2 = Moment
        CSys(str list)-This is an array that includes the name of the coordinate system in which each distributed
            load is defined. It may be Local or the name of a defined coordinate system.
        Dir(int)-This is 1, 2, 3, 4, 5, 6 or 10, indicating the direction of the load.
            1 = Local 1 axis (only applies when CSys is Local)
            2 = Local 2 axis (only applies when CSys is Local)
            3 = Local 3 axis (only applies when CSys is Local)
            4 = X direction (does not apply when CSys is Local)
            5 = Y direction (does not apply when CSys is Local)
            6 = Z direction (does not apply when CSys is Local)
            10 = Gravity direction (only applies when CSys is Global)
            The positive gravity direction (see Dir = 10) is in the negative Global Z direction.
        Value(float)-This is the load value of the distributed load. The distributed load is applied over the full
            length of the cable. [F/L] when MyType is 1 and [FL/L] when MyType is 2
        """
        result=self.SapModel.CableObj.GetLoadDistributed(name)
        return result

    def assign_CableObj_GetLoadGravity(self,name):
        """
        ---This function retrieves the gravity load assignments to cable objects---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        return:
        [index,numberItems,cableName,loadPat,CSys,x,y,z]
        numberItems(int)-The total number of gravity loads retrieved for the specified cable objects.
        cableName(str list)-This is an array that includes the name of the cable object associated with each gravity load.
        loadPat(str list)-This is an array that includes the name of the coordinate system in which the gravity load
            multipliers are specified.
        CSys(str list)-This is an array that includes the name of the coordinate system associated with each gravity load.
        x,y,z(float list)-These are arrays of gravity load multipliers in the x, y and z directions of the specified
            coordinate system.
        """
        result=self.SapModel.CableObj.GetLoadGravity(name)
        return result

    def assign_CableObj_GetLoadStrain(self,name):
        """
        ---This function retrieves the strain load assignments to cable objects---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        return:
        [index,numberItems,CableName,loadPat,Strain,PatternName]
        numberItems(int)-The total number of strain loads retrieved for the specified cable objects.
        CableName(str list)-This is an array that includes the name of the cable object associated with each strain load.
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each strain load.
        Strain(float list)-This is an array that includes the axial strain value. [L/L]
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the strain load.
        """
        result=self.SapModel.CableObj.GetLoadStrain(name)
        return result

    def assign_CableObj_GetLoadTargetForce(self,name):
        """
        ---This function retrieves the target force assignments to cable objects.---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        return:
        [index,numberItems,cableName,LoadPat,P,RD]
        numberItems(int)-The total number of deformation loads retrieved for the specified cable objects.
        cableName(str list)-This is an array that includes the name of the cable object associated with each target force.
        loadPat(str list)-This is an array that includes the name of the load pattern associated with each target force.
        P(float list)-This is an array of axial target force values. [F]
        RD(float list)-This is an array of the relative distances along the cable objects where the axial target force
            values apply.
        """
        result=self.SapModel.CableObj.GetLoadTargetForce(name)
        return result

    def assign_CableObj_GetLoadTemperature(self,name):
        """
        ---This function retrieves the temperature load assignments to cable objects---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        return:
        [index,numberItems,cableName,loadPat,Val,PatternName]
        numberItems(int)-The total number of temperature loads retrieved for the specified cable objects.
        cableName(str list)-This is an array that includes the name of the cable object associated with each temperature load.
        loadPat(str list)-This is an array that includes the name of the load pattern associated with each temperature load.
        Val(float list)-This is an array that includes the temperature load value. [T]
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the
            temperature load.
        """
        result=self.SapModel.CableObj.GetLoadTemperature(name)
        return result

    def assign_CableObj_GetMass(self,name):
        """
        ---This function retrieves the mass per unit length assignment for cable objects---
        inputs:
        name(str)-The name of an existing cable object.
        return:
        [index,massOverL]
        massOverL(float)-The mass per unit length assigned to the cable object. [M/L]
        """
        result=self.SapModel.CableObj.GetMass(name)
        return result

    def assign_CableObj_GetMatTemp(self,name):
        """
        ---This function retrieves the material temperature assignments to cable objects.---
        inputs:
        name(str)-The name of an existing cable object.
        return:
        [index,Temp,PatternName]
        Temp(float)-This is the material temperature value assigned to the cable object. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the material temperature
            for the cable object is uniform along the object at the value specified by Temp.If PatternName is the name
            of a defined joint pattern, the material temperature for the cable object may vary from one end to the other.
            The material temperature at each end of the object is equal to the specified temperature multiplied by the
            pattern value at the joint at the end of the cable object.
        """
        result=self.SapModel.CableObj.GetMatTemp(name)
        return result

    def assign_CableObj_GetNameList(self):
        """
        ---This function retrieves the names of all defined cable objects---
        return:
        [index,numberNames,myName]
        numberNames(int)-The number of cable object names retrieved by the program.
        myName(str list)-This is a one-dimensional array of cable object names.
        """
        result=self.SapModel.CableObj.GetNameList()
        return result

    def assign_CableObj_GetPoints(self,name):
        """
        ---This function retrieves the names of the point objects at each end of a specified cable object.---
        inputs:
        name(str)-The name of a defined cable object.
        return:
        [index,Point1,Point2]
        Point1(str)-The name of the point object at the I-End of the specified cable object.
        Point2(str)-The name of the point object at the J-End of the specified cable object.
        """
        result=self.SapModel.CableObj.GetPoints(name)
        return result

    def assign_CableObj_GetProperty(self,name):
        """
        ---This function retrieves the cable property assigned to a cable object---
        inputs:
        name(str)-The name of a defined cable object.
        return:
        [index,PropName]
        PropName(str)-The name of the cable property assigned to the cable object.
        """
        result=self.SapModel.CableObj.GetProperty(name)
        return result

    def assing_CableObj_GetTransformationMatrix(self,name):
        """
        ---The function returns zero if the cable object transformation matrix is successfully retrieved; otherwise
        it returns a nonzero value.
        ---
        inputs:
        name(str)-The name of an existing cable object.
        return:
        [index,value]
        value(float list)-Value is an array of nine direction cosines that define the transformation matrix.The following
            matrix equation shows how the transformation matrix is used to convert items from the cable object local
            coordinate system to the global coordinate system.In the equation, c0 through c8 are the nine values from the
            transformation array, (Local1, Local2, Local3) are an item (such as a load) in the object local coordinate
            system, and (GlobalX, GlobalY, GlobalZ) are the same item in the global coordinate system.The transformation
            from the local coordinate system to the present coordinate system is the same as that shown above for the
            global system if you substitute the present system for the global system.
        """
        result=self.SapModel.CableObj.GetTransformationMatrix(name)
        return result

    def assign_TendonObj_AddByCoord(self,xi,yi,zi,xj,yj,zj,PropName="Default",UserName="",CSsy="Global"):
        """
        ---This function adds a new tendon object whose end points are at the specified coordinates---
        inputs:
        xi,yi,zi(float)-The coordinates of the I-End of the added tendon object. The coordinates are in the coordinate
            system defined by the CSys item.
        xj,yj,zj(float)-The coordinates of the J-End of the added tendon object. The coordinates are in the coordinate
            system defined by the CSys item.
        PropName(str)-This is Default, None or the name of a defined tendon property.If it is Default, the program
            assigns a default tendon property to the tendon object. If it is None, no tendon property is assigned to
            the tendon object. If it is the name of a defined tendon property, that property is assigned to the tendon object.
        UserName(str)-This is an optional user specified name for the tendon object. If a UserName is specified and that
            name is already used for another tendon object, the program ignores the UserName.
        CSys(str)-The name of the coordinate system in which the tendon object end point coordinates are defined.
        """
        # This is the name that the program ultimately assigns for the tendon object. If no UserName is specified,
        # the program assigns a default name to the tendon object. If a UserName is specified and that name is not
        # used for another frame, cable or tendon object, the UserName is assigned to the tendon object; otherwise
        # a default name is assigned to the tendon object.
        name = ""
        self.SapModel.TendonObj.AddByCoord(xi,yi,zi,xj,yj,zj,name,PropName,UserName,CSsy)

    def assign_TendonObj_AddByPoint(self,Point1,Point2,PropName="Default",UserName=""):
        """
        ---This function adds a new tendon object whose end points are specified by name---
        inputs:
        Point1(str)-The name of a defined point object at the I-End of the added tendon object.
        Point2(str)-The name of a defined point object at the J-End of the added tendon object.
        PropName(str)-This is Default, None or the name of a defined tendon property.If it is Default, the program
            assigns a default tendon property to the tendon object. If it is None, no tendon property is assigned
            to the tendon object. If it is the name of a defined tendon property, that property is assigned to the
            tendon object.
        UserName(str)-This is an optional user specified name for the tendon object. If a UserName is specified and
            that name is already used for another tendon object, the program ignores the UserName.
        """
        # This is the name that the program ultimately assigns for the tendon object. If no UserName is specified,
        # the program assigns a default name to the tendon object. If a UserName is specified and that name is not
        # used for another frame, cable or tendon object, the UserName is assigned to the tendon object; otherwise
        # a default name is assigned to the tendon object.
        name = ""
        self.SapModel.TendonObj.AddByPoint(Point1,Point2,name,PropName,UserName)

    def assign_TendonObj_Count(self):
        """
        ---This function returns a count of the tendon objects in the model---
        """
        result=self.SapModel.TendonObj.Count()
        return result

    def assign_TendonObj_SetDiscretization(self,name,Value,itemType=0):
        """
        ---This function assigns a maximum discretization length to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        Value(float)-The maximum discretization length for the tendon. [L]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.TendonObj.SetDiscretization(name,Value,itemType)

    def assign_TendonObj_SetGroupAssign(self,name,GroupName,Remove=False,itemType=0):
        """
        ---This function adds or removes tendon objects from a specified group.---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        GroupName(str)-The name of an existing group to which the assignment is made.
        Remove(bool)-If this item is False, the specified tendon objects are added to the group specified by the
            GroupName item. If it is True, the tendon objects are removed from the group.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.TendonObj.SetGroupAssign(name,GroupName,Remove,itemType)

    def assign_TendonObj_SetLoadDeformation(self,name,LoadPat,d,itemType=0):
        """
        ---This function assigns deformation loads to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        LoadPat(str)-The name of a defined load pattern.
        d(float)-This is the axial deformation load value. [L]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.TendonObj.SetLoadDeformation(name,LoadPat,d,itemType)

    def assign_TendonObj_SetLoadedGroup(self,name,GroupName,itemType=0):
        """
        ---This function makes the loaded group assignment to tendon objects. A tendon object transfers its load
        to any object that is in the specified group.
        ---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        GroupName(str)-This is the name of an existing group. All objects in the specified group can be loaded by the tendon.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.SapModel.TendonObj.SetLoadedGroup(name,GroupName,itemType)

    def assign_TendonObj_SetLoadForceStress(self,name,loadPat,JackFrom,LoadType,Value,CurvatureCoeff,WobbleCoeff,
                                            LossAnchorage,LossShortening,LossCreep,LossShrinkage,LossSteelRelax,
                                            Replace=True,itemType=0):
        """
        ---This function assigns force/stress loads to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        JackFrom(int)-This is 1, 2 or 3, indicating how the tendon is jacked.
            1 = Tendon jacked from I-End
            2 = Tendon jacked from J-End
            3 = Tendon jacked from both ends
        LoadType(int)-This is either 0 or 1, indicating how the type of load.
            0 = Force,1 = Stress
        Value(float)-This is the load value. [F] whenLoadType is 0, and [F/L2] when Loadtype is 1
        CurvatureCoeff(float)-The curvature coefficient used when calculating friction losses.
        WobbleCoeff(float)-The wobble coefficient used when calculating friction losses. [1/L]
        LossAnchorage(float)-The anchorage set slip. [L]
        LossShortening(float)-The tendon stress loss due to elastic shortening. [F/L2]
        LossCreep(float)-The tendon stress loss due to creep. [F/L2]
        LossShrinkage(float)-The tendon stress loss due to shrinkage. [F/L2]
        LossSteelRelax(float)-The tendon stress loss due to tendon steel relaxation. [F/L2]
        Replace(bool)-If this item is True, all previous force/stress loads, if any, assigned to the specified
            tendon object(s), in the specified load case, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.TendonObj.SetLoadForceStress(name,loadPat,JackFrom,LoadType,Value,CurvatureCoeff,WobbleCoeff,
                                            LossAnchorage,LossShortening,LossCreep,LossShrinkage,LossSteelRelax,
                                            Replace,itemType)

    def assign_TendonObj_SetLoadGravity(self,name,loadPat,x,y,z,Replace=True,CSys="Global",itemType=0):
        """
        ---This function assigns gravity load multipliers to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        x,y,z(float)-These are the gravity load multipliers in the x, y and z directions of the specified coordinate system.
        Replace(bool)-If this item is True, all previous gravity loads, if any, assigned to the specified tendon
            object(s), in the specified load pattern, are deleted before making the new assignment.
        CSys(str)-The coordinate system in which the x, y and z multipliers are specified.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.TendonObj.SetLoadGravity(name,loadPat,x,y,z,Replace,CSys,itemType)

    def assign_TendonObj_SetLoadStrain(self,name,LoadPat,Strain,Replace=True,PatternName="",itemType=0):
        """
        ---This function assigns strain loads to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        LoadPat(str)-The name of a defined load pattern.
        Strain(float)-This is the axial strain load value. [L/L]
        Replace(bool)-If this item is True, all previous strain loads, if any, assigned to the specified tendon
            object(s), in the specified load pattern, are deleted before making the new assignment.
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the strain load for the
            tendon object is uniform along the object at the value specified by Strain.If PatternName is the name of
            a defined joint pattern, the strain load for the tendon object is based on the specified strain value
            multiplied by the pattern value at the joints at each end of the tendon object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.TendonObj.SetLoadStrain(name,LoadPat,Strain,Replace,PatternName,itemType)

    def assign_TendonObj_SetLoadTemperature(self,name,LoadPat,Val,PatternName="",Replace=True,itemType=0):
        """
        ---This function assigns temperature loads to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group depending on the value of the ItemType item.
        LoadPat(str)-The name of a defined load pattern.
        Val(float)-This is the temperature change value. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the temperature load
            for the tendon object is uniform along the object at the value specified by Val.If PatternName is the
            name of a defined joint pattern, the temperature load for the tendon object is based on the specified
            temperature value multiplied by the pattern value at the joints at each end of the tendon object.
        Replace(bool)-If this item is True, all previous temperature loads, if any, assigned to the specified tendon
            object(s), in the specified load case, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.TendonObj.SetLoadTemperature(name,LoadPat,Val,PatternName,Replace,itemType)

    def assign_TendonObj_SetLocalAxes(self,name,Ang,itemType=0):
        """
        ---This function assigns a local axis angle to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        Ang(float)-This is the angle that the local 2 and 3 axes are rotated about the positive local 1 axis,
            from the default orientation. The rotation for a positive angle appears counter clockwise when the
            local +1 axis is pointing toward you. [deg]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.TendonObj.SetLocalAxes(name,Ang,itemType)

    def assign_TendonObj_SetMatTemp(self,name,Temp,PatternName="",itemType=0):
        """
        ---This function assigns material temperatures to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        Temp(float)-This is the material temperature value assigned to the tendon object. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the material temperature
            for the tendon object is uniform along the object at the value specified by Temp.If PatternName is the name
            of a defined joint pattern, the material temperature for the tendon object may vary from one end to the
            other. The material temperature at each end of the object is equal to the specified temperature multiplied
            by the pattern value at the joint at the end of the tendon object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.TendonObj.SetMatTemp(name,Temp,PatternName,itemType)

    def assign_TendonObj_SetProperty(self,name,PropName,itemType=0):
        """
        ---This function assigns a tendon property to a tendon object---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        PropName(str)-This is None or the name of a tendon property to be assigned to the specified tendon object(s).
            None means that no property is assigned to the tendon.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.TendonObj.SetProperty(name,PropName,itemType)

    def assign_TendonObj_SetTCLimits(self,name,LimitCompressionExists,LimitCompression,
                                     LimitTensionExists,LimitTension,itemType=0):
        """
        ---This function makes tension/compression force limit assignments to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        LimitCompressionExists(bool)-This item is True if a compression force limit exists for the tendon object.
        LimitCompression(float)-The compression force limit for the tendon object. [F]
        LimitTensionExists(bool)-This item is True if a tension force limit exists for the tendon object.
        LimitTension(float)-The tension force limit for the tendon object. [F]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.TendonObj.SetTCLimits(name,LimitCompressionExists,LimitCompression,
                                     LimitTensionExists,LimitTension,itemType)

    def assign_TendonObj_SetTendonData(self,name,NumberPoints,MyType,x,y,z,CSys="Global"):
        """
        ---This function assigns the tendon geometric definition parameters to a tendon object---
        inputs:
        name(str)-The name of a defined tendon object.
        NumberPoints(int)-The number of items used to define the tendon geometry.
        MyType(int)-This is an array of values that are 1, 3, 6, 7, 8, or 9, indicating the tendon geometry definition
            parameter for the specified point.
            1 = Start of tendon
            2 = The segment preceding the point is linear
            6 = The specified point is the end of a parabola
            7 = The specified point is an intermediate point on a parabola
            8 = The specified point is the end of a circle
            9 = The specified point is an intermediate point on a parabola
            The first point should always have a MyType value of 1. If it is not equal to 1, the program uses 1 anyway.
            MyType of 6 through 9 is based on using three points to calculate a parabolic or circular arc. MyType 6 and
            8 use the specified point and the two previous points as the three points. MyType 7 and 9 use the specified
            point and the points just before and after the specified point as the three points.
        x(float list)-This is an array of the X (or local 1) coordinate of each point in the coordinate system
            specified by CSys. [L]
        y(float list)-This is an array of the Y (or local 2) coordinate of each point in the coordinate system
            specified by CSys. [L]
        z(float list)-This is an array of the Z (or local 3) coordinate of each point in the coordinate system
            specified by CSys. [L]
        CSys(bool)-This is the coordinate system in which the x, y and z coordinate parameters are defined.
            It is Local or the name of a defined coordinate system.Local means that the point coordinates
            are in the local system of the specified tendon object with the origin assumed to be at the I-End of the tendon.
        """
        self.SapModel.TendonObj.SetTendonData(name,NumberPoints,MyType,x,y,z,CSys)

    def assign_TendonObj_GetDiscretization(self,name):
        """
        ---This function retrieves the maximum discretization length assignment for tendon objects---
        inputs:
        name(str)-The name of an existing tendon object
        return:
        [index,Value]
        Value(float)-The maximum discretization length for the tendon. [L]
        """
        result=self.SapModel.TendonObj.GetDiscretization(name)
        return result

    def assign_TendonObj_GetGroupAssign(self,name):
        """
        ---This function retrieves the names of the groups to which a specified tendon object is assigned---
        inputs:
        name(str)-The name of an existing tendon object
        return:
        [index,numberGroups,Groups]
        numberGroups(int)-The number of group names retrieved.
        Groups(str)-The names of the groups to which the tendon object is assigned
        """
        result=self.SapModel.TendonObj.GetGroupAssign(name)
        return result

    def assign_TendonObj_GetLoadDeformation(self,name):
        """
        ---This function retrieves the deformation load assignments to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        return:
        [index,NumberItems,TendonName,LoadPat,U1]
        NumberItems(int)-The total number of deformation loads retrieved for the specified tendon objects.
        TendonName(str list)-This is an array that includes the name of the tendon object associated with each deformation load.
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each deformation load
        U1(float list)-This is an array of axial deformation load values. [L]
        """
        result=self.SapModel.TendonObj.GetLoadDeformation(name)
        return result

    def assign_TendonObj_GetLoadedGroup(self,name):
        """
        ---This function retrieves the loaded group for tendon objects. A tendon object transfers its load to any
        object that is in the specified group.
        ---
        inputs:
        name(str)-The name of an existing tendon object
        return:
        [index,GroupName]
        GroupName(str)-This is the name of an existing group. All objects in the specified group can be loaded by the tendon.
        """
        result=self.SapModel.TendonObj.GetLoadedGroup(name)
        return result

    def assign_TendonObj_GetLoadForceStress(self,name):
        """
        ---This function retrieves the force/stress load assignments to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        return:
        [index,NumberItems,TendonName,LoadPat,JackFrom,LoadType,Value,CurvatureCoeff,WobbleCoeff,LossAnchorage,
        LossShortening,LossCreep,LossShrinkage,LossSteelRelax]
        NumberItems(int)-The total number of temperature loads retrieved for the specified tendon objects
        TendonName(str list)-This is an array that includes the name of the tendon object associated with each temperature load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each temperature load
        JackFrom(int list)-This is an array that includes 1, 2 or 3, indicating how the tendon is jacked.
            1 = Tendon jacked from I-End
            2 = Tendon jacked from J-End
            3 = Tendon jacked from both ends
        LoadType(int list)-This is an array that includes either 0 or 1, indicating how the type of load.
            0 = Force,1 = Stress
        Value(float list)-This is an array that includes the load value. [F] when LoadType is 0, and [F/L2] when Loadtype is 1
        CurvatureCoeff(float list)-This is an array that includes the curvature coefficient used when calculating friction losses.
        WobbleCoeff(float list)-This is an array that includes the wobble coefficient used when calculating friction losses. [1/L]
        LossAnchorage(float list)-This is an array that includes the anchorage set slip. [L]
        LossShortening(float list)-This is an array that includes the tendon stress loss due to elastic shortening. [F/L2]
        LossCreep(float list)-This is an array that includes the tendon stress loss due to creep. [F/L2]
        LossShrinkage(float list)-This is an array that includes the tendon stress loss due to shrinkage. [F/L2]
        LossSteelRelax(float list)-This is an array that includes the tendon stress loss due to tendon steel relaxation. [F/L2]
        """
        result=self.SapModel.TendonObj.GetLoadForceStress(name)
        return result

    def assign_TendonObj_GetLoadGravity(self,name):
        """
        ---This function retrieves the gravity load assignments to tendon objects.---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        return:
        [index,NumberItems,TendonName,LoadPat,CSys,x,y,z]
        NumberItems(int)-The total number of gravity loads retrieved for the specified tendon objects.
        TendonName(str list)-This is an array that includes the name of the tendon object associated with each gravity load
        LoadPat(str list)-This is an array that includes the name of the coordinate system in which the gravity load
            multipliers are specified.
        CSys(str list)-This is an array that includes the name of the coordinate system associated with each gravity load
        x,y,z(float list)-These are arrays of gravity load multipliers in the x, y and z directions of the specified
            coordinate system.
        """
        result=self.SapModel.TendonObj.GetLoadGravity(name)
        return result

    def assign_TendonObj_GetLoadStrain(self,name):
        """
        ---This function retrieves the strain load assignments to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        return:
        [index,NumberItems,TendonName,LoadPat,Strain,PatternName]
        NumberItems(int)-The total number of strain loads retrieved for the specified tendon objects.
        TendonName(str list)-This is an array that includes the name of the tendon object associated with each strain load.
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each strain load.
        Strain(float)-This is an array that includes the axial strain value. [L/L]
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the strain load.
        """
        result=self.SapModel.TendonObj.GetLoadStrain(name)
        return result

    def assign_TendonObj_GetLoadTemperature(self,name):
        """
        ---This function retrieves the temperature load assignments to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        return:
        [index,NumberItems,TendonName,LoadPat,Val,PatternName]
        NumberItems(int)-The total number of temperature loads retrieved for the specified tendon objects.
        TendonName(str list)-This is an array that includes the name of the tendon object associated with each
            temperature load.
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each temperature load.
        Val(float list)-This is an array that includes the temperature load value. [T]
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the temperature load
        """
        result=self.SapModel.TendonObj.GetLoadTemperature(name)
        return result

    def assign_TendonObj_GetLocalAxes(self,name):
        """
        ---This function retrieves the tendon local axis angle assignment for tendon objects---
        inputs:
        name(str)-The name of an existing tendon object.
        return:
        [index,Ang]
        Ang(float)-This is the angle that the local 2 and 3 axes are rotated about the positive local 1 axis, from
            the default orientation. The rotation for a positive angle appears counter clockwise when the local +1
            axis is pointing toward you. [deg]
        """
        result=self.SapModel.TendonObj.GetLocalAxes(name)
        return result

    def assign_TendonObj_GetMatTemp(self,name):
        """
        ---This function retrieves the material temperature assignments to tendon objects---
        inputs:
        [index,Temp,PatternName]
        Temp(float)-This is the material temperature value assigned to the tendon object. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the material temperature
            for the tendon object is uniform along the object at the value specified by Temp.If PatternName is the name
            of a defined joint pattern, the material temperature for the tendon object may vary from one end to the other.
            The material temperature at each end of the object is equal to the specified temperature multiplied by the
            pattern value at the joint at the end of the tendon object.
        """
        result=self.SapModel.TendonObj.GetMatTemp(name)
        return result

    def assign_TendonObj_GetNameList(self):
        """
        ---This function retrieves the names of all defined tendon objects---
        return:
        [index,NumberNames,MyName]
        NumberNames(int)-The number of tendon object names retrieved by the program.
        MyName(str list)-This is a one-dimensional array of tendon object names.
        """
        result=self.SapModel.TendonObj.GetNameList()
        return result

    def assign_TendonObj_GetPoints(self,name):
        """
        ---This function retrieves the names of the point objects at each end of a specified tendon object---
        inputs:
        name(str)-The name of a defined tendon object
        return:
        [index,Point1,Point2]
        Point1(str)-The name of the point object at the I-End of the specified tendon object.
        Point2(str)-The name of the point object at the J-End of the specified tendon object.
        """
        result=self.SapModel.TendonObj.GetPoints(name)
        return result

    def assign_TendonObj_GetProperty(self,name):
        """
        ---This function retrieves the tendon property assigned to a tendon object---
        inputs:
        name(str)-The name of a defined tendon object.
        return:
        [index,PropName]
        PropName(str)-The name of the tendon property assigned to the tendon object
        """
        result=self.SapModel.TendonObj.GetProperty(name)
        return result

    def assign_TendonObj_GetTCLimits(self,name):
        """
        ---This function retrieves the tension/compression force limit assignments to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object
        return:
        [index,LimitCompressionExists,LimitCompression,LimitTensionExists,LimitTension]
        LimitCompressionExists(bool)-This item is True if a compression force limit exists for the tendon object
        LimitCompression(float)-The compression force limit for the tendon object. [F]
        LimitTensionExists(bool)-This item is True if a tension force limit exists for the tendon object.
        LimitTension(float)-The tension force limit for the tendon object. [F]
        """
        result=self.SapModel.TendonObj.GetTCLimits(name)
        return result

    def assign_TendonObj_GetTendonData(self,name):
        """
        ---This function retrieves the tendon geometric definition parameters for a tendon object---
        inputs:
        name(str)-The name of a defined tendon object
        return:
        [index,NumberItems,MyType,x,y,z]
        NumberItems(int)-The number of items used to define the tendon geometry
        MyType(int list)-This is an array of values that are 1, 3, 6, 7, 8, or 9, indicating the tendon geometry
            definition parameter for the specified point.
            1 = Start of tendon
            2 = The segment preceding the point is linear
            6 = The specified point is the end of a parabola
            7 = The specified point is an intermediate point on a parabola
            8 = The specified point is the end of a circle
            9 = The specified point is an intermediate point on a parabola
            The first point always has a MyType value of 1.MyType of 6 through 9 is based on using three points to
                calculate a parabolic or circular arc. MyType 6 and 8 use the specified point and the two previous
                points as the three points. MyType 7 and 9 use the specified point and the points just before and
                after the specified point as the three points.
        x(float list)-This is an array of the X (or local 1) coordinate of each point in the coordinate system
            specified by CSys. [L]
        y(float list)-This is an array of the Y (or local 2) coordinate of each point in the coordinate system
            specified by CSys. [L]
        z(float list)-This is an array of the Z (or local 3) coordinate of each point in the coordinate system
            specified by CSys. [L]
        """
        result=self.SapModel.TendonObj.GetTendonData(name)
        return result

    def assign_TendonObj_GetTendonGeometry(self,name):
        """
        ---The name of a defined tendon object.---
        inputs:
        name(str)-The name of a defined tendon object.
        return:
        [index,NumberPoints,x,y,z]
        NumberPoints(int)-The number of items used to define the discretized tendon geometry.
        x(float list)-This is an array of the X (or local 1) coordinate of each point in the coordinate system
            specified by CSys. [L]
        y(float list)-This is an array of the Y (or local 2) coordinate of each point in the coordinate system
            specified by CSys. [L]
        z(float list)-This is an array of the Z (or local 3) coordinate of each point in the coordinate system
            specified by CSys. [L]
        """
        result=self.SapModel.TendonObj.GetTendonGeometry(name)
        return result

    def assign_TendonObj_GetTransformationMatrix(self,name):
        """
        ---The function returns zero if the tendon object transformation matrix is successfully retrieved;
        otherwise it returns a nonzero value.
        ---
        inputs:
        name(str)-The name of an existing tendon object.
        return:
        [index,Value]
        Value(float list)-Value is an array of nine direction cosines that define the transformation matrix.The following
            matrix equation shows how the transformation matrix is used to convert items from the tendon object local
            coordinate system to the global coordinate system.In the equation, c0 through c8 are the nine values from
            the transformation array, (Local1, Local2, Local3) are an item (such as a load) in the object local coordinate
            system, and (GlobalX, GlobalY, GlobalZ) are the same item in the global coordinate system.The transformation
            from the local coordinate system to the present coordinate system is the same as that shown above for the global
            system if you substitute the present system for the global system.
        """
        result=self.SapModel.TendonObj.GetTransformationMatrix(name)
        return result

    def assign_AreaObj_AddByCoord(self,NumberPoints,x,y,z,PropName="Default",UserName="",CSys="Global"):
        """
        ---This function adds a new area object, defining points at the specified coordinates---
        inputs:
        NumberPoints(int)-The number of points in the area abject.
        x,y,z(float list)-These are arrays of x, y and z coordinates, respectively, for the corner points of the
            area object. The coordinates are in the coordinate system defined by the CSys item. The coordinates
            should be ordered to run clockwise or counter clockwise around the area object.
        PropName(str)-This is Default, None or the name of a defined area property.If it is Default, the program
            assigns a default area property to the area object. If it is None, no area property is assigned to the
            area object. If it is the name of a defined area property, that property is assigned to the area object.
        UserName(str)-This is an optional user specified name for the area object. If a UserName is specified and
            that name is already used for another area object, the program ignores the UserName.
        CSys(str)-The name of the coordinate system in which the area object point coordinates are defined.
        """
        # This is the name that the program ultimately assigns to the area object. If no UserName is specified,
        # the program assigns a default name to the area object. If a UserName is specified and that name is not
        # used for another area object, the UserName is assigned to the area object; otherwise a default name is
        # assigned to the area object.
        name = ""
        self.SapModel.AreaObj.AddByCoord(NumberPoints,x,y,z,name,PropName,UserName,CSys)

    def assign_AreaObj_AddByPoint(self,NumberPoints,Point,PropName="Default",UserName=""):
        """
        ---This function adds a new area object whose defining points are specified by name---
        inputs:
        NumberPoints(int)-The number of points in the area abject.
        Point(str list)-This is an array containing the names of the point objects that define the added area object.
            The point object names should be ordered to run clockwise or counter clockwise around the area object.
        PropName(str)-This is Default, None or the name of a defined area property.If it is Default, the program
            assigns a default area property to the area object. If it is None, no area property is assigned to the
            area object. If it is the name of a defined area property, that property is assigned to the area object.
        UserName(str)-This is an optional user specified name for the area object. If a UserName is specified and
            that name is already used for another area object, the program ignores the UserName.
        """
        # This is the name that the program ultimately assigns to the area object. If no UserName is specified,
        # the program assigns a default name to the area object. If a UserName is specified and that name is not
        # used for another area object, the UserName is assigned to the area object; otherwise a default name is
        # assigned to the area object.
        name = ""
        self.SapModel.AreaObj.AddByPoint(NumberPoints,Point,name,PropName,UserName)

    def assign_AreaObj_ChangeName(self,name,NewName):
        """
        ---This function applies a new name to an area object---
        inputs:
        name(str)-The existing name of a defined area object.
        NewName(str)-The new name for the area object.
        """
        self.SapModel.AreaObj.ChangeName(name,NewName)

    def assign_AreaObj_Count(self):
        """
        ---This function returns a count of the area objects in the model---
        """
        result=self.SapModel.AreaObj.Count()
        return result

    def assign_AreaObj_SetAutoMesh(self,name,MeshType,n1=2,n2=2,MaxSize1=0,MaxSize2=0,PointOnEdgeFromLine=False,
                                   PointOnEdgeFromPoint=False,ExtendCookieCutLines=False,
                                   Rotation=0,MaxSizeGeneral=0,LocalAxesOnEdge=False,LocalAxesOnFace=False,
                                   ResTraintsOnEdge=False,RestraintsOnFace=False,Group="ALL",SubMesh=False,SubMeshSize=0,
                                   itemType=0):
        """
        ---This function makes automatic meshing assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item.
        MeshType(int)-This item is 0, 1, 2, 3, 4, 5 or 6, indicating the automatic mesh type for the area object.
            0 = No automatic meshing
            1 = Mesh area into a specified number of objects
            2 = Mesh area into objects of a specified maximum size
            3 = Mesh area based on points on area edges
            4 = Cookie cut mesh area based on lines intersecting edges
            5 = Cookie cut mesh area based on points
            6 = Mesh area using General Divide Tool
            Mesh options 1, 2 and 3 apply to quadrilaterals and triangles only.
        n1(int)-This item applies when MeshType = 1. It is the number of objects created along the edge of the
            meshed area object that runs from point 1 to point 2.
        n2(int)-This item applies when MeshType = 1. It is the number of objects created along the edge of the
            meshed area object that runs from point 1 to point 3.
        MaxSize1(float)-This item applies when MeshType = 2. It is the maximum size of objects created along the
            edge of the meshed area object that runs from point 1 to point 2. [L]If this item is input as 0, the
            default value is used. The default value is 48 inches if the database units are English or 120 centimeters
            if the database units are metric.
        MaxSize2(float)-This item applies when MeshType = 2. It is the maximum size of objects created along the edge
            of the meshed area object that runs from point 1 to point 3. [L]If this item is input as 0, the default
            value is used. The default value is 48 inches if the database units are English or 120 centimeters if the
            database units are metric.
        PointOnEdgeFromLine(bool)-This item applies when MeshType = 3. If it is True, points on the area object edges
            are determined from intersections of straight line objects included in the group specified by the Group
            item with the area object edges.
        PointOnEdgeFromPoint(bool)-This item applies when MeshType = 3. If it is True, points on the area object edges
            are determined from point objects included in the group specified by the Group item that lie on the area object edges
        ExtendCookieCutLines(bool)-This item applies when MeshType = 4. MeshType = 4 provides cookie cut meshing based
            on straight line objects included in the group specified by the Group item that intersect the area object
            edges. If the ExtendCookieCutLines item is True, all straight line objects included in the group specified
            by the Group item are extended to intersect the area object edges for the purpose of meshing the area object.
        Rotation(float)-This item applies when MeshType = 5. MeshType = 5 provides cookie cut meshing based on two
            perpendicular lines passing through point objects included in the group specified by the Group item.
            By default these lines align with the area object local 1 and 2 axes. The Rotation item is an angle in
            degrees that the meshing lines are rotated from their default orientation. [deg]
        MaxSizeGeneral(float)-This item applies when MeshType = 6. It is the maximum size of objects created by the
            General Divide Tool.If this item is input as 0, the default value is used. The default value is 48 inches
            if the database units are English or 120 centimeters if the database units are metric.
        LocalAxesOnEdge(bool)-If this item is True, and if both points along an edge of the original area object
            have the same local axes, then the program makes the local axes for added points along the edge the
            same as the edge end points.
        LoalAxesOnFace(bool)-If this item is True, and if all points around the perimeter of the original area object
            have the same local axes, the program makes the local axes for all added points the same as the perimeter points.
        RestraintsOnEdge(bool)-If this item is True, and if both points along an edge of the original area object have
            the same restraint/constraint, then, if the added point and the adjacent corner points have the same local
            axes definition, the program includes the restraint/constraint for added points along the edge.
        RestraintsOnFace(bool)-If this item is True, and if all points around the perimeter of the original area object
            have the same restraint/constraint, then, if an added point and the perimeter points have the same local
            axes definition, the program includes the restraint/constraint for the added point.
        Group(str)-The name of a defined group. Some of the meshing options make use of point and line objects
            included in this group.
        SubMesh(bool)-If this item is True, after initial meshing, the program further meshes any area objects that
            have an edge longer than the length specified by the SubMeshSize item.
        SubMeshSize(bool)-This item applies when the SubMesh item is True. It is the maximum size of area objects to
            remain when the auto meshing is complete. [L]If this item is input as 0, the default value is used.
            The default value is 12 inches if the database units are English or 30 centimeters if the database units are metric.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.AreaObj.SetAutoMesh(name,MeshType,n1,n2,MaxSize1,MaxSize2,PointOnEdgeFromLine,
                                   PointOnEdgeFromPoint,ExtendCookieCutLines,Rotation,MaxSizeGeneral,LocalAxesOnEdge,
                                    LocalAxesOnFace,ResTraintsOnEdge,RestraintsOnFace,Group,SubMesh,SubMeshSize,itemType)

    def assign_AreaObj_SetEdgeConstraint(self,name,ConstraintExists,itemType=0):
        """
        ---This function makes generated edge constraint assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        ConstraintExists(bool)-This item is True if an automatic edge constraint is generated by the program
            for the area object in the analysis model.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.AreaObj.SetEdgeConstraint(name,ConstraintExists,itemType)

    def assign_AreaObj_SetGroupAssign(self,name,GroupName,Remove=False,itemType=0):
        """
        ---This function adds or removes area objects from a specified group---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item.
        GroupName(str)-The name of an existing group to which the assignment is made.
        Remove(bool)-If this item is False, the specified area objects are added to the group specified by the
            GroupName item. If it is True, the area objects are removed from the group.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.AreaObj.SetGroupAssign(name,GroupName,Remove,itemType)

    def assign_AreaObj_SetLoadGravity(self,name,LoadPat,x,y,z,Replace=True,CSys="Global",itemType=0):
        """
        ---This function assigns gravity load multipliers to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item.
        LoadPat(str)-The name of a defined load pattern
        x,y,z(float)-These are the gravity load multipliers in the x, y and z directions of the specified coordinate system
        Replace(bool)-If this item is True, all previous gravity loads, if any, assigned to the specified area object(s),
            in the specified load pattern, are deleted before making the new assignment
        CSys(str)-The coordinate system in which the x, y and z multipliers are specified
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.AreaObj.SetLoadGravity(name,LoadPat,x,y,z,Replace,CSys,itemType)

    def assign_AreaObj_SetLoadPorePressure(self,name,LoadPat,Value,PatternName="",Replace=True,itemType=0):
        """
        ---This function assigns pore pressure loads to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        LoadPat(str(str)-The name of a defined load pattern
        Value(float)-This is the pore pressure value. [F/L2]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the pore pressure
            load for the area object is uniform over the object at the value specified by Value.If PatternName is
            the name of a defined joint pattern, the pore pressure load for the area object is based on the specified
            pore pressure value multiplied by the pattern value at the point objects that define the area object.
        Replace(bool)-If this item is True, all previous pore pressure loads, if any, assigned to the specified area
            object(s), in the specified load case, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.AreaObj.SetLoadPorePressure(name,LoadPat,Value,PatternName,Replace,itemType)

    def assign_AreaObj_SetLoadRotate(self,name,loadPat,Value,itemType=0):
        """
        ---This function assigns rotate loads to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        loadPat(str)-The name of a defined load pattern
        Value(float)-This is the angular velocity. [Cyc/T]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.AreaObj.SetLoadRotate(name,loadPat,Value,itemType)

    def assign_AreaObj_SetLoadStrain(self,name,LoadPat,component,Value,Replace=True,PatternName="",itemType=0):
        """
        ---This function assigns strain loads to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        component(int)-This is 1, 2, 3, 4, 5, 6, 7, 8, or 9, indicating the component to which the strain load is applied.
            1 = Strain11,2 = Strain22,3 = Strain12,4 = Curvature11,5 = Curvature22,6 = Curvature12,7 = Strain13
            8 = Strain23,9 = Strain33
        Value(float)-This is the strain load value. [L/L] for Component = 1, 2, 3, 7, 8, and 9 and [1/L] for Component = 4, 5 and 6
        Replace(bool)-If this item is True, all previous strain loads, if any, assigned to the specified area object(s),
            in the specified load pattern, for the specified degree of freedom, are deleted before making the new assignment
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the strain load for the
            area object is uniform over the object at the value specified by Value.If PatternName is the name of a
            defined joint pattern, the strain load for the area object is based on the specified strain value
            multiplied by the pattern value at the corner points of the area object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.AreaObj.SetLoadStrain(name,LoadPat,component,Value,Replace,PatternName,itemType)

    def assign_AreaObj_SetLoadSurfacePressure(self,name,LoadPat,Face,Value,PatternName="",Replace=True,itemType=0):
        """
        ---This function assigns surface pressure loads to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        Face(int)-This is -1, -2 or a nonzero, positive integer, indicating the area object face to which the
            specified load assignment applies.
            -1 = Bottom face,-2 = Top face,>0 = Edge face
            Note that edge face n is from area object point n to area object point n + 1. For example, edge face
            2 is from area object point 2 to area object point 3.
        Value(float)-This is the surface pressure value. [F/L2]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the surface pressure
            load for the area object face is uniform over the face at the value specified by Value.If PatternName
            is the name of a defined joint pattern, the surface pressure load for the area object face is based on
            the specified surface pressure value multiplied by the pattern value at the point objects that are part of the face.
        Replace(bool)-If this item is True, all previous surface pressure loads, if any, assigned to the specified
            area object(s), in the specified load case, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.AreaObj.SetLoadSurfacePressure(name,LoadPat,Face,Value,PatternName,Replace,itemType)

    def assign_AreaObj_SetLoadTemperature(self,name,LoadPat,MyType,Value,PatternName="",Replace=True,itemType=0):
        """
        ---This function assigns temperature loads to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        MyType(int)-This is either 1 or 3, indicating the type of temperature load.
            1 = Temperature,3 = Temperature gradient along local 3 axis
        Value(float)-This is the temperature change value. [T] for MyType = 1 and [T/L] for MyType = 3
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the temperature
            load for the area object is uniform over the object at the value specified by Value.If PatternName
            is the name of a defined joint pattern the temperature load for the area object is based on the
            specified temperature value multiplied by the pattern value at the joints that define the area object.
        Replace(bool)-If this item is True, all previous temperature loads, if any, assigned to the specified area
            object(s), in the specified load case, are deleted before making the new assignment
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.AreaObj.SetLoadTemperature(name,LoadPat,MyType,Value,PatternName,Replace,itemType)

    def assign_AreaObj_SetLoadUniform(self,name,LoadPat,Value,Dir,Replace=True,CSys="Global",itemType=0):
        """
        ---This function assigns uniform loads to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        Value(float)-The uniform load value. [F/L2]
        Dir(int)-This is an integer between 1 and 11, indicating the direction of the load.
            1 = Local 1 axis (only applies when CSys is Local)
            2 = Local 2 axis (only applies when CSys is Local)
            3 = Local 3 axis (only applies when CSys is Local)
            4 = X direction (does not apply when CSys is Local)
            5 = Y direction (does not apply when CSys is Local)
            6 = Z direction (does not apply when CSys is Local)
            7 = Projected X direction (does not apply when CSys is Local)
            8 = Projected Y direction (does not apply when CSys is Local)
            9 = Projected Z direction (does not apply when CSys is Local)
            10 = Gravity direction (only applies when CSys is Global)
            11 = Projected Gravity direction (only applies when CSys is Global)
            The positive gravity direction (see Dir = 10 and 11) is in the negative Global Z direction.
        Replace(bool)-If this item is True, all previous uniform loads, if any, assigned to the specified area
            object(s), in the specified load pattern, are deleted before making the new assignment
        CSys(str)-This is Local or the name of a defined coordinate system, indicating the coordinate system
            in which the uniform load is specified
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.AreaObj.SetLoadUniform(name,LoadPat,Value,Dir,Replace,CSys,itemType)

    def assign_AreaObj_SetLoadUniformToFrame(self,name,LoadPat,Value,Dir,DistType,Replace=True,CSys="Global",itemType=0):
        """
        ---This function assigns uniform to frame loads to area objects---
        name(str)-The name of an existing area object or group depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        Value(float)-The uniform load value. [F/L2]
        Dir(int)-This is an integer between 1 and 11, indicating the direction of the load.
            1 = Local 1 axis (only applies when CSys is Local)
            2 = Local 2 axis (only applies when CSys is Local)
            3 = Local 3 axis (only applies when CSys is Local)
            4 = X direction (does not apply when CSys is Local)
            5 = Y direction (does not apply when CSys is Local)
            6 = Z direction (does not apply when CSys is Local)
            7 = Projected X direction (does not apply when CSys is Local)
            8 = Projected Y direction (does not apply when CSys is Local)
            9 = Projected Z direction (does not apply when CSys is Local)
            10 = Gravity direction (only applies when CSys is Global)
            11 = Projected Gravity direction (only applies when CSys is Global)
            The positive gravity direction (see Dir = 10 and 11) is in the negative Global Z direction.
        DistType(int)-This is either 1 or 2, indicating the load distribution type.
            1 = One-way load distribution
            2 = Two-way load distribution
            One-way distribution is parallel to the area object local 1 axis. Two-way distribution is parallel to
                the area object local 1 and 2 axes.
        Replace(bool)-If this item is True, all previous uniform loads, if any, assigned to the specified area
            object(s), in the specified load pattern, are deleted before making the new assignment
        CSys(str)-This is Local or the name of a defined coordinate system, indicating the coordinate system in
            which the uniform load is specified
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.AreaObj.SetLoadUniformToFrame(name,LoadPat,Value,Dir,DistType,Replace,CSys,itemType)

    def assign_AreaObj_SetLoadWindPressure_1(self,name,LoadPat,MyType,Cp,DistributionType,itemType=0):
        """
        ---This function assigns wind pressure loads to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item.
        LoadPat(str)-The name of a defined load pattern
        MyType(int)-This is either 1 or 2, indicating the wind pressure type.
            1 = Windward, pressure varies over height
            2 = Other, pressure is constant over height
        Cp(float)-This is the wind pressure coefficient
        DistributionType(int)-This is either 1 or 2, indicating the distribution type.
            1 = To Joints,2 = To Frames – One-way,3 = To Frames – Two-way
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.AreaObj.SetLoadWindPressure_1(name,LoadPat,MyType,Cp,DistributionType,itemType)

    def assign_AreaObj_SetLocalAxes(self,name,Ang,itemType=0):
        """
        ---This function assigns a local axis angle to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        Ang(float)-This is the angle that the local 1 and 2 axes are rotated about the positive local 3 axis
            from the default orientation. The rotation for a positive angle appears counter clockwise when
            the local +3 axis is pointing toward you. [deg]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.AreaObj.SetLocalAxes(name,Ang,itemType)

    def assign_AreaObj_SetMass(self,name,MassOverL,Replace=False,itemType=0):
        """
        ---This function assigns mass per unit area to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        MassOverL(float)-The mass per unit area assigned to the area object. [M/L2]
        Replace(bool)-If this item is True, all existing mass assignments to the area object are removed before
            assigning the specified mas. If it is False, the specified mass is added to any existing mass already
            assigned to the area object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.AreaObj.SetMass(name,MassOverL,Replace,itemType)

    def assign_AreaObj_SetMatTemp(self,name,Temp,PatternName="",itemType=0):
        """
        ---This function assigns material temperatures to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        Temp(float)-This is the material temperature value assigned to the area object. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the material temperature
            for the area object is uniform over the object at the value specified by Temp.If PatternName is the name
            of a defined joint pattern, the material temperature for the area object may vary. The material temperature
            at each corner point around the area object perimeter is equal to the specified temperature multiplied by
            the pattern value at the associated point object. The material temperature at other points in the area
            object is calculated by interpolation from the corner points.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.AreaObj.SetMatTemp(name,Temp,PatternName,itemType)

    def assign_AreaObj_SetModifiers(self,name,Value,itemType=0):
        """
        ---This function sets the modifier assignment for area objects. The default value for all modifiers is one---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        Value(float)-This is an array of ten unitless modifiers.
            Value(0) = Membrane f11 modifier
            Value(1) = Membrane f22 modifier
            Value(2) = Membrane f12 modifier
            Value(3) = Bending m11 modifier
            Value(4) = Bending m22 modifier
            Value(5) = Bending m12 modifier
            Value(6) = Shear v13 modifier
            Value(7) = Shear v23 modifier
            Value(8) = Mass modifier
            Value(9) = Weight modifier
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.AreaObj.SetModifiers(name,Value,itemType)

    def assign_AreaObj_SetNotionalSize(self,name,style,Value):
        """
        ---This function assigns the method to determine the notional size of an area section for the creep and
        shrinkage calculations. This function is currently worked for shell type area section
        ---
        inputs:
        name(str)-The name of an existing shell-type area section property
        style(str)-The type to define the notional size of a section. It can be:
            "Auto" = Program will determine the notional size based on the average thickness of an area element.
            "User" = The notional size is based on the user-defined value.
            "None" = Notional size will not be considered. In other words, the time-dependent effect of this
            section will not be considered.
        Value(float)-For stype is "Auto", the Value represents for the scale factor to the program-determined notional
            size; for stype is “User”, the Value represents for the user-defined notional size [L]; for stype is “None”,
            the Value will not be used and can be set to 1.
        """
        self.SapModel.PropArea.SetNotionalSize(name,style,Value)

    def assign_AreaObj_SetOffsets(self,name,OffsetType,OffsetPattern,OffsetPatternSF,Offset,itemType=0):
        """
        ---This function sets the joint offset assignments for area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        OffsetType(int)-This is 0, 1 or 2, indicating the joint offset type.
            0 = No joint offsets
            1 = User defined joint offsets specified by joint pattern
            2 = User defined joint offsets specified by point
        OffsetPattern(str)-This item applies only when OffsetType = 1. It is the name of the defined
            joint pattern that is used to calculate the joint offsets
        OffesetPatternSF(float)-This item applies only when OffsetType = 1. It is the scale factor applied to
            the joint pattern when calculating the joint offsets. [L]
        Offset(float)-This item applies only when OffsetType = 2. It is an array of joint offsets for each of
            the points that define the area object. [L]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.AreaObj.SetOffsets(name,OffsetType,OffsetPattern,OffsetPatternSF,Offset,itemType)

    def assign_AreaObj_SetProperty(self,name,PropName,itemType=0):
        """
        ---This function assigns an area property to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        PropName(str)-This is None or the name of a area property to be assigned to the specified area object(s).
            None means that no property is assigned to the area object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.AreaObj.SetProperty(name,PropName,itemType)

    def assign_AreaObj_SetSpring(self,name,myType,s,simpleSpringType,LinkProp,Face,SpringLocalOneType,Dir,
                                 OutWard,Vec,Ang,Replace,CSys="Local",itemType=0):
        """
        ---This function makes spring assignments to area objects. The springs are assigned to a specified area object face---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        MyType(int)-This is either 1 or 2, indicating the spring property type.
            1 = Simple spring,2 = Link property
        s(float)-The simple spring stiffness per unit area of the specified area object face. This item applies
            only when MyType = 1. [F/L3]
        SimpleSpringType(int)-This is 1, 2 or 3, indicating the simple spring type. This item applies only when MyType = 1.
            1 = Spring resists tension and compression
            2 = Spring resists compression only
            3 = Spring resists tension only
        LinkProp(str)-The name of the link property assigned to the spring. This item applies only when MyType = 2.
        Face(int)-This is -1, -2 or a nonzero, positive integer indicating the area object face to which the specified
            spring assignment applies.
            -1 = Bottom face,-2 = Top face,>0 = Edge face
            Note that edge face n is from area object point n to area object point n + 1. For example, edge face 2 is
            from area object point 2 to area object point 3.
        SpringLocalOneType(int)-This is 1, 2 or 3, indicating the method used to specify the spring positive local
            1-axis orientation.
            1 = Parallel to area object local axis
            2 = Normal to specified area object face
            3 = User specified direction vector
        Dir(int)-This is 1, 2, 3, -1, -2 or -3, indicating the area object local axis that corresponds to the positive
            local 1-axis of the spring. This item applies only when SpringLocalOneType = 1
        Outward(bool)-This item is True if the spring positive local 1 axis is outward from the specified area object
            face. This item applies only when SpringLocalOneType = 2.
        Vec(float list)-This is an array of three values that define the direction vector of the spring positive local
            1-axis. The direction vector is in the coordinate system specified by the CSys item. This item applies only
            when SpringLocalOneType = 3.
        Ang(float)-This is the angle that the link local 2-axis is rotated from its default orientation. This item
            applies only when MyType = 2. [deg]
        Replace(bool)-If this item is True, all existing spring assignments to the area object are removed before
            assigning the specified spring. If it is False, the specified spring is added to any existing springs
            already assigned to the area object.
        CSys(str)-This is Local (meaning the area object local coordinate system) or the name of a defined coordinate
            system. This item is the coordinate system in which the user specified direction vector, Vec, is specified.
            This item applies only when SpringLocalOneType = 3.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignor
        """
        self.SapModel.AreaObj.SetSpring(name,myType,s,simpleSpringType,LinkProp,Face,SpringLocalOneType,Dir,
                                 OutWard,Vec,Ang,Replace,CSys,itemType)

    def assign_AreaObj_SetThickness(self,name,ThinknessType,ThinknessPattern,ThicknessPatternSF,Thickness,itemType=0):
        """
        ---This function sets the thickness overwrite assignments for area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item.
        ThinknessType(int)-This is 0, 1 or 2, indicating the thickness overwrite type.
            0 = No thickness overwrites
            1 = User defined thickness overwrites specified by joint pattern
            2 = User defined thickness overwrites specified by point
        ThinknessPattern(str)-This item applies only when ThicknessType = 1. It is the name of the defined joint
            pattern that is used to calculate the thicknesses
        ThicknessPatternSF(float)-This item applies only when ThicknessType = 1. It is the scale factor applied
            to the joint pattern when calculating the thicknesses. [L]
        Thickness(float)-This item applies only when ThicknessType = 2. It is an array of thicknesses at each
            of the points that define the area object. [L]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignor
        """
        self.SapModel.AreaObj.SetThickness(name,ThinknessType,ThinknessPattern,ThicknessPatternSF,Thickness,itemType)

    def assign_AreaObj_GetAutoMesh(self,name):
        """
        ---This function retrieves the automatic meshing assignments to area objects---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,MeshType,n1,n2,MaxSize1,MaxSize2,PointOnEdgeFromLine,PointOnEdgeFromPoint,ExtendCookieCutLines,
        Rotation,MaxSizeGeneral,LocalAxesOnEdge,LocalAxesOnFace,RestraintsOnEdge,RestraintsOnFace,Group,SubMesh,
        SubMeshSize]
        MeshType(int)-This item is 0, 1, 2, 3, 4, 5 or 6, indicating the automatic mesh type for the area object.
            0 = No automatic meshing
            1 = Mesh area into a specified number of objects
            2 = Mesh area into objects of a specified maximum size
            3 = Mesh area based on points on area edges
            4 = Cookie cut mesh area based on lines intersecting edges
            5 = Cookie cut mesh area based on points
            6 = Mesh area using General Divide Tool
            Mesh options 1, 2 and 3 apply to quadrilaterals and triangles only.
        n1(int)-This item applies when MeshType = 1. It is the number of objects created along the edge of the
            meshed area object that runs from point 1 to point 2.
        n2(int)-This item applies when MeshType = 1. It is the number of objects created along the edge of the
            meshed area object that runs from point 1 to point 3.
        MaxSize1(float)-This item applies when MeshType = 2. It is the maximum size of objects created along the
            edge of the meshed area object that runs from point 1 to point 2. [L]If this item is input as 0, the
            default value is used. The default value is 48 inches if the database units are English or 120 centimeters
            if the database units are metric.
        MaxSize2(float)-This item applies when MeshType = 2. It is the maximum size of objects created along the edge
            of the meshed area object that runs from point 1 to point 3. [L]If this item is input as 0, the default
            value is used. The default value is 48 inches if the database units are English or 120 centimeters if the
            database units are metric.
        PointOnEdgeFromLine(bool)-This item applies when MeshType = 3. If it is True, points on the area object edges
            are determined from intersections of straight line objects included in the group specified by the Group
            item with the area object edges.
        PointOnEdgeFromPoint(bool)-This item applies when MeshType = 3. If it is True, points on the area object edges
            are determined from point objects included in the group specified by the Group item that lie on the area object edges
        ExtendCookieCutLines(bool)-This item applies when MeshType = 4. MeshType = 4 provides cookie cut meshing based
            on straight line objects included in the group specified by the Group item that intersect the area object
            edges. If the ExtendCookieCutLines item is True, all straight line objects included in the group specified
            by the Group item are extended to intersect the area object edges for the purpose of meshing the area object.
        Rotation(float)-This item applies when MeshType = 5. MeshType = 5 provides cookie cut meshing based on two
            perpendicular lines passing through point objects included in the group specified by the Group item.
            By default these lines align with the area object local 1 and 2 axes. The Rotation item is an angle in
            degrees that the meshing lines are rotated from their default orientation. [deg]
        MaxSizeGeneral(float)-This item applies when MeshType = 6. It is the maximum size of objects created by the
            General Divide Tool.If this item is input as 0, the default value is used. The default value is 48 inches
            if the database units are English or 120 centimeters if the database units are metric.
        LocalAxesOnEdge(bool)-If this item is True, and if both points along an edge of the original area object
            have the same local axes, then the program makes the local axes for added points along the edge the
            same as the edge end points.
        LoalAxesOnFace(bool)-If this item is True, and if all points around the perimeter of the original area object
            have the same local axes, the program makes the local axes for all added points the same as the perimeter points.
        RestraintsOnEdge(bool)-If this item is True, and if both points along an edge of the original area object have
            the same restraint/constraint, then, if the added point and the adjacent corner points have the same local
            axes definition, the program includes the restraint/constraint for added points along the edge.
        RestraintsOnFace(bool)-If this item is True, and if all points around the perimeter of the original area object
            have the same restraint/constraint, then, if an added point and the perimeter points have the same local
            axes definition, the program includes the restraint/constraint for the added point.
        Group(str)-The name of a defined group. Some of the meshing options make use of point and line objects
            included in this group.
        SubMesh(bool)-If this item is True, after initial meshing, the program further meshes any area objects that
            have an edge longer than the length specified by the SubMeshSize item.
        SubMeshSize(bool)-This item applies when the SubMesh item is True. It is the maximum size of area objects to
            remain when the auto meshing is complete. [L]If this item is input as 0, the default value is used.
            The default value is 12 inches if the database units are English or 30 centimeters if the database units are metric.
        """
        result=self.SapModel.AreaObj.GetAutoMesh(name)
        return result

    def assign_AreaObj_GetEdgeConstraint(self,name):
        """
        ---This function retrieves the generated edge constraint assignments to area objects---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,ConstraintExists]
        ConstraintExists(bool)-This item is True if an automatic edge constraint is generated by the program for
            the area object in the analysis model.
        """
        result=self.SapModel.AreaObj.GetEdgeConstraint(name)
        return result

    def assign_AreaObj_GetElm(self,name):
        """
        ---This function retrieves the names of the area elements (analysis model area) associated with a specified
        area object in the object-based model
        ---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,nelm,Elm]
        nelm(int)-The number of area elements created from the specified area object
        Elm(str list)-An array that includes the name of a area element created from the specified area object.
        """
        result=self.SapModel.AreaObj.GetElm(name)
        return result

    def assign_AreaObj_GetGroupAssign(self,name):
        """
        ---This function retrieves the names of the groups to which a specified area object is assigned---
        inputs:
        name(str)-The name of an existing area object.
        return:
        [index,NumberGroups,Groups]
        NumberGroups(int)-The number of group names retrieved.
        Groups(str list)-The names of the groups to which the area object is assigned
        """
        result=self.SapModel.AreaObj.GetGroupAssign(name)
        return result

    def assign_AreaObj_GetLoadGravity(self,name):
        """
        ---This function retrieves the gravity load assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,AreaName,LoadPat,CSys,x,y,z]
        NumberItems(int)-The total number of gravity loads retrieved for the specified area objects
        AreaName(str)-This is an array that includes the name of the area object associated with each gravity load
        LoadPat(str list)-This is an array that includes the name of the coordinate system in which the gravity
            load multipliers are specified
        CSys(str list)-This is an array that includes the name of the coordinate system associated with each gravity load
        x,y,z(float list)-These are arrays of gravity load multipliers in the x, y and z directions of the specified
            coordinate system
        """
        result=self.SapModel.AreaObj.GetLoadGravity(name)
        return result

    def assign_AreaObj_GetLoadPorePressure(self,name):
        """
        ---This function retrieves the pore pressure load assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,AreaName,LoadPat,Value,PatternName]
        NumberItems(int)-The total number of pore pressure loads retrieved for the specified area objects
        AreaName(str list)-This is an array that includes the name of the area object associated with each pore pressure load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each pore pressure load
        Value(float list)-This is an array that includes the pore pressure load value. [F/L2]
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the pore
            pressure load
        """
        result=self.SapModel.AreaObj.GetLoadPorePressure(name)
        return result

    def assign_AreaObj_GetLoadRotate(self,name):
        """
        ---This function retrieves the rotate load assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,AreaName,LoadPat,Value]
        NumberItems(int)-The total number of rotate loads retrieved for the specified area objects.
        AreaName(str list)-This is an array that includes the name of the area object associated with each rotate load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each rotate load
        Value(float list)-This is an array that includes the angular velocity value. [Cyc/T]
        """
        result=self.SapModel.AreaObj.GetLoadRotate(name)
        return result

    def assign_AreaObj_GetLoadStrain(self,name):
        """
        ---This function retrieves the strain load assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,AreaName,LoadPat,component,Value,PatternName]
        NumberItems(int)-The total number of strain loads retrieved for the specified area objects
        AreaName(str list)-This is an array that includes the name of the area object associated with each strain load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each strain load
        Component(int)-This is an array that includes 1, 2, 3, 4, 5, 6, 7, 8, or 9, indicating the component associated
            with each strain load.
            1 = Strain11,2 = Strain22,3 = Strain12,4 = Curvature11,5 = Curvature22,6 = Curvature12,7 = Strain13
            8 = Strain23,9 = Strain33
        Value(float list)-This is an array that includes the strain value. [L/L] for Component = 1, 2, 3, 7, 8, and 9,
            and [1/L] for Component = 4, 5 and 6
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the strain load.
        """
        result=self.SapModel.AreaObj.GetLoadStrain(name)
        return result

    def assign_AreaObj_GetLoadSurfacePressure(self,name):
        """
        ---This function retrieves the surface pressure load assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,AreaName,LoadPat,Face,Value,PatternName]
        NumberItems(int)-The total number of surface pressure loads retrieved for the specified area objects
        AreaName(str list)-This is an array that includes the name of the area object associated with each surface pressure load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each surface pressure load
        Face(int)-This is an array that includes either -1, -2 or a nonzero, positive integer, indicating the area
            object face to which the specified load assignment applies.
            -1 = Bottom face,-2 = Top face,>0 = Edge face
            Note that edge face n is from area object point n to area object point n + 1. For example, edge face 2 is
            from area object point 2 to area object point 3.
        Value(float list)-This is an array that includes the surface pressure load value. [F/L2]
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify
            the surface pressure load.
        """
        result=self.SapModel.AreaObj.GetLoadSurfacePressure(name)
        return result

    def assign_AreaObj_GetLoadTemperature(self,name):
        """
        ---This function retrieves the temperature load assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,AreaName,LoadPat,MyType,Value,PatternName]
        NumberItems(int)-The total number of temperature loads retrieved for the specified area objects
        AreaName(str list)-This is an array that includes the name of the area object associated with each temperature load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each temperature load
        MyType(int)-This is an array that includes either 1 or 3, indicating the type of temperature load.
            1 = Temperature,3 = Temperature gradient along local 3 axis
        Value(float list)-This is an array that includes the temperature load value. [T] for MyType= 1 and [T/L] for MyType= 3
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the temperature load.
        """
        result=self.SapModel.AreaObj.GetLoadTemperature(name)
        return result

    def assign_AreaObj_GetLoadUniform(self,name):
        """
        ---This function retrieves the uniform load assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,AreaName,LoadPat,CSys,Dir,Value]
        NumberItems(int)-The total number of uniform loads retrieved for the specified area objects.
        AreaName(str list)-This is an array that includes the name of the area object associated with each uniform load
        LoadPat(str list)-This is an array that includes the name of the coordinate system in which the uniform load
            is specified.
        CSys(str list)-This is an array that includes the name of the coordinate system associated with each uniform load.
        Dir(int)-This is an integer between 1 and 11, indicating the direction of the load.
            1 = Local 1 axis (only applies when CSys is Local)
            2 = Local 2 axis (only applies when CSys is Local)
            3 = Local 3 axis (only applies when CSys is Local)
            4 = X direction (does not apply when CSys is Local)
            5 = Y direction (does not apply when CSys is Local)
            6 = Z direction (does not apply when CSys is Local)
            7 = Projected X direction (does not apply when CSys is Local)
            8 = Projected Y direction (does not apply when CSys is Local)
            9 = Projected Z direction (does not apply when CSys is Local)
            10 = Gravity direction (only applies when CSys is Global)
            11 = Projected Gravity direction (only applies when CSys is Global)
            The positive gravity direction (see Dir = 10 and 11) is in the negative Global Z direction.
        Value(float)-The uniform load value. [F/L2]
        """
        result=self.SapModel.AreaObj.GetLoadUniform(name)
        return result

    def assign_AreaObj_GetLoadUniformToFrame(self,name):
        """
        ---This function retrieves the uniform to frame load assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,AreaName,LoadPat,CSys,Dir,Value,DistType]
        NumberItems(int)-The total number of uniform loads retrieved for the specified area objects
        AreaName(str list)-This is an array that includes the name of the area object associated with each uniform load.
        LoadPat(str list)-This is an array that includes the name of the coordinate system in which the uniform load is specified
        CSys(str list)-This is an array that includes the name of the coordinate system associated with each uniform load
        Dir(int)-This is an integer between 1 and 11, indicating the direction of the load.
            1 = Local 1 axis (only applies when CSys is Local)
            2 = Local 2 axis (only applies when CSys is Local)
            3 = Local 3 axis (only applies when CSys is Local)
            4 = X direction (does not apply when CSys is Local)
            5 = Y direction (does not apply when CSys is Local)
            6 = Z direction (does not apply when CSys is Local)
            7 = Projected X direction (does not apply when CSys is Local)
            8 = Projected Y direction (does not apply when CSys is Local)
            9 = Projected Z direction (does not apply when CSys is Local)
            10 = Gravity direction (only applies when CSys is Global)
            11 = Projected Gravity direction (only applies when CSys is Global)
            The positive gravity direction (see Dir = 10 and 11) is in the negative Global Z direction
        Value(float)-The uniform load value. [F/L2]
        DistType(int)-This is either 1 or 2, indicating the load distribution type.
            1 = One-way load distribution,2 = Two-way load distribution
            One-way distribution is parallel to the area object local 1 axis. Two-way distribution is parallel
            to the area object local 1 and 2 axes.
        """
        result=self.SapModel.AreaObj.GetLoadUniformToFrame(name)
        return result

    def assign_AreaObj_GetLoadWindPressure_1(self,name):
        """
        ---This function retrieves the wind pressure load assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,AreaName,LoadPat,MyType,Cp,DistributionType]
        NumberItems(int)-The total number of wind pressure loads retrieved for the specified area objects.
        AreaName(str list)-This is an array that includes the name of the area object associated with each wind pressure load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each wind pressure load
        MyType(int)-This is an array that includes either 1 or 2, indicating the wind pressure type.
            1 = Windward, pressure varies over height
            2 = Other, pressure is constant over height
        Cp(float list)-This is an array that includes the wind pressure coefficient value
        DistributionType(int)-This is either 1 or 2, indicating the distribution type.
            1 = To Joints
            2 = To Frames – One-way
            3 = To Frames – Two-way
        """
        result=self.SapModel.AreaObj.GetLoadWindPressure_1(name)
        return result

    def assign_AreaObj_GetLocalAxes(self,name):
        """
        ---This function retrieves the local axis angle assignment for area objects---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,Ang,Advanced]
        Ang(float)-This is the angle that the local 1 and 2 axes are rotated about the positive local 3 axis from
            the default orientation. The rotation for a positive angle appears counter clockwise when the local
            +3 axis is pointing toward you. [deg]
        Advanced(bool)-This item is True if the area object local axes orientation was obtained using advanced
            local axes parameters.
        """
        result=self.SapModel.AreaObj.GetLocalAxes(name)
        return result

    def assign_AreaObj_GetMass(self,name):
        """
        ---This function retrieves the mass per unit area assignment for area objects---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,MassOverL2]
        MassOverL2(float)-The mass per unit area assigned to the area object. [M/L2]
        """
        result=self.SapModel.AreaObj.GetMass(name)
        return result

    def assign_AreaObj_GetMatTemp(self,name):
        """
        ---This function retrieves the material temperature assignments to area objects---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,Temp,PatternName]
        Temp(float)-This is the material temperature value assigned to the area object. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the material
            temperature for the area object is uniform over the object at the value specified by Temp.If PatternName
            is the name of a defined joint pattern, the material temperature for the area object may vary. The material
            temperature at each corner point around the area object perimeter is equal to the specified temperature
            multiplied by the pattern value at the associated point object. The material temperature at other points
            in the area object is calculated by interpolation from the corner points.
        """
        result=self.SapModel.AreaObj.GetMatTemp(name)
        return result

    def assign_AreaObj_GetModifiers(self,name):
        """
        ---This function retrieves the modifier assignment for area objects. The default value for all modifiers is one---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,Value]
        Value(float list)-This is an array of ten unitless modifiers.
            Value(0) = Membrane f11 modifier
            Value(1) = Membrane f22 modifier
            Value(2) = Membrane f12 modifier
            Value(3) = Bending m11 modifier
            Value(4) = Bending m22 modifier
            Value(5) = Bending m12 modifier
            Value(6) = Shear v13 modifier
            Value(7) = Shear v23 modifier
            Value(8) = Mass modifier
            Value(9) = Weight modifier
        """
        result=self.SapModel.AreaObj.GetModifiers(name)
        return result

    def assign_AreaObj_GetNameList(self):
        """
        ---This function retrieves the names of all defined area objects---
        return:
        [index,NumberNames,MyName]
        NumberNames(int)-The number of area object names retrieved by the program
        MyName(str list)-This is a one-dimensional array of area object names
        """
        result=self.SapModel.AreaObj.GetNameList()
        return result

    def assign_AreaObj_GetNotionalSize(self,name):
        """
        ---This function retrieves the method to determine the notional size of an area section for the creep
        and shrinkage calculations. This function is currently worked for shell type area section.
        ---
        inputs:
        name(str)-The name of an existing shell-type area section property
        return:
        [index,stype,Value]
        stype(str)-The type to define the notional size of a section. It can be:
            "Auto" = Program will determine the notional size based on the average thickness of an area element.
            "User" = The notional size is based on the user-defined value.
            "None" = Notional size will not be considered. In other words, the time-dependent effect of this section
            will not be considered.
        Value(float)-For stype is "Auto", the Value represents for the scale factor to the program-determined
            notional size; for stype is “User”, the Value represents for the user-defined notional size [L];
            for stype is “None”, the Value will not be used and can be set to 1.
        """
        result=self.SapModel.PropArea.GetNotionalSize(name)
        return result

    def assign_AreaObj_GetOffsets(self,name):
        """
        ---This function retrieves the joint offset assignments for area objects---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,OffsetType,OffsetPattern,OffsetPatternSF,Offset]
        OffsetType(int)-This is 0, 1 or 2, indicating the joint offset type.
            0 = No joint offsets
            1 = User defined joint offsets specified by joint pattern
            2 = User defined joint offsets specified by point
        OffsetPattern(str)-This item applies only when OffsetType = 1. It is the name of the defined joint
            pattern that is used to calculate the joint offsets
        OffsetPatternSF(float)-This item applies only when OffsetType = 1. It is the scale factor applied to
            the joint pattern when calculating the joint offsets. [L]
        Offset(float list)-This item applies only when OffsetType = 2. It is an array of joint offsets for
            each of the points that define the area object. [L]
        """
        result=self.SapModel.AreaObj.GetOffsets(name)
        return result

    def assign_AreaObj_GetPoints(self,name):
        """
        ---This function retrieves the names of the point objects that define an area object---
        inputs:
        name(str)-The name of a defined area object
        return:
        [index,NumberPoints,Point]
        NumberPoints(int)-The number of point objects that define the area object
        Point(str list)-This is an array containing the names of the point objects that define the area object.
            The point names are in order around the area object
        """
        result=self.SapModel.AreaObj.GetPoints(name)
        return result

    def assign_AreaObj_GetProperty(self,name):
        """
        ---This function retrieves the area property assigned to an area object---
        inputs:
        name(str)-The name of a defined area object
        return:
        [index,PropName]
        PropName(str)-The name of the area property assigned to the area object. This item is None if no area
            property is assigned to the area object.
        """
        result=self.SapModel.AreaObj.GetProperty(name)
        return result

    def assign_AreaObj_GetSpring(self,name):
        """
        ---This function retrieves the spring assignments to an area object face---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,NumberSprings,MyType,s,SimpleSpringType,LinkProp,Face,SpringLocalOneType,Dir,Outward,VecX,
        VecY,VecZ,CSys,Ang]
        NumberSprings(str)-The number of spring assignments made to the specified area object
        MyType(int)-This is either 1 or 2, indicating the spring property type.
            1 = Simple spring,2 = Link property
        s(float)-The simple spring stiffness per unit area of the specified area object face. This item applies
            only when MyType = 1. [F/L3]
        SimpleSpringType(int)-This is 1, 2 or 3, indicating the simple spring type. This item applies only when MyType = 1.
            1 = Spring resists tension and compression
            2 = Spring resists compression only
            3 = Spring resists tension only
        LinkProp(str)-The name of the link property assigned to the spring. This item applies only when MyType = 2.
        Face(int)-This is -1, -2 or a nonzero, positive integer indicating the area object face to which the specified
            spring assignment applies.
            -1 = Bottom face,-2 = Top face,>0 = Edge face
            Note that edge face n is from area object point n to area object point n + 1. For example, edge face 2 is
            from area object point 2 to area object point 3.
        SpringLocalOneType(int)-This is 1, 2 or 3, indicating the method used to specify the spring positive local
            1-axis orientation.
            1 = Parallel to area object local axis
            2 = Normal to specified area object face
            3 = User specified direction vector
        Dir(int)-This is 1, 2, 3, -1, -2 or -3, indicating the area object local axis that corresponds to the positive
            local 1-axis of the spring. This item applies only when SpringLocalOneType = 1
        Outward(bool)-This item is True if the spring positive local 1 axis is outward from the specified area object
            face. This item applies only when SpringLocalOneType = 2.
        Vec(float list)-This is an array of three values that define the direction vector of the spring positive local
            1-axis. The direction vector is in the coordinate system specified by the CSys item. This item applies only
            when SpringLocalOneType = 3.
        CSys(str)-This is Local (meaning the area object local coordinate system) or the name of a defined coordinate
            system. This item is the coordinate system in which the user specified direction vector, Vec, is specified.
            This item applies only when SpringLocalOneType = 3.
        Ang(float)-This is the angle that the link local 2-axis is rotated from its default orientation. This item
            applies only when MyType = 2. [deg]
        """
        result=self.SapModel.AreaObj.GetSpring(name)
        return result

    def assign_AreaObj_GetThickness(self,name):
        """
        ---This function retrieves the thickness overwrite assignments for area objects---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,ThinknessType,ThinknessPattern,ThicknessPatternSF,Thickness]
        ThinknessType(int)-This is 0, 1 or 2, indicating the thickness overwrite type.
            0 = No thickness overwrites
            1 = User defined thickness overwrites specified by joint pattern
            2 = User defined thickness overwrites specified by point
        ThicknessPattern(str)-This item applies only when ThicknessType = 1. It is the name of the defined joint
            that is used to calculate the thicknesses
        ThicknessPatternSF(float)-This item applies only when ThicknessType = 1. It is the scale factor applied
            to the joint pattern when calculating the thicknesses. [L]
        Thickness(float list)-This item applies only when ThicknessType = 2. It is an array of thicknesses at each
            of the points that define the area object. [L]
        """
        result=self.SapModel.AreaObj.GetThickness(name)
        return result

    def assign_AreaObj_GetTransformationMatrix(self,name):
        """
        ---The function returns zero if the area object transformation matrix is successfully retrieved---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,Value]
        Value(float list)-Value is an array of nine direction cosines that define the transformation matrix.The
            following matrix equation shows how the transformation matrix is used to convert items from the area
            object local coordinate system to the global coordinate system.
        """
        result=self.SapModel.AreaObj.GetTransformationMatrix(name)
        return result

    def assign_SolidObj_AddByCoord(self,x,y,z,PropName="Default",UserName="",CSys="Global"):
        """
        ---This function adds a new solid object whose corner points are at the specified coordinates. Note that
        solid objects always are defined with eight corner points
        ---
        inputs:
        x,y,z(float list)-These are arrays of x, y and z coordinates, respectively, for the corner points of the
            solid object. The coordinates are in the coordinate system defined by the CSys item.
        PropName(str)-This is either Default or the name of a defined solid property.If it is Default, the program
            assigns a default solid property to the solid object. If it is the name of a defined solid property,
            that property is assigned to the solid object
        UserName(str)-This is an optional user specified name for the solid object. If a UserName is specified and
            that name is already used for another solid object, the program ignores the UserName
        CSys(str)-The name of the coordinate system in which the solid object point coordinates are defined
        """
        # This is the name that the program ultimately assigns for the solid object. If no UserName is specified,
        # the program assigns a default name to the solid object. If a UserName is specified and that name is not
        # used for another solid object, the UserName is assigned to the solid object; otherwise a default name is
        # assigned to the solid object.
        name = ""
        self.SapModel.SolidObj.AddByCoord(x,y,z,name,PropName,UserName,CSys)

    def assign_SolidObj_AddByPoint(self,Point,PropName="Default",UserName=""):
        """
        ---This function adds a new solid object whose corner points are specified by name---
        inputs:
        Point(str list)-This is an array containing the names of the eight point objects that define
            the corner points of the added solid object
        PropName(str)-This is either Default or the name of a defined solid property
        UserName(str)-This is an optional user specified name for the solid object. If a UserName is specified
            and that name is already used for another solid object, the program ignores the UserName
        """
        # This is the name that the program ultimately assigns for the solid object. If no UserName is specified,
        # the program assigns a default name to the solid object. If a UserName is specified and that name is not
        # used for another solid object, the UserName is assigned to the solid object; otherwise a default name is
        # assigned to the solid object.
        name = ""
        self.SapModel.SolidObj.AddByPoint(Point,name,PropName,UserName)

    def assign_SolidObj_Count(self):
        """
        ---This function returns a count of the solid objects in the model---
        """
        result=self.SapModel.SolidObj.Count()
        return result

    def assign_SolidObj_SetAutoMesh(self,name,MeshType,n1=2,n2=2,n3=2,MaxSize1=0,MaxSize2=0,MaxSize3=0,RestraintsOnEdge=False,
                                    RestraintOnFace=False):
        """
        ---This function makes automatic meshing assignments to solid objects---
        inputs:
        name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        MeshType(int)-This item is 0, 1 or 2, indicating the automatic mesh type for the solid object.
            0 = No automatic meshing
            1 = Mesh solid into a specified number of objects
            2 = Mesh solid into objects of a specified maximum size
        n1(int)-This item applies when MeshType = 1. It is the number of objects created along the edge of the
            meshed solid object that runs from point 1 to point 2
        n2(int)-This item applies when MeshType = 1. It is the number of objects created along the edge of the
            meshed solid object that runs from point 1 to point 3
        n3(int)-This item applies when MeshType = 1. It is the number of objects created along the edge of the
            meshed solid object that runs from point 1 to point 5
        MaxSize1(float)-This item applies when MeshType = 2. It is the maximum size of objects created along the
            edge of the meshed solid object that runs from point 1 to point 2. [L] If this item is input as 0, the
            default value is used. The default value is 48 inches if the database units are English or 120 centimeters
            if the database units are metric
        MaxSize2(float)-This item applies when MeshType = 2. It is the maximum size of objects created along the edge
            of the meshed solid object that runs from point 1 to point 3. [L] If this item is input as 0, the default
            value is used. The default value is 48 inches if the database units are English or 120 centimeters if the
            database units are metric.
        MaxSize3(float)-This item applies when MeshType = 2. It is the maximum size of objects created along the edge
            of the meshed solid object that runs from point 1 to point 5. [L] If this item is input as 0, the default
            value is used. The default value is 48 inches if the database units are English or 120 centimeters if the
            database units are metric.
        RestraintsOnEdge(bool)-If this item is True, and if both points along an edge of the original solid object have
            the same restraint/constraint, then, if the an added point on that edge and the original corner points have
            the same local axes definition, the program assigns the restraint/constraint to the added point
        RestraintsOnFace(bool)-If this item is True, and if all corner points on an solid object face have the same
            restraint/constraint, then, if an added point on that face and the original corner points for the face
            have the same local axes definition, the program assigns the restraint/constraint to the added point.
        """
        self.SapModel.SolidObj.SetAutoMesh(name,MeshType,n1,n2,n3,MaxSize1,MaxSize2,MaxSize3,RestraintsOnEdge,RestraintOnFace)

    def assign_SolidObj_SetEdgeConstraint(self,Name,ConstraintExists,itemType=0):
        """
        ---This function makes generated edge constraint assignments to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        ConstraintExists(bool)-This item is True if an automatic edge constraint is generated by the program for
            the solid object in the analysis model
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.SolidObj.SetEdgeConstraint(Name,ConstraintExists,itemType)

    def assign_SolidObj_SetGroupAssign(self,Name,GroupName,Remove=False,itemType=0):
        """
        ---This function adds or removes solid objects from a specified group---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        GroupName(str)-The name of an existing group to which the assignment is made
        Remove(bool)-If this item is False, the specified solid objects are added to the group specified by the
            GroupName item. If it is True, the solid objects are removed from the group
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.SolidObj.SetGroupAssign(Name,GroupName,Remove,itemType)

    def assign_SolidObj_SetLoadGravity(self,Name,LoadPat,x,y,z,Replace=True,CSys="Global",itemType=0):
        """
        ---This function assigns gravity load multipliers to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        x,y,z(float)-These are the gravity load multipliers in the x, y and z directions of the specified coordinate system
        Replace(bool)-If this item is True, all previous gravity loads, if any, assigned to the specified
            solid object(s), in the specified load pattern, are deleted before making the new assignment
        CSys(str)-The coordinate system in which the x, y and z multipliers are specified
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.SolidObj.SetLoadGravity(Name,LoadPat,x,y,z,Replace,CSys,itemType)

    def assign_SolidObj_SetLoadPorePressure(self,Name,LoadPat,Value,PatternName="",Replace=True,itemType=0):
        """
        ---This function assigns pore pressure loads to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        Value(float)-This is the pore pressure value. [F/L2]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the pore pressure
            load for the solid object is uniform over the object at the value specified by Value.If PatternName
            is the name of a defined joint pattern, the pore pressure load for the solid object is based on the
            specified pore pressure value multiplied by the pattern value at the corner point objects of the solid object.
        Replace(bool)-If this item is True, all previous pore pressure loads, if any, assigned to the specified solid
            object(s), in the specified load case, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.SolidObj.SetLoadPorePressure(Name,LoadPat,Value,PatternName,Replace,itemType)

    def assign_SolidObj_SetLoadStrain(self,Name,LoadPat,Component,Value,Replace=True,PatternName="",itemType=0):
        """
        ---This function assigns strain loads to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        Component(int)-This is 1, 2, 3, 4, 5 or 6, indicating the component to which the strain load is applied.
            1 = Strain11
            2 = Strain22
            3 = Strain33
            4 = Strain12
            5 = Strain13
            6 = Strain23
        Value(float)-This is the strain load value. [L/L]
        Replace(bool)-If this item is True, all previous strain loads, if any, assigned to the specified solid object(s),
            in the specified load pattern, for the specified degree of freedom, are deleted before making the new assignment.
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the strain load for the
            solid object is uniform over the object at the value specified by Value.If PatternName is the name of a
            defined joint pattern, the strain load for the solid object is based on the specified strain value multiplied
            by the pattern value at the corner point objects of the solid object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.SolidObj.SetLoadStrain(Name,LoadPat,Component,Value,Replace,PatternName,itemType)

    def assign_SolidObj_SetLoadSurfacePressure(self,Name,LoadPat,Face,Value,PatternName="",Replace=True,itemType=0):
        """
        ---This function assigns surface pressure loads to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        Face(str)-This is 1, 2, 3, 4, 5 or 6, indicating the solid object face to which the specified load assignment applies.
        Value(float)-This is the surface pressure value. [F/L2]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the surface pressure
            load for the solid object is uniform over the object at the value specified by Value.If PatternName is
            the name of a defined joint pattern, the surface pressure load for the solid object is based on the
            specified surface pressure value multiplied by the pattern value at the corner point objects of the solid object.
        Replace(bool)-If this item is True, all previous surface pressure loads, if any, assigned to the specified solid
            object(s), on the specified face, in the specified load pattern, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.SolidObj.SetLoadSurfacePressure(Name,LoadPat,Face,Value,PatternName,Replace,itemType)

    def assign_SolidObj_SetLoadTemperature(self,Name,LoadPat,Value,PatternName="",Replace=True,itemType=0):
        """
        ---This function assigns temperature loads to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        Value(float)-This is the temperature change value. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the temperature load
            for the solid object is uniform over the object at the value specified by Value.If PatternName is the
            name of a defined joint pattern, the temperature load for the solid object is based on the specified
            temperature value multiplied by the pattern value at the corner point objects of the solid object.
        Replace(bool)-If this item is True, all previous temperature loads, if any, assigned to the specified solid
            object(s), in the specified load case, are deleted before making the new assignment
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.SolidObj.SetLoadTemperature(Name,LoadPat,Value,PatternName,Replace,itemType)

    def assign_SolidObj_SetLocalAxes(self,Name,a,b,c,itemType=0):
        """
        ---This function sets the local axes angles for solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        a,b,c(float)-The local axes of the solid object are defined by first setting the positive local 1, 2 and 3
            axes the same as the positive global X, Y and Z axes and then doing the following: [deg]
                1.Rotate about the 3 axis by angle a.
                2.Rotate about the resulting 2 axis by angle b.
                3.Rotate about the resulting 1 axis by angle c.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.SolidObj.SetLocalAxes(Name,a,b,c,itemType)

    def assign_SolidObj_SetMatTemp(self,Name,Temp,PatternName="",itemType=0):
        """
        ---This function assigns material temperatures to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        Temp(float)-This is the material temperature value assigned to the solid object. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the material
            temperature for the solid object is uniform over the object at the value specified by Temp.If
            PatternName is the name of a defined joint pattern, the material temperature for the solid object
            may vary. The material temperature at each corner point of the solid object is equal to the specified
            temperature multiplied by the pattern value at the associated point object. The material temperature
            at other points in the solid object is calculated by interpolation from the corner points.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.SolidObj.SetMatTemp(Name,Temp,PatternName,itemType)

    def assign_SolidObj_SetProperty(self,Name,PropName,itemType=0):
        """
        ---This function assigns a solid property to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        PropName(str)-This is the name of a solid property to be assigned to the specified solid object(s).
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.SolidObj.SetProperty(Name,PropName,itemType)

    def assign_SolidObj_SetSpring(self,Name,MyType,s,SimpleSpringType,LinkProp,Face,SpringLocalOneType,Dir,
                                  Outward,Vec,Ang,Replace,CSys="Local",itemType=0):
        """
        ---This function makes spring assignments to solid objects. The springs are assigned to a specified solid object face---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        MyType(int)-This is either 1 or 2, indicating the spring property type.
            1 = Simple spring,2 = Link property
        s(float)-The simple spring stiffness per unit area of the specified solid object face. This item applies
            only when MyType = 1. [F/L3]
        SimpleSpringType(int)-This is 1, 2 or 3, indicating the simple spring type. This item applies only when MyType = 1.
            1 = Spring resists tension and compression
            2 = Spring resists compression only
            3 = Spring resists tension only
        LinkProp(str)-The name of the link property assigned to the spring. This item applies only when MyType = 2
        Face(int)-This is 1, 2, 3, 4, 5 or 6, indicating the solid object face to which the specified spring assignment applies
        SpringLocalOneType(int)-This is 1, 2 or 3, indicating the method used to specify the spring positive local 1-axis
            orientation.
            1 = Parallel to solid object local axis
            2 = Normal to specified solid object face
            3 = User specified direction vector
        Dir(int)-This is 1, 2, 3, -1, -2 or -3, indicating the solid object local axis that corresponds to the
            positive local 1-axis of the spring. This item applies only when SpringLocalOneType = 1.
        Outward(bool)-This item is True if the spring positive local 1 axis is outward from the specified solid object
            face. This item applies only when SpringLocalOneType = 2.
        Vec(float list)-This is an array of three values that define the direction vector of the spring positive local
            1-axis. The direction vector is in the coordinate system specified by the CSys item. This item applies only
            when SpringLocalOneType = 3
        Ang(float)-This is the angle that the link local 2-axis is rotated from its default orientation.
            This item applies only when MyType = 2. [deg]
        Replace(bool)-If this item is True, all existing spring assignments to the solid object are removed before
            assigning the specified spring. If it is False, the specified spring is added to any existing springs
            already assigned to the solid object
        CSys(str)-This is Local (meaning the solid object local coordinate system) or the name of a defined coordinate
            system. This item is the coordinate system in which the user specified direction vector, Vec, is specified.
            This item applies only when SpringLocalOneType = 3
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.SolidObj.SetSpring(Name,MyType,s,SimpleSpringType,LinkProp,Face,SpringLocalOneType,Dir,
                                  Outward,Vec,Ang,Replace,CSys,itemType)

    def assign_SolidObj_GetAutoMesh(self,name):
        """
        ---The name of an existing solid object---
        inputs:
        name(str)-The name of an existing solid object
        return:
        [index,MeshType,n1,n2,n3,MaxSize1,MaxSize2,MaxSize3,RestraintsOnEdge,RestraintsOnFace]

        MeshType(int)-This item is 0, 1 or 2, indicating the automatic mesh type for the solid object.
            0 = No automatic meshing
            1 = Mesh solid into a specified number of objects
            2 = Mesh solid into objects of a specified maximum size
        n1(int)-This item applies when MeshType = 1. It is the number of objects created along the edge of the
            meshed solid object that runs from point 1 to point 2
        n2(int)-This item applies when MeshType = 1. It is the number of objects created along the edge of the
            meshed solid object that runs from point 1 to point 3
        n3(int)-This item applies when MeshType = 1. It is the number of objects created along the edge of the
            meshed solid object that runs from point 1 to point 5
        MaxSize1(float)-This item applies when MeshType = 2. It is the maximum size of objects created along the
            edge of the meshed solid object that runs from point 1 to point 2. [L] If this item is input as 0, the
            default value is used. The default value is 48 inches if the database units are English or 120 centimeters
            if the database units are metric
        MaxSize2(float)-This item applies when MeshType = 2. It is the maximum size of objects created along the edge
            of the meshed solid object that runs from point 1 to point 3. [L] If this item is input as 0, the default
            value is used. The default value is 48 inches if the database units are English or 120 centimeters if the
            database units are metric.
        MaxSize3(float)-This item applies when MeshType = 2. It is the maximum size of objects created along the edge
            of the meshed solid object that runs from point 1 to point 5. [L] If this item is input as 0, the default
            value is used. The default value is 48 inches if the database units are English or 120 centimeters if the
            database units are metric.
        RestraintsOnEdge(bool)-If this item is True, and if both points along an edge of the original solid object have
            the same restraint/constraint, then, if the an added point on that edge and the original corner points have
            the same local axes definition, the program assigns the restraint/constraint to the added point
        RestraintsOnFace(bool)-If this item is True, and if all corner points on an solid object face have the same
            restraint/constraint, then, if an added point on that face and the original corner points for the face
            have the same local axes definition, the program assigns the restraint/constraint to the added point.
        """
        result=self.SapModel.SolidObj.GetAutoMesh(name)
        return result

    def assign_SolidObj_GetEdgeConstraint(self,name):
        """
        ---This function retrieves the generated edge constraint assignments to solid objects---
        inputs:
        name(str)-The name of an existing solid object
        return:
        [index,ConstraintExists]

        ConstraintExists(bool)-This item is True if an automatic edge constraint is generated by the
            program for the solid object in the analysis model
        """
        result=self.SapModel.SolidObj.GetEdgeConstraint(name)
        return result

    def assign_SolidObj_GetElm(self,Name):
        """
        ---This function retrieves the names of the solid elements (analysis model solid) associated with a
        specified solid object in the object-based model
        ---
        inputs:
        Name(str)-The name of an existing solid object
        return:
        [index,nelm,Elm]

        nelm(int)-The number of solid elements created from the specified solid object
        Elm(str list)-An array that includes the name of a solid element created from the specified solid object
        """
        result=self.SapModel.SolidObj.GetElm(Name)
        return result

    def assign_SolidObj_GetGroupAssign(self,Name):
        """
        ---This function retrieves the names of the groups to which a specified solid object is assigned---
        inputs:
        Name(str)-The name of an existing solid object
        return:
        [index,NumberGroups,Groups]

        NumberGroups(int)-The number of group names retrieved
        Groups(str list)-The names of the groups to which the solid object is assigned
        """
        result=self.SapModel.SolidObj.GetGroupAssign(Name)
        return result

    def assign_SolidObj_GetLoadGravity(self,Name):
        """
        ---This function retrieves the gravity load assignments to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,SolidName,LoadPat,CSys,x,y,z]

        NumberItems(int)-The total number of gravity loads retrieved for the specified solid objects
        SolidName(str list)-This is an array that includes the name of the solid object associated with each gravity load
        LoadPat(str list)-This is an array that includes the name of the coordinate system in which the gravity load
            multipliers are specified
        CSys(str list)-This is an array that includes the name of the coordinate system associated with each gravity load
        x,y,z(float list)-These are arrays of gravity load multipliers in the x, y and z directions of the specified
            coordinate system
        """
        result=self.SapModel.SolidObj.GetLoadGravity(Name)
        return result

    def assign_SolidObj_GetLoadPorePressure(self,Name):
        """
        ---This function retrieves the pore pressure load assignments to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,SolidName,LoadPat,Value,PatternName]

        NumberItems(int)-The total number of pore pressure loads retrieved for the specified solid objects
        SolidName(str list)-This is an array that includes the name of the solid object associated with each pore pressure load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each pore pressure load
        Value(float list)-This is an array that includes the pore pressure load value. [F/L2]
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the pore
            pressure load
        """
        result=self.SapModel.SolidObj.GetLoadPorePressure(Name)
        return result

    def assign_SolidObj_GetLoadStrain(self,Name):
        """
        ---This function retrieves the strain load assignments to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,SolidName,LoadPat,Component,Value,PatternName]

        NumberItems(int)-The total number of strain loads retrieved for the specified solid objects
        SolidName(str list)-This is an array that includes the name of the solid object associated with each strain load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each strain load
        Component(int)-This is 1, 2, 3, 4, 5 or 6, indicating the component to which the strain load is applied.
            1 = Strain11,2 = Strain22,3 = Strain33,4 = Strain12,5 = Strain13,6 = Strain23
        Value(float list)-This is an array that includes the strain value. [L/L]
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the strain load
        """
        result=self.SapModel.SolidObj.GetLoadStrain(Name)
        return result

    def assign_SolidObj_GetLoadSurfacePressure(self,Name):
        """
        ---This function retrieves the surface pressure load assignments to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,SolidName,LoadPat,Face,Value,PatternName]

        NumberItems(int)-The total number of surface pressure loads retrieved for the specified solid objects
        SolidName(str list)-This is an array that includes the name of the solid object associated with each surface pressure load.
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each surface pressure load
        Face(int list)-This is an array that includes 1, 2, 3, 4, 5 or 6, indicating the solid object face to which the
            specified load assignment applies
        Value(float list)-This is an array that includes the surface pressure load value. [F/L2]
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the
            surface pressure load
        """
        result=self.SapModel.SolidObj.GetLoadSurfacePressure(Name)
        return result

    def assign_SolidObj_GetLoadTemperature(self,Name):
        """
        ---This function retrieves the temperature load assignments to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,SolidName,LoadPat,Value,PatternName]

        NumberItems(int)-The total number of temperature loads retrieved for the specified solid objects
        SolidName(str list)-This is an array that includes the name of the solid object associated with each temperature load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each temperature load
        Value(float list)-This is an array that includes the temperature load value. [T]
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the temperature load
        """
        result=self.SapModel.SolidObj.GetLoadTemperature(Name)
        return result

    def assign_SolidObj_GetLocalAxes(self,Name):
        """
        ---This function retrieves the local axes angles for a solid object---
        inputs:
        Name(str)-The name of an existing solid object
        return:
        [index,a,b,c,Advanced]

        a,b,c(float)-The local axes of the solid object are defined by first setting the positive local 1, 2 and 3
            axes the same as the positive global X, Y and Z axes and then doing the following: [deg]
            1.Rotate about the 3 axis by angle a.
            2.Rotate about the resulting 2 axis by angle b.
            3.Rotate about the resulting 1 axis by angle c.
        Advanced(bool)-This item is True if the solid object local axes orientation was obtained using advanced
            local axes parameters
        """
        result=self.SapModel.SolidObj.GetLocalAxes(Name)
        return result

    def assign_SolidObj_GetMatTemp(self,Name):
        """
        ---This function retrieves the material temperature assignments to solid objects---
        inputs:
        Name(str)-The name of an existing solid object
        return:
        [index,Temp,PatternName]

        Temp(float)-This is the material temperature value assigned to the solid object. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the material temperature
            for the solid object is uniform over the object at the value specified by Temp.If PatternName is the name
            of a defined joint pattern, the material temperature for the solid object may vary. The material temperature
            at each corner point of the solid object is equal to the specified temperature multiplied by the pattern value
            at the associated point object. The material temperature at other points in the solid object is calculated by
            interpolation from the corner points.
        """
        result=self.SapModel.SolidObj.GetMatTemp(Name)
        return result

    def assign_SolidObj_GetNameList(self):
        """
        ---This function retrieves the names of all defined solid objects---
        return:
        [index,NumberNames,MyName]

        NumberNames(int)-The number of solid object names retrieved by the program
        MyName(str list)-This is a one-dimensional array of solid object names
        """
        result=self.SapModel.SolidObj.GetNameList()
        return result

    def assign_SolidObj_GetPoints(self,Name):
        """
        ---This function retrieves the names of the corner point objects of a solid object---
        inputs:
        Name(str)-The name of a defined solid object
        return:
        [index,Point]

        Point(str list)-This is an array containing the names of the corner point objects of the solid object
        """
        result=self.SapModel.SolidObj.GetPoints(Name)
        return result

    def assign_SolidObj_GetProperty(self,Name):
        """
        ---This function retrieves the solid property assigned to a solid object---
        inputs:
        Name(str)-The name of a defined solid object
        return:
        [index,PropName]

        PropName(str)-The name of the solid property assigned to the solid object
        """
        result=self.SapModel.SolidObj.GetProperty(Name)
        return result

    def assign_SolidObj_GetSpring(self,Name):
        """
        ---This function retrieves the spring assignments to a solid object face---
        inputs:
        Name(str)-The name of an existing solid object
        return:
        [index,NumberSprings,MyType,s,SimpleSpringType,LinkProp,Face,SpringLocalOneType,Dir,Outward,VecX,
        VecY,VecZ,CSys,Ang]

        NumberSprings(int)-The number of springs assignments made to the specified solid object
        MyType(int)-This is either 1 or 2, indicating the spring property type.
            1 = Simple spring,2 = Link property
        s(float)-The simple spring stiffness per unit area of the specified solid object face. This item applies
            only when MyType = 1. [F/L3]
        SimpleSpringType(int)-This is 1, 2 or 3, indicating the simple spring type. This item applies only when MyType = 1.
            1 = Spring resists tension and compression
            2 = Spring resists compression only
            3 = Spring resists tension only
        LinkProp(str)-The name of the link property assigned to the spring. This item applies only when MyType = 2
        Face(int)-This is 1, 2, 3, 4, 5 or 6, indicating the solid object face to which the specified spring assignment applies
        SpringLocalOneType(int)-This is 1, 2 or 3, indicating the method used to specify the spring positive local 1-axis
            orientation.
            1 = Parallel to solid object local axis
            2 = Normal to specified solid object face
            3 = User specified direction vector
        Dir(int)-This is 1, 2, 3, -1, -2 or -3, indicating the solid object local axis that corresponds to the
            positive local 1-axis of the spring. This item applies only when SpringLocalOneType = 1.
        Outward(bool)-This item is True if the spring positive local 1 axis is outward from the specified solid object
            face. This item applies only when SpringLocalOneType = 2.
        VecX(float list)-Each value in this array is the X-axis or solid object local 1-axis component (depending on
            the CSys specified) of the user specified direction vector for the spring local 1-axis. The direction
            vector is in the coordinate system specified by the CSys item. This item applies only when the corresponding
            SpringLocalOneType = 3.
        VecY(float list)-Each value in this array is the Y-axis or solid object local 2-axis component (depending on
            the CSys specified) of the user specified direction vector for the spring local 1-axis. The direction
            vector is in the coordinate system specified by the CSys item. This item applies only when the corresponding
            SpringLocalOneType = 3.
        VecZ(float list)-Each value in this array is the X-axis or solid object local 3-axis component (depending on the
            CSys specified) of the user specified direction vector for the spring local 1-axis. The direction vector is
            in the coordinate system specified by the CSys item. This item applies only when the corresponding SpringLocalOneType = 3.
        CSys(str)-This is Local (meaning the solid object local coordinate system) or the name of a defined coordinate
            system. This item is the coordinate system in which the user specified direction vector, Vec, is specified.
            This item applies only when SpringLocalOneType = 3
        Ang(float)-This is the angle that the link local 2-axis is rotated from its default orientation.
            This item applies only when MyType = 2. [deg]
        """
        result=self.SapModel.SolidObj.GetSpring(Name)
        return result

    def assign_SolidObj_GetTransformationMatrix(self,Name):
        """
        ---The function returns zero if the solid object transformation matrix is successfully retrieved---
        inputs:
        Name(str)-The name of an existing solid object
        return:
        [index,Value]

        Value(float list)-Value is an array of nine direction cosines that define the transformation matrix.The following
            matrix equation shows how the transformation matrix is used to convert items from the solid object local
            coordinate system to the global coordinate system.In the equation, c0 through c8 are the nine values from
            the transformation array, (Local1, Local2, Local3) are an item (such as a load) in the object local coordinate
            system, and (GlobalX, GlobalY, GlobalZ) are the same item in the global coordinate system.The transformation
            from the local coordinate system to the present coordinate system is the same as that shown above for the global
            system if you substitute the present system for the global system.
        """
        result=self.SapModel.SolidObj.GetTransformationMatrix(Name)
        return result

    def assign_LinkObj_AddByCoord(self,xi,yi,zi,xj,yj,zj,IsSingleJoint=False,PropName="Default",
                                  UserName="",CSys="Global"):
        """
        ---This function adds a new link object whose end points are at the specified coordinates---
        inputs:
        xi,yi,zi(float)-The coordinates of the I-End of the added link object. The coordinates are in the coordinate
            system defined by the CSys item
        xj,yj,zj(float)-The coordinates of the J-End of the added link object. The coordinates are in the coordinate
            system defined by the CSys item
        IsSingleJoint(bool)-This item is True if a one-joint link is added and False if a two-joint link is added
        PropName(str)-This is either Default or the name of a defined link property.If it is Default the program
            assigns a default link property to the link object. If it is the name of a defined link property, that
            property is assigned to the link object
        UserName(str)-This is an optional user specified name for the link object. If a UserName is specified and
            that name is already used for another link object, the program ignores the UserName
        CSys(str)-The name of the coordinate system in which the link object end point coordinates are defined
        """
        #This is the name that the program ultimately assigns for the link object. If no UserName is specified,
        # the program assigns a default name to the link object. If a UserName is specified and that name is not
        # used for another link object, the UserName is assigned to the link object; otherwise a default name is
        # assigned to the link object
        Name=""
        self.SapModel.LinkObj.AddByCoord(xi,yi,zi,xj,yj,zj,Name,IsSingleJoint,PropName,UserName,CSys)

    def assign_LinkObj_AddByPoint(self,Point1,Point2,IsSingleJoint=False,PropName="Default",UserName=""):
        """
        ---This function adds a new link object whose end points are specified by name---
        inputs:
        Point1(str)-The name of a defined point object at the I-End of the added link object
        Point2(str)-The name of a defined point object at the J-End of the added link object.
            This item is ignored if the IsSingleJoint item is True
        IsSingleJoint(bool)-This item is True if a one-joint link is added and False if a two-joint link is added
        PropName(str)-This is either Default or the name of a defined link property.If it is Default the program
            assigns a default link property to the link object. If it is the name of a defined link property, that
            property is assigned to the link object
        UserName(str)-This is an optional user specified name for the link object. If a UserName is specified and
            that name is already used for another link object, the program ignores the UserName
        """
        # This is the name that the program ultimately assigns for the link object. If no UserName is specified,
        # the program assigns a default name to the link object. If a UserName is specified and that name is not
        # used for another link object, the UserName is assigned to the link object; otherwise a default name is
        # assigned to the link object
        Name = ""
        self.SapModel.LinkObj.AddByPoint(Point1,Point2,Name,IsSingleJoint,PropName,UserName)

    def assign_LinkObj_Count(self):
        """
        ---This function returns a count of the link objects in the model---
        """
        result=self.SapModel.LinkObj.Count()
        return result

    def assign_LinkObj_SetGroupAssign(self,Name,GroupName,Remove=False,itemType=0):
        """
        ---This function adds or removes link objects from a specified group---
        inputs:
        Name(str)-The name of an existing link object or group, depending on the value of the ItemType item
        GroupName(str)-The name of an existing group to which the assignment is made
        Remove(bool)-If this item is False, the specified link objects are added to the group specified by the
            GroupName item. If it is True, the link objects are removed from the group
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.LinkObj.SetGroupAssign(Name,GroupName,Remove,itemType)

    def assign_LinkObj_SetLoadDeformation(self,Name,LoadPat,DOF,d,itemType=0):
        """
        ---This function assigns deformation loads to link objects---
        inputs:
        Name(str)-The name of an existing link object or group, depending on the value of the ItemType item
        LoadPat(int)-This is one(str)-The name of a defined load pattern
        DOF(bool list)-This is a array of boolean values indicating if the considered degree of freedom has a deformation load.
            DOF(1) = U1,DOF(2) = U2,DOF(3) = U3,DOF(4) = R1,DOF(5) = R2,DOF(6) = R3
        d(float list)-This is a array of deformation load values. The deformations specified for a given degree of
            freedom are applied only if the corresponding DOF item for that degree of freedom is True.
            d(1) = U1 deformation [L]
            d(2) = U2 deformation [L]
            d(3) = U3 deformation [L]
            d(4) = R1 deformation [rad]
            d(5) = R2 deformation [rad]
            d(6) = R3 deformation [rad]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.LinkObj.SetLoadDeformation(Name,LoadPat,DOF,d,itemType)

    def assign_LinkObj_SetLoadGravity(self,Name,LoadPat,x,y,z,Replace=True,CSys="Global",itemType=0):
        """
        ---This function assigns gravity load multipliers to link objects---
        inputs:
        Name(str)-The name of an existing link object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        x,y,z(float)-These are the gravity load multipliers in the x, y and z directions of the specified coordinate system
        Replace(bool)-If this item is True, all previous gravity loads, if any, assigned to the specified link object(s),
            in the specified load pattern, are deleted before making the new assignment
        CSys(str)-The coordinate system in which the x, y and z multipliers are specified
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.LinkObj.SetLoadGravity(Name,LoadPat,x,y,z,Replace,CSys,itemType)

    def assign_LinkObj_SetLoadTargetForce(self,Name,LoadPat,DOF,f,RD,itemType=0):
        """
        ---This function assigns target forces to frame objects---
        inputs:
        Name(str)-The name of an existing link object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        DOF(float list)-This is a array of boolean values indicating if the considered degree of freedom has a target force.
            DOF(1) = P,DOF(2) = V2,DOF(3) = V3,DOF(4) = T,DOF(5) = M2,DOF(6) = M3
        f(float list)-This is a array of target force values. The target forces specified for a given degree of freedom
            are applied only if the corresponding DOF item for that degree of freedom is True.
            f(1) = P [F]
            f(2) = V2 [F]
            f(3) = V3 [F]
            f(4) = T [FL]
            f(5) = M2 [FL]
            f(6) = M3 [FL]
        RD(float list)-This is a array of relative distances along the link objects where the target force values apply.
            The relative distances specified for a given degree of freedom are applicable only if the corresponding DOF
            item for that degree of freedom is True. The relative distance must be between 0 and 1, 0 <= RD <=1.
            RD(1) = relative location for P target force
            RD(2) = relative location for V2 target force
            RD(3) = relative location for V3 target force
            RD(4) = relative location for T target force
            RD(5) = relative location for M2 target force
            RD(6) = relative location for M3 target force
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.LinkObj.SetLoadTargetForce(Name,LoadPat,DOF,f,RD,itemType)

    def assign_LinkObj_SetLocalAxes(self,Name,Ang,itemType=0):
        """
        ---This function assigns a local axis angle to link objects---
        inputs:
        Name(str)-The name of an existing link object or group, depending on the value of the ItemType item
        Ang(float)-This is the angle that the local 2 and 3 axes are rotated about the positive local 1 axis,
            from the default orientation or, if the Advanced item is True, from the orientation determined
            by the plane reference vector. The rotation for a positive angle appears counter clockwise when
            the local +1 axis is pointing toward you. [deg]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.LinkObj.SetLocalAxes(Name,Ang,itemType)

    def assign_LinkObj_SetProperty(self,Name,PropName,itemType=0):
        """
        ---This function assigns a link property to link objects---
        inputs:
        Name(str)-The name of an existing link object or group, depending on the value of the ItemType item
        PropName(str)-This is the name of a link property to be assigned to the specified link object(s).
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.LinkObj.SetProperty(Name,PropName,itemType)

    def assign_LinkObj_SetPropertyFD(self,Name,PropName,itemType=0):
        """
        ---This function assigns a frequency dependent link property to link objects---
        inputs:
        Name(str)-The name of an existing link object or group, depending on the value of the ItemType item
        PropName(str)-This is either None or the name of a frequency dependent link property to be assigned to the
            specified link object(s). None means that no frequency dependent link property is assigned to the link object
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.SapModel.LinkObj.SetPropertyFD(Name,PropName,itemType)

    def assign_LinkObj_GetElm(self,Name):
        """
        ---This function retrieves the name of the link element (analysis model link) associated with a specified
        link object in the object-based model
        ---
        inputs:
        Name(str)-The name of an existing link object
        return:
        [index,Elm]

        Elm(str)-The name of the link element created from the specified link object
        """
        result=self.SapModel.LinkObj.GetElm(Name)
        return result

    def assign_LinkObj_GetGroupAssign(self,Name):
        """
        ---This function retrieves the names of the groups to which a specified link object is assigned---
        inputs:
        Name(str)-The name of an existing link object
        return:
        [index,NumberGroups,Groups]

        NumberGroups(int)-The number of group names retrieved
        Groups(str list)-The names of the groups to which the link object is assigned
        """
        result=self.SapModel.LinkObj.GetGroupAssign(Name)
        return result

    def assign_LinkObj_GetLoadDeformation(self,Name):
        """
        ---This function retrieves the deformation load assignments to link objects---
        inputs:
        Name(str)-The name of an existing link object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,LinkName,LoadPat,dof1,dof2,dof3,dof4,dof5,dof6,U1,U2,U3,R1,R2,R3,itemType=0]

        NumberItems(int)-The total number of deformation loads retrieved for the specified link objects
        LinkName(str list)-This is an array that includes the name of the link object associated with each deformation load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each deformation load
        dof1,dof2,dof3,dof4,dof5,dof6(bool)-These are arrays of boolean values, indicating if the considered degree of
            freedom has a deformation load.
            dof1 = U1
            dof2 = U2
            dof3 = U3
            dof4 = R1
            dof5 = R2
            dof6 = R3
        U1,U2,U3,R1,R2,R3(float)-These are arrays of deformation load values. The deformations specified for a given
            degree of freedom are applicable only if the corresponding DOF item for that degree of freedom is True.
            U1 = U1 deformation [L]
            U2 = U2 deformation [L]
            U3 = U3 deformation [L]
            R1 = R1 deformation [rad]
            R2 = R2 deformation [rad]
            R3 = R3 deformation [rad]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        result=self.SapModel.LinkObj.GetLoadDeformation(Name)
        return result

    def assign_LinkObj_GetLoadGravity(self,Name):
        """
        ---This function retrieves the gravity load assignments to link objects---
        inputs:
        Name(str)-The name of an existing link object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,LinkName,LoadPat,CSys,x,y,z]

        NumberItems(int)-The total number of gravity loads retrieved for the specified link objects
        LinkName(str list)-This is an array that includes the name of the link object associated with each gravity load.
        LoadPat(str list)-This is an array that includes the name of the coordinate system in which the gravity load
            multipliers are specified
        CSys(str list)-This is an array that includes the name of the coordinate system associated with each gravity load
        x,y,z(float)-These are arrays of gravity load multipliers in the x, y and z directions of the specified coordinate system
        """
        result=self.SapModel.LinkObj.GetLoadGravity(Name)
        return result

    def assign_LinkObj_GetLoadTargetForce(self,Name):
        """
        ---This function retrieves the target force assignments to link objects---
        inputs:
        Name(str)-The name of an existing link object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,LinkName,LoadPat,dof1,dof2,dof3,dof4,dof5,dof6,P,V2,V3,T,M2,M3,T1,T2,T3,T4,T5,T6]

        NumberItems(int)-The total number of deformation loads retrieved for the specified link objects
        LinkName(str)-This is an array that includes the name of the link object associated with each target force
        LoadPat(str)-This is an array that includes the name of the load pattern associated with each target force
        dof1,dof2,dof3,dof4,dof5,dof6(bool)-These are arrays of boolean values indicating if the considered degree of
            freedom has a target force assignment.
            dof1 = P
            dof2 = V2
            dof3 = V3
            dof4 = T
            dof5 = M2
            dof6 = M3
        P,V2,V3,T,M2,M3(float)-These are arrays of target force values. The target forces specified for a given
            degree of freedom are applicable only if the corresponding DOF item for that degree of freedom is True.
            U1 = U1 deformation [L]
            U2 = U2 deformation [L]
            U3 = U3 deformation [L]
            R1 = R1 deformation [rad]
            R2 = R2 deformation [rad]
            R3 = R3 deformation [rad]
        T1,T2,T3,T4,T5,T6(float)-These are arrays of the relative distances along the link objects where the target
            force values apply. The relative distances specified for a given degree of freedom are applicable only
            if the corresponding dofn item for that degree of freedom is True.
            T1 = relative location for P target force
            T2 = relative location for V2 target force
            T3 = relative location for V3 target force
            T4 = relative location for T target force
            T5 = relative location for M2 target force
            T6 = relative location for M3 target force
        """
        result=self.SapModel.LinkObj.GetLoadTargetForce(Name)
        return result

    def assign_LinkObj_GetLocalAxes(self,Name):
        """
        ---This function retrieves the local axis angle assignment for link objects---
        inputs:
        Name(str)-The name of an existing link object
        return:
        [index,Ang,Advanced]

        Ang(float)-This is the angle that the local 2 and 3 axes are rotated about the positive local 1 axis, from the
            default orientation or, if the Advanced item is True, from the orientation determined by the plane reference
            vector. The rotation for a positive angle appears counter clockwise when the local +1 axis is pointing toward
            you. [deg]
        Advanced(bool)-This item is True if the link object local axes orientation was obtained using advanced local axes parameters
        """
        result=self.SapModel.LinkObj.GetLocalAxes(Name)
        return result

    def assign_LinkObj_GetNameList(self):
        """
        ---This function retrieves the names of all defined link objects---
        return:
        [index,NumberNames,MyName]

        NumberNames(int)-The number of link object names retrieved by the program
        MyName(str list)-This is a one-dimensional array of link object names
        """
        result=self.SapModel.LinkObj.GetNameList()
        return result

    def assign_LinkObj_GetPoints(self,Name):
        """
        ---This function retrieves the names of the point objects at each end of a specified link object---
        inputs:
        Name(str)-The name of a defined link object
        return:
        [index,Point1,Point2]

        Point1(str)-The name of the point object at the I-End of the specified link object
        Point2(str)-The name of the point object at the J-End of the specified link object
        """
        result=self.SapModel.LinkObj.GetPoints(Name)
        return result

    def assign_LinkObj_GetProperty(self,Name):
        """
        ---This function retrieves the link property assigned to a link object---
        inputs:
        Name(str)-The name of a defined link object
        return:
        [index,PropName]

        PropName(str)-The name of the link property assigned to the link object
        """
        result=self.SapModel.LinkObj.GetProperty(Name)
        return result

    def assign_LinkObj_GetPropertyFD(self,Name):
        """
        ---This function retrieves the frequency dependent link property assigned to a link object---
        inputs:
        Name(str)-The name of a defined link object
        return:
        [index,PropName]

        PropName(str)-The name of the frequency dependent link property assigned to the link object. This item is
            None if there is no frequency dependent link property assigned to the link object
        """
        result=self.SapModel.LinkObj.GetPropertyFD(Name)
        return result

    def assign_LinkObj_GetTransformationMatrix(self,Name):
        """
        ---The function returns zero if the link object transformation matrix is successfully retrieved;
        otherwise it returns a nonzero value
        ---
        inputs:
        Name(str)-The name of an existing link object
        return:
        [index,Value]

        Value(float list)-Value is an array of nine direction cosines that define the transformation matrix.The following
            matrix equation shows how the transformation matrix is used to convert items from the link object local
            coordinate system to the global coordinate system.In the equation, c0 through c8 are the nine values from
            the transformation array, (Local1, Local2, Local3) are an item (such as a load) in the object local coordinate
            system, and (GlobalX, GlobalY, GlobalZ) are the same item in the global coordinate system.The transformation
            from the local coordinate system to the present coordinate system is the same as that shown above for the global
            system if you substitute the present system for the global system.
        """
        result=self.SapModel.LinkObj.GetTransformationMatrix(Name)
        return result

    def analyze_CreateAnalysisModel(self):
        """
        ---This function creates the analysis model. If the analysis model is already created and current, nothing is done.
        The function returns zero if the analysis model is successfully created or it already exists and is current,
        otherwise it returns a nonzero value.It is not necessary to call this function before running an analysis.
        The analysis model is automatically created, if necessary, when the model is run
        ---
        """
        self.SapModel.Analyze.CreateAnalysisModel()

    def analyze_SetActiveDOF(self,DOF):
        """
        ---This function sets the model global degrees of freedom---
        inputs:
        DOF(bool list)-This is an array of 6 boolean values, indicating if the specified model global
            degree of freedom is active.
            DOF(0) = UX,DOF(1) = UY,DOF(2) = UZ,DOF(3) = RX,DOF(4) = RY,DOF(5) = RZ
        """
        self.SapModel.Analyze.SetActiveDOF(DOF)

    def analyze_SetRunCaseFlag(self,Name,Run,All=False):
        """
        ---This function sets the run flag for load cases---
        inputs:
        Name(str)-The name of an existing load case that is to have its run flag set
        Run(bool)-If this item is True, the specified load case is to be run
        All(bool)-If this item is True, the run flag is set as specified by the Run item for all load cases,
            and the Name item is ignored
        """
        self.SapModel.Analyze.SetRunCaseFlag(Name,Run,All)

    def analyze_SetSolverOption_2(self,SolverType,SolverProcessType,NumberParallelRuns,StiffCase):
        """
        ---This function sets the model solver options---
        inputs:
        SoverType(int)-This is 0, 1 or 2, indicating the solver type.
            0 = Standard solver
            1 = Advanced solver
            2 = Multi-threaded solver
        SolverProcessType(int)-This is 0, 1 or 2, indicating the process the analysis is run.
            0 = Auto (program determined)
            1 = GUI process
            2 = Separate process
        NumberParallelRuns(int)-This is an integer between -8 and 8, inclusive, not including -1.
            -8 to -2 = Auto parallel (use up to all physical cores - max 8). Treated the same as 0.
            -1 = Illegal value; will return an error.
            0 = Auto parallel (use up to all physical cores).
            1 = Serial.
            2 to 8 = User defined parallel (use up to this fixed number of cores - max 8).
        StiffCase(str)-The name of the load case used when outputting the mass and stiffness matrices to
            text files If this item is blank, no matrices are output
        """
        self.SapModel.Analyze.SetSolverOption_2(SolverType,SolverProcessType,NumberParallelRuns,StiffCase)

    def analyze_MergeAnalysisResults(self,FileName):
        """
        ---See “Merging Analysis Results” section in program help file for requirements and limitations.
        The analysis model is automatically created as part of this function.
        The function returns zero if analysis results are successfully merged, otherwise it returns a nonzero value.
        IMPORTANT NOTE: Your model must have a file path defined before merging analysis results. If the model is
        opened from an existing file, a file path is defined. If the model is created from scratch, the File.Save
        function must be called with a file name before merging analysis results. Saving the file creates the file path.
        ---
        inputs:
        FileName(str)-The full path of a model file from which the analysis results are to be merged
        """
        self.SapModel.Analyze.MergeAnalysisResults(FileName)

    def analyze_ModifyUnDeformedGeometry(self,CaseName,SF,Stage=-1,Original=False):
        """
        ---This function modifies the undeformed geometry based on displacements obtained from a specified load case---
        inputs:
        CaseName(str)-The name of the static load case from which displacements are obtained
        SF(float)-The scale factor applied to the displacements
        Stage(int)-This item applies only when the specified load case is a staged construction load case. It is the
            stage number from which the displacements are obtained. Specifying a -1 for this item means to use the last run stage
        Original(bool)-If this item is True, all other input items in this function are ignored and the original
            undeformed geometry data is reinstated
        """
        self.SapModel.Analyze.ModifyUnDeformedGeometry(CaseName,SF,Stage,Original)

    def analyze_RunAnalysis(self):
        """
        ---This function runs the analysis. The analysis model is automatically created as part of this function.
        The function returns zero if the analysis model is successfully run, otherwise it returns a nonzero value.
        IMPORTANT NOTE: Your model must have a file path defined before running the analysis. If the model is opened
        from an existing file, a file path is defined. If the model is created from scratch, the File.Save function
        must be called with a file name before running the analysis. Saving the file creates the file path.
        ---
        """
        self.SapModel.Analyze.RunAnalysis()

    def analyze_ModifyUnDeformedGeometryModeShape(self,CaseName,Mode,MaxDisp,Direction,Original=False):
        """
        ---This function modifies the undeformed geometry based on the shape of a specified mode from a specified
        modal or buckling load case
        ---
        inputs:
        CaseName(str)-The name of a modal or buckling load case
        Mode(int)-The mode shape to consider
        MaxDisp(float)-The maximum displacement to which the mode shape will be scaled
        Direction(int)-The direction in which to apply the geometry modification
        Original(bool)-If this item is True, all other input items in this function are ignored and
            the original undeformed geometry data is reinstated
        """
        self.SapModel.Analyze.ModifyUndeformedGeometryModeShape(CaseName,Mode,MaxDisp,Direction,Original)

    def analyze_GetActiveDOF(self):
        """
        ---This function retrieves the model global degrees of freedom---
        return:
        [index,DOF]

        DOF(bool list)-This is an array of 6 boolean values, indicating if the specified model global degree of
            freedom is active.
            DOF(0) = UX
            DOF(1) = UY
            DOF(2) = UZ
            DOF(3) = RX
            DOF(4) = RY
            DOF(5) = RZ
        """
        result=self.SapModel.Analyze.GetActiveDOF()
        return result

    def analyze_GetCaseStatus(self):
        """
        ---This function retrieves the status for all load cases---
        return:
        [index,NumberItems,CaseName,Status]

        NumberItems(int)-The number of load cases for which the status is reported
        CaseName(str list)-This is an array that includes the name of each analysis case for which the status is reported
        Status(int list)-This is an array of that includes 1, 2, 3 or 4, indicating the load case status.
            1 = Not run
            2 = Could not start
            3 = Not finished
            4 = Finished
        """
        result=self.SapModel.Analyze.GetCaseStatus()
        return result

    def analyze_GetRunCaseFlag(self):
        """
        ---This function retrieves the run flags for all analysis cases---
        return:
        [index,NumberItems,CaseName,Run]

        NumberItems(int)-The number of load cases for which the run flag is reported
        CaseName(str list)-This is an array that includes the name of each analysis case for which the run flag is reported
        Run(bool list)-This is an array of boolean values indicating if the specified load case is to be run
        """
        result=self.SapModel.Analyze.GetRunCaseFlag()
        return result

    def analyze_GetSolverOption_2(self):
        """
        ---This function retrieves the model solver options---
        return:
        [index,SoverType,SolverProcessType,NumberParallelRuns,StiffCase]

        SoverType(int)-This is 0, 1 or 2, indicating the solver type.
            0 = Standard solver
            1 = Advanced solver
            2 = Multi-threaded solver
        SolverProcessType(int)-This is 0, 1 or 2, indicating the process the analysis is run.
            0 = Auto (program determined)
            1 = GUI process
            2 = Separate process
        NumberParallelRuns(int)-This is an integer between -8 and 8, inclusive, not including -1.
            -8 to -2 = Auto parallel (use up to all physical cores - max 8). Treated the same as 0.
            -1 = Illegal value; will return an error.
            0 = Auto parallel (use up to all physical cores).
            1 = Serial.
            2 to 8 = User defined parallel (use up to this fixed number of cores - max 8).
        StiffCase(str)-The name of the load case used when outputting the mass and stiffness matrices to
            text files If this item is blank, no matrices are output
        """
        result=self.SapModel.Analyze.GetSolverOption_2()
        return result

    def results_Setup_SelectAllSectionCutsForOutput(self,Selected):
        """
        ---This function selects or deselects all section cuts for output.The function returns 0 if the selected flag
        is successfully set, otherwise it returns nonzero.Please note that all section cuts are, by default, selected
        for output when they are created
        ---
        inputs:
        Selected(bool)-This item is True if all section cuts are to be selected for output, or False if no section
            cuts are to be selected for output
        """
        self.SapModel.Results.Setup.SelectAllSectionCutsForOutput(Selected)

    def results_Setup_DeselectAllCasesAndCombosForOutput(self):
        """
        ---The function deselects all load cases and response combinations for output---
        """
        self.SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()

    def results_Setup_SetCaseSelectedForOutput(self,Name,Selected=True):
        """
        ---This function sets an load case selected for output flag---
        inputs:
        Name(str)-The name of an existing load case
        Selected(bool)-This item is True if the specified load case is to be selected for output, otherwise it is False
        """
        self.SapModel.Results.Setup.SetCaseSelectedForOutput(Name,Selected)

    def results_Setup_SetComboSelectedForOutput(self,Name,Selected=True):
        """
        ---This function sets a load combination selected for output flag---
        inputs:
        Name(str)-The name of an existing load combination
        Selected(bool)-This item is True if the specified load combination is to be selected for output, otherwise it is False
        """
        self.SapModel.Results.Setup.SetComboSelectedForOutput(Name,Selected)

    def results_Setup_SetOptionBaseReactLoc(self,gx,gy,gz):
        """
        ---This function sets the global coordinates of the location at which the base reactions are reported---
        inputs:
        gx,gy,gz(float)-The global coordinates of the location at which the base reactions are reported
        """
        self.SapModel.Results.Setup.SetOptionBaseReactLoc(gx,gy,gz)

    def results_Setup_SetOptionBucklingMode(self,BuckModeStart,BuckModeEnd,BuckModeAll=False):
        """
        ---This function sets the buckling modes for which buckling factors are reported---
        inputs:
        BuckModeStart(int)-The first buckling mode for which the buckling factor is reported when the BuckModeAll item is False
        BuckModeEnd(int)-The last buckling mode for which the buckling factor is reported when the BuckModeAll item is False
        BuckModeAll(bool)-If this item is True, buckling factors are reported for all calculated buckling modes.
            If it is False, buckling factors are reported for the buckling modes indicated by the BuckModeStart and BuckModeEnd items
        """
        self.SapModel.Results.Setup.SetOptionBucklingMode(BuckModeStart,BuckModeEnd,BuckModeAll)

    def results_Setup_SetOptionDirectHist(self,Value):
        """
        ---This function sets the output option for direct history results---
        inputs:
        Value(int)-This item is 1, 2 or 3
            1 = Envelopes
            2 = Step-by-Step
            3 = Last Step
        """
        self.SapModel.Results.Setup.SetOptionDirectHist(Value)

    def results_Setup_SetOptionModalHist(self,Value):
        """
        ---This function sets the output option for modal history results---
        inputs:
        Value(int)-This item is 1, 2 or 3
            1 = Envelopes
            2 = Step-by-Step
            3 = Last Step
        """
        self.SapModel.Results.Setup.SetOptionModalHist(Value)

    def results_Setup_SetOptionModeShape(self,ModeShapeStart,ModeShapeEnd,ModeShapesAll=False):
        """
        ---This function sets the modes for which mode shape results are reported---
        inputs:
        ModeShapeStart(int)-The first mode for which results are reported when the ModeShapesAll item is False
        ModeShapeEnd(int)-The last mode for which results are reported when the ModeShapesAll item is False
        ModeShapesAll(bool)-If this item is True, results are reported for all calculated modes. If it is False,
            results are reported for the modes indicated by the ModeShapeStart and ModeShapeEnd items
        """
        self.SapModel.Results.Setup.SetOptionModeShape(ModeShapeStart,ModeShapeEnd,ModeShapesAll)

    def results_Setup_SetOptionMultiStepStatic(self,Value):
        """
        ---This function sets the output option for multistep static linear results---
        inputs:
        Value(int)-This item is 1, 2 or 3
            1 = Envelopes
            2 = Step-by-Step
            3 = Last Step
        """
        self.SapModel.Results.Setup.SetOptionMultiStepStatic(Value)

    def results_Setup_SetOptionMultiValuedCombo(self,Value):
        """
        ---This function sets the output option for multi-valued load combination results---
        inputs:
        Value(int)-This item is either 1, 2, or 3.
            1 = Envelopes
            2 = Multiple values, if possible
            3 = Correspondence
        """
        self.SapModel.Results.Setup.SetOptionMultiValuedCombo(Value)

    def results_Setup_SetOptionNLStatic(self,Value):
        """
        ---This function sets the output option for nonlinear static results---
        inputs:
        Value(int)-This item is 1, 2 or 3
            1 = Envelopes
            2 = Step-by-Step
            3 = Last Step
        """
        self.SapModel.Results.Setup.SetOptionNLStatic(Value)

    def results_Setup_SetOptionPSD(self,Value):
        """
        ---This function sets the output option for power spectral density results---
        inputs:
        Value(int)-This item is either 1 or 2
            1 = RMS
            2 = sqrt(PSD)
        """
        self.SapModel.Results.Setup.SetOptionPSD(Value)

    def results_Setup_SetOptionSteadyState(self,Value,SteadyStateOption):
        """
        ---This function sets the output option for steady state results---
        inputs:
        Value(int)-This item is either 1 or 2
            1 = Envelopes
            2 = At Frequencies
        SteadyStateOption(int)-This item is 1, 2 or 3
            1 = In and Out of Phase
            2 = Magnitude
            3 = All
        """
        self.SapModel.Results.Setup.SetOptionSteadyState(Value,SteadyStateOption)

    def results_Setup_SetSectionCutSelectedForOutput(self,Name,Selected):
        """
        ---This function selects or deselects a defined section cut for output---
        inputs:
        Name(str)-The name of a defined section cut
        Selected(bool)-This item is True if the section cut is to be selected for output, or False if no section
            cut should not be selected for output
        """
        self.SapModel.Results.Setup.SetSectionCutSelectedForOutput(Name,Selected)

    def results_Setup_GetCaseSelectedForOutput(self,Name):
        """
        ---This function checks if an load case is selected for output---
        inputs:
        Name(str)-The name of an existing load case
        return:
        [index,Selected]

        Selected(bool)-This item is True if the specified load case is selected for output
        """
        result=self.SapModel.Results.Setup.GetCaseSelectedForOutput(Name)
        return result

    def results_Setup_GetComboSelectedForOutput(self,Name):
        """
        ---This function checks if a load combination is selected for output---
        inputs:
        Name(str)-The name of an existing load combination
        return:
        [index,Selected]
        Selected(bool)-This item is True if the specified load combination is selected for output
        """
        result=self.SapModel.Results.Setup.GetComboSelectedForOutput(Name)
        return result

    def results_Setup_GetOptionBaseReactLoc(self):
        """
        ---This function retrieves the global coordinates of the location at which the base reactions are reported---
        return:
        [index,gx,gy,gz]

        gx,gy,gz(float)-The global coordinates of the location at which the base reactions are reported
        """
        result=self.SapModel.Results.Setup.GetOptionBaseReactLoc()
        return result

    def results_Setup_GetOptionBucklingMode(self):
        """
        ---This function retrieves the buckling modes for which buckling factors are reported---
        return:
        [index,BuckModeStart,BuckModeEnd,BuckModeAll]

        BuckModeStart(int)-The first buckling mode for which the buckling factor is reported when the BuckModeAll item is False
        BuckModeEnd(int)-The last buckling mode for which the buckling factor is reported when the BuckModeAll item is False
        BuckModeAll(bool)-If this item is True, buckling factors are reported for all calculated buckling modes.
            If it is False, buckling factors are reported for the buckling modes indicated by the BuckModeStart and BuckModeEnd items
        """
        result=self.SapModel.Results.Setup.GetOptionBucklingMode()
        return result

    def results_Setup_GetOptionDirectHist(self):
        """
        ---This function retrieves the output option for direct history results---
        return:
        [index,Value]

        Value(int)-This item is either 1, 2 or 3
            1 = Envelopes
            2 = Step-by-Step
            3 = Last Step
        """
        result=self.SapModel.Results.Setup.GetOptionDirectHist()
        return result

    def results_Setup_GetOptionModalHist(self):
        """
        ---This function retrieves the output option for modal history results---
        return:
        [index,Value]

        Value(int)-This item is either 1, 2 or 3
            1 = Envelopes
            2 = Step-by-Step
            3 = Last Step
        """
        result=self.SapModel.Results.Setup.GetOptionModalHist()
        return result

    def results_Setup_GetOptionModeShape(self):
        """
        ---This function retrieves the modes for which mode shape results are reported---
        return:
        [index,ModeShapeStart,ModeShapeEnd,ModeShapesAll]

        ModeShapeStart(int)-The first mode for which results are reported when the ModeShapesAll item is False
        ModeShapeEnd(int)-The last mode for which results are reported when the ModeShapesAll item is False
        ModeShapesAll(bool)-If this item is True, results are reported for all calculated modes. If it is False,
            results are reported for the modes indicated by the ModeShapeStart and ModeShapeEnd items
        """
        result=self.SapModel.Results.Setup.GetOptionModeShape()
        return result

    def results_Setup_GetOptionMultiStepStatic(self):
        """
        ---This function retrieves the output option for multistep static linear results---
        return:
        [index,Value]

        Value(int)-This item is either 1, 2 or 3
            1 = Envelopes
            2 = Step-by-Step
            3 = Last Step
        """
        result=self.SapModel.Results.Setup.GetOptionMultiStepStatic()
        return result

    def results_Setup_GetOptionMultiValuedCombo(self):
        """
        ---This function retrieves the output option for multi-valued load combination results---
        return:
        [index,Value]

        Value(int)-This item is either 1, 2, or 3
            1 = Envelopes
            2 = Multiple values, if possible
            3 = Correspondence
        """
        result=self.SapModel.Results.Setup.GetOptionMultiValuedCombo()
        return result

    def results_Setup_GetOptionNLStatic(self):
        """
        ---This function retrieves the output option for nonlinear static results---
        return:
        [index,Value]

        Value(int)-This item is either 1, 2 or 3
            1 = Envelopes
            2 = Step-by-Step
            3 = Last Step
        """
        result=self.SapModel.Results.Setup.GetOptionNLStatic()
        return result

    def results_Setup_GetOptionPSD(self):
        """
        ---This function retrieves the output option for power spectral density results---
        return:
        [index,Value]

        Value(int)-This item is either 1 or 2
            1 = RMS
            2 = sqrt(PSD)
        """
        result=self.SapModel.Results.Setup.GetOptionPSD()
        return result

    def results_Setup_GetOptionSteadyState(self):
        """
        ---This function retrieves the output option for steady state results---
        return:
        [index,Value,SteadyStateOption]

        Value(int)-This item is either 1 or 2
            1 = Envelopes
            2 = At Frequencies
        SteadyStateOption(int)-This item is 1, 2 or 3
            1 = In and Out of Phase
            2 = Magnitude
            3 = All
        """
        result=self.SapModel.Results.Setup.GetOptionSteadyState()
        return result

    def results_Setup_GetSectionCutSelectedForOutput(self,Name):
        """
        ---This function retrieves whether a defined section cut is selected for output---
        inputs:
        Name(str)-The name of a defined section cut
        return:
        [index,Selected]

        Selected(bool)-This item is True if the section cut is to be selected for output, or False if the section cut
            is not selected for output
        """
        result=self.SapModel.Results.Setup.GetSectionCutSelectedForOutput(Name)
        return result

    def results_AreaForceShell(self,Name,itemTypeElm=0):
        """
        ---This function reports the area forces for the specified area elements that are assigned shell section
        properties (not plane or asolid properties). Note that the forces reported are per unit of in-plane length
        ---
        inputs:
        Name(str)-The name of an existing area object, area element or group of objects, depending on the value of the
            ItemTypeElm item
        itemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the area elements corresponding to the area object
            specified by the Name item.
            If this item is Element, the result request is for the area element specified by the Name item.
            If this item is GroupElm, the result request is for the area elements corresponding to all area objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for area elements corresponding to all selected area
            objects, and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,F11,F22,F12,FMax,Fmin,FAngle,FVM,M11,
        M22,M12,MMax,MMin,MAngle,V13,V23,VMax,VAngle]
        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the area object name associated with each result, if any
        Elm(str list)-This is an array that includes the area element name associated with each result
        PointElm(str list)-This is an array that includes the name of the point element where the results are reported
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated
            with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        F11(float list)-The area element internal F11 membrane direct force per length reported in the area element
            local coordinate system. [F/L]
        F22(float list)-The area element internal F22 membrane direct force per length reported in the area element
            local coordinate system. [F/L]
        F12(float list)-The area element internal F12 membrane shear force per length reported in the area element
            local coordinate system. [F/L]
        FMax(float list)-The maximum principal membrane force per length. [F/L]
        FMin(float list)-The minimum principal membrane force per length. [F/L]
        FAngle(float list)-The angle measured counter clockwise (when the local 3 axis is pointing toward you) from
            the area local 1 axis to the direction of the maximum principal membrane force. [deg]
        FVM(float list)-The area element internal Von Mises membrane force per length. [F/L]
        M11(float list)-The area element internal M11 plate bending moment per length reported in the area element
            local coordinate system. This item is only reported for area elements with properties that allow plate
            bending behavior. [FL/L]
        M22(float list)-The area element internal M22 plate bending moment per length reported in the area element
            local coordinate system. This item is only reported for area elements with properties that allow plate
            bending behavior. [FL/L]
        M12(float list)-The area element internal M12 plate twisting moment per length reported in the area element
            local coordinate system. This item is only reported for area elements with properties that allow plate
            bending behavior. [FL/L]
        MMax(float list)-The maximum principal plate moment per length. This item is only reported for area elements
            with properties that allow plate bending behavior. [FL/L]
        MMin(float list)-The minimum principal plate moment per length. This item is only reported for area elements
            with properties that allow plate bending behavior. [FL/L]
        MAngle(float list)-The angle measured counter clockwise (when the local 3 axis is pointing toward you) from
            the area local 1 axis to the direction of the maximum principal plate moment. This item is only reported
            for area elements with properties that allow plate bending behavior. [deg]
        V13(float list)-The area element internal V13 plate transverse shear force per length reported in the area
            element local coordinate system. This item is only reported for area elements with properties that
            allow plate bending behavior. [F/L]
        V23(float list)-The area element internal V23 plate transverse shear force per length reported in the area
            element local coordinate system. This item is only reported for area elements with properties that
            allow plate bending behavior. [F/L]
        VMax(float list)-The maximum plate transverse shear force. It is equal to the square root of the sum of the
            squares of V13 and V23. This item is only reported for area elements with properties that allow plate
            bending behavior. [F/L]
        VAngle(float list)-The angle measured counter clockwise (when the local 3 axis is pointing toward you) from
            the area local 1 axis to the direction of Vmax. This item is only reported for area elements with properties
            that allow plate bending behavior. [deg]
        """
        result=self.SapModel.Results.AreaForceShell(Name,itemTypeElm)
        return result

    def results_AreaJointForcePlane(self,Name,ObjectElm=0):
        """
        ---This function reports the area joint forces for the point elements at each corner of the specified plane
        elements that have plane-type or asolid-type properties (not shell).
        ---
        inputs:
        Name(str)-The name of an existing area object, area element or group of objects depending on the value of the
            ItemTypeElm item
        ObjectElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the plane elements corresponding to the area object
            specified by the Name item.
            If this item is Element, the result request is for the plane element specified by the Name item.
            If this item is GroupElm, the result request is for the plane elements corresponding to all area objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for plane elements corresponding to all selected area
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,F1,F2,F3,M1,M2,M3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the area object name associated with each result, if any
        Elm(str list)-This is an array that includes the plane element name associated with each result
        PointElm(str list)-This is an array that includes the point element name associated with each result.
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        F1,F2,F3(float list)-These are one dimensional arrays that include the joint force components in the
            point element local axes directions. [F]
        M1,M2,M3(float list)-These are one dimensional arrays that include the joint moment components about
            the point element local axes. [FL]
        """
        result=self.SapModel.Results.AreaJointForcePlane(Name,ObjectElm)
        return result

    def results_AreaJointForceShell(self,Name,ItemTypeElm=0):
        """
        ---This function reports the area joint forces for the point elements at each corner of the specified area
        elements that have shell-type properties (not plane or asolid).
        ---
        inputs:
        Name(str)-The name of an existing area object, area element or group of objects, depending on the value of
            the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the area elements corresponding to the area object
            specified by the Name item.
            If this item is Element, the result request is for the area element specified by the Name item.
            If this item is GroupElm, the result request is for the area elements corresponding to all area objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for area elements corresponding to all selected area
            objects and the Name item is ignored
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,F1,F2,F3,M1,M2,M3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the area object name associated with each result, if any
        Elm(str list)-This is an array that includes the area element name associated with each result
        PointElm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        F1,F2,F3(float list)-These are one dimensional arrays that include the joint force components in the point
            element local axes directions. [F]
        M1,M2,M3(float list)-These are one dimensional arrays that include the joint moment components about the
            point element local axes. [FL]
        """
        result=self.SapModel.Results.AreaJointForceShell(Name,ItemTypeElm)
        return result

    def results_AreaStrainShell(self,Name,ItemTypeElm=0):
        """
        ---This function reports the area strains for the specified area elements that are assigned shell section
        properties (not plane or asolid properties). Strains are reported at each point element associated with
        the area element
        ---
        inputs:
        Name(str)-The name of an existing area object, area element or group of objects, depending on the value of
            the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the area elements corresponding to the area
            object specified by the Name item.
            If this item is Element, the result request is for the area element specified by the Name item.
            If this item is GroupElm, the result request is for the area elements corresponding to all area objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for area elements corresponding to all selected area
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,E11Top,E22Top,G12Top,E11Bot,E22Bot,G12Bot,
        EMaxTop,EMinTop,EMaxBot,EMinBot,EAngleTop,EAngleBot,EVMTop,EVMBot,G13Avg,G23Avg,GMaxAvg,GAngleAvg]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the area object name associated with each result, if any
        Elm(str list)-This is an array that includes the area element name associated with each result
        PointElm(str list)-This is an array that includes the name of the point element where the results are reported
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        E11Top,E22Top,G12Top,E11Bot,E22Bot,G12Bot(float)-The area element internal E11, E22 and G12 strains, at the
            top or bottom of the specified area element, at the specified point element location, reported in the
            area element local coordinate system
        EMaxTop,EMinTop,EMaxBot,EMinBot(float)-The area element maximum and minimum principal strains, at the top or
            bottom of the specified area element, at the specified point element location
        EAngleTop,EAngleBot(float)-The angle measured counter clockwise (when the local 3 axis is pointing toward
            you) from the area local 1 axis to the direction of the maximum principal strain, at the top or bottom
            of the specified area element. [deg]
        EVMTop,EVMBot(float)-The area element internal top or bottom Von Mises strain at the specified point element
        G13Avg,G23Avg(float)-The area element average G13 or G23 out-of-plane shear strain at the specified point
            element. These items are only reported for area elements with properties that allow plate bending behavior
        GMaxAvg(float)-The area element maximum average out-of-plane shear strain. It is equal to the square root
            of the sum of the squares of G13Avg and G23Avg. This item is only reported for area elements with properties
            that allow plate bending behavior
        GAngleAvg(float)-The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the
            area local 1 axis to the direction of GMaxAvg. This item is only reported for area elements with
            properties that allow plate bending behavior. [deg]
        """
        result=self.SapModel.Results.AreaStrainShell(Name,ItemTypeElm)
        return result

    def results_Setup_AreaStrainShellLayered(self,Name,ItemTypeElm=0):
        """
        ---This function reports the area strains for the specified area elements that are assigned layered shell
        section properties
        ---
        inputs:
        Name(str)-The name of an existing area object, area element or group of objects, depending on the value
            of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the area elements corresponding to the area object
            specified by the Name item.
            If this item is Element, the result request is for the area element specified by the Name item.
            If this item is GroupElm, the result request is for the area elements corresponding to all area objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for area elements corresponding to all selected area
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,Layer,IntPtNum,IntPtLoc,PointElm,LoadCase,StepType,StepNum,E11,E22,G12,EMax,
        EMin,EAngle,EVM,G13Avg,G23Avg,GMaxAvg,GangleAvg]
        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the area object name associated with each result, if any
        Elm(str list)-This is an array that includes the area element name associated with each result
        Layer(str list)-This is an array that includes the layer name associated with each result
        IntPtNum(int list)-This is an array that includes the integration point number within the specified layer of
            the area element
        IntPtLoc(float list)-This is an array that includes the integration point relative location within the specified
            layer of the area element. The location is between -1 (bottom of layer) and +1 (top of layer), inclusive. The
            midheight of the layer is at a value of 0
        PointElm(str list)-This is an array that includes the name of the point element where the results are reported
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated
            with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        E11,E22,G12(float list)-The area element internal E11, E22 and G12 strains, at the specified point element
            location, for the specified layer and layer integration point, reported in the area element local coordinate system
        EMax,EMin(float)-The area element maximum and minimum principal strains, at the specified point element location,
            for the specified layer and layer integration point
        EAngle(float)-The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the area
            local 1 axis to the direction of the maximum principal strain. [deg
        EVM(float)-The area element internal Von Mises strain at the specified point element location, for the specified
            layer and layer integration point
        G13Avg,G23Avg(float)-The area element average G13 or G23 out-of-plane shear strain at the specified point element
            location, for the specified layer and layer integration point
        GMaxAvg(float)-The area element maximum average out-of-plane shear strain for the specified layer and layer
            integration point. It is equal to the square root of the sum of the squares of G13Avg and G23Avg
        GAngleAvg(float)-The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the area
            local 1 axis to the direction of GMaxAvg. [deg]
        """
        result=self.SapModel.Results.AreaStrainShellLayered(Name,ItemTypeElm)
        return result

    def results_AreaStressPlane(self,Name,ItemTypeElm=0):
        """
        ---This function reports the stresses for the specified plane elements that are assigned plane or asolid
        section properties (not shell properties).
        ---
        inputs:
        Name(str)-The name of an existing area object, area element or group of objects, depending on the value
            of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the plane elements corresponding to the area object
            specified by the Name item.
            If this item is Element, the result request is for the plane element specified by the Name item.
            If this item is GroupElm, the result request is for the plane elements corresponding to all area objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for plane elements corresponding to all selected area
            objects, and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,S11,S22,S33,S12,SMax,SMin,SAngle,SVM]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the area object name associated with each result, if any
        Elm(str list)-This is an array that includes the plane element name associated with each result
        PointElm(str list)-This is an array that includes the name of the point element where the results are reported
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        S11,S22,S33,S12(float)-The plane element internal S11, S22, S33 and S12 stresses, at the specified point
            element location, reported in the area element local coordinate system. [F/L2]
        SMax,SMin(float)-The plane element maximum and minimum principal stresses at the specified point element location. [F/L2]
        SAngle(float)-The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the
            plane element local 1 axis to the direction of the maximum principal stress. [deg]
        SVM(float)-The plane element internal Von Mises stress at the specified point element. [F/L2]
        """
        result=self.SapModel.Results.AreaStressPlane(Name,ItemTypeElm)
        return result

    def results_AreaStressShell(self,Name,ItemTypeElm=0):
        """
        ---This function reports the area stresses for the specified area elements that are assigned shell section
        properties (not plane or asolid properties). Stresses are reported at each point element associated with
        the area element
        ---
        inputs:
        Name(str)-The name of an existing area object, area element or group of objects, depending on the value of
            the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the area elements corresponding to the area object
            specified by the Name item.
            If this item is Element, the result request is for the area element specified by the Name item.
            If this item is GroupElm, the result request is for the area elements corresponding to all area objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for area elements corresponding to all selected area
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,S11Top,S22Top,S12Top,S11Bot,S22Bot,S12Bot,
        SMaxTop,SMinTop,SMaxBot,SMinBot,SAngleTop,SAngleBot,SVMTop,SVMBot,S13Avg,S23Avg,SMaxAvg,SAngleAvg]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the area object name associated with each result, if any
        Elm(str list)-This is an array that includes the area element name associated with each result
        PointElm(str list)-This is an array that includes the name of the point element where the results are reported
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated
            with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        S11Top,S22Top,S12Top,S11Bot,S22Bot,S12Bot(float)-The area element internal S11, S22 and S12 stresses, at
            the top or bottom of the specified area element, at the specified point element location, reported in
            the area element local coordinate system. [F/L2]
        SMaxTop,SMinTop,SMaxBot,SMinBot(float)-The area element maximum and minimum principal stresses, at the top or
            bottom of the specified area element, at the specified point element location. [F/L2]
        SAngleTop,SAngleBot(float)-The angle measured counter clockwise (when the local 3 axis is pointing toward you)
            from the area local 1 axis to the direction of the maximum principal stress, at the top or bottom of the
            specified area element. [deg]
        SVMTop,SVMBot(float)-The area element internal top or bottom Von Mises stress at the specified point element. [F/L2]
        S13Avg,S23Avg(float)-The area element average S13 or S23 out-of-plane shear stress at the specified point element.
            These items are only reported for area elements with properties that allow plate bending behavior. [F/L2]
        SMaxAvg(float)-The area element maximum average out-of-plane shear stress. It is equal to the square root of
            the sum of the squares of S13Avg and S23Avg. This item is only reported for area elements with properties
            that allow plate bending behavior. [F/L2]
        SAngleAvg(float)-The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the
            area local 1 axis to the direction of SMaxAvg. This item is only reported for area elements with properties
            that allow plate bending behavior. [deg]
        """
        result=self.SapModel.Results.AreaStressShell(Name,ItemTypeElm)
        return result

    def results_AreaStressShellLayered(self,Name,ItemTypeElm=0):
        """
        ---This function reports the area stresses for the specified area elements that are assigned layered shell
        section properties
        ---
        inputs:
        Name(str)-The name of an existing area object, area element or group of objects, depending on the value of the
            ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the area elements corresponding to the area object
            specified by the Name item.
            If this item is Element, the result request is for the area element specified by the Name item.
            If this item is GroupElm, the result request is for the area elements corresponding to all area objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for area elements corresponding to all selected area
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,Layer,IntPtNum,IntPtLoc,PointElm,LoadCase,StepType,StepNum,S11,S22,S12,SMax,SMin,
        SAngle,SVM,S13Avg,S23Avg,SMaxAvg,SAngleAvg]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the area object name associated with each result, if any
        Elm(str list)-This is an array that includes the area element name associated with each result
        Layer(str list)-This is an array that includes the layer name associated with each result
        IntPtNum(int list)-This is an array that includes the integration point number within the specified
            layer of the area element
        IntPtLoc(float list)-This is an array that includes the integration point relative location within the
            specified layer of the area element. The location is between -1 (bottom of layer) and +1 (top of layer),
            inclusive. The midheight of the layer is at a value of 0
        PointElm(str list)-This is an array that includes the name of the point element where the results are reported
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated
            with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        S11,S22,S12(float)-The area element internal S11, S22 and S12 stresses, at the specified point element
            location, for the specified layer and layer integration point, reported in the area element local
            coordinate system. [F/L2]
        SMax,SMin(float)-The area element maximum and minimum principal stresses, at the specified point element
            location, for the specified layer and layer integration point. [F/L2]
        SAngle(float)-The angle measured counter clockwise (when the local 3 axis is pointing toward you) from
            the area local 1 axis to the direction of the maximum principal stress. [deg]
        SVM(float)-The area element internal Von Mises stress at the specified point element location, for the
            specified layer and layer integration point. [F/L2]
        S13Avg,S23Avg(float)-The area element average S13 or S23 out-of-plane shear stress at the specified point
            element location, for the specified layer and layer integration point. [F/L2]
        SMaxAvg(float)-The area element maximum average out-of-plane shear stress for the specified layer and layer
            integration point. It is equal to the square root of the sum of the squares of S13Avg and S23Avg. [F/L2]
        SAngleAvg(float)-The angle measured counter clockwise (when the local 3 axis is pointing toward you) from
            the area local 1 axis to the direction of SMaxAvg. [deg]
        """
        result=self.SapModel.Results.AreaStressShellLayered(Name,ItemTypeElm)
        return result

    def results_AssembledJointMass_1(self,MassSourceName,Name,itemTypeElm):
        """
        ---This function reports the assembled joint masses for the specified point elements---
        inputs:
        MassSourceName(str)-The name of an existing mass source definition. If this value is left empty or
            unrecognized, data for all mass sources will be returned
        Name(str)-The name of an existing point element or group of objects, depending on the value of the ItemTypeElm item
        itemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the point element corresponding to the point
            object specified by the Name item.
            If this item is Element, the result request is for the point element specified by the Name item.
            If this item is GroupElm, the result request is for all point elements directly or indirectly specified
            in the group specified by the Name item.
            If this item is SelectionElm, the result request is for all point elements directly or indirectly
            selected and the Name item is ignored.
        return:
        [index,NumberResults,PointElm,MassSource,U1,U2,U3,R1,R2,R3]

        NumberResults(int)-The total number of results returned by the program
        PointElm(str list)-This is an array that includes the point element name associated with each result
        MassSource(str list)-This is an array that includes the mass source name associated with each result
        U1,U2,U3(float)-These are one dimensional arrays that include the translational mass in the point
            element local 1, 2 and 3 axes directions, respectively, for each result. [M]
        R1,R2,R3(float)-These are one dimensional arrays that include the rotational mass moment of inertia
            about the point element local 1, 2 and 3 axes, respectively, for each result. [ML2]
        """
        result=self.SapModel.Results.AssembledJointMass_1(MassSourceName,Name,itemTypeElm)
        return result

    def results_BaseReact(self):
        """
        ---This function reports the structure total base reactions---
        return:
        [index,NumberResults,LoadCase,StepType,StepNum,FX,Fy,Fz,Mx,My,Mz,gx,gy,gz]

        NumberResults(int)-The total number of results returned by the program
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated with each resul
        StepType(str list)-This is an array that includes the step type, if any, for each result.
        StepNum(int)-This is an array that includes the step number, if any, for each result
        Fx,Fy,Fz(float list)-These are one dimensional arrays that include the base reaction forces in the global
            X, Y and Z directions, respectively, for each result. [F]
        Mx,My,Mz(float list)-These are one dimensional arrays that include the base reaction moments about the global
            X, Y and Z axes, respectively, for each result. [FL]
        gx,gy,gz(float)-These are the global X, Y and Z coordinates of the point at which the base reactions are reported. [L]
        """
        result=self.SapModel.Results.BaseReact()
        return result

    def results_BaseReactWithCentroid(self):
        """
        ---This function reports the structure total base reactions and includes information on the centroid of the
        translational reaction forces
        ---
        return:
        [index,NumberResults,LoadCase,StepType,StepNum,Fx,Fy,Fz,Mx,My,Mz,gx,gy,gz,XCentroidForFx,YCentroidForFx,
        ZCentroidForFx,XCentroidForFy,YCentroidForFy,ZCentroidForFy,XCentroidForFz,YCentroidForFz,ZCentroidForFz]

        NumberResults(int)-The total number of results returned by the program
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int)-This is an array that includes the step number, if any, for each result
        Fx,Fy,Fz(float list)-These are one dimensional arrays that include the base reaction forces in the global
            X, Y and Z directions, respectively, for each result. [F]
        Mx,My,Mz(float list)-These are one dimensional arrays that include the base reaction moments about the global
            X, Y and Z axes, respectively, for each result. [FL]
        gx,gy,gz(float)-These are the global X, Y and Z coordinates of the point at which the base reactions are reported. [L]
        XCentroidForFx,YCentroidForFx,ZCentroidForFx(float list)-These are arrays of the global X, Y and Z coordinates,
            respectively, of the centroid of all global X-direction translational reaction forces for each result
        XCentroidFforFy,YCentroidForFy,ZCentroidForFy(float list)-These are arrays of the global X, Y and Z coordinates,
            respectively, of the centroid of all global Y-direction translational reaction forces for each result
        XCentroidForFz,YCentroidForFz,ZCentroidForFz(float list)-These are arrays of the global X, Y and Z coordinates,
            respectively, of the centroid of all global Z-direction translational reaction forces for each result
        """
        result=self.SapModel.Results.BaseReactWithCentroid()
        return result

    def results_BucklingFactor(self):
        """
        ---This function reports buckling factors obtained from buckling load cases---
        return:
        [index,NumberResults,LoadCase,StepType,StepNum,Factor]

        NumberResults(int)-The total number of results returned by the program
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated with each result
        StepType(str list)-This is an array that includes the step type for each result. For buckling factors, the step type is always Mode
        StepNum(int list)-This is an array that includes the step number for each result. For buckling factors,
            the step number is always the buckling mode number
        Factor(float list)-This is an array that includes the buckling factors
        """
        result=self.SapModel.Results.BucklingFactor()
        return result

    def results_FrameForce(self,Name,ItemTypeElm=0):
        """
        ---This function reports the frame forces for the specified line elements---
        return:
        [index,NumberResults,Obj,ObjSta,Elm,ElmSta,LoadCase,StepType,StepNum,P,V2,V3,T,M2,M3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the line object name associated with each result, if any
        ObjSta(float list)-This is an array that includes the distance measured from the I-end of the line object
            to the result location
        Elm(str list)-This is an array that includes the line element name associated with each result
        ElmSta(float list)-This is an array that includes the distance measured from the I-end of the line
            element to the result location
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        P,V2,V3(float list)-These are one dimensional arrays that include the axial force, shear force in the
            local 2 direction, and shear force in the local 3 direction, respectively, for each result. [F]
        T,M2,M3(float list)-These are one dimensional arrays that include the torsion, moment about the local 2axis,
            and moment about the local 3-axis, respectively, for each result. [FL]
        """
        result=self.SapModel.Results.FrameForce(Name,ItemTypeElm)
        return result

    def results_FrameJointForce(self,Name,ItemTypeElm=0):
        """
        ---This function reports the frame joint forces for the point elements at each end of the specified line elements---
        inputs:
        Name(str)-The name of an existing line object, line element or group of objects depending on the value of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the line elements corresponding to the line object
            specified by the Name item.
            If this item is Element, the result request is for the line element specified by the Name item.
            If this item is GroupElm, the result request is for the line elements corresponding to all line objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for line elements corresponding to all selected line
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,F1,F2,F3,M1,M2,M3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the line object name associated with each result, if any
        Elm(str list)-This is an array that includes the line element name associated with each result
        PointElm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        F1,F2,F3(float list)-These are one dimensional arrays that include the joint force components in the point
            element local axes directions. [F]
        M1,M2,M3(float list)-These are one dimensional arrays that include the joint moment components about the
            point element local axes. [FL]
        """
        result=self.SapModel.Results.FrameJointForce(Name,ItemTypeElm)
        return result

    def results_GeneralizedDispl(self,Name):
        """
        ---This function reports the displacement values for the specified generalized displacements---
        inputs:
        Name(str)-The name of an existing generalized displacement for which results are returned. If the program does
            not recognize this name as a defined generalized displacement, it returns results for all selected generalized
            displacements, if any. For example, entering a blank string (i.e., "") for the name will prompt the program
            to return results for all selected generalized displacements
        return:
        [index,NumberResults,GD,LoadCase,StepType,StepNum,DType,Value]

        NumberResults(int)-The total number of results returned by the program
        GD(str list)-This is an array that includes the generalized displacement name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        DType(str list)-This is an array that includes the generalized displacement type for each result.
            It is either Translation or Rotation
        Value(float list)-This is an array of the generalized displacement values for each result.[L] when DType is
            Translation , [rad] when DType is Rotation
        """
        result=self.SapModel.Results.GeneralizedDispl(Name)
        return result

    def results_JointAcc(self,Name,ItemTypeElm=0):
        """
        ---This function reports the joint accelerations for the specified point elements. The accelerations
        reported by this function are relative accelerations
        ---
        inputs:
        Name(str)-The name of an existing point object, point element, or group of objects,
            depending on the value of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the point element corresponding to the point
            object specified by the Name item.
            If this item is Element, the result request is for the point element specified by the Name item.
            If this item is GroupElm, the result request is for all point elements directly or indirectly specified in
            the group specified by the Name item.
            If this item is SelectionElm, the result request is for all point elements directly or indirectly selected
            and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,LoadCase,StepType,StepNum,U1,U2,U3,R1,R2,R3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the point object name associated with each result, if any.
            Some results will have no point object associated with them. For those cases, this item will be blank
        Elm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        U1,U2,U3(float list)-These are one dimensional arrays that include the translational acceleration in the point
            element local 1, 2 and 3 axes directions, respectively, for each result. [L/s2]
        R1,R2,R3(float list)-These are one dimensional arrays that include the rotational acceleration about the point
            element local 1, 2 and 3 axes, respectively, for each result. [rad/s2]
        """
        result=self.SapModel.Results.JointAcc(Name,ItemTypeElm)
        return result

    def results_JointAccAbs(self,Name,ItemTypeElm=0):
        """
        ---This function reports the joint absolute accelerations for the specified point elements. Absolute and
        relative accelerations are the same, except when reported for time history load cases subjected to acceleration
        loading
        ---
        inputs:
        Name(str)-The name of an existing point object, point element, or group of objects depending on the value
            of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the point element corresponding to the point object
            specified by the Name item.
            If this item is Element, the result request is for the point element specified by the Name item.
            If this item is GroupElm, the result request is for all point elements directly or indirectly specified in
            the group specified by the Name item.
            If this item is SelectionElm, the result request is for all point elements directly or indirectly selected
            and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,LoadCase,StepType,StepNum,U1,U2,U3,R1,R2,R3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the point object name associated with each result, if any.
            Some results will have no point object associated with them. For those cases, this item will be blank
        Elm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        U1,U2,U3(float list)-These are one dimensional arrays that include the translational acceleration in the point
            element local 1, 2 and 3 axes directions, respectively, for each result. [L/s2]
        R1,R2,R3(float list)-These are one dimensional arrays that include the rotational acceleration about the point
            element local 1, 2 and 3 axes, respectively, for each result. [rad/s2]
        """
        result=self.SapModel.Results.JointAccAbs(Name,ItemTypeElm)
        return result

    def results_JointDispl(self,Name,ItemTypeElm=0):
        """
        ---This function reports the joint displacements for the specified point elements. The displacements reported
        by this function are relative displacements
        ---
        inputs:
        Name(str)-The name of an existing point object, point element, or group of objects depending on the value
            of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the point element corresponding to the point object
            specified by the Name item.
            If this item is Element, the result request is for the point element specified by the Name item.
            If this item is GroupElm, the result request is for all point elements directly or indirectly specified in
            the group specified by the Name item.
            If this item is SelectionElm, the result request is for all point elements directly or indirectly selected
            and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,LoadCase,StepType,StepNum,U1,U2,U3,R1,R2,R3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the point object name associated with each result, if any.
            Some results will have no point object associated with them. For those cases, this item will be blank
        Elm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        U1,U2,U3(float list)-These are one dimensional arrays that include the displacement in the point element
            local 1, 2 and 3 axes directions, respectively, for each result. [L]
        R1,R2,R3(float list)-These are one dimensional arrays that include the rotation about the point element
            local 1, 2 and 3 axes, respectively, for each result. [rad]
        """
        result=self.SapModel.Results.JointDispl(Name,ItemTypeElm)
        return result

    def results_JointDisplAbs(self,Name,ItemTypeElm=0):
        """
        ---This function reports the absolute joint displacements for the specified point elements. Absolute and
        relative displacements are the same except when reported for time history load cases subjected to acceleration
        loading
        ---
        inputs:
        Name(str)-The name of an existing point object, point element, or group of objects depending on the value
            of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the point element corresponding to the point object
            specified by the Name item.
            If this item is Element, the result request is for the point element specified by the Name item.
            If this item is GroupElm, the result request is for all point elements directly or indirectly specified in
            the group specified by the Name item.
            If this item is SelectionElm, the result request is for all point elements directly or indirectly selected
            and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,LoadCase,StepType,StepNum,U1,U2,U3,R1,R2,R3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the point object name associated with each result, if any.
            Some results will have no point object associated with them. For those cases, this item will be blank
        Elm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        U1,U2,U3(float list)-These are one dimensional arrays that include the displacement in the point element
            local 1, 2 and 3 axes directions, respectively, for each result. [L]
        R1,R2,R3(float list)-These are one dimensional arrays that include the rotation about the point element
            local 1, 2 and 3 axes, respectively, for each result. [rad]
        """
        result=self.SapModel.Results.JointDisplAbs(Name,ItemTypeElm)
        return result

    def results_JointReact(self,Name,ItemTypeElm=0):
        """
        ---This function reports the joint reactions for the specified point elements. The reactions reported are from
        restraints, springs and grounded (one-joint) links---
        inputs:
        Name(str)-The name of an existing line object, line element or group of objects depending on the value of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the line elements corresponding to the line object
            specified by the Name item.
            If this item is Element, the result request is for the line element specified by the Name item.
            If this item is GroupElm, the result request is for the line elements corresponding to all line objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for line elements corresponding to all selected line
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,F1,F2,F3,M1,M2,M3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the line object name associated with each result, if any
        Elm(str list)-This is an array that includes the line element name associated with each result
        PointElm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        F1,F2,F3(float list)-These are one dimensional arrays that include the reaction forces in the point element
            local 1, 2 and 3 axes directions, respectively, for each result. [F]
        M1,M2,M3(float list)-These are one dimensional arrays that include the reaction moments about the point
            element local 1, 2 and 3 axes, respectively, for each result. [FL]
        """
        result=self.SapModel.Results.JointReact(Name,ItemTypeElm)
        return result

    def results_JointVel(self,Name,ItemTypeElm=0):
        """
        ---This function reports the joint velocities for the specified point elements. The velocities reported by
        this function are relative velocities
        ---
        inputs:
        Name(str)-The name of an existing point object, point element, or group of objects depending on the value
            of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the point element corresponding to the point object
            specified by the Name item.
            If this item is Element, the result request is for the point element specified by the Name item.
            If this item is GroupElm, the result request is for all point elements directly or indirectly specified in
            the group specified by the Name item.
            If this item is SelectionElm, the result request is for all point elements directly or indirectly selected
            and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,LoadCase,StepType,StepNum,U1,U2,U3,R1,R2,R3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the point object name associated with each result, if any.
            Some results will have no point object associated with them. For those cases, this item will be blank
        Elm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        U1,U2,U3(float list)-These are one dimensional arrays that include the translational velocity in the
            point element local 1, 2 and 3 axes directions, respectively, for each result. [L/s]
        R1,R2,R3(float list)-These are one dimensional arrays that include the rotational velocity about the
            point element local 1, 2 and 3 axes, respectively, for each result. [rad/s]
        """
        result=self.SapModel.Results.JointVel(Name,ItemTypeElm)
        return result

    def results_JointVelAbs(self,Name,ItemTypeElm=0):
        """
        ---This function reports the joint absolute velocities for the specified point elements. Absolute and
        relative velocities are the same, except when reported for time history load cases subjected to acceleration
        loading---
        inputs:
        Name(str)-The name of an existing point object, point element, or group of objects depending on the value
            of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the point element corresponding to the point object
            specified by the Name item.
            If this item is Element, the result request is for the point element specified by the Name item.
            If this item is GroupElm, the result request is for all point elements directly or indirectly specified in
            the group specified by the Name item.
            If this item is SelectionElm, the result request is for all point elements directly or indirectly selected
            and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,LoadCase,StepType,StepNum,U1,U2,U3,R1,R2,R3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the point object name associated with each result, if any.
            Some results will have no point object associated with them. For those cases, this item will be blank
        Elm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        U1,U2,U3(float list)-These are one dimensional arrays that include the translational velocity in the
            point element local 1, 2 and 3 axes directions, respectively, for each result. [L/s]
        R1,R2,R3(float list)-These are one dimensional arrays that include the rotational velocity about the
            point element local 1, 2 and 3 axes, respectively, for each result. [rad/s]
        """
        result=self.SapModel.Results.JointVelAbs(Name,ItemTypeElm)
        return result

    def results_LinkDeformation(self,Name,ItemTypeElm=0):
        """
        ---This function reports the link internal deformations---
        inputs:
        Name(str)-The name of an existing point object, point element, or group of objects depending on the value
            of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the point element corresponding to the point object
            specified by the Name item.
            If this item is Element, the result request is for the point element specified by the Name item.
            If this item is GroupElm, the result request is for all point elements directly or indirectly specified in
            the group specified by the Name item.
            If this item is SelectionElm, the result request is for all point elements directly or indirectly selected
            and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,LoadCase,StepType,StepNum,U1,U2,U3,R1,R2,R3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the point object name associated with each result, if any.
            Some results will have no point object associated with them. For those cases, this item will be blank
        Elm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        U1,U2,U3(float list)-These are one dimensional arrays that include the internal translational deformation
            of the link in the link element local axes directions. [L]
        R1,R2,R3(float list)-These are one dimensional arrays that include the internal rotational deformation
            of the link about the link element local axes. [rad]
        """
        result=self.SapModel.Results.LinkDeformation(Name,ItemTypeElm)
        return result

    def results_LinkForce(self,Name,ItemTypeElm=0):
        """
        ---This function reports the link forces at the point elements at the ends of the specified link elements---
        inputs:
        Name(str)-The name of an existing point object, point element, or group of objects depending on the value
            of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the point element corresponding to the point object
            specified by the Name item.
            If this item is Element, the result request is for the point element specified by the Name item.
            If this item is GroupElm, the result request is for all point elements directly or indirectly specified in
            the group specified by the Name item.
            If this item is SelectionElm, the result request is for all point elements directly or indirectly selected
            and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,P,V2,V3,T,M2,M3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the line object name associated with each result, if any
        Elm(str list)-This is an array that includes the line element name associated with each result
        PointElm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        P(float list)-This is an array that includes the link axial force (in the link local 1-axis direction)
            at the specified point element. [F]
        V2,V3(float list)-These are one dimensional arrays that include the link shear force components in the link
            element local axes directions. [F]
        T(float list)-This is an array that includes the link torsion (about the link local 1-axis) at the specified
            point element. [FL]
        M2,M3(float list)-These are one dimensional arrays that include the link moment components about the link
            element local axes. [FL]
        """
        result=self.SapModel.Results.LinkForce(Name,ItemTypeElm)
        return result

    def results_LinkJointForce(self,Name,ItemTypeElm=0):
        """
        ---This function reports the joint forces for the point elements at the ends of the specified link elements---
        inputs:
        Name(str)-The name of an existing line object, line element or group of objects depending on the value of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the line elements corresponding to the line object
            specified by the Name item.
            If this item is Element, the result request is for the line element specified by the Name item.
            If this item is GroupElm, the result request is for the line elements corresponding to all line objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for line elements corresponding to all selected line
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,F1,F2,F3,M1,M2,M3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the line object name associated with each result, if any
        Elm(str list)-This is an array that includes the line element name associated with each result
        PointElm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        F1,F2,F3(float list)-These are one dimensional arrays that include the joint force components in the point
            element local axes directions. [F]
        M1,M2,M3(float list)-These are one dimensional arrays that include the joint moment components about the
            point element local axes. [FL]
        """
        result=self.SapModel.Results.LinkJointForce(Name,ItemTypeElm)
        return result

    def results_ModalLoadParticipationRatios(self):
        """
        ---This function reports the modal load participation ratios for each selected modal analysis case---
        return:[index,NumberResults,LoadCase,ItemType,Item,Stat,Dyn]

        NumberResults(int)-The total number of results returned by the program
        LoadCase(str list)-This is an array that includes the name of the modal load case associated with each result
        ItemType(str list)-This is an array that includes Load Pattern, Acceleration, Link or Panel Zone. It specifies
            the type of item for which the modal load participation is reported.
        Item(str list)-This is an array whose values depend on the ItemType. If the ItemType is Load Pattern,
            this is the name of the load pattern.
            If the ItemType is Acceleration, this is UX, UY, UZ, RX, RY, or RZ, indicating the acceleration direction.
            If the ItemType is Link, this is the name of the link followed by U1, U2, U3, R1, R2, or R3 (in parenthesis),
            indicating the link degree of freedom for which the output is reported.
            If the ItemType is Panel Zone, this is the name of the joint to which the panel zone is assigned, followed
            by U1, U2, U3, R1, R2, or R3 (in parenthesis), indicating the degree of freedom for which the output is reported.

        Stat(float list)-This is an array that includes the percent static load participation ratio
        Dyn(float list)-This is an array that includes the percent dynamic load participation ratio
        """
        result=self.SapModel.Results.ModalLoadParticipationRatios()
        return result

    def results_Setup_ModalParticipatingMassRatios(self):
        """
        ---This function reports the modal participating mass ratios for each mode of each selected modal analysis case---
        return:
        [index,NumberResults,LoadCase,StepType,StepNum,Period,Ux,Uy,Uz,SumUx,SUmUy,SumUz,Rx,Ry,Rz,SumRx,SumRy,SumRz]

        NumberResults(int)-The total number of results returned by the program
        LoadCase(str list)-This is an array that includes the name of the modal load case associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result. For modal results, this will always be Mode
        StepNum(int list)-This is an array that includes the step number for each result. For modal results, this is always the mode number
        Period(float)-This is an array that includes the period for each result. [s]
        Ux(float list)-This is an array that includes the modal participating mass ratio for the structure Uy degree of
            freedom. The ratio applies to the specified mode.
        Uy(float list)-This is an array that includes the modal participating mass ratio for the structure Uy degree of
            freedom. The ratio applies to the specified mode.
        Uz(float list)-This is an array that includes the modal participating mass ratio for the structure Uz degree of
            freedom. The ratio applies to the specified mode
        SumUx(float list)-This is an array that includes the cumulative sum of the modal participating mass ratios for
            the structure Ux degree of freedom
        SumUy(float list)-This is an array that includes the cumulative sum of the modal participating mass ratios for
            the structure Uy degree of freedom
        SumUz(float list)-This is an array that includes the cumulative sum of the modal participating mass ratios for
            the structure Uz degree of freedom
        Rx(float list)-This is an array that includes the modal participating mass ratio for the structure Rx degree of
            freedom. The ratio applies to the specified mode
        Ry(float list)-This is an array that includes the modal participating mass ratio for the structure Ry degree of
            freedom. The ratio applies to the specified mode
        Rz(float list)-This is an array that includes the modal participating mass ratio for the structure Rz degree of
            freedom. The ratio applies to the specified mode
        SumRx(float list)-This is an array that includes the cumulative sum of the modal participating mass ratios for
            the structure Rx degree of freedom
        SumRy(float list)-This is an array that includes the cumulative sum of the modal participating mass ratios for
            the structure Ry degree of freedom
        SumRz(float list)-This is an array that includes the cumulative sum of the modal participating mass ratios for
            the structure Rz degree of freedom
        """
        result=self.SapModel.Results.ModalParticipatingMassRatios()
        return result

    def results_ModalParticipationFactors(self):
        """
        ---This function reports the modal participation factors for each mode of each selected modal analysis case---
        return:
        [index,NumberResults,LoadCase,StepType,StepNum,Period,Ux,Uy,Uz,Rx,Ry,Rz,ModalMass,ModalStiff]

        NumberResults(int)-The total number of results returned by the program
        LoadCase(str list)-This is an array that includes the name of the modal load case associated with each result.
        StepType(str list)-This is an array that includes the step type, if any, for each result. For modal results,
            this will always be Mode.
        StepNum(int list)-This is an array that includes the step number for each result. For modal results, this will
            always be the mode number.
        Period(float list)-This is an array that includes the period for each result. [s]
        Ux(float list)-This is an array that includes the modal participation factor for the structure Ux degree of
            freedom. The factor applies to the specified mode. [Fs2]
        Uy(float list)-This is an array that includes the modal participation factor for the structure Uy degree of
            freedom. The factor applies to the specified mode. [Fs2]
        Uz(float list)-This is an array that includes the modal participation factor for the structure Uz degree of
            freedom. The factor applies to the specified mode. [Fs2]
        Rx(float list)-This is an array that includes the modal participation factor for the structure Rx degree of
            freedom. The factor applies to the specified mode. [FLs2]
        Ry(float list)-This is an array that includes the modal participation factor for the structure Ry degree of
            freedom. The factor applies to the specified mode. [FLs2]
        Rz(float list)-This is an array that includes the modal participation factor for the structure Rz degree of
            freedom. The factor applies to the specified mode. [FLs2]
        ModalMass(float list)-This is an array that includes the modal mass for the specified mode.  This is a measure
            of the kinetic energy in the structure as it is deforming in the specified mode. [FLs2]
        ModalStiff(float list)-This is an array that includes the modal stiffness for the specified mode.  This is a
            measure of the strain energy in the structure as it is deforming in the specified mode. [FL]
        """
        result=self.SapModel.Results.ModalParticipationFactors()
        return result

    def results_ModalPeriod(self):
        """
        ---SapModel.Results.ModalPeriod(NumberResults, LoadCase, StepType, StepNum, Period, Frequency, CircFreq, EigenValue)---
        return:
        [index,NumberResults,LoadCase,StepType,StepNum,Period,Frequency,CricFreq,EigenValue]

        NumberResults(int)-The number total of results returned by the program
        LoadCase(str list)-This is an array that includes the name of the modal analysis case associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result. For modal results
            this is always be Mode
        StepNum(int list)-This is an array that includes the step number for each result. For modal results this is
            always the mode number
        Period(float list)-This is an array that includes the period for each result. [s]
        Frequency(float list)-This is an array that includes the cyclic frequency for each result. [1/s]
        CircFreq(float list)-This is an array that includes the circular frequency for each result. [rad/s]
        EigenValue(float list)-This is an array that includes the eigenvalue for the specified mode for each result. [rad2/s2]
        """
        result=self.SapModel.Results.ModalPeriod()
        return result

    def results_ModeShape(self,Name,ItemTypeElm=0):
        """
        ---This function reports the modal displacements (mode shapes) for the specified point elements---
        inputs:
        Name(str)-The name of an existing point element or group of objects, depending on the value of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the point element corresponding to the point object
                specified by the Name item.
            If this item is Element, the result request is for the point element specified by the Name item.
            If this item is GroupElm, the result request is for all point elements directly or indirectly specified in
            the group specified by the Name item.
            If this item is SelectionElm, the result request is for all point elements directly or indirectly selected
            and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,LoadCase,StepType,StepNum,U1,U2,U3,R1,R2,R3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the point object name associated with each result, if any.
            Some results will have no point object associated with them. For these cases this item will be blank
        Elm(str list)-This is an array that includes the point element name associated with each result.
        LoadCase(str list)-This is an array that includes the name of the modal analysis case associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result. For mode shape results,
            this is always be Mode.
        StepNum(int list)-This is an array that includes the step number for each result. For mode shape results,
            this is always the mode number
        U1,U2,U3(float list)-These are one dimensional arrays that include the displacement in the point element
            local 1, 2 and 3 axes directions, respectively, for each result. [L]
        R1,R2,R3(float list)-These are one dimensional arrays that include the rotation about the point element
            local 1, 2 and 3 axes, respectively, for each result. [rad]
        """
        result=self.SapModel.Results.ModeShape(Name,ItemTypeElm)
        return result

    def results_SolidJointForce(self,Name,ItemTypeElm=0):
        """
        ---This function reports the joint forces for the point elements at each corner of the specified solid elements---
        inputs:
        Name(str)-The name of an existing solid object, solid element, or group of objects, depending on the value of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the solid elements corresponding to the solid object
            specified by the Name item.
            If this item is Element, the result request is for the solid element specified by the Name item.
            If this item is GroupElm, the result request is for the solid elements corresponding to all solid objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for solid elements corresponding to all selected solid
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,F1,F2,F3,M1,M2,M3]

        NumberResults(int)-The total number of results returned by the program.
        Obj(str list)-This is an array that includes the solid object name associated with each result, if any.
        Elm(str list)-This is an array that includes the solid element name associated with each result
        PointElm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result.
        F1,F2,F3(float list)-These are one dimensional arrays that include the joint force components in the point
            element local axes directions. [F]
        M1,M2,M3(float list)-These are one dimensional arrays that include the joint moment components about the
            point element local axes. [FL]
        """
        result=self.SapModel.Results.SolidJointForce(Name,ItemTypeElm)
        return result

    def results_SolidStrain(self,Name,ItemTypeElm=0):
        """
        ---This function reports the strains for the specified solid elements. Strains are reported at each point
        element associated with the solid element---
        inputs:
        Name(str)-The name of an existing solid object, solid element, or group of objects, depending on the value of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the solid elements corresponding to the solid object
            specified by the Name item.
            If this item is Element, the result request is for the solid element specified by the Name item.
            If this item is GroupElm, the result request is for the solid elements corresponding to all solid objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for solid elements corresponding to all selected solid
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,E11,E22,E33,G12,G13,G23,EMax,EMid,EMin,EVM,
        DirCosMax1,DirCosMax2,DirCosMax3,DirCosMid1,DirCosMid2,DirCosMid3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the solid object name associated with each result, if any
        Elm(str list)-This is an array that includes the solid element name associated with each result
        PointElm(str list)-This is an array that includes the name of the point element where the results are reported
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated
            with each result.
        StepType(str list)-This is an array that includes the step type, if any, for each result.
        StepNum(int list)-This is an array that includes the step number, if any, for each result.
        E11,E22,E33,G12,G13,G23(float)-The solid element internal E11, E22, E33, G12, G13 and G23 strains at the
            specified point element location, reported in the solid element local coordinate system.
        EMax,EMid,EMin(float)-The solid element maximum, middle and minimum principal strains at the specified point element location
        EVM(float)-The solid element internal Von Mises strain at the specified point element location
        DirCosMax1,DirCosMax2,DirCosMax3(float)-These are three direction cosines defining the orientation of the
            maximum principal strain with respect to the solid element local axes.
        DirCosMid1,DirCosMid2,DirCosMid3(float)-These are three direction cosines defining the orientation of the
            middle principal strain with respect to the solid element local axes
        DirCosMin1,DirCosMin2,DirCosMin3(float)-These are three direction cosines defining the orientation of the
            minimum principal strain with respect to the solid element local axes.
        """
        result=self.SapModel.Results.SolidStrain(Name,ItemTypeElm)
        return result

    def results_SolidStress(self,Name,ItemTypeElm=0):
        """
        ---This function reports the stresses for the specified solid elements. Stresses are reported at
        each point element associated with the solid element---
        inputs:
        Name(str)-The name of an existing solid object, solid element, or group of objects, depending on the value of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the solid elements corresponding to the solid object
            specified by the Name item.
            If this item is Element, the result request is for the solid element specified by the Name item.
            If this item is GroupElm, the result request is for the solid elements corresponding to all solid objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for solid elements corresponding to all selected solid
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,S11,S22,S33,S12,S13,S23,SMax,SMid,SMin,SVM,
        DirCosMax1,DirCosMax2,DirCosMax3,DirCosMid1,DirCosMid2,DirCosMid3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the solid object name associated with each result, if any
        Elm(str list)-This is an array that includes the solid element name associated with each result
        PointElm(str list)-This is an array that includes the name of the point element where the results are reported
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated
            with each result.
        StepType(str list)-This is an array that includes the step type, if any, for each result.
        StepNum(int list)-This is an array that includes the step number, if any, for each result.
        S11,S22,S33,S12,S13,S23(float)-The solid element internal S11, S22, S33, S12, S13 and S23 stresses at the
            specified point element location, reported in the solid element local coordinate system. [F/L2]
        SMax,SMid,SMin(float)-The solid element maximum, middle and minimum principal stresses at the specified point
            element location. [F/L2]
        DirCosMax1,DirCosMax2,DirCosMax3(float)-These are three direction cosines defining the orientation of the
            maximum principal stress with respect to the solid element local axes.
        DirCosMid1,DirCosMid2,DirCosMid3(float)-These are three direction cosines defining the orientation of the
            middle principal stress with respect to the solid element local axes
        DirCosMin1,DirCosMin2,DirCosMin3(float)-These are three direction cosines defining the orientation of the
            minimum principal stress with respect to the solid element local axes.
        """
        result=self.SapModel.Results.SolidStress(Name,ItemTypeElm)
        return result

    def results_StepLabel(self):
        """
        ---This function generates the step label for analyzed linear multi-step, nonlinear multi-step, or
        staged-construction load cases. For other load case types, the label will be blank---
        return:
        [index,LoadCase,StepNum,Label]

        LoadCase(str)-The name of an existing linear multi-step, nonlinear multi-step, or staged-construction load case
        StepNum(int)-This is an overall step number from the specified load case. The range of values of StepNum for a
            given load case can be obtained from most analysis results calls, such as SapObject.SapModel.Results.JointDispl
        Label(str)-The is the step label, including the name or number of the stage, the step number within the stage,
            and the age of the structure for time-dependent load cases
        """
        result=self.SapModel.Results.StepLabel()
        return result















#########################################################################

#########################################################################

#########################################################################
if __name__ == '__main__':
    #############################################
    # sapPyInstance=SAP2000Py()
    # sapPyInstance.initializeNewModel()
    # sapPyInstance.newBlank()
    #############################################
    # sapPyInstance.define_material_SetMatrial("myMat",1)
    # sapPyInstance.define_material_SetMPIsotropic("myMat",345,0.2,2.15e-5)
    # sapPyInstance.define_material_SetWeightAndMass("myMat",24.99)
    # sapPyInstance.define_material_SetOTendon_1("myMat",230, 255, 1, 1, -0.1)
    # sapPyInstance.define_material_SetORebar_1("myMat", 62, 93, 70, 102, 2, 2, 0.02, 0.1, -0.1, False)
    # sapPyInstance.define_material_SetOSteel_1("myMat",55, 68, 60, 70, 0)
    # sapPyInstance.define_material_SetSSCurve("myMat",[-0.2,-0.1,0,0.1,0.2],[-5,-2,0,1,4])
    # sapPyInstance.define_material_SetOConcrete_1("myMat",5, False, 0, 1, 2, 0.0022, 0.0052, -0.1)
    # sapPyInstance.define_material_TendonUser("mytondon",18, 2000, 2e-5)
    # sapPyInstance.define_material_AddMaterial("myConcrete", 2, "China", "JTG", "JTG D62-2004 C15")
    # sapPyInstance.define_material_AddMaterial("mysteel345",1,"China","JTG","GB/T 714-2008 Q690q")
    #############################################
    # sapPyInstance.define_section_Cable_SetPro("caleSect","mytondon",0.2)
    # sapPyInstance.define_section_PropFrame_SetGeneral("myRect","myMat",2,1.6667,1.6667,0.6667,0.1667,0.4578)
    # sapPyInstance.define_section_Tendon_SetProp("mytonden","mytondon",1,0.02)
    # sapPyInstance.define_section_Area_SetPlane("myplaneArea",1,"myMat",0.23)
    # sapPyInstance.define_section_Area_SetShell_1("myshell",1,"myMat",0.22)
    # sapPyInstance.define_section_PropSolid_SetProp("mySold","myMat")
    # sapPyInstance.define_section_PropLink_SetLinear("myLiner",["U1"],[],{"U1":2000},{})
    # sapPyInstance.define_section_PropLink_SetMultiLinearElastic("mymultiLinear",["U1"],[],["U1"],{"U1":2000},{"U1":0.05})
    # sapPyInstance.define_section_PropLink_SetMultiLinearPoints("mymultiLinear",1,[-5,-3,0,1,4],[-0.2,-0.1,0,0.05,0.1])
    # sapPyInstance.define_material_PropLink_SetMultiLinearPlastic("mymultiLinearP",["U1"],[],["U1"],{"U1":2000},{"U1":0.05})
    # sapPyInstance.define_section_PropLink_SetMultiLinearPoints("mymultiLinearP",1,[-5,-3,0,1,4],[-0.2,-0.1,0,0.05,0.1],0)
    # sapPyInstance.define_section_PropLink_SetDamper("myDamper",["U2"],[],["U2"],{"U2":1000},{"U2":0.05},{"U2":10001},
    #                                                 {"U2":2001},{"U2":0.3})
    # sapPyInstance.define_section_PropLink_SetDamperBilinear("myDamperBiliear",["U2"],[],["U2"],{"U2":1000},{"U2":0.05},
    #                                                         {"U2":10001},{"U2":0.041},{"U2":0.032},{"U2":2003})
    # sapPyInstance.define_section_PropLink_SetGap("myLinkGap",["U2"],[],["U2"],{"U2":1000},{"U2":0.05},{"U2":2001},{"U2":1.2})
    # sapPyInstance.define_section_PropLink_SetHook("myLinkHook",["U2"],[],["U2"],{"U2":1000},{"U2":0.05},{"U2":2001},{"U2":1.2})
    # sapPyInstance.define_section_PropLink_SetPlasticWen("myPlasticWen",["U2"],[],["U2"],{"U2":1000},{"U2":0.05},{"U2":2001},
    #                                                     {"U2":300},{"U2":0.2},{"U2":0.1})
    # sapPyInstance.define_section_PropLink_SetRubberIsolator("myRubberIsolator",["U2"],[],["U2"],{"U2":1000},{"U2":0.05},
                                                            # {"U2":2001},{"U2":300},{"U2":0.2})
    # sapPyInstance.define_section_PropLink_SetFrictionIsolator("myFrictionIso",["U2"],[],["U2"],{"U2":1000},{"U2":0.05},
                                    # {"U2":1002},{"U2":0.01},{"U2":2.21},{"U2":0.12},{"U2":0},0.043)
    #############################################
    # sapPyInstance.define_Groups_SetGroup("mygrop1")


    #############################################



    # sapPyInstance.define_jointConstraints_SetBody("mybody",["UX","UY","UZ","RX","RY","RZ"])
    # sapPyInstance.define_jointConstraints_SetBeam("myBeam")
    # sapPyInstance.define_jointConstraints_SetDiaphragm("myDiaphram")
    # sapPyInstance.define_jointConstraints_SetEqual("myEqual",["UX"])
    # sapPyInstance.define_jointConstraints_SetLine("myLine",["UX","UZ"])
    # sapPyInstance.define_jointConstraints_SetLocal("mylocal",["U1","R2"])
    # sapPyInstance.define_jointConstraints_SetPlate("myPlate",3)
    # sapPyInstance.define_jointConstraints_SetRod("myrod",3)
    # sapPyInstance.define_jointConstraints_SetWeld("myweld",["UX"],1)
    #############################################
    # sapPyInstance.define_generalizedDisplacements_Add("myGeneralPoint",1)
    # sapPyInstance.define_generalizedDisplacements_SetPoint("myGeneralPoint","point1",{"U1":0.5})
    #############################################
    # sapPyInstance.define_functions_FuncRS_SetChinese2010("myResFunc", 0.18, 5, 0.36, 1, 0.04)
    # sapPyInstance.define_functions_FuncRS_SetJTGB022013("myJTGB02", 1, 0.18, 0.36, 0.4, 1, 0.04)
    # sapPyInstance.define_functions_FuncRS_SetCJJ1662011("myCJJ166", 1, 0.35, 0.25, 0.04)
    # sapPyInstance.define_functions_FuncRS_SetUser("myUserResFunc",[0.1,0.2,0.3,0.4],[0.4,0.6,0.8,0.3],0.05)
    # sapPyInstance.define_functions_FuncTH_SetUser("myUserRTH",[0.1,0.2,0.3,0.4],[0.4,0.6,0.8,0.3])
    #############################################
    # sapPyInstance.define_LoadPatterns_Add("quakePattern",5,0)
    #############################################
    # sapPyInstance.define_LoadCases_StaticLinear_SetCase("myStaticLinear")
    # sapPyInstance.define_LoadCases_StaticLinear_SetInitialCase("myStaticLinear","DEAD")
    # sapPyInstance.define_LoadCases_StaticLinear_SetLoads("myStaticLinear",2,["Load","Accel"],["Dead","UX"],[1.2,2.3])

    # sapPyInstance.define_LoadCases_StaticLinearMultistep_SetCase("myStaticLinerMulti")
    # sapPyInstance.define_loadCases_StaticLinearMultistep_SetInitialCase("myStaticLinerMulti")
    # sapPyInstance.define_loadCases_StaticLinearMultistep_SetLoads_1("myStaticLinerMulti",2,["Load","Accel"],
    #         ["DEAD","UZ"],[0.7,1.2],[0,0],[1,1],[1,1],[1,1],[1,1])

    # sapPyInstance.define_LoadCases_StaticNonlinear_SetCase("myStaticNonLinear")

    # sapPyInstance.define_loadCases_Buckling_SetCase("myBuckling")
    # sapPyInstance.define_loadCases_Buckling_SetInitialCase("myBuckling")
    # sapPyInstance.define_loadCases_Buckling_SetLoads("myBuckling",2,["load","Accel"],["DEAD","UZ"],[0.7,1.2])
    # sapPyInstance.define_loadCases_Buckling_SetParameters("myBuckling",7,1e-7)

    # sapPyInstance.define_loadCases_DirHistLinear_SetCase("myDirHistLinear")
    # sapPyInstance.define_loadCases_DirHistLinear_SetDampProportional("myDirHistLinear",2,0,0,0.1,1,0.05,0.06)
    # sapPyInstance.define_functions_FuncTH_SetUser("TH-1",[0.0,0.1],[0.0,0.1])
    # sapPyInstance.define_loadCases_DirHistLinear_SetLoads("myDirHistLinear",2,["Load","Accel"],["DEAD","U2"],
    #                                                       ["TH-1","TH-1"],TF=[0.5,0.3])
    # sapPyInstance.define_loadCases_DirHistLinear_SetTimeIntegration("myDirHistLinear",4)
    # sapPyInstance.define_loadCases_DirHistLinear_SetTimeStep("myDirHistLinear",1000,0.005)

    # sapPyInstance.define_loadCases_DirHistNonlinear_SetCase("myHistNonLiner")
    # sapPyInstance.define_loadCases_DirHistNonlinear_SetDampProportional("myHistNonLiner",2,0,0,0.1,1,0.05,0.06)
    # sapPyInstance.define_loadCases_DirHistNonlinear_SetGeometricNonlinearity("myHistNonLiner",2)
    # sapPyInstance.define_functions_FuncTH_SetUser("TH-1", [0.0, 0.1], [0.0, 0.1])
    # sapPyInstance.define_loadCases_DirHistNonlinear_SetLoads("myHistNonLiner",2,["Load","Accel"],["DEAD","U2"],
    #                                                       ["TH-1","TH-1"],TF=[0.5,0.3])
    # sapPyInstance.define_loadCases_DirHistNonlinear_SetMassSource("myHistNonLiner")
    # sapPyInstance.define_loadCases_DirHistNonlinear_SetSolControlParameters("myHistNonLiner")
    # sapPyInstance.define_loadCases_DirHistNonlinear_SetTimeIntegration("myHistNonLiner")
    # sapPyInstance.define_loadCases_DirHistNonlinear_SetTimeStep("myHistNonLiner",1002,0.004)

    # sapPyInstance.define_loadCases_ModalEigen_SetCase("myModalEigen")
    # sapPyInstance.define_loadCases_ModalEigen_SetInitialCase("myModalEigen")
    # sapPyInstance.define_loadCases_ModalEigen_SetLoads("myModalEigen",2,["Load","Accel"],["DEAD","UZ"])
    # sapPyInstance.define_loadCases_ModalEigen_SetNumberModes("myModalEigen",15,2)
    # sapPyInstance.define_loadCases_ModalEigen_SetParameters("myModalEigen")

    # sapPyInstance.define_loadCases_ModalRitz_SetCase("myModelRitz")
    # sapPyInstance.define_loadCases_ModalRitz_SetLoads("myModelRitz",2,["Load","Accel"],["DEAD","UZ"],TargetPar=[98,97])
    # sapPyInstance.define_loadCases_ModalRitz_SetNumberModes("myModelRitz",MaxModes=20)

    #cannot work
    # sapPyInstance.define_loadCases_ModHistLinear_SetCase("myModHistLiner")
    # sapPyInstance.define_loadCases_ModHistLinear_SetDampConstant("myModHistLiner",0.05)
    # sapPyInstance.define_loadCases_ModHistLinear_SetDampProportional("myHistNonLiner",1,0.1,0.2)
    # sapPyInstance.define_functions_FuncTH_SetUser("TH-1",[0.0,0.1],[0.0,0.1])
    # sapPyInstance.define_loadCases_ModHistLinear_SetLoads("myHistNonLiner",1,["Accel"],["U2"],["TH-1"])
    # sapPyInstance.define_loadC

    # sapPyInstance.define_loadCases_ModHistNonlinear_SetCase("modHistNonLiner")
    # sapPyInstance.define_loadCases_ModHistNonlinear_SetDampConstant("modHistNonLiner",0.035)
    # sapPyInstance.define_loadCases_ModHistNonlinear_SetDampInterpolated("modHistNonLiner",5,3,[0.001,0.3,1],[0.1,0.03,0.05])
    # sapPyInstance.define_loadCases_ModHistNonlinear_SetDampOverrides("modHistNonLiner",2,[1,2],[0.02,0.03])
    # sapPyInstance.define_loadCases_ModHistNonlinear_SetDampProportional("modHistNonLiner",2,0, 0, 0.1, 1, 0.05, 0.06)
    # sapPyInstance.define_functions_FuncTH_SetUser("TH-1", [0.0, 0.1], [0.0, 0.1])
    # sapPyInstance.define_loadCases_ModHistNonlinear_SetLoads("modHistNonLiner",1,["Accel"],["U1"],
    #                                                          ["TH-1"])
    # sapPyInstance.define_loadCases_ModHistNonlinear_SetModalCase("modHistNonLiner","MODAL")
    # sapPyInstance.define_loadCases_ModHistNonlinear_SetSolControlParameters("modHistNonLiner",etol=1e-9)
    # sapPyInstance.define_loadCases_ModHistNonlinear_SetTimeStep("modHistNonLiner",120, 0.05)

    # sapPyInstance.define_loadCases_ResponseSpectrum_SetCase("responseSpect")
    # sapPyInstance.define_loadCases_ResponseSpectrum_SetDampConstant("responseSpect",0.035)
    # sapPyInstance.define_loadCases_ResponseSpectrum_SetDampInterpolated("responseSpect",5,3,[0.001,0.3,1],
    #                                                                     [0.1,0.03,0.05])
    # sapPyInstance.define_loadCases_ResponseSpectrum_SetDampOverrides("responseSpect",2,[1,2],[0.02,0.03])
    # sapPyInstance.define_loadCases_ResponseSpectrum_SetDampProportional("responseSpect",2,0,0,0.1,1,0.05,0.06)
    # sapPyInstance.define_loadCases_ResponseSpectrum_SSetDiaphragmEccentricityOverride("responseSpect",1,50)
    # sapPyInstance.define_loadCases_ResponseSpectrum_SetDirComb("responseSpect",3)
    # sapPyInstance.define_loadCases_ResponseSpectrum_SetEccentricity("responseSpect",0.05)
    # sapPyInstance.define_functions_FuncRS_SetChinese2010("myResFunc", 0.18, 5, 0.36, 1, 0.04)
    # sapPyInstance.define_loadCases_ResponseSpectrum_SetLoads("responseSpect",2,["U1","U2"],["myResFunc","myResFunc"],
    #                                                          [1.2,1.2])
    # sapPyInstance.define_loadCases_ResponseSpectrum_SetModalCase("responseSpect","MODAL")
    # sapPyInstance.define_loadCases_ResponseSpectrum_SetModalComb_1("responseSpect",4, 0.5, 1.2, 1)
    #############################################
    # sapPyInstance.define_SourceMass_SetMassSource("myMass",True,False,False,False)
    #############################################
    # sapPyInstance.define_RespCombo_Add("myComb",3)
    # sapPyInstance.define_RespCombo_SetCaseList("myComb",0,"DEAD",1.4)
    #############################################
    # sapPyInstance.assign_PointObj_AddCartesian(12,37,0,UserName="A1")
    # sapPyInstance.assign_PointObj_AddCartesian(12, 37,2, UserName="A2")
    # sapPyInstance.assign_PointObj_AddCylindrical(12,37,0,UserName="A2")
    # sapPyInstance.assign_PointObj_AddSpherical(12,37,23,UserName="A3")
    # pointNum=sapPyInstance.assign_PointObj_Count()
    # print(pointNum)

    # sapPyInstance.define_jointConstraints_SetDiaphragm("Diaph1")
    # sapPyInstance.assign_PointObj_SetConstraint("A1","Diaph1")
    # sapPyInstance.assign_PointObj_SetConstraint("A2", "Diaph1")

    # sapPyInstance.file_New2DFrame(0,3, 124, 3, 200)
    # nums=sapPyInstance.assign_PointObj_GetCommonTo("6")
    # print(nums)

    # results=sapPyInstance.assign_PointObj_GetConnectivity("11")
    # print(results)

    # sapPyInstance.define_jointConstraints_SetDiaphragm("Diaph1")
    # for i1 in range(4,17,4):
    #     print(i1)
    #     sapPyInstance.assign_PointObj_SetConstraint(str(i1),"Diaph1")
    # results=sapPyInstance.assign_PointObj_GetConstraint("4")
    # print(results)

    # sapPyInstance.defineCoordSystem("csys1",[10,10,0,45,0,0])
    # sapPyInstance.SetPresentCoordSystem("csys1")
    # for i1 in range(1,8):
    #     result=sapPyInstance.assign_PointObj_GetCoordCartesian(str(i1))
    #     print(result)

    # for i1 in range(1,8):
    #     result=sapPyInstance.assign_PointObj_GetCoordCylindrical(str(i1))
    #     print(result)

    # for i1 in range(1,8):
    #     result=sapPyInstance.assign_PointObj_GetCoordSpherical(str(i1))
    #     print(result)

    # for i1 in range(1,8):
        # result=sapPyInstance.assign_PointObj_GetElm(str(i1))
        # print(result)

        # result=sapPyInstance.assign_PointObj_GetLocalAxes(str(i1))
        # print(result)

        # result=sapPyInstance.assign_PointObj_GetMass(str(i1))
        # print(result)

        # result=sapPyInstance.assign_PointObj_GetNameList()
        # print(result)

    # sapPyInstance.assign_PointObj_SetSpring("3",[0,0,10,0,0,0])
    # result=sapPyInstance.assign_PointObj_GetSpring("3")
    # print(result)

    # k=[0 for each in range(21)]
    # k[2],k[17]=10,4
    # sapPyInstance.assign_PointObj_SetSpringCoupled("3",k)
    # result=sapPyInstance.assign_PointObj_GetSpringCoupled("3")
    # result=sapPyInstance.assign_PointObj_IsSpringCoupled("3")
    # print(result)

    # sapPyInstance.define_Groups_SetGroup("Group1")
    # sapPyInstance.assign_PointObj_SetGroupAssign("3","Group1")
    # sapPyInstance.assign_PointObj_SetGroupAssign("6", "Group1")
    # sapPyInstance.assign_PointObj_SetGroupAssign("9", "Group1")

    # sapPyInstance.define_Groups_SetGroup("Group1")
    # sapPyInstance.define_Groups_SetGroup("Group2")
    # sapPyInstance.assign_PointObj_SetGroupAssign("3", "Group1")
    # sapPyInstance.assign_PointObj_SetGroupAssign("3", "Group2")
    # result=sapPyInstance.assign_PointObj_GetGroupAssign("3")
    # print(result)

    # sapPyInstance.assign_PointObj_SetLoadDispl("1","DEAD",[10,0,0,0,0,0])
    # result=sapPyInstance.assign_PointObj_GetLoadDispl("1")
    # print(result)

    # value=[10,0,0,0,0,0]
    # sapPyInstance.assign_PointObj_SetLoadForce("1","DEAD",value)

    # sapPyInstance.assign_PointObj_SetLocalAxes("1",90,0,0)

    # sapPyInstance.assign_PointObj_SetMass("1",[10,0,0,0,0,0])

    # result=sapPyInstance.assign_PointObj_GetRestraint("1")
    # print(result)

    # value=[True,True,True,True,True,True]
    # sapPyInstance.assign_PointObj_SetRestraint("1",value)
    #############################################
    # sapPyInstance.assign_FrameObj_AddByCoord(-300, 0, 0, -100, 0, 124,userName="AddFrame")

    # sapPyInstance.assign_FrameObj_AddByPoint("1","6",userName="FrameByPoints")

    # sapPyInstance.assign_FrameObj_ChangeName("1", "MyFrame")

    # countNum=sapPyInstance.assign_FrameObj_Count()
    # print(countNum)

    # sapPyInstance.assign_FrameObj_Delete("1")

    # sapPyInstance.assign_FrameObj_SetAutoMesh("3", True, True, True, 0, 0)
    # result=sapPyInstance.assign_FrameObj_GetAutoMesh("3")
    # print(result)

    # sapPyInstance.assign_FrameObj_SetDesignProcedure("8", 2)

    # sapPyInstance.assign_FrameObj_SetEndLengthOffset("15", False, 12, 12, 0.5)

    # sapPyInstance.assign_FrameObj_SetEndSkew("15", 10, 20)

    # sapPyInstance.define_Groups_SetGroup("Group1")
    # sapPyInstance.define_Groups_SetGroup("Group2")
    # sapPyInstance.assign_FrameObj_SetGroupAssign("2", "Group1")
    # sapPyInstance.assign_FrameObj_SetGroupAssign("2", "Group2")
    # result=sapPyInstance.assign_FrameObj_GetGroupAssign("2")
    # print(result)

    # Offset1=[10,11,12]
    # Offset2 = [20, 21, 22]
    # sapPyInstance.assign_FrameObj_SetInsertionPoint("15", 7, False, True, Offset1, Offset2)

    # DOF=[True,False,False,False,False,False]
    # d=[2,0,0,0,0,0]
    # sapPyInstance.assign_FrameObj_SetLoadDeformation("1", "DEAD", DOF, d)
    # result=sapPyInstance.assign_FrameObj_GetLoadDeformation("1")
    # print(result)

    # sapPyInstance.assign_FrameObj_SetLoadDistributed("15", "DEAD", 1, 10, 0, 1, 0.08, 0.08)
    # sapPyInstance.assign_FrameObj_SetLoadDistributed("14", "DEAD", 1, 10, 0, 1, 0.08, 0.08)
    # result=sapPyInstance.assign_FrameObj_GetLoadDistributed("15")
    # print(result)

    # sapPyInstance.assign_FrameObj_SetLoadGravity("1", "DEAD", 0, 0, -1)
    # result=sapPyInstance.assign_FrameObj_GetLoadGravity("1")
    # print(result)

    # sapPyInstance.assign_FrameObj_SetLoadPoint("15", "DEAD", 1, 10, .5, 20)
    # result=sapPyInstance.assign_FrameObj_GetLoadPoint("15")
    # print(result)

    # sapPyInstance.assign_FrameObj_SetLoadStrain("1", "DEAD", 1, 0.001)
    # result=sapPyInstance.assign_FrameObj_GetLoadStrain("1")
    # print(result)

    # DOF=[True,True,True,True,False,False]
    # f=[50,20,30,-456,0,0]
    # RD=[0.5,0.6,0.8,0.9,0,0]
    # sapPyInstance.assign_FrameObj_SetLoadTargetForce("1", "DEAD", DOF, f, RD)
    # result=sapPyInstance.assign_FrameObj_GetLoadTargetForce("1")
    # print(result)

    # sapPyInstance.assign_FrameObj_SetLoadTemperature("1", "DEAD", 1, 50)
    # result=sapPyInstance.assign_FrameObj_GetLoadTemperature("1")
    # print(result)

    # sapPyInstance.assign_FrameObj_SetLoadTransfer("1", False)

    # sapPyInstance.assign_FrameObj_SetLocalAxes("3", 30)
    # result=sapPyInstance.assign_FrameObj_GetLocalAxes("3")
    # print(result)

    # sapPyInstance.assign_FrameObj_SetMass("1", 1)
    # result=sapPyInstance.assign_FrameObj_GetMass("1")
    # print(result)

    # sapPyInstance.assign_FrameObj_SetMaterialOverwrite("3", "4000Psi")

    # sapPyInstance.assign_FrameObj_SetMatTemp("1", 50)
    # result=sapPyInstance.assign_FrameObj_GetMatTemp("1")
    # print(result)

    # value=[1,1,1,1,5,1,1,1]
    # sapPyInstance.assign_FrameObj_SetModifiers("3", value)

    # stype="Auto"
    # value=1.1
    # sapPyInstance.assign_FrameObj_SetNotionalSize("FSEC1", stype,value)

    # sapPyInstance.assign_FrameObj_SetOutputStations("15", 1, 18)

    # sapPyInstance.assign_FrameObj_SetPDeltaForce("1", 100, 0, True)
    # result=sapPyInstance.assign_FrameObj_GetPDeltaForce("1")
    # print(result)

    # ii=[False,False,False,False,False,True]
    # jj = [False, False, False, False, False, True]
    # sapPyInstance.assign_FrameObj_SetReleases("13", ii, jj)
    # result=sapPyInstance.assign_FrameObj_GetReleases("13")
    # print(result)

    # sapPyInstance.assign_FrameObj_SetSection("13", "None")

    # sapPyInstance.assign_FrameObj_SetSpring("13", 1, 1, 1, "", 1, 2, 0,[0,0,0], 0, False)
    # result=sapPyInstance.assign_FrameObj_GetSpring("13")
    # print(result)

    # sapPyInstance.assign_FrameObj_SetTCLimits("1", False, 0, True, 100)
    # result=sapPyInstance.assign_FrameObj_GetTCLimits("1")
    # print(result)

    # result=sapPyInstance.assign_FrameObj_GetNameList()
    # print(result)

    # result=sapPyInstance.assign_FrameObj_GetPoints("3")
    # print(result)

    # result=sapPyInstance.assign_FrameObj_GetSection("3")
    # print(result)

    # result=sapPyInstance.assign_FrameObj_GetTransformationMatrix("3")
    # print(result)
    #############################################
    # sapPyInstance.assign_CableObj_AddByCoord(-300, 0, 0, -100, 0, 124, UserName="myCable")

    # sapPyInstance.assign_CableObj_AddByPoint("1", "6",UserName="MyCable")
    # sapPyInstance.assign_CableObj_ChangeName("MyCable","newCable")

    # result=sapPyInstance.assign_CableObj_Count()
    # print(result)

    # sapPyInstance.assign_CableObj_SetCableData("MyCable", 7, 1, 0, 0, 24)

    # sapPyInstance.define_Groups_SetGroup("Group1")
    # sapPyInstance.assign_CableObj_SetGroupAssign("MyCable","Group1")

    # sapPyInstance.assign_CableObj_SetLoadDeformation("MyCable","DEAD",2)
    # result = sapPyInstance.assign_CableObj_GetLoadDeformation("MyCable")
    # print(result)

    # sapPyInstance.assign_CableObj_SetLoadDistributed("MyCable","DEAD",1,10,0.08)
    # result=sapPyInstance.assign_CableObj_GetLoadDistributed("MyCable")
    # print(result)

    # sapPyInstance.assign_CableObj_SetLoadGravity("MyCable", "DEAD", 0, 0, -1)
    # result=sapPyInstance.assign_CableObj_GetLoadGravity("MyCable")
    # print(result)

    # sapPyInstance.assign_CableObj_SetLoadStrain("MyCable","DEAD",0.001)
    # result=sapPyInstance.assign_CableObj_GetLoadStrain("MyCable")
    # print(result)

    # sapPyInstance.assign_CableObj_SetLoadTargetForce("MyCable","DEAD",50,0.5)
    # result=sapPyInstance.assign_CableObj_GetLoadTargetForce("MyCable")
    # print(result)

    # sapPyInstance.assign_CableObj_SetLoadTemperature("MyCable","DEAD",50)
    # result=sapPyInstance.assign_CableObj_GetLoadTemperature("MyCable")
    # print(result)

    # sapPyInstance.assign_CableObj_SetMass("MyCable",0.0001)
    # result=sapPyInstance.assign_CableObj_GetMass("MyCable")
    # print(result)

    # sapPyInstance.assign_CableObj_SetMatTemp("MyCable",50)
    # result=sapPyInstance.assign_CableObj_GetMatTemp("MyCable")
    # print(result)

    # sapPyInstance.assign_CableObj_SetProperty("MyCable","CAB1")

    # result=sapPyInstance.assign_CableObj_GetCableData("MyCable")
    # print(result)

    # result=sapPyInstance.assign_CableObj_GetCableGeometry("MyCable")
    # print(result)

    # result=sapPyInstance.assign_CableObj_GetElm("MyCable")
    # print(result)

    # result=sapPyInstance.assign_CableObj_GetGroupAssign("MyCable")
    # print(result)

    # result=sapPyInstance.assign_CableObj_GetNameList()
    # print(result)

    # result=sapPyInstance.assign_CableObj_GetPoints("MyCable")
    # print(result)

    # result=sapPyInstance.assign_CableObj_GetProperty("MyCable")
    # print(result)

    # result=sapPyInstance.assing_CableObj_GetTransformationMatrix("MyCable")
    # print(result)

    #############################################
    # sapPyInstance.assign_TendonObj_AddByCoord(-288, 0, 288, 288, 0, 288,UserName="MyTendon")
    # sapPyInstance.assign_TendonObj_AddByPoint("3", "9",UserName="MyTendon")

    # result=sapPyInstance.assign_TendonObj_Count()
    # print(result)

    # sapPyInstance.assign_TendonObj_SetDiscretization("MyTendon",12)
    # result=sapPyInstance.assign_TendonObj_GetDiscretization("MyTendon")
    # print(result)

    # sapPyInstance.define_Groups_SetGroup("Group1")
    # sapPyInstance.assign_TendonObj_SetGroupAssign("MyTendon","Group1")
    # result=sapPyInstance.assign_TendonObj_GetGroupAssign("MyTendon")
    # print(result)

    # sapPyInstance.assign_TendonObj_SetLoadDeformation("MyTendon","DEAD",2)
    # result=sapPyInstance.assign_TendonObj_GetLoadDeformation("MyTendon")
    # print(result)

    # sapPyInstance.assign_TendonObj_SetLoadedGroup("MyTendon","Group1")
    # result=sapPyInstance.assign_TendonObj_GetLoadedGroup("MyTendon")
    # print(result)

    # sapPyInstance.assign_TendonObj_SetLoadForceStress("MyTendon", "DEAD", 1, 0, 100, 0.15, 8.333E-05, 0.25, 3, 5, 7, 5)
    # result=sapPyInstance.assign_TendonObj_GetLoadForceStress("MyTendon")
    # print(result)

    # sapPyInstance.assign_TendonObj_SetLoadGravity("MyTendon", "DEAD", 0, 0, -1)
    # result=sapPyInstance.assign_TendonObj_GetLoadGravity("MyTendon")
    # print(result)

    # sapPyInstance.assign_TendonObj_SetLoadStrain("MyTendon", "DEAD", 0.001)
    # result=sapPyInstance.assign_TendonObj_GetLoadStrain("MyTendon")
    # print(result)

    # sapPyInstance.assign_TendonObj_SetLoadTemperature("MyTendon", "DEAD", 50)
    # result=sapPyInstance.assign_TendonObj_GetLoadTemperature("MyTendon")
    # print(result)

    # sapPyInstance.assign_TendonObj_SetLocalAxes("MyTendon",30)
    # result=sapPyInstance.assign_TendonObj_GetLocalAxes("MyTendon")
    # print(result)

    # sapPyInstance.assign_TendonObj_SetMatTemp("MyTendon",50)
    # result=sapPyInstance.assign_TendonObj_GetMatTemp("MyTendon")
    # print(result)

    # sapPyInstance.assign_TendonObj_SetProperty("MyTendon","TEN1")

    # sapPyInstance.assign_TendonObj_SetTCLimits("MyTendon", True, 0, True, 100)
    # result=sapPyInstance.assign_TendonObj_GetTCLimits("MyTendon")
    # print(result)

    # NumberPoints=3
    # MyType=[1,7,6]
    # x=[0,288,576]
    # y=[0,-12,0]
    # z=[0,0,0]
    # sapPyInstance.assign_TendonObj_SetTendonData("MyTendon", NumberPoints, MyType, x, y, z, "Local")
    # result=sapPyInstance.assign_TendonObj_GetTendonData("MyTendon")
    # print(result)

    # result=sapPyInstance.assign_TendonObj_GetNameList()
    # print(result)

    # result=sapPyInstance.assign_TendonObj_GetPoints("MyTendon")
    # print(result)

    # result=sapPyInstance.assign_TendonObj_GetProperty("MyTendon")
    # print(result)

    # result=sapPyInstance.assign_TendonObj_GetTendonGeometry("MyTendon")
    # print(result)

    # result=sapPyInstance.assign_TendonObj_GetTransformationMatrix("MyTendon")
    # print(result)

    #############################################
    # x=[50,100,150,100,50,0]
    # y=[0,0,40,80,80,40]
    # z=[0,0,0,0,0,0]
    # sapPyInstance.assign_AreaObj_AddByCoord(6,x,y,z,UserName="MyArea")

    # sapPyInstance.file_New2DFrame(0, 2, 144, 2, 288)
    # sapPyInstance.assign_AreaObj_AddByPoint(4,["1","4","5","2"],UserName="MyArea")

    # sapPyInstance.file_NewWall(2, 48, 2, 48)
    # sapPyInstance.assign_AreaObj_SetAutoMesh("1",3,PointOnEdgeFromLine=True,PointOnEdgeFromPoint=True)
    # result=sapPyInstance.assign_AreaObj_GetAutoMesh("1")
    # print(result)
    # sapPyInstance.assign_AreaObj_SetEdgeConstraint("1",True)
    # result=sapPyInstance.assign_AreaObj_GetEdgeConstraint("1")
    # print(result)

    # sapPyInstance.define_Groups_SetGroup("Group1")
    # sapPyInstance.assign_AreaObj_SetGroupAssign("1","Group1")
    # result=sapPyInstance.assign_AreaObj_GetGroupAssign("1")
    # print(result)

    # sapPyInstance.assign_AreaObj_SetLoadGravity("1","DEAD",0,0,-1)
    # result=sapPyInstance.assign_AreaObj_GetLoadGravity("1")
    # print(result)

    # sapPyInstance.assign_AreaObj_SetLoadPorePressure("1","DEAD",0.1)
    # result=sapPyInstance.assign_AreaObj_GetLoadPorePressure("1")
    # print(result)

    # sapPyInstance.assign_AreaObj_SetLoadRotate("1","DEAD",30)
    # result=sapPyInstance.assign_AreaObj_GetLoadRotate("1")
    # print(result)

    # sapPyInstance.assign_AreaObj_SetLoadStrain("1", "DEAD", 1, 0.001)
    # result=sapPyInstance.assign_AreaObj_GetLoadStrain("1")
    # print(result)

    # sapPyInstance.assign_AreaObj_SetLoadSurfacePressure("1", "DEAD", -1, .1)
    # result=sapPyInstance.assign_AreaObj_GetLoadSurfacePressure("1")
    # print(result)

    # sapPyInstance.assign_AreaObj_SetLoadTemperature("1", "DEAD", 1, 50)
    # result=sapPyInstance.assign_AreaObj_GetLoadTemperature("1")
    # print(result)

    # sapPyInstance.assign_AreaObj_SetLoadUniform("1", "DEAD", -0.01, 3, False, "Local")
    # result=sapPyInstance.assign_AreaObj_GetLoadUniform("1")
    # print(result)

    # sapPyInstance.assign_AreaObj_SetLoadUniformToFrame("1", "DEAD", 0.01, 10, 2, False, "Global")
    # result=sapPyInstance.assign_AreaObj_GetLoadUniformToFrame("1")
    # print(result)

    # sapPyInstance.assign_AreaObj_SetLoadWindPressure_1("1", "DEAD", 1, 0.8, 1)
    # result=sapPyInstance.assign_AreaObj_GetLoadWindPressure_1("1")
    # print(result)

    # sapPyInstance.assign_AreaObj_SetLocalAxes("1",30)
    # result=sapPyInstance.assign_AreaObj_GetLocalAxes("1")
    # print(result)

    # sapPyInstance.assign_AreaObj_SetMass("1", .0001)
    # result=sapPyInstance.assign_AreaObj_GetMass("1")
    # print(result)

    # sapPyInstance.assign_AreaObj_SetMatTemp("1",50)
    # result=sapPyInstance.assign_AreaObj_GetMatTemp("1")
    # print(result)
    # Value=[0.01,1,1,1,1,1,1,1,1,1]
    # sapPyInstance.assign_AreaObj_SetModifiers("1",Value)
    # result=sapPyInstance.assign_AreaObj_GetModifiers("1")
    # print(result)

    # sapPyInstance.assign_AreaObj_SetNotionalSize("ASEC1","Auto",1.1)
    # result=sapPyInstance.assign_AreaObj_GetNotionalSize("ASEC1")
    # print(result)

    # Offset=[12,12,12,12]
    # sapPyInstance.assign_AreaObj_SetOffsets("1", 2, "", 1, Offset)
    # result=sapPyInstance.assign_AreaObj_GetOffsets("1")
    # print(result)

    # sapPyInstance.assign_AreaObj_SetProperty("4","None")
    # result=sapPyInstance.assign_AreaObj_GetProperty("4")
    # print(result)

    # Vec=[0,0,0]
    # sapPyInstance.assign_AreaObj_SetSpring("1", 1, 1, 1, "", -1, 1, 3, True, Vec, 0, False, "Local")
    # result=sapPyInstance.assign_AreaObj_GetSpring("1")
    # print(result)

    # Thickness= [12, 12, 12, 12]
    # sapPyInstance.assign_AreaObj_SetThickness("1", 2, "", 1, Thickness)
    # result=sapPyInstance.assign_AreaObj_GetThickness("1")
    # print(result)

    # result=sapPyInstance.assign_AreaObj_GetElm("1")
    # print(result)

    # result=sapPyInstance.assign_AreaObj_GetNameList()
    # print(result)

    # result=sapPyInstance.assign_AreaObj_GetPoints("1")
    # print(result)

    # result=sapPyInstance.assign_AreaObj_GetTransformationMatrix("1")
    # print(result)
    #############################################
    # x=[0,100,0,100,0,100,0,100]
    # y=[0,0,100,100,0,0,100,100]
    # z=[0,0,0,0,100,100,100,100]
    # sapPyInstance.assign_SolidObj_AddByCoord(x,y,z,UserName="mySolid")

    # sapPyInstance.file_New3DFrame(0,2, 144, 3, 288, 2, 288)
    # Point=["1","10","4","13","2","11","5","14"]
    # sapPyInstance.assign_SolidObj_AddByPoint(Point,UserName="MySolid")

    # sapPyInstance.file_NewSolidBlock(300, 400, 200,True,"Default",2, 2, 2)
    # result=sapPyInstance.assign_SolidObj_Count()
    # print(result)

    # sapPyInstance.assign_SolidObj_SetAutoMesh("1",1,3,3,3)
    # result=sapPyInstance.assign_SolidObj_GetAutoMesh("1")
    # print(result)

    # result=sapPyInstance.assign_SolidObj_GetElm("1")
    # print(result)

    # sapPyInstance.assign_SolidObj_SetEdgeConstraint("1",True)
    # result=sapPyInstance.assign_SolidObj_GetEdgeConstraint("1")
    # print(result)

    # sapPyInstance.define_Groups_SetGroup("Group1")
    # sapPyInstance.assign_SolidObj_SetGroupAssign("1","Group1")
    # result=sapPyInstance.assign_SolidObj_GetGroupAssign("1")
    # print(result)

    # sapPyInstance.assign_SolidObj_SetLoadGravity("ALL", "DEAD", 0, 0, -1,False,"Global",1)
    # result=sapPyInstance.assign_SolidObj_GetLoadGravity("1")
    # print(result)
    #
    # sapPyInstance.assign_SolidObj_SetLoadPorePressure("1", "DEAD", .1)
    # result=sapPyInstance.assign_SolidObj_GetLoadPorePressure("1")
    # print(result)

    # sapPyInstance.assign_SolidObj_SetLoadStrain("1", "DEAD", 1, 0.001)
    # result=sapPyInstance.assign_SolidObj_GetLoadStrain("1")
    # print(result)

    # sapPyInstance.assign_SolidObj_SetLoadSurfacePressure("1", "DEAD", 1, .1)
    # result=sapPyInstance.assign_SolidObj_GetLoadSurfacePressure("1")
    # print(result)

    # sapPyInstance.assign_SolidObj_SetLoadTemperature("1", "DEAD", 50)
    # result=sapPyInstance.assign_SolidObj_GetLoadTemperature("1")
    # print(result)

    # sapPyInstance.assign_SolidObj_SetLocalAxes("1",30,40,50)
    # result=sapPyInstance.assign_SolidObj_GetLocalAxes("1")
    # print(result)

    # sapPyInstance.assign_SolidObj_SetMatTemp("1",50)
    # result=sapPyInstance.assign_SolidObj_GetMatTemp("1")
    # print(result)

    # sapPyInstance.assign_SolidObj_SetProperty("1","Solid1")
    # result=sapPyInstance.assign_SolidObj_GetProperty("1")
    # print(result)

    # Vec=[0,0,0]
    # sapPyInstance.assign_SolidObj_SetSpring("1", 1, 1, 1, "", 1, 1, 3, True, Vec, 0, False, "Local")
    # result=sapPyInstance.assign_SolidObj_GetSpring("1")
    # print(result)

    # result=sapPyInstance.assign_SolidObj_GetNameList()
    # print(result)

    # result=sapPyInstance.assign_SolidObj_GetPoints("1")
    # print(result)

    # result=sapPyInstance.assign_SolidObj_GetTransformationMatrix("1")
    # print(result)
    #############################################
    # sapPyInstance.file_New2DFrame(0,2, 144, 2, 288)
    # sapPyInstance.assign_LinkObj_AddByCoord(-288, 0, 288, 0, 0, 0,UserName="MyLink")

    # sapPyInstance.assign_LinkObj_AddByPoint("1","5",UserName="MyLink2")
    # sapPyInstance.assign_LinkObj_AddByPoint("3","",UserName="MyLink1",IsSingleJoint=True)
    #
    # result=sapPyInstance.assign_LinkObj_Count()
    # print(result)

    # sapPyInstance.define_Groups_SetGroup("Group1")
    # sapPyInstance.assign_LinkObj_SetGroupAssign("MyLink2","Group1")
    # result=sapPyInstance.assign_LinkObj_GetGroupAssign("MyLink2")
    # print(result)

    # DOF=[True,False,False,False,False,False]
    # d=[2,0,0,0,0,0]
    # sapPyInstance.assign_LinkObj_SetLoadDeformation("MyLink2","DEAD",DOF,d)
    # result=sapPyInstance.assign_LinkObj_GetLoadDeformation("MyLink2")
    # print(result)

    # sapPyInstance.assign_LinkObj_SetLoadGravity("MyLink2","DEAD",0,0,-1)
    # result=sapPyInstance.assign_LinkObj_GetLoadGravity("MyLink2")
    # print(result)

    # DOF=[True,False,False,False,False,False]
    # f=[50,0,0,0,0,0]
    # RD=[1,0,0,0,0,0]
    # sapPyInstance.assign_LinkObj_SetLoadTargetForce("MyLink2","DEAD",DOF,f,RD)
    # result=sapPyInstance.assign_LinkObj_GetLoadTargetForce("MyLink2")
    # print(result)

    # sapPyInstance.assign_LinkObj_SetLocalAxes("MyLink2",30)
    # result=sapPyInstance.assign_LinkObj_GetLocalAxes("MyLink2")
    # print(result)

    # sapPyInstance.assign_LinkObj_SetProperty("MyLink2","Link1")
    # result=sapPyInstance.assign_LinkObj_GetProperty("MyLink2")
    # print(result)

    # sapPyInstance.assign_LinkObj_SetPropertyFD("MyLink2","None")
    # result=sapPyInstance.assign_LinkObj_GetPropertyFD("MyLink2")
    # print(result)

    # result=sapPyInstance.assign_LinkObj_GetElm("MyLink2")
    # print(result)

    # result=sapPyInstance.assign_LinkObj_GetNameList()
    # print(result)

    # result=sapPyInstance.assign_LinkObj_GetPoints("MyLink2")
    # print(result)

    # result=sapPyInstance.assign_LinkObj_GetTransformationMatrix("MyLink2")
    # print(result)

    #############################################
    # sapPyInstance.file_New2DFrame(0,3, 124, 3, 200)
    # sapPyInstance.analyze_CreateAnalysisModel()

    # DOF=[True,True,True,False,False,False]
    # sapPyInstance.analyze_SetActiveDOF(DOF)

    # sapPyInstance.analyze_SetRunCaseFlag("MODAL",False)

    # sapPyInstance.analyze_SetSolverOption_2(1,1,3,"DEAD")

    # sapPyInstance.file_Save("\sample.sdb")
    # sapPyInstance.analyze_RunAnalysis()
    #
    # sapPyInstance.analyze_ModifyUnDeformedGeometryModeShape("MODAL",1,1.0,2)

    # result=sapPyInstance.analyze_GetActiveDOF()
    # print(result)

    # result=sapPyInstance.analyze_GetCaseStatus()
    # print(result)

    # result=sapPyInstance.analyze_GetRunCaseFlag()
    # print(result)

    # result=sapPyInstance.analyze_GetSolverOption_2()
    # print(result)

    #############################################
    # sapPyInstance.file_New2DFrame(0,3, 124, 3, 200)
    # sapPyInstance.results_Setup_SelectAllSectionCutsForOutput(True)
    #
    # sapPyInstance.results_Setup_SetCaseSelectedForOutput("DEAD")

    # sapPyInstance.results_Setup_SetComboSelectedForOutput("COMB1")

    # sapPyInstance.results_Setup_SetOptionBaseReactLoc(0,0,0)

    # sapPyInstance.results_Setup_SetOptionBucklingMode(1,1)

    # sapPyInstance.results_Setup_SetOptionDirectHist(1)

    # sapPyInstance.results_Setup_SetOptionModalHist(1)

    # sapPyInstance.results_Setup_SetOptionModeShape(1,3)

    # sapPyInstance.results_Setup_SetOptionMultiStepStatic(1)

    # sapPyInstance.results_Setup_SetOptionMultiValuedCombo(1)

    # sapPyInstance.results_Setup_SetOptionNLStatic(1)

    # sapPyInstance.results_Setup_SetOptionPSD(1)

    # sapPyInstance.results_Setup_SetOptionSteadyState(1,1)

    # sapPyInstance.results_Setup_SetSectionCutSelectedForOutput("SCut1",True)

    # result=sapPyInstance.results_Setup_GetCaseSelectedForOutput("DEAD")
    # print(result)

    # result=sapPyInstance.results_Setup_GetComboSelectedForOutput("COMB1")
    # print(result)

    # result=sapPyInstance.results_Setup_GetOptionBaseReactLoc()
    # print(result)

    # result=sapPyInstance.results_Setup_GetOptionBucklingMode()
    # print(result)

    # result=sapPyInstance.results_Setup_GetOptionDirectHist()
    # print(result)

    # result=sapPyInstance.results_Setup_GetOptionModalHist()
    # print(result)

    # result=sapPyInstance.results_Setup_GetOptionModeShape()
    # print(result)

    # result=sapPyInstance.results_Setup_GetOptionMultiStepStatic()
    # print(result)

    # result=sapPyInstance.results_Setup_GetOptionMultiValuedCombo()
    # print(result)

    # result=sapPyInstance.results_Setup_GetOptionNLStatic()
    # print(result)
    #############################################
    # sapPyInstance.file_NewWall(6,48,6,48)
    # sapPyInstance.file_Save("\sample.sdb")
    # sapPyInstance.analyze_RunAnalysis()
    # sapPyInstance.results_Setup_DeselectAllCasesAndCombosForOutput()
    # sapPyInstance.results_Setup_SetCaseSelectedForOutput("DEAD")
    # result=sapPyInstance.results_AreaForceShell("1")
    # print(result)

    # sapPyInstance.file_OpenFile("Example 3-001-incomp.sdb")
    # sapPyInstance.analyze_RunAnalysis()
    # sapPyInstance.results_Setup_DeselectAllCasesAndCombosForOutput()
    # sapPyInstance.results_Setup_SetCaseSelectedForOutput("MEMBRANE")
    # result=sapPyInstance.results_AreaJointForcePlane("1")
    # print(result)

    # sapPyInstance.file_NewWall(6, 48, 6, 48)
    # sapPyInstance.file_Save("\sample.sdb")
    # sapPyInstance.analyze_RunAnalysis()
    # sapPyInstance.results_Setup_DeselectAllCasesAndCombosForOutput()
    # sapPyInstance.results_Setup_SetCaseSelectedForOutput("DEAD")
    # result=sapPyInstance.results_AreaJointForceShell("1")
    # print(result)

    # sapPyInstance.file_NewWall(6, 48, 6, 48)
    # sapPyInstance.file_Save("\sample.sdb")
    # sapPyInstance.analyze_RunAnalysis()
    # sapPyInstance.results_Setup_DeselectAllCasesAndCombosForOutput()
    # sapPyInstance.results_Setup_SetCaseSelectedForOutput("DEAD")
    # result=sapPyInstance.results_AreaStrainShell("1")
    # print(result)

    # sapPyInstance.file_OpenFile("Example 3-001-incomp.sdb")
    # sapPyInstance.analyze_RunAnalysis()
    # sapPyInstance.results_Setup_DeselectAllCasesAndCombosForOutput()
    # sapPyInstance.results_Setup_SetCaseSelectedForOutput("MEMBRANE")
    # result=sapPyInstance.results_AreaStressPlane("1")
    # print(result)

    # sapPyInstance.file_New2DFrame(0, 3, 124, 3, 200)
    # sapPyInstance.define_SourceMass_SetMassSource("MyMassSource",True,True,True,True,1,["DEAD"],[1.25])
    # sapPyInstance.file_Save("\sample.sdb")
    # sapPyInstance.analyze_RunAnalysis()
    # result=sapPyInstance.results_AssembledJointMass_1("","1",0)
    # print(result)

    # sapPyInstance.file_New2DFrame(0, 3, 124, 3, 200)
    # sapPyInstance.file_Save("\sample.sdb")
    # sapPyInstance.analyze_RunAnalysis()
    # sapPyInstance.results_Setup_DeselectAllCasesAndCombosForOutput()
    # sapPyInstance.results_Setup_SetCaseSelectedForOutput("DEAD")
    # result=sapPyInstance.results_BaseReact()
    # print(result)

    # sapPyInstance.file_New2DFrame(0, 3, 124, 3, 200)
    # sapPyInstance.file_Save("\sample.sdb")
    # sapPyInstance.analyze_RunAnalysis()
    # sapPyInstance.results_Setup_DeselectAllCasesAndCombosForOutput()
    # sapPyInstance.results_Setup_SetCaseSelectedForOutput("DEAD")
    # result=sapPyInstance.results_BaseReactWithCentroid()
    # print(result)


    # sapPyInstance.file_OpenFile("F:\pythonInteractSAP2000\pythonInteractSAP2000\Verification\AnalysisExamples\Example 1-019a.sdb")
    # sapPyInstance.analyze_RunAnalysis()
    # sapPyInstance.results_Setup_DeselectAllCasesAndCombosForOutput()
    # sapPyInstance.results_Setup_SetCaseSelectedForOutput("BUCK1")
    # result=sapPyInstance.results_BucklingFactor()
    # print(result)

    # sapPyInstance.file_New2DFrame(0, 3, 124, 3, 200)
    # sapPyInstance.file_Save("\sample.sdb")
    # sapPyInstance.analyze_RunAnalysis()
    # sapPyInstance.results_Setup_DeselectAllCasesAndCombosForOutput()
    # sapPyInstance.results_Setup_SetCaseSelectedForOutput("DEAD")
    # result=sapPyInstance.results_FrameForce("1")
    # print(result)

    # sapPyInstance.file_New2DFrame(0, 3, 124, 3, 200)
    # sapPyInstance.file_Save("\sample.sdb")
    # sapPyInstance.analyze_RunAnalysis()
    # sapPyInstance.results_Setup_DeselectAllCasesAndCombosForOutput()
    # sapPyInstance.results_Setup_SetCaseSelectedForOutput("DEAD")
    # result=sapPyInstance.results_FrameJointForce("1")
    # print(result)

    # sapPyInstance.file_OpenFile("F:\pythonInteractSAP2000\pythonInteractSAP2000\Verification\AnalysisExamples\Example 1-022.sdb")
    # sapPyInstance.analyze_RunAnalysis()
    # sapPyInstance.results_Setup_DeselectAllCasesAndCombosForOutput()
    # sapPyInstance.results_Setup_SetCaseSelectedForOutput("MHIST1")
    # sapPyInstance.results_Setup_SetOptionModalHist(2)
    # result=sapPyInstance.results_JointAcc("22")
    # print(result)

    # sapPyInstance.file_New2DFrame(0, 3, 124, 3, 200)
    # sapPyInstance.file_Save("\sample.sdb")
    # sapPyInstance.analyze_RunAnalysis()
    # sapPyInstance.results_Setup_DeselectAllCasesAndCombosForOutput()
    # sapPyInstance.results_Setup_SetCaseSelectedForOutput("MODAL")
    # result=sapPyInstance.results_ModalLoadParticipationRatios()
    # print(result)

    # sapPyInstance.file_New2DFrame(0, 3, 124, 3, 200)
    # sapPyInstance.file_Save("\sample.sdb")
    # sapPyInstance.analyze_RunAnalysis()
    # sapPyInstance.results_Setup_DeselectAllCasesAndCombosForOutput()
    # sapPyInstance.results_Setup_SetCaseSelectedForOutput("MODAL")
    # result=sapPyInstance.results_Setup_ModalParticipatingMassRatios()
    # print(result)
    #############################################
    # sapPyInstance.saveModel("F:\pythonInteractSAP2000\savedModel.sdb")
    # sapPyInstance.openModel("F:\pythonInteractSAP2000资料\curvedBridge.sdb")
    # sapPyInstance.getUnits()
    # sapPyInstance.getFileName()
    # sapPyInstance.getCoordSystem()
    # sapPyInstance.getSapVersion()
    # sapPyInstance.defineCoordSystem("csys1",[10,10,0,45,0,0])
    # sapPyInstance.SetPresentCoordSystem("csys1")
    # sapPyInstance.setUnits(1)
    # sapPyInstance.getProjectInfo()
    # sapPyInstance.changeUnits()
    # sapPyInstance.closeModel()



