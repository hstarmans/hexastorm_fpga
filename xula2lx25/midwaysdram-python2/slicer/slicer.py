'''
@company: Hexastorm
@author: Rik Starmans
'''

import vtk  
from vtk.util.numpy_support import vtk_to_numpy



import math
import numpy as np # in windows powershell use & "file" for install
import os
from scipy import ndimage
import cv2
# to profile memory
# from memory_profiler import profile
# import above decorator and decorate functions with @profile decorator

class slicer(object):
    '''
    This object creates the slices for the Lepus Next Gen. 
    
    VTK is used to cut an STL or AMF file into slices and convert it to array. The interior of a contour is set to 255, the exterior to 0. 
    The positions of the diodes are calculated via the function createcoordinates. The function patternfiles interpolates
    the array created bt VTK.
    It also scales back the array from 0-255 to 0-3. The function arraytopat convert the resulting list of array to pattern files.
    '''
    
    def __init__(self):
        # set LNXT parameters
        # TODO: determine angle from speed
        self.angle=44.81             # angle of the polygon with respect to the A4 in degrees, e.g. 44.8 degrees in the LNXT design documents
        self.f=230                   # number of pixels per polygon facet, integer>n+blacks;
        self.n=216                   # number of effective pixels per polygon facet
        self.m=216                   # integer; next diode offset (+m,+m-n-1)
        self.u=20.02E-3              # distance in mm between the spots along the the direction of the polygon
        self.v=19.96E-3              # double distance in mm between subsequent polygonlines
        self.nmod = 2                # number of modules 
        self.lnxtheight=125.1        # height of the platform in mm, e.g. for an A4 297 mm
        self.lnxtwidth=125.1         # width of the platform in mm, e.g. for an A4 210 mm
        self.layerheight=0.1         # slice thickness in mm
        # 32 bit limit!! recompile python with flags to go below 0.05 mm
        self.samplegridsize=0.05     # height and width of the of sample gridth
        self.xpermm=1/self.samplegridsize               # x pixels per mm,  !!!!NOTE!!!! REFRESH COORDINATES, 
        self.ypermm=1/self.samplegridsize               # y pixels per mm 
        self.ucor=np.array(self.nmod*20*[0.0])       # the u-offset in mm, np array is required  
        self.vcor=np.array(self.nmod*20*[0.0])                 # the v-offset in mm
        self.currentdir=os.path.dirname(os.path.realpath(__file__))
        #TODO: can also be done via python library, i.e. temp folder 
        self.folder=os.path.join(self.currentdir,'static','patternfiles')
        self.reader=None             # STL reader, set via filename
        self.mapper=None             # polydata, set via filename
    
    @property
    def filename(self):
        return self._filename
    
    @filename.setter
    def filename(self, name='oshw.stl'):
        self._filename=name
        self.reader = vtk.vtkSTLReader()
        self.reader.SetFileName(os.path.join(self.currentdir,'static','upload',self.filename))
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(self.reader.GetOutputPort())
   
    def getlayers(self):
        '''
        return number of layers in the object
        '''
        # instantiate reader
       
        bounds=self.mapper.GetBounds()
        layers=math.floor((bounds[5]-bounds[4])/self.layerheight)
        return layers
    
    def stltoarray(self, zheight):
        '''slices STL to an array
    
        The height is the position where the layer is retrieved.
        :param zheigh: z height where to take a cut in mm
        '''
        # generate contour by cutting the STL trough its center axis aligned with
        # a plane
        # NOTE: an alternative might be to use the VTK imagemapper class
        contourCutter = vtk.vtkCutter()
        contourCutter.SetInputConnection(self.reader.GetOutputPort())
        cutPlane = vtk.vtkPlane()
        cntr=list(self.mapper.GetCenter())
        cutPlane.SetOrigin(cntr[0],cntr[1],zheight)
        cutPlane.SetNormal(0, 0, 1)
        contourCutter.SetCutFunction(cutPlane)
        stripper = vtk.vtkStripper()
        stripper.SetInputConnection(contourCutter.GetOutputPort())
        stripper.Update()  #updates are crucial
        # that's our contour
        contour = stripper.GetOutput()
        # prepare the binary image's voxel grid
        bounds = [0]*6
        contour.GetBounds(bounds)
        print("bounds "+str(bounds))
        # spacing is [width, height, length]  #TODO: length is it really cubical grid, why does this exist?
        spacing = [self.samplegridsize, self.samplegridsize, self.layerheight]
        print("spacing "+str(spacing))
        # compute dimensions
        dim = [0]*3
        for i in range(3):
            dim[i] = int(round(math.ceil((bounds[i * 2 + 1] - bounds[i * 2]) / spacing[i]))) + 1 
            if (dim[i] < 1):
                dim[i] = 1
        inval = 255
        outval = 0        
        blank=np.ones((dim[0]-1)*(dim[1]-1),dtype=np.uint8)*inval # create an array of 255
        blank_string=blank.tostring() 
        dataImporter = vtk.vtkImageImport()       
        dataImporter.CopyImportVoidPointer(blank_string,len(blank_string))
        dataImporter.SetDataScalarTypeToUnsignedChar()
        dataImporter.SetNumberOfScalarComponents(1)
        dataImporter.SetWholeExtent(0, dim[0]-1, 0, dim[1]-1, 0, dim[2] - 1)
        dataImporter.SetDataExtent(0, dim[0]-1, 0, dim[1]-1, 0, dim[2] - 1)
        origin = [0]*3
        origin[0] = bounds[0]
        origin[1] = bounds[2]
        origin[2] = bounds[4]
        
        # polygonal data -. image stencil:
        pol2stenc = vtk.vtkPolyDataToImageStencil()
        pol2stenc.SetInputConnection(stripper.GetOutputPort())
        pol2stenc.DebugOn()
        pol2stenc.SetOutputOrigin(origin)
        pol2stenc.SetOutputSpacing(spacing)
        pol2stenc.SetOutputWholeExtent(dataImporter.GetDataExtent())
       
        # cut the corresponding white image and set the background:
        imgstenc = vtk.vtkImageStencil()
        imgstenc.SetInputConnection(dataImporter.GetOutputPort())
        imgstenc.SetStencilConnection(pol2stenc.GetOutputPort())
        imgstenc.ReverseStencilOff()
        imgstenc.SetBackgroundValue(outval)
        
        imgstenc.Update()
        # convert the stencil to a numpy array
        vtk_image=imgstenc.GetOutput()
        width, height, _ = vtk_image.GetDimensions()
        vtk_array = vtk_image.GetPointData().GetScalars()
        components = vtk_array.GetNumberOfComponents()
        arr = vtk_to_numpy(vtk_array).reshape(height, width, components)
        # only grab values layer 0
        arr=arr[:,:,0].astype(np.uint8, copy=False)
        # pad slice to it has  here 0 top 12 bottom 0 left and 0 right
        padheight=self.lnxtheight*self.ypermm-height
        padwidth=self.lnxtwidth*self.xpermm-width
        arr=np.lib.pad(arr, ((round(padheight/2), math.floor(padheight/2)), (round(padwidth/2), math.floor(padwidth/2))), mode='constant', constant_values=0)
        arr = arr.astype(np.uint8, copy=False) #prevents ghosting in slices
        arr = np.flipud(arr)
        return arr
    
    def createpreview(self, arr,filename=None):
        resized_image = cv2.resize(arr, (400, 400)) 
        if filename==None:
            filename=os.path.join(self.folder,'preview.png')
        cv2.imwrite(filename,resized_image)
        
    def fxpos(self,i,j):
        '''
        calculates the diode x-position as a function of diode i and pixel j
        :param i: the diode number
        :param j: the pixel number
        '''
        result=np.sin(np.radians(self.angle))*self.u*(j%self.f+i*self.n-(self.f-self.n-2)//2)
        xcor=self.ucor[i]*np.cos(np.radians(90-self.angle))-(self.vcor[i]%self.v)*np.sin(np.radians(90-self.angle-90))
        result+=xcor
        return result*self.xpermm
    
    def fypos(self,i,j):
        '''
        calculates the diode y-position as a function of diode i and pixel j
        :param i: the diode number
        :param j: the pixel number
        '''
        result=(np.cos(np.radians(self.angle))*self.u*(j%self.f+(i%20-1)*self.n-(self.f-self.n-2)//2)+(j//self.f)*(self.v/np.sin(np.radians(self.angle)))
              -i%20*self.m*(self.v/np.sin(np.radians(self.angle))))
        ycor=self.ucor[i]*np.cos(np.radians(90-self.angle))+(self.vcor[i]%self.v)*np.sin(np.radians(90-self.angle))
        result+=ycor
        return result*self.ypermm
    
    def createcoordinates(self,mod):
        '''
        returns the position of the diodes for a single module and stores them (20, number of lines)
        :param mod: the module number, that is 0 or 1 etc..
        '''
        lof = self.m-(np.cos(np.radians(self.angle))*self.u*self.n)*(np.sin(np.radians(self.angle))/self.v)
        nol=int(round(self.lnxtheight//(self.v/np.sin(np.radians(44.8)))+19*lof)) # number of lines perfect case
        maxoffset=int(round(max(self.vcor)/self.v)) # extra lines at end due to v-offset
        minoffset=int(round(min(self.vcor)/self.v))
        nol=int(nol+abs(maxoffset)-abs(minoffset)) # number of line offset included
        # i is diode, j is pixel, mod is module, f is pixels per line, below output is float, input is int32
        xpos=np.fromfunction(lambda i, j: self.fxpos(i+mod*20,j), (20, nol*self.f), dtype=np.int32)
        ypos=np.fromfunction(lambda i, j: self.fypos(i+mod*20,j), (20, int(nol*self.f)), dtype=np.int32)
        for diode in range(0,20):
            # calculate the line offset and pixeloffset
            lineoffset=int(round(self.vcor[diode+mod*20]/self.v)-minoffset)
            pixoffset=int(round(self.ucor[diode+mod*20]/self.u))
            # use the lineoffset
            if self.f-self.n-pixoffset<0:
                raise Exception("Pixoffset is too large, cannot be compensated")
            # values mapped to the negative plane are send to zero in interpolation scheme
            pixelson=np.array(lineoffset*self.f*[-1]+(nol-lineoffset)*(pixoffset*[-1]+self.n*[1]+(self.f-self.n-pixoffset)*[-1]))
            xpos[diode,:]=xpos[diode,:]*pixelson
            ypos[diode,:]=ypos[diode,:]*pixelson
        
        # concatenate; here [[x0,x1],[y0,y1]]
        ids=np.concatenate(([xpos.flatten()],[ypos.flatten()]), axis=0)
        # read write used to save memory
        np.save(os.path.join(self.folder,"ids"+str(mod)+".npy"),ids)
            
    def patternfile(self, layerarr, mod):
        '''returns the pattern file as numpy array, shape 32*lines, i.e. 20 diodes range 0-3 per module
    
        The led control module reads out 64 bits per time instant. The last 24 bits are random. The first 40
        bits contain the information for 20 diodes, 2 bits per diode. It returns a list with numpy  arrays shape (32 , as long as needed)   
        :param img: 8 bit PIL Image
        :param mod: module number
        '''
        if layerarr.max()==0:
            raise Exception("Slice is empty")
        layer = layerarr//(255//3)
        # don't calculate interpolation coordinates but read it from disk, saves memory
        ids=np.load(os.path.join(self.folder,"ids"+str(mod)+".npy"))
        # values outside image are mapped to 0
        ptrn=ndimage.map_coordinates(input=layer, output=np.uint8,coordinates=ids, order=1, mode="constant",cval=0)
        ptrn=ptrn.reshape(20,len(ptrn)//20)
        # pad zeroes to create form by FPGA ; here 0 top 12 bottom 0 left and 0 right
        ptrn=np.lib.pad(ptrn, ((0, 12), (0, 0)), mode='constant', constant_values=0)
        return ptrn
    
    def plotptrn(self,ptrnlst,xres=0,yres=0):
        '''
        functions plots the modules and returns an image
        
        e.g. xres=5,yres=5 resuts in a 611x1221 image
        :param ptrnfile: result of the functions patternfiles
        '''
        if xres==0 or yres==0:
            xres=self.xpermm
            yres=self.ypermm
        # i diode j pixel, np.int32 --> input to array
        xcor=np.fromfunction(lambda i, j: self.fxpos(i,j)*xres, (20*self.nmod, ptrnlst[0].shape[1]), dtype=np.int32)
        ycor=np.fromfunction(lambda i, j: self.fypos(i,j)*yres, (20*self.nmod, ptrnlst[0].shape[1]), dtype=np.int32)
        # here the output of the array is defined
        xcor = xcor.astype(np.int32, copy=False)
        ycor = ycor.astype(np.int32, copy=False)
        #ycor=ycor+abs(ycor.min())
        # x and y cannot be negative
        if xcor.min()<0:
            xcor+=abs(xcor.min())
        if ycor.min()<0:
            ycor+=abs(ycor.min())
        # number of pixels ptrnfile.shape[1]
        a=np.zeros((ycor.max()+1,xcor.max()+1))
        for i in range(0,20*self.nmod):
                #adding prevents zeroes from overwriting ones
                a[ycor[i,:],xcor[i,:]]+=ptrnlst[i//20][i%20,:]
        img = cv2.fromarray(np.uint8(a*(255/3)))
        return img

    def readbin(self,name):
        '''
        reads a pat file
        :param name:
        '''
        pat=np.fromfile(name,dtype=np.uint8)
        if len(pat)%8 is not 0:
            raise Exception("Pattern file not multiple of 8")
        #split bits
        pat64=pat//64
        pat16=pat%64//16
        pat4=pat%16//4
        pat1=pat%4
        # stack rows
        pat=np.vstack((pat1,pat4,pat16,pat64))
        # flatten column style i.e. Fortran
        pat=pat.flatten(order='F')
        # reshape
        pat=pat.reshape(len(pat)//32,32)
        # select the correct rows, only info on row 16 of layer 01 mod1, there is is info on mod2
        # transpose for compatibility with result patternfile
        pat=pat[:,0:20].T
        return pat
    
    def numpywrite(self, pixeldata, filename):
        # ensure it is the write type before writing
        pixeldata=pixeldata.astype(np.uint8)
        pixeldata.tofile(filename) 
    
    def arraytopat(self, ptrnarray):
        '''

        converts numpy array created by pattern files and returns a list of bytes
       
        :param ptrnarray: a ptrnarray, the maximum of the array should be 3

        '''
        ptrnarray=np.transpose(ptrnarray)
        ptrnarray=ptrnarray.reshape(ptrnarray.size//4,4)
        ptrnarray=ptrnarray.astype(np.uint8,copy=False)
        multpl=np.array([[1,4,16,64]],dtype=np.uint8) 
        ptrnarray=ptrnarray*multpl # broadcast is fast
        ptrnarray=ptrnarray.sum(axis=1)
        ptrnarray = ptrnarray.astype(np.uint8, copy=False) #otherwise you have double, double is default in numpy as it is faster
        lst=ptrnarray.ravel() #ravel returns a view which is much faster than flatten
        return lst
    

if __name__ == "__main__":
    from time import time  
    t = time()
    slic3r=slicer()
    slic3r.layerheight=0.1
    slic3r.filename='tkiceramicsmodel.stl'
    #TODO: only needed due to 64 bit <--> 32 bit
    print("There are "+str(slic3r.getlayers())+" layers.")
    # Create slices and store to a pattern file
    arr = slic3r.stltoarray(0.1)
    slic3r.createpreview(arr)
    print("Slicing layer with VTK takes "+str(time()-t)+" seconds")
    #slic3r.createcoordinates()
    t=time()
    #TODO: add threads to code sample
    ptrn0 = slic3r.patternfile(arr,0)
    ptrn1=  slic3r.patternfile(arr,1)
    # diodes which are on
    # lst=[i for i in range(ptrn0.shape[0]) if ptrn0[i,:].sum()>0]
    # [i for i in range(ptrn1.shape[0]) if ptrn1[i,:].sum()>0]
    # [x[0] for x in enumerate(lst) if x[1]==2]
    ptrnlst=[ptrn0,ptrn1]   
    for idx, item in enumerate(ptrnlst):
        patfile=slic3r.arraytopat(item)
        filename = os.path.join(slic3r.folder,"module"+str(idx)+".pat")
        slic3r.numpywrite(patfile,filename)
    print("Parsing to pat takes "+str(round(time()-t))+" seconds")
    print("Slicing done!")
    # testing the slices can only be done at 64 bit, VTK is however installed for 32 bit
    
 
    
    
